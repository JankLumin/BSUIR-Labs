from django.urls import path
from .views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import re_path

urlpatterns = [
                  path('', PropertyListView.as_view(), name='property-list'),
                  path('signup/', SignUpView.as_view(), name='signup'),
                  path('admin/', admin.site.urls),
                  path('properties/', PropertyListView.as_view(), name='property-list'),
                  path('properties/<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
                  path('properties/new/', PropertyCreateView.as_view(), name='property-create'),
                  path('properties/<int:pk>/edit/', PropertyUpdateView.as_view(), name='property-update'),
                  path('properties/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property-delete'),
                  re_path(r'^articles/(?P<year>[0-9]{4})-(?P<month>[0-9]{1,2})-(?P<day>[0-9]{1,2})/(?P<pk>\d+)/$',
                          ArticleDetailView.as_view(), name='article-detail'),
                  path('articles/', ArticleListView.as_view(), name='article-list'),
                  path('news/', NewsListView.as_view(), name='news-list'),
                  path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
                  path('vacancies/', VacancyListView.as_view(), name='vacancy-list'),
                  path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy-detail'),
                  path('contacts/', ContactListView.as_view(), name='contact-list'),
                  path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
                  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('currency-rates/', currency_rates_view, name='currency-rates'),
                  path('map/', map_view, name='map-view'),
                  path('statistics/', StatisticsView.as_view(), name='statistics'),
                  path('article-stats/', article_statistics_view, name='article-statistics')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
