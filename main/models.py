from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    is_tool_owner = models.BooleanField(default=False, db_index=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    verified = models.BooleanField(default=False, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['is_tool_owner', 'verified']),
        ]

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class Tool(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tools', db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField()
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    daily_rate = models.DecimalField(max_digits=6, decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.BooleanField(default=True, db_index=True)
    condition = models.CharField(max_length=50, db_index=True)
    location = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'location']),
            models.Index(fields=['hourly_rate', 'availability']),
            models.Index(fields=['condition', 'category_id']),
            models.Index(fields=['owner_id', 'created_at']),
            models.Index(fields=['created_at', 'availability']),
        ]

    def __str__(self):
        return self.name

class ToolImage(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='images', db_index=True)
    image = models.ImageField(upload_to='tool_images/')
    is_primary = models.BooleanField(default=False)

class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    renter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals', db_index=True)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, db_index=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['renter_id', 'status']),
            models.Index(fields=['tool_id', 'status']),
            models.Index(fields=['created_at', 'status']),
            models.Index(fields=['total_cost', 'status']),
        ]

class Review(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, db_index=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['rating', 'created_at']),
            models.Index(fields=['reviewer_id', 'created_at']),
            models.Index(fields=['rental_id', 'rating']),
        ]

    def __str__(self):
        return f"Review for {self.rental}"

class Transaction(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, db_index=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    commission = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, db_index=True)
    payment_method = models.CharField(max_length=50, db_index=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['rental_id', 'status']),
            models.Index(fields=['amount', 'status']),
            models.Index(fields=['payment_method', 'status']),
            models.Index(fields=['created_at', 'status']),
        ]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id', 'is_read']),
            models.Index(fields=['created_at', 'is_read']),
        ]

    def __str__(self):
        return f"Notification for {self.user}"

class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    document_type = models.CharField(max_length=50)
    document_number = models.CharField(max_length=50)
    verified_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['verified_at', 'status']),
        ]

    def __str__(self):
        return f"Verification for {self.user}"

class Insurance(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, db_index=True)
    policy_number = models.CharField(max_length=100, unique=True)
    coverage_amount = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    premium = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['coverage_amount', 'rental_id']),
        ]

    def __str__(self):
        return f"Insurance {self.policy_number}"

class Dispute(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE, db_index=True)
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    description = models.TextField()
    status = models.CharField(max_length=20, db_index=True)
    resolution = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['rental_id', 'status']),
            models.Index(fields=['initiator_id', 'status']),
            models.Index(fields=['created_at', 'status']),
            models.Index(fields=['resolved_at', 'status']),
        ]

    def __str__(self):
        return f"Dispute for {self.rental}"

class Maintenance(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, db_index=True)
    description = models.TextField()
    date = models.DateTimeField(db_index=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    performed_by = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['tool_id', 'date']),
            models.Index(fields=['cost', 'date']),
            models.Index(fields=['date', 'tool_id']),
        ]

    def __str__(self):
        return f"Maintenance for {self.tool.name}"

class PromotionalCampaign(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, db_index=True)
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['discount_percentage', 'is_active']),
            models.Index(fields=['is_active', 'start_date', 'end_date']),
        ]

    def __str__(self):
        return self.name

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    preferred_categories = models.ManyToManyField(Category)
    max_rental_distance = models.IntegerField(help_text="Maximum distance in km")
    receive_promotions = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
        ]

    def __str__(self):
        return f"Preferences for {self.user}"
