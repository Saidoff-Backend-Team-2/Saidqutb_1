from django.contrib import admin
from .models import *


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


class AboutUsGalleryInline(admin.StackedInline):
    model = AboutUsGallery
    extra = 2


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    inlines = [AboutUsGalleryInline]


@admin.register(AboutUsGallery)
class AboutUsGalleryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contacts)
admin.site.register(ContactWithUs)
admin.site.register(SocialMedia)


