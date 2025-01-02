from django_filters import rest_framework as filters
from django.db.models import Q
from .models import (
    Tool,
    Rental,
    Review,
    Transaction,
    Dispute,
    Maintenance,
    PromotionalCampaign,
)


class ToolFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="hourly_rate", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="hourly_rate", lookup_expr="lte")
    location = filters.CharFilter(field_name="location", lookup_expr="icontains")
    category_name = filters.CharFilter(
        field_name="category__name", lookup_expr="icontains"
    )
    owner_name = filters.CharFilter(method="filter_owner_name")
    rating = filters.NumberFilter(method="filter_rating")
    min_rating = filters.NumberFilter(method="filter_min_rating")
    available_from = filters.DateTimeFilter(method="filter_availability")
    available_to = filters.DateTimeFilter(method="filter_availability")
    condition = filters.CharFilter(lookup_expr="iexact")
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Tool
        fields = ["category", "availability", "condition", "location"]

    def filter_owner_name(self, queryset, name, value):
        return queryset.filter(
            Q(owner__first_name__icontains=value)
            | Q(owner__last_name__icontains=value)
            | Q(owner__username__icontains=value)
        )

    def filter_rating(self, queryset, name, value):
        return queryset.filter(rental__review__rating=value).distinct()

    def filter_min_rating(self, queryset, name, value):
        return queryset.filter(rental__review__rating__gte=value).distinct()

    def filter_availability(self, queryset, name, value):
        if name == "available_from":
            return queryset.exclude(
                rental__start_date__lte=value, rental__end_date__gte=value
            )
        elif name == "available_to":
            return queryset.exclude(
                rental__start_date__lte=value, rental__end_date__gte=value
            )
        return queryset


class RentalFilter(filters.FilterSet):
    min_cost = filters.NumberFilter(field_name="total_cost", lookup_expr="gte")
    max_cost = filters.NumberFilter(field_name="total_cost", lookup_expr="lte")
    tool_name = filters.CharFilter(field_name="tool__name", lookup_expr="icontains")
    renter_name = filters.CharFilter(method="filter_renter_name")
    owner_name = filters.CharFilter(method="filter_owner_name")
    start_after = filters.DateTimeFilter(field_name="start_date", lookup_expr="gte")
    end_before = filters.DateTimeFilter(field_name="end_date", lookup_expr="lte")
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    has_review = filters.BooleanFilter(
        field_name="review", lookup_expr="isnull", exclude=True
    )
    has_insurance = filters.BooleanFilter(
        field_name="insurance", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = Rental
        fields = ["status", "tool", "renter"]

    def filter_renter_name(self, queryset, name, value):
        return queryset.filter(
            Q(renter__first_name__icontains=value)
            | Q(renter__last_name__icontains=value)
            | Q(renter__username__icontains=value)
        )

    def filter_owner_name(self, queryset, name, value):
        return queryset.filter(
            Q(tool__owner__first_name__icontains=value)
            | Q(tool__owner__last_name__icontains=value)
            | Q(tool__owner__username__icontains=value)
        )


class ReviewFilter(filters.FilterSet):
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr="lte")
    tool_name = filters.CharFilter(
        field_name="rental__tool__name", lookup_expr="icontains"
    )
    reviewer_name = filters.CharFilter(method="filter_reviewer_name")
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Review
        fields = ["rating", "rental"]

    def filter_reviewer_name(self, queryset, name, value):
        return queryset.filter(
            Q(reviewer__first_name__icontains=value)
            | Q(reviewer__last_name__icontains=value)
            | Q(reviewer__username__icontains=value)
        )


class TransactionFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr="lte")
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    tool_name = filters.CharFilter(
        field_name="rental__tool__name", lookup_expr="icontains"
    )

    class Meta:
        model = Transaction
        fields = ["status", "payment_method", "rental"]


class DisputeFilter(filters.FilterSet):
    tool_name = filters.CharFilter(
        field_name="rental__tool__name", lookup_expr="icontains"
    )
    initiator_name = filters.CharFilter(method="filter_initiator_name")
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    resolved = filters.BooleanFilter(
        field_name="resolved_at", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = Dispute
        fields = ["status", "rental"]

    def filter_initiator_name(self, queryset, name, value):
        return queryset.filter(
            Q(initiator__first_name__icontains=value)
            | Q(initiator__last_name__icontains=value)
            | Q(initiator__username__icontains=value)
        )


class MaintenanceFilter(filters.FilterSet):
    min_cost = filters.NumberFilter(field_name="cost", lookup_expr="gte")
    max_cost = filters.NumberFilter(field_name="cost", lookup_expr="lte")
    tool_name = filters.CharFilter(field_name="tool__name", lookup_expr="icontains")
    date_after = filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    date_before = filters.DateTimeFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Maintenance
        fields = ["tool", "performed_by"]


class PromotionalCampaignFilter(filters.FilterSet):
    min_discount = filters.NumberFilter(
        field_name="discount_percentage", lookup_expr="gte"
    )
    max_discount = filters.NumberFilter(
        field_name="discount_percentage", lookup_expr="lte"
    )
    active_on = filters.DateTimeFilter(method="filter_active_on")

    class Meta:
        model = PromotionalCampaign
        fields = ["is_active"]

    def filter_active_on(self, queryset, name, value):
        return queryset.filter(start_date__lte=value, end_date__gte=value)
