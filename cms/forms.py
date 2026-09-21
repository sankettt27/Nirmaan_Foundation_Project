"""
cms/forms.py — Django ModelForms for CMS content management.

Each form provides validated input for creating/editing CMS items
via the Admin CMS dashboard.
"""

from django import forms
from .models import (
    Banner, VisionMission, Statistic, Initiative,
    AboutMilestone, TeamMember, AboutEvent,
    ImpactStory, AnnualReport, VolunteerOpportunity,
    PartnerOrganization, OfficeLocation, FAQ, ContactInquiry
)


# ─────────────────────────────────────────────────────────────
# SHARED WIDGET ATTRS
# ─────────────────────────────────────────────────────────────

_text_attrs = {
    'class': 'cms-input',
    'autocomplete': 'off',
}

_textarea_attrs = {
    'class': 'cms-input cms-textarea',
    'rows': 4,
}

_select_attrs = {
    'class': 'cms-input cms-select',
}

_file_attrs = {
    'class': 'cms-file-input',
    'accept': 'image/*',
}

_number_attrs = {
    'class': 'cms-input cms-number',
    'min': '0',
}

_checkbox_attrs = {
    'class': 'cms-checkbox',
}


# ─────────────────────────────────────────────────────────────
# BANNER FORM
# ─────────────────────────────────────────────────────────────

