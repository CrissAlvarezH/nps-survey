from django.contrib import admin

from .models import Country, Company, CompanyUser, Nps


class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]


admin.site.register(Country, CountryAdmin)


class CompanyUserInline(admin.TabularInline):
    model = CompanyUser


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "country_name"]
    inlines = (CompanyUserInline,)


admin.site.register(Company, CompanyAdmin)


class NpsAdmin(admin.ModelAdmin):
    list_display = ["user", "answer", "created_at"]


admin.site.register(Nps, NpsAdmin)
