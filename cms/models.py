"""
cms/models.py — Content Management System Models for Nirmaan Foundation.

Assignment 2: Home Page Content Management System

Models:
    Banner         — Hero section image slider items
    VisionMission  — Vision & Mission content blocks
    Statistic      — Impact statistics counters
    Initiative     — Programs/initiatives showcase cards

All models include:
    - `order` field for admin-controlled display ordering
    - `is_active` toggle for publish/unpublish without deleting
    - `created_at` / `updated_at` timestamps for audit trail
"""

from django.db import models


class Banner(models.Model):
    """
    Hero section banner/slider item.

    Admins can upload multiple banner images with titles, subtitles,
    and call-to-action buttons. Banners are displayed in order on the
    public home page hero section.
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Banner Title',
        help_text='Main heading displayed on the banner (e.g., "One Mission. Many Ways to Create Change.")',
    )
    subtitle = models.TextField(
        blank=True,
        verbose_name='Subtitle',
        help_text='Supporting text displayed below the title',
    )
    image = models.ImageField(
        upload_to='cms/banners/',
        blank=True,
        null=True,
        verbose_name='Banner Image',
        help_text='Recommended size: 1920x1080px. Leave blank to use default background.',
    )
    button_text = models.CharField(
        max_length=50,
        blank=True,
        default='Learn More',
        verbose_name='Button Text',
    )
    button_link = models.CharField(
        max_length=300,
        blank=True,
        default='#programs',
        verbose_name='Button Link',
        help_text='URL or anchor link (e.g., #programs, /register/)',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
        help_text='Lower numbers appear first',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
        help_text='Uncheck to hide this banner from the public site',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_banner'
        ordering = ['order', '-created_at']
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        status = '✓' if self.is_active else '✗'
        return f'[{status}] {self.title}'


class VisionMission(models.Model):
    """
    Vision & Mission content blocks.

    Each record represents either a 'vision' or 'mission' content item.
    Multiple items per section type are supported for flexibility.
    """
    SECTION_CHOICES = [
        ('vision', 'Vision'),
        ('mission', 'Mission'),
    ]

    section_type = models.CharField(
        max_length=10,
        choices=SECTION_CHOICES,
        verbose_name='Section Type',
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Title',
        help_text='Heading for this vision/mission item',
    )
    content = models.TextField(
        verbose_name='Content',
        help_text='Full text content for this section',
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='bi-star-fill',
        verbose_name='Bootstrap Icon Class',
        help_text='Bootstrap icon class name (e.g., bi-eye-fill, bi-bullseye)',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_vision_mission'
        ordering = ['section_type', 'order', '-created_at']
        verbose_name = 'Vision / Mission Item'
        verbose_name_plural = 'Vision / Mission Items'

    def __str__(self):
        status = '✓' if self.is_active else '✗'
        return f'[{status}] [{self.get_section_type_display()}] {self.title}'


class Statistic(models.Model):
    """
    Impact statistics displayed on the home page.

    Values are stored as text to support formatted numbers like "30K+", "7.5K+", "18+".
    """
    label = models.CharField(
        max_length=100,
        verbose_name='Label',
        help_text='Description text (e.g., "Children Impacted Every Year")',
    )
    value = models.CharField(
        max_length=50,
        verbose_name='Value',
        help_text='Stat value as displayed (e.g., "30K+", "7,500+", "18+")',
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='bi-graph-up-arrow',
        verbose_name='Bootstrap Icon Class',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_statistic'
        ordering = ['order', '-created_at']
        verbose_name = 'Statistic'
        verbose_name_plural = 'Statistics'

    def __str__(self):
        status = '✓' if self.is_active else '✗'
        return f'[{status}] {self.value} — {self.label}'


class Initiative(models.Model):
    """
    Programs/initiatives showcase cards on the home page.

    Each initiative has an image, title, description, and tag.
    Displayed in a grid on the Programs section.
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Initiative Title',
    )
    description = models.TextField(
        verbose_name='Description',
        help_text='Brief description of this program/initiative',
    )
    image = models.ImageField(
        upload_to='cms/initiatives/',
        blank=True,
        null=True,
        verbose_name='Initiative Image',
        help_text='Recommended size: 600x400px',
    )
    tag = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Tag',
        help_text='Category tag (e.g., "In Schools", "Beyond Schools", "Youth Leadership")',
    )
    link = models.CharField(
        max_length=300,
        blank=True,
        default='#programs',
        verbose_name='Link',
        help_text='URL or anchor for "Learn more" button',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_initiative'
        ordering = ['order', '-created_at']
        verbose_name = 'Initiative'
        verbose_name_plural = 'Initiatives'

    def __str__(self):
        status = '✓' if self.is_active else '✗'
        return f'[{status}] {self.title}'