class BannerForm(forms.ModelForm):
    """Form for creating/editing Banner items."""

    class Meta:
        model = Banner
        fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., One Mission. Many Ways to Create Change.'}),
            'subtitle': forms.Textarea(attrs={**_textarea_attrs, 'placeholder': 'Supporting text for the banner...', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs=_file_attrs),
            'button_text': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Become a Volunteer'}),
            'button_link': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., #volunteer or /register/'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# VISION / MISSION FORM
# ─────────────────────────────────────────────────────────────

class VisionMissionForm(forms.ModelForm):
    """Form for creating/editing Vision & Mission items."""

    class Meta:
        model = VisionMission
        fields = ['section_type', 'title', 'content', 'icon', 'order', 'is_active']
        widgets = {
            'section_type': forms.Select(attrs=_select_attrs),
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Our Vision for India'}),
            'content': forms.Textarea(attrs={**_textarea_attrs, 'placeholder': 'Full text content for this section...'}),
            'icon': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., bi-eye-fill or bi-bullseye'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# STATISTIC FORM
# ─────────────────────────────────────────────────────────────

class StatisticForm(forms.ModelForm):
    """Form for creating/editing Impact Statistics."""

    class Meta:
        model = Statistic
        fields = ['value', 'label', 'icon', 'order', 'is_active']
        widgets = {
            'value': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., 30K+ or 7,500+'}),
            'label': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Children Impacted Every Year'}),
            'icon': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., bi-people-fill'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# INITIATIVE FORM
# ─────────────────────────────────────────────────────────────

class InitiativeForm(forms.ModelForm):
    """Form for creating/editing Initiative/Program items."""

    class Meta:
        model = Initiative
        fields = [
            'title', 'description', 'image', 'tag', 'link',
            'detailed_content', 'key_features', 'curriculum_highlight', 'beneficiaries_reached',
            'order', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Strong Foundations'}),
            'description': forms.Textarea(attrs={**_textarea_attrs, 'placeholder': 'Brief description for home page card...'}),
            'image': forms.ClearableFileInput(attrs=_file_attrs),
            'tag': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., In Schools, STEM & Digital'}),
            'link': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., #programs or /programs/'}),
            'detailed_content': forms.Textarea(attrs={**_textarea_attrs, 'rows': 6, 'placeholder': 'Comprehensive program overview for the Programs page...'}),
            'key_features': forms.Textarea(attrs={**_textarea_attrs, 'rows': 4, 'placeholder': 'Enter key features / highlights, one bullet per line...'}),
            'curriculum_highlight': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Foundational Numeracy & Robotics'}),
            'beneficiaries_reached': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., 15,000+ Students'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# ABOUT MILESTONE FORM
# ─────────────────────────────────────────────────────────────

class AboutMilestoneForm(forms.ModelForm):
    class Meta:
        model = AboutMilestone
        fields = ['year', 'title', 'description', 'icon', 'order', 'is_active']
        widgets = {
            'year': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., 2014 or 2018–2020'}),
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Foundation Established in Bengaluru'}),
            'description': forms.Textarea(attrs={**_textarea_attrs, 'placeholder': 'Milestone background and achievements...'}),
            'icon': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., bi-flag-fill, bi-mortarboard-fill'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# TEAM MEMBER FORM
# ─────────────────────────────────────────────────────────────

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'category', 'bio', 'photo', 'linkedin_url', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Dr. Ananya Sen'}),
            'role': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Co-Founder & Executive Director'}),
            'category': forms.Select(attrs=_select_attrs),
            'bio': forms.Textarea(attrs={**_textarea_attrs, 'rows': 3, 'placeholder': 'Brief biographical background...'}),
            'photo': forms.ClearableFileInput(attrs=_file_attrs),
            'linkedin_url': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'https://linkedin.com/in/...'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# ABOUT EVENT FORM
# ─────────────────────────────────────────────────────────────

class AboutEventForm(forms.ModelForm):
    class Meta:
        model = AboutEvent
        fields = ['title', 'event_date', 'location', 'tag', 'description', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Annual Children STEM Expo 2026'}),
            'event_date': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., February 2026 or Ongoing'}),
            'location': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Bengaluru Chapter'}),
            'tag': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Community Drive, Workshop, Youth Summit'}),
            'description': forms.Textarea(attrs={**_textarea_attrs, 'placeholder': 'Event description, highlights, and participant outcomes...'}),
            'image': forms.ClearableFileInput(attrs=_file_attrs),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# IMPACT STORY FORM
# ─────────────────────────────────────────────────────────────

class ImpactStoryForm(forms.ModelForm):
    class Meta:
        model = ImpactStory
        fields = ['name', 'role_or_school', 'location', 'quote', 'story', 'photo', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Rajesh Kumar / ZP Govt School'}),
            'role_or_school': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Class 9 Scholar'}),
            'location': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Bengaluru, Karnataka'}),
            'quote': forms.Textarea(attrs={**_textarea_attrs, 'rows': 3, 'placeholder': 'Short impactful quote or headline...'}),
            'story': forms.Textarea(attrs={**_textarea_attrs, 'rows': 5, 'placeholder': 'Full transformation story and journey...'}),
            'photo': forms.ClearableFileInput(attrs=_file_attrs),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# ANNUAL REPORT FORM
# ─────────────────────────────────────────────────────────────

class AnnualReportForm(forms.ModelForm):
    class Meta:
        model = AnnualReport
        fields = ['title', 'fiscal_year', 'summary', 'file_url', 'cover_image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Annual Impact & Financial Disclosure Report'}),
            'fiscal_year': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., 2024–2025'}),
            'summary': forms.Textarea(attrs={**_textarea_attrs, 'rows': 3, 'placeholder': 'Brief overview of financials, audits, and program reach...'}),
            'file_url': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'PDF download URL or link'}),
            'cover_image': forms.ClearableFileInput(attrs=_file_attrs),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# VOLUNTEER OPPORTUNITY FORM
# ─────────────────────────────────────────────────────────────

class VolunteerOpportunityForm(forms.ModelForm):
    class Meta:
        model = VolunteerOpportunity
        fields = ['title', 'commitment', 'mode', 'location', 'description', 'requirements', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Weekend Teaching Mentor (Math & Science)'}),
            'commitment': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., 2–4 hours / weekend'}),
            'mode': forms.Select(attrs=_select_attrs),
            'location': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Bengaluru, Mumbai, Pune Chapters'}),
            'description': forms.Textarea(attrs={**_textarea_attrs, 'placeholder': 'What this volunteer role entails...'}),
            'requirements': forms.Textarea(attrs={**_textarea_attrs, 'rows': 4, 'placeholder': 'Requirements / skills, one bullet per line...'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# PARTNER ORGANIZATION FORM
# ─────────────────────────────────────────────────────────────

class PartnerOrganizationForm(forms.ModelForm):
    class Meta:
        model = PartnerOrganization
        fields = ['name', 'category', 'logo', 'website_url', 'testimonial', 'representative_name', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Infosys Foundation / Wipro Cares'}),
            'category': forms.Select(attrs=_select_attrs),
            'logo': forms.ClearableFileInput(attrs=_file_attrs),
            'website_url': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'https://...'}),
            'testimonial': forms.Textarea(attrs={**_textarea_attrs, 'rows': 3, 'placeholder': 'Optional partner quote or endorsement...'}),
            'representative_name': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Sunita Rao, Head of CSR'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# OFFICE LOCATION FORM
# ─────────────────────────────────────────────────────────────

class OfficeLocationForm(forms.ModelForm):
    class Meta:
        model = OfficeLocation
        fields = ['city', 'address', 'email', 'phone', 'is_hq', 'order', 'is_active']
        widgets = {
            'city': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Bengaluru'}),
            'address': forms.Textarea(attrs={**_textarea_attrs, 'rows': 3, 'placeholder': 'Street, Area, Pin code...'}),
            'email': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'bengaluru@nirmaanfoundation.org'}),
            'phone': forms.TextInput(attrs={**_text_attrs, 'placeholder': '+91 80 0000 0000'}),
            'is_hq': forms.CheckboxInput(attrs=_checkbox_attrs),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }


# ─────────────────────────────────────────────────────────────
# FAQ FORM
# ─────────────────────────────────────────────────────────────

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['category', 'question', 'answer', 'order', 'is_active']
        widgets = {
            'category': forms.Select(attrs=_select_attrs),
            'question': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., How do I get an 80G tax exemption certificate?'}),
            'answer': forms.Textarea(attrs={**_textarea_attrs, 'rows': 4, 'placeholder': 'Clear and helpful answer...'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }

