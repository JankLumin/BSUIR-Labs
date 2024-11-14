# WebPages/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    AddToCartView,
    ApplyPromoCodeView,
    BannerViewSet,
    CartView,
    ContactListCreateView,
    PartnerViewSet,
    RemoveFromCartView,
    ReviewViewSet,
    PromoCodeViewSet,
    NewsViewSet,
    CompanyInfoViewSet,
    FAQViewSet,
    JobOpeningViewSet,
    EmployeeViewSet,
    UpdateCartItemQuantityView,
    CheckoutView,
    PaymentSuccessView,
    PromoCodeListView,
    ReviewListView,
    ReviewCreateView,
    about,
    news_list,
    news_detail,
    faq_list,
    employee_list,
    privacy_policy,
    job_openings_list,
    register,
    login_view,
    logout_view,
    profile_view,
    profile_update,
    home,
    property_detail,
    demonstration_view,
    task7_prototype_view,
    task7_class_view,
    task8_view,
    task9_view,
)

router = DefaultRouter()
router.register(r"banners", BannerViewSet)
router.register(r"partners", PartnerViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"promo-codes", PromoCodeViewSet)
router.register(r"news", NewsViewSet)
router.register(r"company-info", CompanyInfoViewSet)
router.register(r"faqs", FAQViewSet)
router.register(r"job-openings", JobOpeningViewSet)
router.register(r"employees", EmployeeViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("news/", news_list, name="news_list"),
    path("news/<int:pk>/", news_detail, name="news_detail"),
    path("faq/", faq_list, name="faq_list"),
    path("contacts/", employee_list, name="employee_list"),
    path("privacy/", privacy_policy, name="privacy_policy"),
    path("job-openings/", job_openings_list, name="job_openings_list"),
    path("profile/", profile_view, name="profile"),
    path("profile/update/<int:pk>/", profile_update, name="profile_update"),
    path(
        "apartments/<int:id>/",
        property_detail,
        {"property_type": "apartment"},
        name="apartment_detail",
    ),
    path(
        "houses/<int:id>/",
        property_detail,
        {"property_type": "house"},
        name="house_detail",
    ),
    path(
        "commercial_properties/<int:id>/",
        property_detail,
        {"property_type": "commercial_property"},
        name="commercial_property_detail",
    ),
    path(
        "garages/<int:id>/",
        property_detail,
        {"property_type": "garage"},
        name="garage_detail",
    ),
    path("cart/", CartView.as_view(), name="cart_detail"),
    path(
        "cart/add/<int:product_id>/<str:product_type>/",
        AddToCartView.as_view(),
        name="add_to_cart",
    ),
    path(
        "cart/remove/<int:item_id>/",
        RemoveFromCartView.as_view(),
        name="remove_from_cart",
    ),
    path(
        "cart/update/<int:item_id>/",
        UpdateCartItemQuantityView.as_view(),
        name="update_cart_item",
    ),
    path("cart/apply-promo/", ApplyPromoCodeView.as_view(), name="apply_promo_code"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("payment_success/", PaymentSuccessView.as_view(), name="payment_success"),
    path("promo_codes/", PromoCodeListView.as_view(), name="promo_code_list"),
    path("reviews/", ReviewListView.as_view(), name="review_list"),
    path("reviews/add/", ReviewCreateView.as_view(), name="add_review"),
    path("demonstration/", demonstration_view, name="demonstration"),
    path("api/contacts/", ContactListCreateView.as_view(), name="contact-list-create"),
    path("task7_prototype/", task7_prototype_view, name="task7_prototype"),
    path("task7_class/", task7_class_view, name="task7_class"),
    path("task8/", task8_view, name="task8"),
    path("task9/", task9_view, name="task9"),
]
