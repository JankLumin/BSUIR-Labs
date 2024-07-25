from django.test import TestCase, RequestFactory
from django.urls import reverse
from Lab5.views import *
from Lab5.models import *
from Lab5.forms import *
from datetime import date, timedelta
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError


class ArticleModelTest(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Тестовая статья",
            content="Содержание тестовой статьи",
            publish_date=timezone.now()
        )

    def test_article_creation(self):
        self.assertTrue(isinstance(self.article, Article))
        self.assertEqual(str(self.article), self.article.title)

    def test_get_local_time(self):
        formatted_time = self.article.get_local_time()
        self.assertIn(formatted_time[-8:],
                      str(self.article.publish_date.astimezone(get_localzone()).strftime('%H:%M:%S')))

    def test_get_utc_time(self):
        formatted_time = self.article.get_utc_time()
        self.assertIn(formatted_time[-8:], str(self.article.publish_date.astimezone(pytz.utc).strftime('%H:%M:%S')))


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(info="Описание компании")

    def test_company_creation(self):
        self.assertTrue(isinstance(self.company, Company))
        self.assertEqual(self.company.info, "Описание компании")


class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            phone="+375291112233",
            email="test@example.com",
            description="Описание контакта"
        )

    def test_phone_validation(self):
        self.contact.full_clean()

    def test_invalid_phone(self):
        self.contact.phone = "12345"
        with self.assertRaises(ValidationError):
            self.contact.full_clean()


class ReviewModelTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username="user1",
                                              password="testpass123")
        self.review = Review.objects.create(
            user=user,
            rating=5,
            text="Отличный отзыв",
            date=datetime.date.today()
        )

    def test_review_creation(self):
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(self.review.rating, 5)


class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        pass

    def test_birth_date_field_required(self):
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'standard',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)

    def test_birth_date_validation_under_18(self):
        birth_date = date.today() - timedelta(days=17 * 365)
        form = CustomUserCreationForm(data={
            'username': 'testuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'role': 'standard',
            'birth_date': birth_date
        })
        self.assertFalse(form.is_valid())
        self.assertIn('birth_date', form.errors)
        self.assertEqual(form.errors['birth_date'], ['You must be at least 18 years old to register.'])

    def test_form_inherits_user_creation_fields(self):
        form = CustomUserCreationForm()
        self.assertIn('username', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        self.assertIn('role', form.fields)
        self.assertTrue(form.fields['role'].required)


def create_owner():
    owner = CustomUser.objects.create_user(username='owner', password='testpassword123')
    return owner


class PropertyListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner = create_owner()

        self.property = Property.objects.create(
            title="House",
            description="Nice house",
            price=100000,
            num_rooms=4,
            area=200,
            year_built=1999,
            owner=self.owner
        )

    def test_property_list_view(self):
        request = self.factory.get(reverse('property-list'))
        response = PropertyListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('House', response.rendered_content)


class PropertyDetailViewTest(TestCase):
    def setUp(self):
        owner = CustomUser.objects.create_user(username='admin', password='test123')

        self.property = Property.objects.create(
            title="House",
            description="Nice house",
            price=100000,
            num_rooms=4,
            area=200,
            year_built=2000,
            owner=owner
        )

    def test_login_required(self):
        response = self.client.get(reverse('property-detail', kwargs={'pk': self.property.pk}))
        self.assertEqual(response.status_code, 302)

    def test_detail_view(self):
        self.client.login(username='admin', password='test123')
        response = self.client.get(reverse('property-detail', kwargs={'pk': self.property.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('House', response.content.decode())


class PropertyCreateViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='admin', password='12345', role='admin')
        self.client.login(username='admin', password='12345')

    def test_form_display(self):
        response = self.client.get(reverse('property-create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_create_property(self):
        post_data = {
            'title': 'New Home',
            'description': 'Beautiful new home',
            'price': 200000,
            'num_rooms': 4,
            'area': 150,
            'year_built': 2020,
            'owner': self.user.pk
        }
        response = self.client.post(reverse('property-create'), post_data)
        self.assertEqual(response.status_code, 200)

