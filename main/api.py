from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Tool, Category, ToolImage, Rental, Review,
    Transaction, Notification, UserVerification,
    Insurance, Dispute, Maintenance, PromotionalCampaign,
    UserPreferences, User
)
from .serializers import (
    ToolSerializer, CategorySerializer, ToolImageSerializer,
    RentalSerializer, ReviewSerializer, TransactionSerializer,
    NotificationSerializer, UserVerificationSerializer,
    InsuranceSerializer, DisputeSerializer, MaintenanceSerializer,
    PromotionalCampaignSerializer, UserPreferencesSerializer,
    UserSerializer
)
from .filters import (
    ToolFilter, RentalFilter, ReviewFilter, TransactionFilter,
    DisputeFilter, MaintenanceFilter, PromotionalCampaignFilter
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsRenterOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.renter or request.user == obj.tool.owner

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ToolFilter
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['hourly_rate', 'created_at', 'name']

    def get_queryset(self):
        queryset = Tool.objects.annotate(
            average_rating=Avg('rental__review__rating'),
            total_rentals=Count('rental')
        )
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        tool = self.get_object()
        serializer = ToolImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tool=tool)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RentalViewSet(viewsets.ModelViewSet):
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated, IsRenterOrOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RentalFilter
    search_fields = ['tool__name', 'renter__username']
    ordering_fields = ['start_date', 'end_date', 'total_cost', 'created_at']

    def get_queryset(self):
        user = self.request.user
        return Rental.objects.filter(
            models.Q(renter=user) | models.Q(tool__owner=user)
        )

    def perform_create(self, serializer):
        tool = Tool.objects.get(id=serializer.validated_data['tool_id'])
        total_cost = self.calculate_total_cost(
            tool,
            serializer.validated_data['start_date'],
            serializer.validated_data['end_date']
        )
        serializer.save(renter=self.request.user, total_cost=total_cost)

    @staticmethod
    def calculate_total_cost(tool, start_date, end_date):
        duration = end_date - start_date
        hours = duration.total_seconds() / 3600
        days = hours / 24
        weeks = days / 7

        if weeks >= 1:
            return tool.weekly_rate * weeks
        elif days >= 1:
            return tool.daily_rate * days
        else:
            return tool.hourly_rate * hours

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ReviewFilter
    search_fields = ['comment', 'rental__tool__name']
    ordering_fields = ['rating', 'created_at']

    def get_queryset(self):
        return Review.objects.filter(
            models.Q(reviewer=self.request.user) |
            models.Q(rental__tool__owner=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TransactionFilter
    search_fields = ['rental__tool__name']
    ordering_fields = ['amount', 'created_at']

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(
            models.Q(rental__renter=user) |
            models.Q(rental__tool__owner=user)
        )

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'read']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

class UserVerificationViewSet(viewsets.ModelViewSet):
    serializer_class = UserVerificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserVerification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')

class InsuranceViewSet(viewsets.ModelViewSet):
    serializer_class = InsuranceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Insurance.objects.filter(
            models.Q(rental__renter=user) |
            models.Q(rental__tool__owner=user)
        )

class DisputeViewSet(viewsets.ModelViewSet):
    serializer_class = DisputeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DisputeFilter
    search_fields = ['description', 'rental__tool__name']
    ordering_fields = ['created_at', 'resolved_at']

    def get_queryset(self):
        user = self.request.user
        return Dispute.objects.filter(
            models.Q(initiator=user) |
            models.Q(rental__tool__owner=user) |
            models.Q(rental__renter=user)
        )

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user, status='open')

class MaintenanceViewSet(viewsets.ModelViewSet):
    serializer_class = MaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MaintenanceFilter
    search_fields = ['description', 'tool__name']
    ordering_fields = ['date', 'cost']

    def get_queryset(self):
        return Maintenance.objects.filter(tool__owner=self.request.user)

class PromotionalCampaignViewSet(viewsets.ModelViewSet):
    queryset = PromotionalCampaign.objects.filter(is_active=True)
    serializer_class = PromotionalCampaignSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PromotionalCampaignFilter
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'discount_percentage']

class UserPreferencesViewSet(viewsets.ModelViewSet):
    serializer_class = UserPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPreferences.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
