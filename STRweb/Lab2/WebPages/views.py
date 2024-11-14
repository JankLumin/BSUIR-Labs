from decimal import Decimal
from django.views import View
from rest_framework import viewsets
from django.shortcuts import get_object_or_404, render, redirect
from UserManagement.models import CustomUser
from UserManagement.serializers import CustomUserSerializer
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
import requests
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, authenticate, login
from rest_framework import viewsets
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import (
    Banner,
    Cart,
    CartItem,
    Partner,
    Review,
    PromoCode,
    News,
    CompanyInfo,
    FAQ,
    JobOpening,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserProfileForm, ReviewForm
import requests
from .serializers import (
    BannerSerializer,
    PartnerSerializer,
    ReviewSerializer,
    PromoCodeSerializer,
    NewsSerializer,
    CompanyInfoSerializer,
    FAQSerializer,
    JobOpeningSerializer,
)
from .forms import RegisterForm, LoginForm


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer


class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PromoCodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CompanyInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer


class JobOpeningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = JobOpening.objects.all()
    serializer_class = JobOpeningSerializer


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(role="employee")
    serializer_class = CustomUserSerializer


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            api_url = "http://127.0.0.1:8000/users/register/"
            data = {
                "username": form.cleaned_data["username"],
                "email": form.cleaned_data["email"],
                "password": form.cleaned_data["password"],
                "phone_number": form.cleaned_data["phone_number"],
            }
            response = requests.post(api_url, data=data)
            if response.status_code == 201:
                messages.success(
                    request,
                    "Регистрация прошла успешно. Пожалуйста, проверьте вашу почту для подтверждения регистрации.",
                )
                return redirect("login")
            else:
                messages.error(request, f"Ошибка регистрации: {response.text}")
    else:
        form = RegisterForm()

    return render(request, "registration.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            api_url = "http://127.0.0.1:8000/api/token/"
            data = {
                "username": username,
                "password": password,
            }
            response = requests.post(api_url, data=data)
            if response.status_code == 200:
                token = response.json().get("access")
                request.session["token"] = token
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("profile")
                else:
                    messages.error(
                        request, "Не удалось аутентифицировать пользователя."
                    )
            else:
                messages.error(
                    request,
                    "Неверное имя пользователя или пароль, либо ваша учетная запись не активирована.",
                )
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    request.session.flush()
    return redirect("home")


def about(request):
    response = requests.get("http://127.0.0.1:8000/webpages/api/company-info/1/")
    if response.status_code == 200:
        company_info = response.json()
    else:
        company_info = {}

    return render(request, "about.html", {"company_info": company_info})


def news_list(request):

    response = requests.get("http://127.0.0.1:8000/webpages/api/news/")

    if response.status_code == 200:
        articles = response.json()
    else:
        articles = {}

    return render(request, "news_list.html", {"articles": articles})


def news_detail(request, pk):
    response = requests.get(f"http://127.0.0.1:8000/webpages/api/news/{pk}/")

    if response.status_code == 200:
        article = response.json()
        if "published_date" in article:
            article["published_date"] = datetime.fromisoformat(
                article["published_date"].replace("Z", "+00:00")
            )
    else:
        article = {}

    return render(request, "news_detail.html", {"article": article})


def faq_list(request):
    response = requests.get("http://127.0.0.1:8000/webpages/api/faqs/")

    if response.status_code == 200:
        faqs = response.json()
        for faq in faqs:
            if "added_date" in faq:
                faq["added_date"] = datetime.fromisoformat(
                    faq["added_date"].replace("Z", "+00:00")
                )
    else:
        faqs = []

    return render(request, "faq_list.html", {"faqs": faqs})


def employee_list(request):
    response = requests.get("http://127.0.0.1:8000/webpages/api/employees/")

    if response.status_code == 200:
        employees = response.json()
    else:
        employees = []

    return render(request, "employee_list.html", {"employees": employees})


def privacy_policy(request):
    return render(request, "privacy_policy.html")


def job_openings_list(request):
    response = requests.get("http://127.0.0.1:8000/webpages/api/job-openings/")

    if response.status_code == 200:
        job_openings = response.json()
    else:
        job_openings = []

    return render(request, "job_openings_list.html", {"job_openings": job_openings})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            api_url = f"http://127.0.0.1:8000/users/profile/{request.user.id}/"
            headers = {"Authorization": f'Token {request.session.get("token")}'}
            data = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "phone_number": form.cleaned_data["phone_number"],
                "photo": form.cleaned_data["photo"],
                "description": form.cleaned_data["description"],
            }
            response = requests.put(api_url, data=data, headers=headers)
            if response.status_code == 200:
                messages.success(request, "Профиль успешно обновлен!")
                return redirect("profile")
            else:
                messages.error(request, f"Ошибка обновления профиля: {response.text}")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "profile.html", {"form": form})


