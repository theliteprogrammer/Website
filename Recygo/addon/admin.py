from django.contrib import admin

from django.contrib import admin
from addon.models import AboutUS, BasicAddon, NewsLetterText, FooterBenefits, AffiliateLandingPage ,Company, PaymentMethod ,EarningPoints, PayoutMethod, Policy, TaxRate, SuperUserSignUpPin, ContactUs, FAQs, AnnouncementsModal, AnnouncementsTopbar, ChangeLog, PlatformNotifications, TutorialVideo, SupportContactInformation, HomePageSetup, Home_One, Home_Two, Team, Partner, Feature, BecomeAVendor, Home_One_Sidebar
from import_export.admin import ImportExportModelAdmin


class NewsLetterText_Tab(admin.TabularInline):
    model = NewsLetterText

class Feature_Tab(admin.TabularInline):
    model = Feature

class AffiliateLandingPage_Tab(admin.TabularInline):
    model = AffiliateLandingPage

class BecomeAVendor_Tab(admin.TabularInline):
    model = BecomeAVendor

class Team_Tab(admin.TabularInline):
    model = Team
    extra = 0

class Partner_Tab(admin.TabularInline):
    model = Partner
    extra = 0


class FooterBenefits_Tab(admin.TabularInline):
    model = FooterBenefits

class HomeOne_Tab(admin.TabularInline):
    model = Home_One
    extra = 0


class HomeTwo_Tab(admin.TabularInline):
    model = Home_Two
    extra = 0

class HomeOne_Sidebar_Tab(admin.TabularInline):
    model = Home_One_Sidebar
    extra = 0


class ChangeLogAdmin(ImportExportModelAdmin):
    list_editable = ['active', 'date']
    list_display = ['title', 'active', 'date']

class AboutUsAdmin(ImportExportModelAdmin):
    inlines = [Feature_Tab, Team_Tab, Partner_Tab]
    list_display = ['thumbnail', 'title']


class BasicAddonsAdmin(ImportExportModelAdmin):
    inlines = [NewsLetterText_Tab, FooterBenefits_Tab, AffiliateLandingPage_Tab, BecomeAVendor_Tab]
    list_editable = ['service_fee_percentage', 'affiliate_commission_percentage', 'currency_abbreviation', 'vendor_fee_percentage', 'registration_form_type', 'header_type' ,'send_email_notifications', 'payout_vendor_fee_immediately']
    list_display = ['view_more', 'currency_sign', 'service_fee_percentage', 'affiliate_commission_percentage', 'currency_abbreviation', 'vendor_fee_percentage', 'registration_form_type', 'header_type' ,'send_email_notifications', 'payout_vendor_fee_immediately']


class EarningPointsAdmin(ImportExportModelAdmin):
    list_display = ['signup_point', "enable_signup_point"]


class HomePageSetupAdmin(ImportExportModelAdmin):
    inlines = [HomeOne_Tab, HomeOne_Sidebar_Tab]
    list_editable = ['homepage_type']
    list_display = ['title', "homepage_type"]


class HomeOneAdmin(ImportExportModelAdmin):
    list_editable = ['small_text', 'small_sub_text' ,'main_text', 'description_text' ,'background_color', 'button_text', 'button_url', 'active', 'first']
    list_display = ['homepage', "home_image", 'small_text', 'small_sub_text' ,'main_text', 'description_text' ,'background_color', 'button_text', 'button_url', 'active', 'first']

class HomeTwoAdmin(ImportExportModelAdmin):
    pass

    # list_editable = ['small_title', 'main_title', 'sub_title', 'button_text', 'button_url', 'active']
    # list_display = ['homepage', "home_image", 'small_title', 'main_title', 'sub_title', 'button_text', 'button_url', 'active']





class CompanyAdmin(ImportExportModelAdmin):
    list_editable = ['website_address', 'homepage', 'logo_type']
    list_display = ['name', 'website_address', 'homepage', 'logo_type']
    
class TaxRateAdmin(ImportExportModelAdmin):
    search_fields = ['country', 'custom_name']
    list_editable = ['rate', 'custom_name', 'active']
    list_display = ['country', 'rate', 'custom_name', 'active']
    
    
class ContactUsAdmin(ImportExportModelAdmin):
    list_editable = ['resolved']
    list_display = ['topic', 'full_name', 'email', 'subject', 'resolved', 'date']

class FAQsAdmin(ImportExportModelAdmin):
    list_editable = ['share']
    list_display = ['question', 'answer', 'email', 'share']


class PlatformNotificationsAdmin(ImportExportModelAdmin):
    list_display = ['title', 'active']

class TutorialVideoAdmin(ImportExportModelAdmin):
    list_editable = ['how_to_use_platform', 'how_to_use_affiliate_system', 'how_to_become_a_vendor']
    list_display = ['title', 'how_to_use_platform', 'how_to_use_affiliate_system', 'how_to_become_a_vendor']

class PaymentMethodAdmin(ImportExportModelAdmin):
    list_editable = ['active']
    list_display = ['name', 'active']

class PayoutMethodAdmin(ImportExportModelAdmin):
    list_editable = ['active']
    list_display = ['name', 'active']


admin.site.register(BasicAddon, BasicAddonsAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Policy)
admin.site.register(AboutUS, AboutUsAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(FAQs, FAQsAdmin)
admin.site.register(AnnouncementsModal)
admin.site.register(AnnouncementsTopbar)
admin.site.register(ChangeLog, ChangeLogAdmin)
admin.site.register(PlatformNotifications, PlatformNotificationsAdmin)
admin.site.register(SupportContactInformation)
admin.site.register(TaxRate, TaxRateAdmin)
admin.site.register(HomePageSetup, HomePageSetupAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(PayoutMethod, PayoutMethodAdmin)
admin.site.register(BecomeAVendor)
admin.site.register(AffiliateLandingPage)

# admin.site.register(Home_One, HomeOneAdmin)
# admin.site.register(Home_Two, HomeTwoAdmin)
# admin.site.register(EarningPoints, EarningPointsAdmin)
# admin.site.register(SuperUserSignUpPin)

