from django.contrib import admin

from .models import User, Organization, Event


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'organization'
    )
    list_filter = ('organization',)
    search_fields = ('email', 'first_name', 'last_name')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'address',
        'postcode'
    )
    search_fields = ('title', 'description', 'address', 'postcode')


class OrganizationInline(admin.TabularInline):
    model = Organization


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'description',
        'image',
        'date'
    )
    search_fields = ('title', 'description',)
    inlines = (OrganizationInline,)
