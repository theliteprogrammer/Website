from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import WasteCategory, WasteItem, Employee, CollectionPoint, WasteOrder, CollectionEvent, CollectedWaste, WastePlan, Notification, Donation

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    list_display = ('thumbnail', 'full_name', 'user', 'role', 'active')
    search_fields = ('active',)

@admin.register(WasteCategory)
class WasteCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ('user', 'waste_plan', 'order', 'type', 'is_read')
    search_fields = ('user__username',)

# @admin.register(WasteItem)
class WasteItemAdmin(ImportExportModelAdmin):
    list_display = ('name', 'category', 'hazardous', 'recyclable')
    list_filter = ('category', 'hazardous', 'recyclable')
    search_fields = ('name',)

@admin.register(WastePlan)
class WastePlanAdmin(ImportExportModelAdmin):
    list_editable = ('user', 'name', 'category', 'price', 'active')
    list_display = ('thumbnail', 'user', 'name', 'category', 'price', 'active')
    list_filter = ('category', 'active')
    search_fields = ('name',)

@admin.register(WasteOrder)
class WasteOrderAdmin(ImportExportModelAdmin):
    list_display = ('thumbnail', 'waste_plan', 'oid', 'user', 'payment_status', 'price', 'collected_status', 'collector', 'active', 'date')
    list_editable = ('payment_status', 'price', 'collected_status', 'collector', 'active')
    list_filter = ('payment_status', 'active')
    search_fields = ('oid', 'waste_plan__name')


@admin.register(Donation)
class DonationAdmin(ImportExportModelAdmin):
    list_display = ('full_name', 'email', 'amount', 'payment_status', 'date')
    list_filter = ('payment_status', )
    search_fields = ('did', 'full_name')

# @admin.register(CollectionPoint)
class CollectionPointAdmin(ImportExportModelAdmin):
    list_display = ('name', 'address', 'capacity', 'current_fill')
    list_filter = ('capacity',)
    search_fields = ('name',)

# @admin.register(CollectionEvent)
class CollectionEventAdmin(ImportExportModelAdmin):
    list_display = ('collection_point', 'date', 'collected_weight')
    list_filter = ('date', 'collection_point')
    search_fields = ('collection_point__name',)

# @admin.register(CollectedWaste)
class CollectedWasteAdmin(ImportExportModelAdmin):
    list_display = ('event', 'waste_item', 'quantity', 'weight')
    list_filter = ('event__date', 'waste_item')
    search_fields = ('event__collection_point__name', 'waste_item__name')

