from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Tool, Rental, Review, UserPreferences, Category


class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = [
            "name",
            "description",
            "category",
            "hourly_rate",
            "daily_rate",
            "weekly_rate",
            "condition",
            "location",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hourly_rate = cleaned_data.get("hourly_rate")
        daily_rate = cleaned_data.get("daily_rate")
        weekly_rate = cleaned_data.get("weekly_rate")

        if daily_rate and hourly_rate and daily_rate < hourly_rate * 8:
            raise ValidationError(
                "Daily rate should be at least 8 times the hourly rate."
            )
        if weekly_rate and daily_rate and weekly_rate < daily_rate * 5:
            raise ValidationError(
                "Weekly rate should be at least 5 times the daily rate."
            )

        return cleaned_data


class ToolImageForm(forms.Form):
    image = forms.ImageField()
    is_primary = forms.BooleanField(required=False)


class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date < timezone.now():
                raise ValidationError("Start date cannot be in the past.")
            if end_date <= start_date:
                raise ValidationError("End date must be after start date.")

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4}),
        }


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ["preferred_categories", "max_rental_distance", "receive_promotions"]
        widgets = {
            "preferred_categories": forms.CheckboxSelectMultiple(),
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, empty_label="All Categories"
    )
    min_price = forms.DecimalField(min_value=0, required=False)
    max_price = forms.DecimalField(min_value=0, required=False)
    location = forms.CharField(max_length=100, required=False)
    available_from = forms.DateTimeField(
        required=False, widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    available_to = forms.DateTimeField(
        required=False, widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")
        available_from = cleaned_data.get("available_from")
        available_to = cleaned_data.get("available_to")

        if min_price and max_price and min_price > max_price:
            raise ValidationError("Minimum price should be less than maximum price.")

        if available_from and available_to and available_from > available_to:
            raise ValidationError(
                "'Available from' should be earlier than 'Available to'."
            )

        return cleaned_data


class DisputeForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea)
    evidence = forms.FileField(required=False)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


class InsuranceForm(forms.Form):
    accept_insurance = forms.BooleanField(required=False)
    coverage_amount = forms.DecimalField(min_value=0, required=False)

    def clean(self):
        cleaned_data = super().clean()
        accept_insurance = cleaned_data.get("accept_insurance")
        coverage_amount = cleaned_data.get("coverage_amount")

        if accept_insurance and not coverage_amount:
            raise ValidationError(
                "Please specify the coverage amount if you want insurance."
            )

        return cleaned_data
