"""
cms/admin.py — Django Admin registration for CMS models.

Provides a fallback admin interface for managing CMS content
via Django's built-in admin panel at /admin/.
"""

from django.contrib import admin
from .models import (
    Banner, VisionMission, Statistic, Initiative,
    AboutMilestone, TeamMember, AboutEvent,
    ImpactStory, AnnualReport, VolunteerOpportunity,
    PartnerOrganization, OfficeLocation, FAQ, ContactInquiry
)


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')
    ordering = ('order',)


@admin.register(VisionMission)
class VisionMissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'section_type', 'order', 'is_active', 'created_at')
    list_filter = ('section_type', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'content')
    ordering = ('section_type', 'order')


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('label', 'value')
    ordering = ('order',)


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'curriculum_highlight', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'tag')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description', 'detailed_content')
    ordering = ('order',)


@admin.register(AboutMilestone)
class AboutMilestoneAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('year', 'title', 'description')
    ordering = ('order', 'year')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'role', 'bio')
    ordering = ('category', 'order')


@admin.register(AboutEvent)
class AboutEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'tag', 'order', 'is_active')
    list_filter = ('tag', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description', 'location')
    ordering = ('order', '-created_at')


@admin.register(ImpactStory)
class ImpactStoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_or_school', 'location', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'quote', 'story')
    ordering = ('order', '-created_at')


@admin.register(AnnualReport)
class AnnualReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'fiscal_year', 'order', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'fiscal_year', 'summary')
    ordering = ('order', '-fiscal_year')


@admin.register(VolunteerOpportunity)
class VolunteerOpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'commitment', 'mode', 'order', 'is_active')
    list_filter = ('mode', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'description', 'location')
    ordering = ('order',)


@admin.register(PartnerOrganization)
class PartnerOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'representative_name', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'representative_name', 'testimonial')
    ordering = ('order', 'name')


@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'phone', 'email', 'is_hq', 'order', 'is_active')
    list_filter = ('is_hq', 'is_active')
    list_editable = ('is_hq', 'order', 'is_active')
    search_fields = ('city', 'address', 'email', 'phone')
    ordering = ('-is_hq', 'order')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('question', 'answer')
    ordering = ('category', 'order')


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'subject', 'is_resolved', 'created_at')
    list_filter = ('category', 'is_resolved')
    list_editable = ('is_resolved',)
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('is_resolved', '-created_at')

