from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .forms import UserCreationForm, UserChangeForm
from .models import MyUser


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'is_superuser', 'is_active', 'phone', 'avatar')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_active', 'phone', 'avatar', 'subscribes')}),
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ('subscribes',)


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
