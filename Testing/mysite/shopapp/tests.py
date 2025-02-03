from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from string import ascii_letters
from random import choices
from .models import Product , Order
from .views import ProductCreateView


class CreateProductViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='ivan_test',
                                            password='090206vb')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.product_name = ''.join(choices(ascii_letters, k=10)) # будет взято 10 случайных символов
        Product.objects.filter(name=self.product_name).delete() # удаляем из бд, у кого совпадут имена

    def test_product_create_view(self):
        res = self.client.post(
            reverse('shopapp:product_create'),
            {
                'name':self.product_name,
                'price':'142',
                'discount':'1',
                'description':'test product ',
            }
        )
        self.assertRedirects(res, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.product = Product.objects.create(name='Test Details')

    @classmethod
    def tearDownClass(cls):
        cls.product.delete()

    def test_product_details_view(self):
        res = self.client.get(
            reverse('shopapp:product_details',
                    kwargs={'pk':self.product.pk}),
        )
        self.assertEqual(res.status_code, 200)

    def test_product_details_view_and_check_content(self):
        res = self.client.get(
            reverse('shopapp:product_details',
                    kwargs={'pk': self.product.pk}),
        )
        self.assertEqual(res.status_code, 200)



class OrderListViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='ivan_test',
                                            password='090206vb')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()


    def setUp(self):
        self.client.force_login(self.user)

    def test_orders_view(self):
        res = self.client.get(reverse('shopapp:orders_list'))
        self.assertContains(res, 'Orders')

    def test_orders_view_not_authenticated(self):
        self.client.logout()
        res = self.client.get(reverse('shopapp:orders_list'))
        self.assertIn(str(settings.LOGIN_URL), res.url)


class OrderDetailViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='test_user',
                                                        password='testpassword')

        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)


        cls.product = Product.objects.create(name='Test product',
                                         price=100,
                                         discount=10,
                                         description='Test product description',
                                         )
        cls.order = Order.objects.create(delivery_address='Test Address',
                                          promocode='test',
                                          user=cls.user)
        cls.order.products.add(cls.product)

    @classmethod
    def tearDownClass(cls):
        cls.order.delete()
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)

    def test_order_details(self):
        res = self.client.get(
            reverse('shopapp:order_details',
                    kwargs={'pk': self.order.pk}))

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.order.delivery_address)
        self.assertContains(res, self.order.promocode)
        self.assertEqual(res.context['order'].pk, self.order.pk)


