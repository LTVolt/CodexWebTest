from django.contrib import admin

from .models import Amenity, Favorite, Lead, Location, Property, PropertyImage, PropertyType, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone_number", "created_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "phone_number")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("district", "city", "neighborhood", "postal_code")
    search_fields = ("district", "city", "neighborhood", "postal_code")


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "agent",
        "listing_type",
        "status",
        "price",
        "location",
        "is_featured",
        "created_at",
    )
    list_filter = ("listing_type", "status", "property_type", "is_featured", "location__district")
    list_select_related = ("agent", "property_type", "location")
    search_fields = ("title", "slug", "description", "address")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("amenities",)
    inlines = [PropertyImageInline]


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "property", "status", "created_at")
    list_filter = ("status",)
    list_select_related = ("property", "customer")
    search_fields = ("full_name", "email", "phone", "property__title")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "property", "created_at")
    list_select_related = ("user", "property")
    search_fields = ("user__username", "property__title")
