from django.db import models
from django.utils.text import slugify
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator

from userauths.models import Profile, User

import datetime
import shortuuid
from shortuuid.django_fields import ShortUUIDField

PAYMENT_STATUS = (
    ("paid", "Paid"),
    ("initiated", 'Initiated'),
    ("processing", "Processing"),
    ("pending", "Pending"),
    ("cancelled", "Cancelled"),
    ("failed", 'Failed'),
    ("unpaid", 'Unpaid'),
)


EMPLOYEE_ROLE = (
    ("Driver", "Driver"),
    ("Collector", 'Collector'),
    ("Sorter", "Sorter"),
    ("Recycling Specialist", "Recycling Specialist"),
    ("Route Planner", "Route Planner"),
    ("Dispatcher", 'Dispatcher'),
    ("Supervisor", 'Supervisor'),
    ("Maintenance Technician", 'Maintenance Technician'),

)


NOTIFICATION_TYPE = (
    ("New Subscriber", "New Subscriber"),
    ("Collection Date Scheduled", 'Collection Date Scheduled'),
    ("Collection Cancelled", "Collection Cancelled"),
    ("New Collection Job", "New Collection Job"),
    ("New Driving Job", "New Driving Job"),
    ("Waste Collected", "Waste Collected"),
    ("New Donation", "New Donation",)
    
)

COLLECTION_STATUS = (
    ("Collected", "Collected"),
    ("Not Collected", 'Not Collected'),
    ("Pending", "Pending"),
    ("Scheduled", "Scheduled"),
    ("Delayed", "Delayed"),
    ("Cancelled", 'Cancelled'),
    ("In Progress", 'In Progress'),
)


ORDER_STATUS = (
    ("pending", "pending"),
    ("fulfilled", "fulfilled"),
    ("partially_fulfilled", "Partially Fulfilled"),
    ("cancelled", "Cancelled"),
    
)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    role= models.CharField(max_length=200, choices=EMPLOYEE_ROLE, default="Collector")
    active = models.BooleanField(default=True)
    collected_waste = models.ManyToManyField("core.WasteOrder")
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.user.username)
    
    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)

    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.user.profile.image.url))

    def full_name(self):
        return str(self.user.profile.full_name)


class WasteCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(unique=False, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
            
        super(WasteCategory, self).save(*args, **kwargs) 

class WasteItem(models.Model):
    wiid = ShortUUIDField(length=5, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    disposal_instructions = models.TextField(null=True, blank=True)
    hazardous = models.BooleanField(default=False)
    recyclable = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=False, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
            
        super(WasteItem, self).save(*args, **kwargs) 
    
    class Meta:
        ordering = ['-date']

class WastePlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    wpid = ShortUUIDField(length=5, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    image = models.FileField(upload_to="waste_plan", default="waste_plan_default.jpg", null=True, blank=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=False, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
            
        super(WastePlan, self).save(*args, **kwargs)

    
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

    class Meta:
        ordering = ['-date']

class WasteOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user")
    waste_plan = models.ForeignKey(WastePlan, on_delete=models.CASCADE)
    payment_status= models.CharField(max_length=20, choices=PAYMENT_STATUS, default="unpaid")
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    vat = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    address= models.CharField(max_length=1000)
    phone= models.CharField(max_length=1000)
    active = models.BooleanField(default=False)
    success_id = ShortUUIDField(length=300, max_length=505, alphabet="abcdefghijklmnopqrstuvxyz1234567890")
    oid = ShortUUIDField(length=5, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, editable=True)
    
    collector = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    collected_status= models.CharField(max_length=20, choices=COLLECTION_STATUS, default="Not Collected")
    date_to_be_collected = models.DateTimeField(default=datetime.datetime.now, editable=True)
    message_to_subscriber = models.CharField(max_length=10000, null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.waste_plan.name)
    
    # def save(self, *args, **kwargs):
    #     super(WasteOrder, self).save(*args, **kwargs)

    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.waste_plan.image.url))


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    waste_plan = models.ForeignKey(WastePlan, on_delete=models.CASCADE)
    order = models.ForeignKey(WasteOrder, on_delete=models.CASCADE)
    type= models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default="New Subscriber")
    is_read = models.BooleanField(default=False)
    oid = ShortUUIDField(length=5, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, editable=True)
    
    def __str__(self):
        return str(self.waste_plan.name)

    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.waste_plan.image.url))

    class Meta:
        ordering = ['-date']


class CollectionPoint(models.Model):
    cpid = ShortUUIDField(length=5, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    capacity = models.PositiveIntegerField()
    current_fill = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=False, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
    
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:2]
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
            
        super(CollectionPoint, self).save(*args, **kwargs)

class CollectionEvent(models.Model):
    ceid = ShortUUIDField(length=5, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    collection_point = models.ForeignKey(CollectionPoint, on_delete=models.CASCADE)
    collected_weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateField()

    def __str__(self):
        return f"Collection at {self.collection_point} on {self.date}"

class CollectedWaste(models.Model):
    cwid = ShortUUIDField(length=5, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    event = models.ForeignKey(CollectionEvent, on_delete=models.CASCADE)
    waste_item = models.ForeignKey(WasteItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} {self.waste_item} collected at {self.event}"



class Donation(models.Model):
    full_name= models.CharField(max_length=1000)
    email= models.EmailField(max_length=1000)
    amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    payment_status= models.CharField(max_length=20, choices=PAYMENT_STATUS, default="unpaid")
    success_id = ShortUUIDField(length=300, max_length=505, alphabet="abcdefghijklmnopqrstuvxyz1234567890")
    did = ShortUUIDField(length=15, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz", null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, editable=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.full_name)