@login_required
def profile_update(request, pk):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен!")
            return redirect("profile")
        else:
            messages.error(request, "Ошибка при обновлении профиля.")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "profile.html", {"form": form})


def home(request):
    api_base_url = "http://127.0.0.1:8000/"

    # Запросы к API для получения данных
    banners_response = requests.get(f"{api_base_url}webpages/api/banners/")
    news_response = requests.get(f"{api_base_url}webpages/api/news/")
    partners_response = requests.get(f"{api_base_url}webpages/api/partners/")
    company_info_response = requests.get(f"{api_base_url}webpages/api/company-info/")

    # Запросы к разным типам недвижимости
    apartments_response = requests.get(f"{api_base_url}api/apartments/")
    houses_response = requests.get(f"{api_base_url}api/houses/")
    commercial_properties_response = requests.get(
        f"{api_base_url}api/commercial_properties/"
    )
    garages_response = requests.get(f"{api_base_url}api/garages/")

    # Проверка успешности запросов
    banners = banners_response.json() if banners_response.status_code == 200 else []
    latest_news = news_response.json() if news_response.status_code == 200 else []
    partners = partners_response.json() if partners_response.status_code == 200 else []
    company_info = (
        company_info_response.json()[0]
        if company_info_response.status_code == 200 and company_info_response.json()
        else None
    )

    # Объединение всех типов недвижимости и извлечение первой фотографии
    properties = []
    if apartments_response.status_code == 200:
        apartments = apartments_response.json()
        for apartment in apartments:
            if apartment["photos_read"]:
                apartment["image"] = apartment["photos_read"][0]["image"]
            else:
                apartment["image"] = None
            apartment["property_type"] = "apartment"
            properties.append(apartment)

    if houses_response.status_code == 200:
        houses = houses_response.json()
        for house in houses:
            if house["photos_read"]:
                house["image"] = house["photos_read"][0]["image"]
            else:
                house["image"] = None
            house["property_type"] = "house"
            properties.append(house)

    if commercial_properties_response.status_code == 200:
        commercial_properties = commercial_properties_response.json()
        for commercial_property in commercial_properties:
            if commercial_property["photos_read"]:
                commercial_property["image"] = commercial_property["photos_read"][0][
                    "image"
                ]
            else:
                commercial_property["image"] = None
            commercial_property["property_type"] = "commercial_property"
            properties.append(commercial_property)

    if garages_response.status_code == 200:
        garages = garages_response.json()
        for garage in garages:
            if garage["photos_read"]:
                garage["image"] = garage["photos_read"][0]["image"]
            else:
                garage["image"] = None
            garage["property_type"] = "garage"
            properties.append(garage)

    # Подготовка данных для шаблона
    context = {
        "banners": banners,
        "latest_news": latest_news[:1],  # Берём только последнюю новость
        "partners": partners,
        "properties": properties,  # Все типы недвижимости
        "company_logo": (
            company_info.get("logo") if company_info else None
        ),  # Логотип компании
    }

    return render(request, "home.html", context)


def property_detail(request, id, property_type):
    api_base_url = "http://127.0.0.1:8000/"

    # Определение эндпоинта в зависимости от типа недвижимости
    if property_type == "apartment":
        property_response = requests.get(f"{api_base_url}api/apartments/{id}/")
        template_name = "apartment_detail.html"
    elif property_type == "house":
        property_response = requests.get(f"{api_base_url}api/houses/{id}/")
        template_name = "house_detail.html"
    elif property_type == "commercial_property":
        property_response = requests.get(
            f"{api_base_url}api/commercial_properties/{id}/"
        )
        template_name = "commercial_property_detail.html"
    elif property_type == "garage":
        property_response = requests.get(f"{api_base_url}api/garages/{id}/")
        template_name = "garage_detail.html"
    else:
        property_response = None

    # Проверка успешности запроса
    if property_response and property_response.status_code == 200:
        property_data = property_response.json()
    else:
        property_data = None

    # Подготовка данных для шаблона
    context = {"property": property_data}

    return render(request, template_name, context)


