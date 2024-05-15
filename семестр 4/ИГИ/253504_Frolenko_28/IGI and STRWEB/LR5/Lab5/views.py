from django.db.models.functions import TruncDay
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.db.models import Count, Sum, Q
from .forms import *
import requests
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponseForbidden
from functools import wraps
import logging

logger = logging.getLogger('django')


class PropertyListView(ListView):
    model = Property
    template_name = 'property_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')
        sort_by = self.request.GET.get('sort', 'title')

        logger.debug(f"Fetching properties with query: '{query}' and sort by: '{sort_by}'")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query)
            )
            logger.debug(f"Filtered properties count: {queryset.count()}")

        return queryset.order_by(sort_by)


class PropertyDetailView(LoginRequiredMixin, DetailView):
    model = Property
    template_name = 'property_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            logger.warning("Attempt to access PropertyDetailView without authentication")
            return self.handle_no_permission()
        logger.info(f"User {request.user.username} accessed PropertyDetailView")
        return super().dispatch(request, *args, **kwargs)


class PropertyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Property
    fields = ['title', 'description', 'price', 'photo', 'num_rooms', 'area', 'year_built', 'owner', 'agents']
    template_name = 'property_form.html'

    def test_func(self):
        has_permission = (self.request.user.is_authenticated and
                          (self.request.user.role == 'employee' or self.request.user.role == 'admin'))
        if not has_permission:
            logger.warning(f"User {self.request.user.username} failed to pass test_func in PropertyCreateView")
        return has_permission

    def form_valid(self, form):
        logger.info(f"Property created by {self.request.user.username}: {form.cleaned_data['title']}")
        return super().form_valid(form)

    success_url = reverse_lazy('property-list')


class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    fields = ['title', 'description', 'price', 'photo', 'num_rooms', 'area', 'year_built', 'owner', 'agents']
    template_name = 'property_form.html'

    def test_func(self):
        has_permission = (self.request.user.is_authenticated and
                          self.request.user.role in ['employee', 'admin'])
        if not has_permission:
            logger.warning(f"User {self.request.user.username} failed to pass test_func in PropertyUpdateView")
        return has_permission

    def form_valid(self, form):
        logger.info(f"Property updated by {CustomUser.username}: {form.cleaned_data['title']}")
        return super().form_valid(form)

    success_url = reverse_lazy('property-list')


class PropertyDeleteView(DeleteView):
    model = Property
    template_name = 'property_confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} is deleting property with id {kwargs.get('pk')}")
        return super().delete(request, *args, **kwargs)

    success_url = reverse_lazy('property-list')


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'


class NewsListView(ListView):
    model = News
    template_name = 'news_list.html'


class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancy_list.html'


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'vacancy_detail.html'


class ContactListView(ListView):
    model = Contact
    template_name = 'contact_list.html'


class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contact_detail.html'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden()
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to access this page.")
        return _wrapped_view
    return decorator


def get_currency_rate(cur_code):
    url = f"https://api.nbrb.by/exrates/rates/{cur_code}?parammode=2"
    response = requests.get(url)
    response.raise_for_status()
    rate_info = response.json()
    return rate_info['Cur_OfficialRate'], rate_info['Cur_Scale']


@role_required(['employee', 'admin'])
def currency_rates_view(request):
    usd_rate, usd_scale = get_currency_rate('USD')
    eur_rate, eur_scale = get_currency_rate('EUR')
    return render(request, 'currency_rates.html', {
        'usd_rate': usd_rate,
        'eur_rate': eur_rate
    })


def map_view(request):
    properties = [
        {'name': 'My Company', 'lat': 53.907790, 'lng': 27.588807, 'description': 'Описание объекта 1'},
    ]
    context = {
        'properties': properties
    }
    return render(request, 'map_template.html', context)


def article_statistics_view(request):
    data = Article.objects.annotate(date=TruncDay('publish_date')).values('date').annotate(count=Count('id')).order_by(
        'date')
    labels = [item['date'].strftime('%Y-%m-%d') for item in data]
    counts = [item['count'] for item in data]
    context = {
        'labels': labels,
        'data': counts,
    }
    return render(request, 'article_stats.html', context)


class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        users = CustomUser.objects.filter(birth_date__isnull=False)

        today = date.today()
        ages = [today.year - user.birth_date.year - (
                (today.month, today.day) < (user.birth_date.month, user.birth_date.day)) for user in users]

        df_users = pd.DataFrame(ages, columns=['age'])
        context['average_age'] = df_users['age'].mean()
        context['median_age'] = df_users['age'].median()

        context['most_popular_type'] = PropertyType.objects.annotate(count=Count('property')).order_by('-count').first()
        context['most_profitable_type'] = PropertyType.objects.annotate(total_income=Sum('property__price')).order_by(
            '-total_income').first()

        return context
