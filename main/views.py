from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import (
    Tool,
    Rental,
    Review,
    User,
    Category,
    UserPreferences,
)
from .forms import (
    ToolForm,
    RentalRequestForm,
    ReviewForm,
    UserPreferencesForm,
)


class HomeView(ListView):
    model = Tool
    template_name = "main/pages/index.html"
    context_object_name = "featured_tools"

    def get_queryset(self):
        return Tool.objects.filter(availability=True).order_by("-created_at")[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class ToolListView(ListView):
    model = Tool
    template_name = "tool_list.html"
    context_object_name = "tools"
    paginate_by = 20

    def get_queryset(self):
        queryset = Tool.objects.filter(availability=True)
        category = self.request.GET.get("category")
        search_query = self.request.GET.get("search")

        if category:
            queryset = queryset.filter(category__name=category)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(
                    description__icontains=search_query)
            )

        return queryset.order_by("-created_at")


class ToolDetailView(DetailView):
    model = Tool
    template_name = "tool_detail.html"
    context_object_name = "tool"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rental_form"] = RentalRequestForm()
        context["reviews"] = Review.objects.filter(rental__tool=self.object)
        context["average_rating"] = context["reviews"].aggregate(Avg("rating"))[
            "rating__avg"
        ]
        return context


class CreateToolView(LoginRequiredMixin, CreateView):
    model = Tool
    form_class = ToolForm
    template_name = "create_tool.html"
    success_url = reverse_lazy("my_tools")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class UpdateToolView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tool
    form_class = ToolForm
    template_name = "update_tool.html"
    success_url = reverse_lazy("my_tools")

    def test_func(self):
        return self.get_object().owner == self.request.user


class DeleteToolView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tool
    template_name = "delete_tool.html"
    success_url = reverse_lazy("my_tools")

    def test_func(self):
        return self.get_object().owner == self.request.user


class RentalRequestView(LoginRequiredMixin, FormView):
    form_class = RentalRequestForm
    template_name = "rental_request.html"

    def form_valid(self, form):
        tool = get_object_or_404(Tool, pk=self.kwargs["pk"])
        rental = form.save(commit=False)
        rental.renter = self.request.user
        rental.tool = tool
        rental.save()
        # Send notification to tool owner
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("rental_confirmation", kwargs={"pk": self.kwargs["pk"]})


class MyToolsView(LoginRequiredMixin, ListView):
    model = Tool
    template_name = "my_tools.html"
    context_object_name = "tools"

    def get_queryset(self):
        return Tool.objects.filter(owner=self.request.user)


class MyRentalsView(LoginRequiredMixin, ListView):
    model = Rental
    template_name = "my_rentals.html"
    context_object_name = "rentals"

    def get_queryset(self):
        return Rental.objects.filter(renter=self.request.user)


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "create_review.html"

    def form_valid(self, form):
        rental = get_object_or_404(Rental, pk=self.kwargs["rental_pk"])
        form.instance.rental = rental
        form.instance.reviewer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("tool_detail", kwargs={"pk": self.object.rental.tool.pk})


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email", "phone_number", "address"]
    template_name = "user_profile.html"
    success_url = reverse_lazy("user_profile")

    def get_object(self):
        return self.request.user


class UserPreferencesView(LoginRequiredMixin, UpdateView):
    model = UserPreferences
    form_class = UserPreferencesForm
    template_name = "user_preferences.html"
    success_url = reverse_lazy("user_preferences")

    def get_object(self):
        preferences, created = UserPreferences.objects.get_or_create(
            user=self.request.user
        )
        return preferences


def search_tools(request):
    query = request.GET.get("q", "")
    tools = Tool.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    data = [
        {"id": tool.id, "name": tool.name,
            "hourly_rate": str(tool.hourly_rate)}
        for tool in tools
    ]
    return JsonResponse(data, safe=False)