class CartView(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = Decimal("0.00")  # Используем Decimal для точности

        # Перебираем элементы корзины и извлекаем данные о каждом товаре из API
        for item in cart_items:
            if item.product_type == "apartment":
                api_url = f"http://127.0.0.1:8000/api/apartments/{item.product_id}/"
            elif item.product_type == "house":
                api_url = f"http://127.0.0.1:8000/api/houses/{item.product_id}/"
            elif item.product_type == "commercial_property":
                api_url = f"http://127.0.0.1:8000/api/commercial_properties/{item.product_id}/"
            elif item.product_type == "garage":
                api_url = f"http://127.0.0.1:8000/api/garages/{item.product_id}/"
            else:
                continue

            response = requests.get(api_url)
            if response.status_code == 200:
                item_data = response.json()
                item.title = item_data.get("title")
                item.price = Decimal(
                    item_data.get("price")
                )  # Преобразуем цену в Decimal
                total_price += item.price * item.quantity

        # Применяем промокод, если он есть
        if cart.promo_code:
            discount = cart.promo_code.discount / Decimal(
                "100"
            )  # Преобразуем процент в Decimal
            total_price = total_price * (Decimal("1.00") - discount)

        context = {
            "cart_items": cart_items,
            "total_price": round(
                total_price, 2
            ),  # Округляем до двух знаков после запятой
            "promo_code": cart.promo_code,
        }
        return render(request, "cart_detail.html", context)


@method_decorator(login_required, name="dispatch")
class AddToCartView(View):
    def post(self, request, product_id, product_type):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            product_type=product_type,
        )
        if not created:
            cart_item.quantity += 1
        cart_item.save()

        return redirect("cart_detail")


class RemoveFromCartView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        return redirect("cart_detail")


class UpdateCartItemQuantityView(View):
    def post(self, request, item_id):
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        new_quantity = request.POST.get("quantity", 1)
        cart_item.quantity = max(1, int(new_quantity))
        cart_item.save()
        return redirect("cart_detail")


class ApplyPromoCodeView(View):
    def post(self, request):
        promo_code = request.POST.get("promo_code")
        cart = get_object_or_404(Cart, user=request.user)
        promo = PromoCode.objects.filter(code=promo_code, active=True).first()

        if promo and promo.expiration_date >= timezone.now().date():
            cart.promo_code = promo
            cart.save()
            return redirect("cart_detail")
        else:
            return redirect("cart_detail")


class CheckoutView(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()

        total_price = Decimal("0.00")
        for item in cart_items:
            if item.product_type == "apartment":
                api_url = f"http://127.0.0.1:8000/api/apartments/{item.product_id}/"
            elif item.product_type == "house":
                api_url = f"http://127.0.0.1:8000/api/houses/{item.product_id}/"
            elif item.product_type == "commercial_property":
                api_url = f"http://127.0.0.1:8000/api/commercial_properties/{item.product_id}/"
            elif item.product_type == "garage":
                api_url = f"http://127.0.0.1:8000/api/garages/{item.product_id}/"
            else:
                continue

            response = requests.get(api_url)
            if response.status_code == 200:
                item_data = response.json()
                item.title = item_data.get("title")
                item.price = Decimal(item_data.get("price", "0.00"))
                item.total_price = item.price * item.quantity
                total_price += item.total_price

        # Применение скидки от промокода
        if cart.promo_code:
            discount = cart.promo_code.discount / Decimal("100")
            total_price = total_price * (Decimal("1.00") - discount)

        context = {
            "cart_items": cart_items,
            "total_price": round(total_price, 2),
            "promo_code": cart.promo_code,
        }
        return render(request, "checkout.html", context)


class PaymentSuccessView(View):
    def get(self, request):
        # Получаем корзину пользователя
        cart = Cart.objects.get(user=request.user)

        # Удаляем все товары из корзины
        cart.items.all().delete()

        # Убираем промокод
        cart.promo_code = None
        cart.save()

        return render(request, "payment_success.html")


class PromoCodeListView(ListView):
    model = PromoCode
    template_name = "promo_code_list.html"
    context_object_name = "promo_codes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Отфильтровываем действующие промокоды
        context["active_promo_codes"] = PromoCode.objects.filter(
            active=True, expiration_date__gte=timezone.now().date()
        )
        # Промокоды, срок действия которых истек
        context["archived_promo_codes"] = PromoCode.objects.filter(
            active=False
        ) | PromoCode.objects.filter(expiration_date__lt=timezone.now().date())
        return context


class ReviewListView(ListView):
    model = Review
    template_name = "review_list.html"
    context_object_name = "reviews"
    ordering = ["-date_posted"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ratings"] = range(1, 11)  # Рейтинги от 1 до 10
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "add_review.html"  # Изменено на соответствующее название
    success_url = reverse_lazy("review_list")  # Убедитесь, что URL name корректен

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def demonstration_view(request):
    return render(request, "demonstration.html")
