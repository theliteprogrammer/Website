from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from django.dispatch import receiver


from PIL import Image
from shortuuid.django_fields import ShortUUIDField
import os 


IDENTITY_TYPE = (
    ("national_id_card", "National ID Card"),
    ("drivers_licence", "Drives Licence"),
    ("international_passport", "International Passport")
)

GENDER = (
    ("femail", "Female"),
    ("male", "Male"),
)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return 'user_{0}/{1}'.format(instance.user.id,  filename)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        if self.username:
             return self.username
        else:
            return f"No Username"

    # def save(self, *args, **kwargs):
    #     if self.roles == "wcfm_vendor":
    #         "vendor.Vendor".objects.create(user=self, profile=None)
    #     else:
    #         self.product.status = "published"
    #         self.product.save()
            
    #     super(User, self).save(*args, **kwargs) 



class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz123")
    image = models.FileField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    postal_code = models.CharField(max_length=1000, null=True, blank=True)

    facebook = models.URLField(default="https://facebook.com/", null=True, blank=True)
    instagram = models.URLField(default="https://instagram.com/", null=True, blank=True)
    twitter = models.URLField(default="https://twitter.com/", null=True, blank=True)
    whatsApp = models.CharField(default="+123 (456) 789", max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        if self.full_name:
            return f"{self.full_name}"
        else:
            return f"{self.user.username}"
        
    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs) 

    
    def profile_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" object-fit:"cover" />' % (self.image))

    
    
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)



