from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from account.models import User


class UserCreationForm(forms.ModelForm):
    username  = forms.CharField()
    email     = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('__all__' )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('This username has been taken.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email has been taken.'))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):       
    username = forms.CharField()
    email    = forms.EmailField(required=True)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('__all__' )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.id).exists():
            raise forms.ValidationError(_('This username has been taken.'))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(email=self.instance.email).exists():
            raise forms.ValidationError(_('This email has been taken.'))
        return email

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'username', 'gender', 'score', 'is_admin')
    list_filter = ('gender', 'is_admin', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Personal info', {'fields': ('username','fullname', 'gender', 'dob', 'score', 'avatar', 'avatar_preview')}),
        ('Permissions', {'fields': ('is_admin', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'fullname', 'email', 'score')
    readonly_fields = ('created_at', 'is_active', 'avatar_preview')

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.exclude(is_superuser=True)
        return qs

    def avatar_preview(self, obj):
        return obj.avatar_preview

    avatar_preview.short_description = 'Avatar Preview'

admin.site.site_header = "Pacer Demo Admin Portal"  
admin.site.site_title  = "Pacer Demo Admin Portal" 
admin.site.index_title = "Pacer Demo Admin Portal" 
admin.site.register(User, UserAdmin)