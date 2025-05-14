from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    '''
    Defines an inline admin interface for the Profile model, allowing
    profiles to be edited directly within the User admin page.
    '''
    model = Profile


class UserAdmin(admin.ModelAdmin):
    '''
    Customizes the admin interface for the User model by specifying
    fields to display and integrating the ProfileInline to allow
    editing of related Profile instances directly within the User
    admin page.
    '''
    model = User

    # fields = ['username']
    inlines = [ProfileInline]


admin.site.unregister(User)

admin.site.register(User, UserAdmin)
