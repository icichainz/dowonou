from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "main"

urlpatterns = [
    path("",views.index_page,name="index"),
    # Home and search
   # path("", views.HomeView.as_view(), name="home"),
    path("search/", views.ToolListView.as_view(), name="search"),
    path("ajax/search-tools/", views.search_tools, name="ajax_search_tools"),
    # Tool related URLs
    path("tools/", views.ToolListView.as_view(), name="tool_list"),
    path("tool/<int:pk>/", views.ToolDetailView.as_view(), name="tool_detail"),
    path("tool/create/", views.CreateToolView.as_view(), name="create_tool"),
    path("tool/<int:pk>/update/", views.UpdateToolView.as_view(), name="update_tool"),
    path("tool/<int:pk>/delete/", views.DeleteToolView.as_view(), name="delete_tool"),
    # Rental related URLs
    path("tool/<int:pk>/rent/", views.RentalRequestView.as_view(), name="rent_tool"),
    # path('rental/<int:pk>/confirm/', views.RentalConfirmationView.as_view(), name='rental_confirmation'),
    path("my-rentals/", views.MyRentalsView.as_view(), name="my_rentals"),
    # User related URLs
    path("my-tools/", views.MyToolsView.as_view(), name="my_tools"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("preferences/", views.UserPreferencesView.as_view(), name="user_preferences"),
    # Review URLs
    path(
        "rental/<int:rental_pk>/review/",
        views.ReviewCreateView.as_view(),
        name="create_review",
    ),
    # Authentication URLs
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="rental_platform:home"),
        name="logout",
    ),
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    path(
        "password-reset/", auth_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Additional features
    #    path('contact/', views.ContactView.as_view(), name='contact'),
    # path('about/', views.AboutView.as_view(), name='about'),
    # path('terms/', views.TermsView.as_view(), name='terms'),
    # path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    # API endpoints (for future expansion)
    # path('api/tools/', views.ToolListAPIView.as_view(), name='api_tool_list'),
    # path('api/tool/<int:pk>/', views.ToolDetailAPIView.as_view(), name='api_tool_detail'),
    # Admin URLs (consider using Django Admin for these)
    # path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    # path('admin/users/', views.AdminUserListView.as_view(), name='admin_user_list'),
    # path('admin/tools/', views.AdminToolListView.as_view(), name='admin_tool_list'),
    # path('admin/rentals/', views.AdminRentalListView.as_view(), name='admin_rental_list'),
    # Dispute handling
    # path('dispute/create/<int:rental_pk>/', views.CreateDisputeView.as_view(), name='create_dispute'),
    # path('disputes/', views.DisputeListView.as_view(), name='dispute_list'),
    # path('dispute/<int:pk>/', views.DisputeDetailView.as_view(), name='dispute_detail'),
    # Insurance
    # path('insurance/<int:rental_pk>/', views.InsuranceView.as_view(), name='insurance'),
    # Notifications
    # path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    # path('notification/<int:pk>/mark-read/', views.MarkNotificationReadView.as_view(), name='mark_notification_read'),
]
