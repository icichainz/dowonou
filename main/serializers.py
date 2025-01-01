from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Tool, Category, ToolImage, Rental, Review,
    Transaction, Notification, UserVerification,
    Insurance, Dispute, Maintenance, PromotionalCampaign,
    UserPreferences
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'is_tool_owner', 'phone_number', 'address', 'verified']
        read_only_fields = ['verified']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ToolImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolImage
        fields = ['id', 'image', 'is_primary']

class ToolSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ToolImageSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    total_rentals = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tool
        fields = ['id', 'owner', 'category', 'name', 'description',
                 'hourly_rate', 'daily_rate', 'weekly_rate',
                 'availability', 'condition', 'location', 'images',
                 'average_rating', 'total_rentals', 'created_at', 'updated_at']

class RentalSerializer(serializers.ModelSerializer):
    tool = ToolSerializer(read_only=True)
    renter = UserSerializer(read_only=True)
    tool_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Rental
        fields = ['id', 'tool', 'tool_id', 'renter', 'start_date',
                 'end_date', 'status', 'total_cost', 'created_at']
        read_only_fields = ['status', 'total_cost']

    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rental', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['rental', 'reviewer']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'rental', 'amount', 'commission', 'status',
                 'payment_method', 'transaction_id', 'created_at']
        read_only_fields = ['commission', 'transaction_id']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
        read_only_fields = ['user']

class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVerification
        fields = ['id', 'user', 'document_type', 'document_number',
                 'verified_at', 'status']
        read_only_fields = ['verified_at', 'status']

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = ['id', 'rental', 'policy_number', 'coverage_amount',
                 'premium', 'start_date', 'end_date']
        read_only_fields = ['policy_number']

class DisputeSerializer(serializers.ModelSerializer):
    initiator = UserSerializer(read_only=True)

    class Meta:
        model = Dispute
        fields = ['id', 'rental', 'initiator', 'description', 'status',
                 'resolution', 'created_at', 'resolved_at']
        read_only_fields = ['status', 'resolution', 'resolved_at']

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id', 'tool', 'description', 'date', 'cost', 'performed_by']

class PromotionalCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionalCampaign
        fields = '__all__'
        read_only_fields = ['is_active']

class UserPreferencesSerializer(serializers.ModelSerializer):
    preferred_categories = CategorySerializer(many=True, read_only=True)
    preferred_category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = UserPreferences
        fields = ['id', 'user', 'preferred_categories', 'preferred_category_ids',
                 'max_rental_distance', 'receive_promotions']
        read_only_fields = ['user']

    def create(self, validated_data):
        category_ids = validated_data.pop('preferred_category_ids', [])
        preferences = super().create(validated_data)
        preferences.preferred_categories.set(category_ids)
        return preferences

    def update(self, instance, validated_data):
        category_ids = validated_data.pop('preferred_category_ids', None)
        preferences = super().update(instance, validated_data)
        if category_ids is not None:
            preferences.preferred_categories.set(category_ids)
        return preferences
