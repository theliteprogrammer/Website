from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import mark_safe
from django.utils.text import slugify
import shortuuid
import datetime

STATUS = (
    ("live", "Live"),
    ("maintainance", "Maintainance"),
    ("error", "Error"),
)

REG_FORM = (
    ("classic", "Classic"),
    ("dynamic", "Dynamic"),
)

SERVICE_FEE_CHARGE_TYPE = (
    ("percentage", "Percentage"),
    ("flat_rate", "Flat Rate"),
)


CONTACT_REASON = (
    ("talk_to_an_agent ", "Talk To An Agent "),
    ("complaint", "Complaint"),
    ("report_product", "Report Product"),
    ("report_vendor", "Report Vendor"),
    ("new_feature_idea", "New Feature Idea"),
    ("report_a_bug", "Report a Bug"),
)



HOMEPAGE_STYLE_2 = (
    ("1", "Homepage 1"),
    ("2", "Homepage 2"),
    ("3", "Homepage 3"),
    ("4", "Homepage 4"),
    
)

LOGO_TYPE = (
    ("use_image", "Use Company Image"),
    ("use_name", "Use Company Name"),
    ("use_landscape", "Use Landscape Image"),
    
)

REVIEW_TYPE = (
    ("any_authenticated_user", "Allow any user that is logged in to review a product"),
    ("only_purchased_user", "Allow only users who have purchased a product to review the product"),
)

NAVIGATION_BAR_STYLE = (
    ('1', "Header 1"),
    ('2', "Header 2"),
)


PRODUCT_PAYMENT_METHOD = (
    ("PayPal", "PayPal"),
    ("Stripe", "Stripe"),
    ("Cash On Delivery", "Cash On Delivery"),
    
)

ACCOUNT_CREATION = (
    ("create_account", "Create Account Automatically Before Checkout"),
    ("dont_create_account", "Do Not Create Account Before Checkout"),
)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = ("Payment Method")
        verbose_name_plural = ("Payment Method")
        ordering = ['-date']

    def __str__(self):
        return self.name
    

class PayoutMethod(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = ("Payout Method")
        verbose_name_plural = ("Payout Method")
        ordering = ['-date']

    def __str__(self):
        return self.name
    


class UnitTypes(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = ("Unit Types")
        verbose_name_plural = ("Unit Types")
        ordering = ['-date']

    def __str__(self):
        return self.name

class BasicAddon(models.Model):
    view_more = models.CharField(default="View All", max_length=10)
    service_fee_percentage = models.IntegerField(default=5, help_text="NOTE: Numbers added here are in percentage (%)ve.g 4%")
    service_fee_flat_rate = models.DecimalField(default=0.7, max_digits=12, decimal_places=2 ,help_text="NOTE: Add the amount you want to charge as service fee e.g $2.30")
    service_fee_charge_type = models.CharField(default="percentage", max_length=30, choices=SERVICE_FEE_CHARGE_TYPE)
    
    affiliate_commission_percentage = models.IntegerField(default=50, help_text="NOTE: Numbers added here are in percentage (%)")
    general_tax_percentage = models.IntegerField(default=5, help_text="NOTE: Numbers added here are in percentage (%)")
    vendor_fee_percentage = models.IntegerField(default=5, help_text="NOTE: Numbers added here are in percentage (%)")
    currency_sign = models.CharField(default="$", max_length=10)
    currency_abbreviation = models.CharField(default="USD", max_length=10)
    registration_form_type = models.CharField(max_length=50, choices=REG_FORM, default="classic")
    send_email_notifications = models.BooleanField(default=False)
    payout_vendor_fee_immediately = models.BooleanField(default=True)
    payment_method = models.ManyToManyField(PaymentMethod, blank=True)
    review_type = models.CharField(default="any_authenticated_user", max_length=130, choices=REVIEW_TYPE)
    header_type = models.CharField(default='1', max_length=130, choices=NAVIGATION_BAR_STYLE)
    account_creation_type = models.CharField(default='create_account', max_length=130, choices=ACCOUNT_CREATION)
    image_upload_limit = models.IntegerField(default=10)
    
    class Meta:
        verbose_name = ("Settings")
        verbose_name_plural = ("Settings")


class BecomeAVendor(models.Model):
    addon = models.OneToOneField(BasicAddon, on_delete=models.CASCADE)
    image = models.FileField(default="blank.jpg", null=True, blank=True)
    sub_title = models.CharField(default="Become a Vendor", max_length=1000, null=True, blank=True)
    title = models.CharField(default="Start Selling With Us Today", max_length=1000, null=True, blank=True)
    content = CKEditor5Field(null=True, blank=True, config_name='extends')
    
    class Meta:
        verbose_name = ("Become a Vendor")
        verbose_name_plural = ("Become a Vendor")

    def __str__(self):
        return self.title
    
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

class AffiliateLandingPage(models.Model):
    addon = models.OneToOneField(BasicAddon, on_delete=models.CASCADE)
    image = models.FileField(default="blank.jpg", null=True, blank=True)
    sub_title = models.CharField(default="Earn Commissions", max_length=1000, null=True, blank=True)
    title = models.CharField(default="Partner with us to earn commissions.", max_length=1000, null=True, blank=True)
    content = CKEditor5Field(null=True, blank=True, config_name='extends')
    
    class Meta:
        verbose_name = ("Affiliate Landing Page")
        verbose_name_plural = ("Affiliate Landing Page")

    def __str__(self):
        return self.title
    
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))




