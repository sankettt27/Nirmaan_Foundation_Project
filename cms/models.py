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
    detailed_content = models.TextField(
        blank=True,
        verbose_name='Detailed Description',
        help_text='In-depth description for the dedicated Programs page',
    )
    key_features = models.TextField(
        blank=True,
        verbose_name='Key Highlights / Features',
        help_text='Key features, enter one bullet point per line',
    )
    curriculum_highlight = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Curriculum Focus',
        help_text='e.g., Foundational Numeracy, Digital Robotics, Leadership',
    )
    beneficiaries_reached = models.CharField(
        max_length=50,
        blank=True,
        default='10,000+ Students',
        verbose_name='Beneficiaries Reached',
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
        verbose_name = 'Initiative / Program'
        verbose_name_plural = 'Initiatives / Programs'

    def __str__(self):
        status = '✓' if self.is_active else '✗'
        return f'[{status}] {self.title}'


# ============================================================
# ABOUT US PAGE MODELS (ASSIGNMENT 3)
# ============================================================

class OurStory(models.Model):
    """
    Stores the narrative content for the 'Our Story' section.
    Database table: our_story (as specified in Assignment 3).
    """
    content = models.TextField(
        verbose_name='Story Content',
        help_text="Detailed narrative describing the NGO's founding, journey, and community impact."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'our_story'
        verbose_name = 'Our Story'
        verbose_name_plural = 'Our Story'

    def __str__(self):
        return f"Our Story (Updated {self.updated_at.strftime('%Y-%m-%d') if self.updated_at else 'New'})"


class CoreValue(models.Model):
    """
    Stores guiding principles for the 'Core Values' section.
    Database table: core_values (as specified in Assignment 3).
    """
    value = models.CharField(
        max_length=255,
        verbose_name='Core Value',
        help_text='A single core value (e.g., Integrity, Inclusivity, Empathy, Transparency)'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
        help_text='Brief explanation of how this value guides our work'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='bi-shield-check',
        verbose_name='Bootstrap Icon Class',
        help_text='Bootstrap icon class (e.g., bi-shield-check, bi-heart-fill, bi-gem)'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'core_values'
        ordering = ['order', 'id']
        verbose_name = 'Core Value'
        verbose_name_plural = 'Core Values'

    def __str__(self):
        return self.value


class Program(models.Model):
    """
    Stores key focus areas and initiatives for the 'Programs' section.
    Database table: programs (as specified in Assignment 3).
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Program Name',
        help_text='Name of the program (e.g., Free Educational Resources)'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Program Description',
        help_text='Detailed description of the program and key activities'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        default='bi-mortarboard-fill',
        verbose_name='Bootstrap Icon Class'
    )
    image = models.ImageField(
        upload_to='cms/programs/',
        blank=True,
        null=True,
        verbose_name='Program Image',
        help_text='Upload an image to represent this program focus area'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Display Order'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'programs'
        ordering = ['order', 'id']
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'

    def __str__(self):
        return self.name


class AboutMilestone(models.Model):
    """Timeline journey milestone on the About Us page."""
    year = models.CharField(max_length=20, verbose_name='Year / Period', help_text='e.g., "2014" or "2018–2020"')
    title = models.CharField(max_length=200, verbose_name='Milestone Title')
    description = models.TextField(verbose_name='Description')
    icon = models.CharField(max_length=50, blank=True, default='bi-flag-fill', verbose_name='Bootstrap Icon')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_about_milestone'
        ordering = ['order', 'year']
        verbose_name = 'About Milestone'
        verbose_name_plural = 'About Milestones'

    def __str__(self):
        return f'{self.year} — {self.title}'


class TeamMember(models.Model):
    """
    Leadership and Advisory team member on the About Us page.
    Database table: team_members (as specified in Assignment 3).
    """
    CATEGORY_CHOICES = [
        ('leadership', 'Leadership Team'),
        ('advisory', 'Advisory Board'),
        ('chapter_lead', 'Chapter Lead'),
    ]

    name = models.CharField(max_length=255, verbose_name='Full Name')
    role = models.CharField(max_length=255, verbose_name='Designation / Role')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='leadership', verbose_name='Category')
    bio = models.TextField(blank=True, verbose_name='Short Bio')
    photo = models.ImageField(upload_to='cms/team/', blank=True, null=True, verbose_name='Photo', help_text='Recommended: square 400x400px')
    image_url = models.CharField(max_length=255, blank=True, default='', verbose_name='Image URL', help_text="URL or path to the team member's photo")
    linkedin_url = models.CharField(max_length=300, blank=True, verbose_name='LinkedIn Profile URL')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'team_members'
        ordering = ['category', 'order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f'{self.name} ({self.role})'

    def get_image_display_url(self):
        if self.photo:
            try:
                return self.photo.url
            except Exception:
                pass
        if self.image_url:
            return self.image_url
        return ''

    def save(self, *args, **kwargs):
        if self.photo and not self.image_url:
            try:
                self.image_url = self.photo.url
            except Exception:
                pass
        super().save(*args, **kwargs)


class AboutEvent(models.Model):
    """Events, activities, and gallery items on the About Us page."""
    title = models.CharField(max_length=200, verbose_name='Event Title')
    event_date = models.CharField(max_length=100, blank=True, verbose_name='Date / Timeframe', help_text='e.g., "February 2026"')
    location = models.CharField(max_length=150, blank=True, default='Bengaluru', verbose_name='Location')
    tag = models.CharField(max_length=50, blank=True, default='Community Drive', verbose_name='Tag / Category')
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(upload_to='cms/events/', blank=True, null=True, verbose_name='Event Image', help_text='Recommended: 800x500px')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_about_event'
        ordering = ['order', '-created_at']
        verbose_name = 'Event / Activity'
        verbose_name_plural = 'Events & Activities'

    def __str__(self):
        return self.title


# ============================================================
# IMPACT PAGE MODELS
# ============================================================

class ImpactStory(models.Model):
    """Student and community transformation case studies on Impact page."""
    name = models.CharField(max_length=150, verbose_name='Beneficiary / School Name')
    role_or_school = models.CharField(max_length=150, blank=True, verbose_name='Class / School / Role', help_text='e.g., "Grade 8, Government High School"')
    location = models.CharField(max_length=100, blank=True, default='Bengaluru', verbose_name='City / Location')
    quote = models.TextField(verbose_name='Key Quote', help_text='Highlight quote that captures the impact')
    story = models.TextField(blank=True, verbose_name='Full Transformation Story')
    photo = models.ImageField(upload_to='cms/impact_stories/', blank=True, null=True, verbose_name='Photo', help_text='Recommended: 600x600px')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_impact_story'
        ordering = ['order', '-created_at']
        verbose_name = 'Impact Story'
        verbose_name_plural = 'Impact Stories'

    def __str__(self):
        return f'{self.name} — {self.location}'


class AnnualReport(models.Model):
    """Annual audited reports and disclosures on Impact page."""
    title = models.CharField(max_length=200, verbose_name='Report Title')
    fiscal_year = models.CharField(max_length=50, verbose_name='Fiscal Year', help_text='e.g., "2024–25"')
    summary = models.TextField(blank=True, verbose_name='Summary Highlights')
    file_url = models.CharField(max_length=500, blank=True, default='#', verbose_name='Download Link or PDF URL')
    cover_image = models.ImageField(upload_to='cms/reports/', blank=True, null=True, verbose_name='Report Cover Image')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_annual_report'
        ordering = ['order', '-fiscal_year']
        verbose_name = 'Annual Report'
        verbose_name_plural = 'Annual Reports'

    def __str__(self):
        return f'{self.title} ({self.fiscal_year})'


# ============================================================
# VOLUNTEER PAGE MODELS
# ============================================================

class VolunteerOpportunity(models.Model):
    """Available volunteer tracks and drives on Volunteer page."""
    MODE_CHOICES = [
        ('in_person', 'In-Person (Classrooms)'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote / Online'),
    ]

    title = models.CharField(max_length=200, verbose_name='Role Title', help_text='e.g., "Weekend Teaching Volunteer"')
    commitment = models.CharField(max_length=100, default='2–4 hours / weekend', verbose_name='Time Commitment')
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='in_person', verbose_name='Engagement Mode')
    location = models.CharField(max_length=150, default='Bengaluru, Mumbai, Pune Chapters', verbose_name='Locations')
    description = models.TextField(verbose_name='Role Overview')
    requirements = models.TextField(blank=True, verbose_name='Requirements', help_text='Enter one bullet point per line')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_volunteer_opportunity'
        ordering = ['order', '-created_at']
        verbose_name = 'Volunteer Opportunity'
        verbose_name_plural = 'Volunteer Opportunities'

    def __str__(self):
        return self.title


# ============================================================
# PARTNER / CSR PAGE MODELS
# ============================================================

class PartnerOrganization(models.Model):
    """CSR and institutional partners on Partner With Us page."""
    CATEGORY_CHOICES = [
        ('corporate', 'Corporate CSR Partner'),
        ('foundation', 'Philanthropic Foundation'),
        ('institutional', 'Institutional Partner'),
    ]

    name = models.CharField(max_length=200, verbose_name='Partner Name')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='corporate', verbose_name='Category')
    logo = models.ImageField(upload_to='cms/partners/', blank=True, null=True, verbose_name='Partner Logo')
    website_url = models.CharField(max_length=300, blank=True, verbose_name='Partner Website URL')
    testimonial = models.TextField(blank=True, verbose_name='Partner Testimonial / Endorsement')
    representative_name = models.CharField(max_length=150, blank=True, verbose_name='Representative & Title')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_partner_organization'
        ordering = ['order', 'name']
        verbose_name = 'Partner Organization'
        verbose_name_plural = 'Partner Organizations'

    def __str__(self):
        return self.name


# ============================================================
# CONTACT PAGE & FAQ MODELS
# ============================================================

class OfficeLocation(models.Model):
    """Physical chapters and branch offices on Contact page."""
    city = models.CharField(max_length=100, verbose_name='City / Chapter Name')
    address = models.TextField(verbose_name='Full Address')
    email = models.CharField(max_length=150, default='hello@nirmaanfoundation.org', verbose_name='Email')
    phone = models.CharField(max_length=50, default='+91 80 0000 0000', verbose_name='Phone')
    is_hq = models.BooleanField(default=False, verbose_name='Is Headquarters')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_office_location'
        ordering = ['-is_hq', 'order', 'city']
        verbose_name = 'Office Location'
        verbose_name_plural = 'Office Locations'

    def __str__(self):
        return f'{self.city} {"(HQ)" if self.is_hq else ""}'


class FAQ(models.Model):
    """Frequently asked questions displayed across pages."""
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('volunteer', 'Volunteering'),
        ('programs', 'Programs & Education'),
        ('partner', 'CSR & Partnerships'),
        ('donation', 'Donations & Tax Benefits'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general', verbose_name='Category')
    question = models.CharField(max_length=300, verbose_name='Question')
    answer = models.TextField(verbose_name='Answer')
    order = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cms_faq'
        ordering = ['category', 'order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class ContactInquiry(models.Model):
    """Visitor contact form submissions."""
    CATEGORY_CHOICES = [
        ('general', 'General Inquiry'),
        ('volunteer', 'Volunteering'),
        ('partner', 'CSR / Partnership'),
        ('donation', 'Donation / Tax Exemption'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=150, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email Address')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Phone Number')
    subject = models.CharField(max_length=200, verbose_name='Subject')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general', verbose_name='Category')
    message = models.TextField(verbose_name='Message')
    is_resolved = models.BooleanField(default=False, verbose_name='Resolved / Handled')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Submitted At')

    class Meta:
        db_table = 'cms_contact_inquiry'
        ordering = ['is_resolved', '-created_at']
        verbose_name = 'Contact Inquiry'
        verbose_name_plural = 'Contact Inquiries'

    def __str__(self):
        status = '✓' if self.is_resolved else '●'
        return f'[{status}] {self.name} — {self.subject}'


# ============================================================
# PROJECTS PAGE MODELS (ASSIGNMENT 4)
# ============================================================

class Project(models.Model):
    """
    Nirmaan Foundation Projects.
    Database table: projects (as specified in Assignment 4).
    """
    STATUS_CHOICES = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Upcoming', 'Upcoming'),
    ]

    title = models.CharField(max_length=255, verbose_name='Project Title')
    description = models.TextField(verbose_name='Description')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Status')
    start_date = models.DateField(blank=True, null=True, verbose_name='Start Date')
    end_date = models.DateField(blank=True, null=True, verbose_name='End Date')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Location')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-start_date', 'title']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    @property
    def primary_image(self):
        return self.images.first()


class ProjectImage(models.Model):
    """
    Multiple images associated with a Project.
    Database table: project_images (as specified in Assignment 4).
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name='Project')
    image_url = models.ImageField(upload_to='cms/projects/', verbose_name='Image URL')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_images'
        ordering = ['-uploaded_at']
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    def __str__(self):
        return f"Image for {self.project.title}"


# ============================================================
# MEDIA PAGE MODELS (ASSIGNMENT 5)
# ============================================================

class PressRelease(models.Model):
    """
    Press releases for the media page.
    """
    title = models.CharField(max_length=255, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    release_date = models.DateField(verbose_name='Release Date')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'press_release'
        ordering = ['-release_date', '-created_at']
        verbose_name = 'Press Release'
        verbose_name_plural = 'Press Releases'

    def __str__(self):
        return self.title


class MediaCoverage(models.Model):
    """
    External media coverage links.
    """
    title = models.CharField(max_length=255, verbose_name='Title')
    url = models.URLField(max_length=2083, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'media_coverage'
        ordering = ['-created_at']
        verbose_name = 'Media Coverage'
        verbose_name_plural = 'Media Coverage'

    def __str__(self):
        return self.title


class ImageGallery(models.Model):
    """
    Image gallery for the media page.
    """
    image_path = models.ImageField(upload_to='cms/gallery/', max_length=2083, verbose_name='Image Path')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Description')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image_gallery'
        ordering = ['-uploaded_at']
        verbose_name = 'Image Gallery'
        verbose_name_plural = 'Image Galleries'

    def __str__(self):
        return self.description or f"Gallery Image {self.id}"


class Video(models.Model):
    """
    Video links for the media page.
    """
    video_url = models.URLField(max_length=2083, verbose_name='Video URL')
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name='Description')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'video'
        ordering = ['-uploaded_at']
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.description or f"Video {self.id}"

    @property
    def embed_url(self):
        """Convert standard YouTube URLs to privacy-enhanced embed URLs for iframes."""
        if 'youtube.com/watch?v=' in self.video_url:
            video_id = self.video_url.split('v=')[1][:11]
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
        elif 'youtu.be/' in self.video_url:
            video_id = self.video_url.split('youtu.be/')[1][:11]
            return f"https://www.youtube-nocookie.com/embed/{video_id}"
        return self.video_url


# ============================================================
# VOLUNTEER REGISTRATION MODEL (ASSIGNMENT 6 — VOLUNTEER DASHBOARD)
# ============================================================

class VolunteerRegistration(models.Model):
    """
    Tracks a volunteer's registration for a VolunteerOpportunity.

    Flow:
        Volunteer registers → status=Pending
        Admin reviews → sets Approved or Rejected
        Volunteer dashboard shows real-time status

    Enforces: one registration per volunteer per opportunity (unique_together).
    """
    STATUS_CHOICES = [
        ('pending',  'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    volunteer = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='volunteer_registrations',
        verbose_name='Volunteer',
    )
    opportunity = models.ForeignKey(
        'VolunteerOpportunity',
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='Opportunity',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status',
    )
    note = models.TextField(
        blank=True,
        verbose_name='Admin Note',
        help_text='Internal note from admin about this registration',
    )
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='Registered At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    class Meta:
        db_table = 'volunteer_registration'
        unique_together = ('volunteer', 'opportunity')
        ordering = ['-registered_at']
        verbose_name = 'Volunteer Registration'
        verbose_name_plural = 'Volunteer Registrations'

    def __str__(self):
        return f'{self.volunteer.full_name} → {self.opportunity.title} [{self.get_status_display()}]'

    @property
    def status_badge_class(self):
        """Return CSS class for status badge."""
        return {
            'pending':  'badge-warning',
            'approved': 'badge-success',
            'rejected': 'badge-danger',
        }.get(self.status, 'badge-secondary')
