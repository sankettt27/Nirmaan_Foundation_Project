"""
cms/forms.py — Django ModelForms for CMS content management.

Each form provides validated input for creating/editing CMS items
via the Admin CMS dashboard.
"""

from django import forms
from .models import Banner, VisionMission, Statistic, Initiative


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
        fields = ['title', 'description', 'image', 'tag', 'link', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., Strong Foundations'}),
            'description': forms.Textarea(attrs={**_textarea_attrs, 'placeholder': 'Brief description of this program...'}),
            'image': forms.ClearableFileInput(attrs=_file_attrs),
            'tag': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., In Schools'}),
            'link': forms.TextInput(attrs={**_text_attrs, 'placeholder': 'e.g., #programs or /programs/strong-foundations/'}),
            'order': forms.NumberInput(attrs=_number_attrs),
            'is_active': forms.CheckboxInput(attrs=_checkbox_attrs),
        }