class NewsLetterText(models.Model):
    addon = models.ForeignKey(BasicAddon, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(default="Subscrible & Get 10% Discount", max_length=1000, null=True, blank=True)
    sub_title = models.CharField(default="Get E-mail updates about our latest shop and special offers.", max_length=1000, null=True, blank=True)
    image = models.FileField(upload_to='general_images', default="logo.jpg", null=True, blank=True)
    active = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name = ("News Letter Write Up")
        verbose_name_plural = ("News Letter Write Up")


class FooterBenefits(models.Model):
    addon = models.ForeignKey(BasicAddon, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.FileField(upload_to='general_images')
    title = models.CharField(max_length=1000, null=True, blank=True)
    sub_title = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=False)

    
    
    class Meta:
        verbose_name = ("Platform Benefits (Footer)")
        verbose_name_plural = ("Platform Benefits (Footer)")


        

class Policy(models.Model):
    terms_and_conditions = CKEditor5Field(null=True, blank=True, config_name='extends')
    return_policy = CKEditor5Field(null=True, blank=True, config_name='extends')
    privacy_policy = CKEditor5Field(null=True, blank=True, config_name='extends')
    cookie_policy = CKEditor5Field(null=True, blank=True, config_name='extends')

    
    class Meta:
        verbose_name = ("Policy")
        verbose_name_plural = ("Policy")

    def __str__(self):
        return "Policy"
    

class AboutUS(models.Model):
    image = models.FileField(default="logo.jpg", null=True, blank=True)
    title = models.CharField(default="Global Leading Online Shop", max_length=1000, null=True, blank=True)
    content = CKEditor5Field(null=True, blank=True, config_name='extends')
    
    class Meta:
        verbose_name = ("About Us")
        verbose_name_plural = ("About Us")

    def __str__(self):
        return self.title
    
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

    

class Feature(models.Model):
    title = models.CharField(default="Secured Payment and Fast Delivery", max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)
    about_us = models.ForeignKey(AboutUS, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = ("Feature")
        verbose_name_plural = ("Feature")

    def __str__(self):
        return self.title
    

class Team(models.Model):
    image = models.FileField(default="logo.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=1000)
    role = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)
    about_us = models.ForeignKey(AboutUS, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = ("Team")
        verbose_name_plural = ("Team")

    def __str__(self):
        return self.full_name
    
    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

    

class Partner(models.Model):
    logo = models.FileField(default="logo.jpg", null=True, blank=True)
    company_name = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    about_us = models.ForeignKey(AboutUS, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = ("Partner")
        verbose_name_plural = ("Partner")

    def __str__(self):
        return self.company_name
    


class EarningPoints(models.Model):
    signup_point = models.IntegerField(default=10)
    enable_signup_point = models.BooleanField(default=True)
    text = models.CharField(default="Point", max_length=10 )
    referral_point = models.PositiveIntegerField(default=500, help_text="Enter an amount that user will get when they refer thier friend")

    
    class Meta:
        verbose_name_plural = ("Earning Points")
        
    def __str__(self):
        return "Earning Points"



class Company(models.Model):
    logo = models.FileField(default="logo.jpg")
    logo_type = models.CharField(default="use_image", max_length=30, choices=LOGO_TYPE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    website_address = models.CharField(max_length=500, help_text="Add the website address without the slash /")
    admin_website_address = models.CharField(max_length=500, help_text="Add the admin address without the slash /")
    footer = models.CharField(max_length=1000)
    facebook = models.CharField(default="https://facebook.com/", max_length=1000)
    instagram = models.CharField(default="https://instagram.com/", max_length=1000)
    twitter = models.CharField(default="https://twitter.com/", max_length=1000)
    linkedin = models.CharField(default="https://linkedin.com/", max_length=1000)
    youtube = models.CharField(default="https://youtube.com/", max_length=1000)
    telegram = models.CharField(default="https://telegram.com/", max_length=1000)
    homepage = models.CharField(choices=STATUS, max_length=1000, default="live")
    secret_key = models.CharField(max_length=1000, null=True, blank=True)
    public_key = models.CharField(max_length=1000, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Company Information"

    def __str__(self):
        return f"{self.name}"
    
    

class SupportContactInformation(models.Model):
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    address = models.CharField(max_length=1000, null=True, blank=True)
    working_days = models.CharField(max_length=1000, null=True, blank=True, default="Monday - Friday")
    open_time = models.CharField(max_length=100, null=True, blank=True, default="08 AM")
    closing_time = models.CharField(max_length=100, null=True, blank=True, default="05 PM")
    
    class Meta:
        verbose_name_plural = "Support Contact Information"

    def __str__(self):
        return f"Support Contact Information"
    
    
class TaxRate(models.Model):
    country = models.CharField(max_length=200)
    rate = models.IntegerField(default=5, help_text="Numbers added here are in percentage (5 = 5%)")
    active = models.BooleanField(default=True)
    custom_name = models.CharField(default="Tax", max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Tax Rates"

    def __str__(self):
        return f"{self.country}"
    
    
class SuperUserSignUpPin(models.Model):
    pin = models.CharField(default="17880984243324543", max_length=100)

    def __str__(self):
        return self.pin
    
    

class ContactUs(models.Model):
    cid = ShortUUIDField(length=20, max_length=25, alphabet="abcdefghijklnopqstuv")
    topic = models.CharField(max_length=50, choices=CONTACT_REASON, default="talk_to_an_agent")
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Us "

    def __str__(self):
        return f"{self.full_name}"
    
    

class FAQs(models.Model):
    fid = ShortUUIDField(length=20, max_length=25, alphabet="abcdefghijklnopqstuv")
    question = models.CharField(max_length=100)
    answer = models.TextField(null=True, blank=True)
    share = models.BooleanField(default=False)
    email = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = ("FAQs")
        verbose_name_plural = ("FAQs")

    def __str__(self):
        return self.question
    
    
class AnnouncementsTopbar(models.Model):
    announcement = CKEditor5Field(config_name='extends')
    link_text = models.CharField(max_length=100,null=True, blank=True)
    link_url = models.URLField(null=True, blank=True)
    show_link = models.BooleanField(default=False)
    alert_bg = models.CharField(max_length=100,null=True, blank=True, help_text="Options are: alert-success, alert-danger, alert-warning, alert-primary, alert-dark & animate-grad for gradient alert")
    active = models.BooleanField(default=False)
    version = models.CharField(max_length=10000, editable=False ,help_text="NOTICE: Do not modify the version field")
    

    def __str__(self):
        return "Announcement Topbar"

    class Meta:
        verbose_name = "Announcement Topbar"
        verbose_name_plural = "Announcements Topbar"

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        self.version = uuid_key
            
        super(AnnouncementsTopbar, self).save(*args, **kwargs) 


class AnnouncementsModal(models.Model):
    title = models.CharField(max_length=1000)
    announcement = CKEditor5Field(config_name='extends')
    link_text = models.CharField(max_length=100,null=True, blank=True)
    link_url = models.URLField(null=True, blank=True)
    show_link = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    entrance_delay = models.PositiveIntegerField(default=10, help_text="The numbers added here are in 'mili-seconds'")
    version = models.CharField(max_length=10000, editable=False ,help_text="NOTICE: Do not modify the version field")

    

    def __str__(self):
        return "Announcement Modal"

    class Meta:
        verbose_name = "Announcement Modal"
        verbose_name_plural = "Announcements Modal"

    def save(self, *args, **kwargs):
        uuid_key = shortuuid.uuid()
        self.version = uuid_key
            
        super(AnnouncementsModal, self).save(*args, **kwargs) 


class ChangeLog(models.Model):
    title = models.CharField(max_length=1000)
    announcement = CKEditor5Field(config_name='extends')
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=False, blank=True, null=True, help_text="*Optional: Add the date when the update became live")

    def __str__(self):
        return "Change Log"

    class Meta:
        verbose_name = "Change Log"
        verbose_name_plural = "Change Log"
        


class PlatformNotifications(models.Model):
    image = models.FileField(upload_to="notifications", null=True, blank=True)
    title = models.CharField(max_length=1000)
    content = CKEditor5Field(null=True, blank=True, config_name='extends')
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    nid = ShortUUIDField(length=20, max_length=25, alphabet="abcdefghijklnopqstuv")

    class Meta:
        verbose_name = ("Platform Update Notifications")
        verbose_name_plural = ("Platform Update Notifications")
        ordering = ['date']

class TutorialVideo(models.Model):
    title = models.CharField(default="Video Links", max_length=100)
    how_to_use_platform = models.URLField(default="https://youtube.com", null=True, blank=True)
    how_to_use_affiliate_system = models.URLField(default="https://youtube.com", null=True, blank=True)
    how_to_become_a_vendor = models.URLField(default="https://youtube.com", null=True, blank=True)
    
    class Meta:
        verbose_name = ("Tutorial Video")
        verbose_name_plural = ("Tutorial Video")



        
        
class HomePageSetup(models.Model):
    title = models.CharField(default="Home Page Setup", max_length=50)
    homepage_type = models.CharField(default="1", max_length=50, choices=HOMEPAGE_STYLE_2)
    
    class Meta:
        verbose_name_plural = ("Home Page Setup")
        


class Home_One(models.Model):
    image = models.FileField(upload_to="homepage", blank=True, null=True)
    small_text = models.CharField(default="Hey there, Welcome!", max_length=1010)
    small_sub_text = models.CharField(default="Explore our hot collections  ", max_length=1010)
    main_text = models.CharField(default="20% OFF Today", max_length=20)
    description_text = models.CharField(default="Lorem Ipsum is the best way of writing destiny car type Lorem Ipsum is the best way of writing destiny car type", max_length=1010)
    button_text = models.CharField(default="Shop Now", max_length=100)
    button_url = models.URLField(default="https://recygo.com/shop/", max_length=1000)
    background_color = models.CharField(default="bg-purple", max_length=100, help_text="Backgrounds: bg-purple, bg-red, bg-green, bg-orange, bg-gray")
    first = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    homepage = models.ForeignKey(HomePageSetup, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = ("Home One")
        
    def home_image(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

class Home_One_Sidebar(models.Model):
    image = models.FileField(upload_to="homepage", blank=True, null=True)
    small_text = models.CharField(default="Hey there, Welcome!", max_length=1010)
    main_text = models.CharField(default="20% OFF Today", max_length=40)
    description_text = models.CharField(default="Lorem Ipsum is the best way of writing destiny car type Lorem Ipsum is the best way of writing destiny car type", max_length=1010)
    button_text = models.CharField(default="Shop Now", max_length=100)
    button_url = models.URLField(default="https://recygo.com/shop/", max_length=1000)
    background_color = models.CharField(default="bg-purple", max_length=100, help_text="Backgrounds: bg-purple, bg-red, bg-green, bg-orange, bg-gray")
    active = models.BooleanField(default=True)
    homepage = models.ForeignKey(HomePageSetup, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = ("Home One Sidebar")
        
    def home_image(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))



class Home_Two(models.Model):
    homepage = models.ForeignKey(HomePageSetup, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to="homepage", blank=True, null=True)
    small_title = models.CharField(default="Hey there, Welcome!", max_length=1010)
    main_title = models.CharField(default="Keep your new born baby engaged", max_length=1010)
    sub_title = models.CharField(default="Lorem Ipsum is the best way of writing destiny car type", max_length=1010)
    button_text = models.CharField(default="Shop Now", max_length=100)
    button_url = models.URLField(default="https://recygo.com/shop/", max_length=1000)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = ("Home Two")
        
    def home_image(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))




class NewsLetter(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True, null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True, editable=True)


    def __str__(self):
        return self.email
    
class AnalyticsTrackingCode(models.Model):
    name_of_analytics = models.CharField(max_length=1000, help_text="Enter the name of analytics. E.g: Google Analytics")
    head_tag = models.TextField(null=True, blank=True, help_text="Any code pasted here would be added in the head tag. NOTE: Include the scripts or link tags")
    body_tag = models.TextField(null=True, blank=True, help_text="Codes pasted here would be added in the body tag. NOTE: Include the script or links or element tags")
    active = models.BooleanField(default=True)
    date = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True, editable=True)


    def __str__(self):
        return self.name_of_analytics

class Customers(models.Model):
    full_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    mobile = models.CharField(max_length=1000)
    country = models.ForeignKey("addon.TaxRate", on_delete=models.SET_NULL, null=True, blank=True)
    spent = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    cid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Customers"

    # def __str__(self):
    #     if self.full_name:
    #         return self.full_name
    #     elif self.user:
    #         return str(self.user)
    #     else:
    #         return str(self.cid)
