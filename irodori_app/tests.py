from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer, Activity

class CustomerModelTests(TestCase):
    """
    Customerモデルに関するテスト
    """

    def test_initial_customer_count(self):
        """初期状態ではデータが0件であること"""
        saved_customers = Customer.objects.all()
        self.assertEqual(saved_customers.count(), 0)

    def test_create_customer(self):
        """顧客データ1件を作成し、正しく保存されるか"""
        # 1. データを作成・保存
        customer = Customer.objects.create(
            company_name='テスト株式会社',
            contact_name='テスト 太郎',
            email='test@example.com'
        )

        # 2. データベースから全件取得
        saved_customers = Customer.objects.all()

        # 3. 検証(Assertion)
        self.assertEqual(saved_customers.count(), 1)
        self.assertEqual(saved_customers[0].company_name, "テスト株式会社")


class CustomerViewTests(TestCase):
    """
    Viewに関するテスト
    """

    def setUp(self):
        # テストユーザー作成
        self.user = User.objects.create_user(username='testuser', password='password')

        # 他ユーザー作成
        self.other_user = User.objects.create_user(username='otheruser', password='password')

        # 顧客データ作成（self.user 担当）
        self.customer = Customer.objects.create(
            company_name="自分の担当顧客",
            contact_name="担当者A",
            email="a@example.com",
            user=self.user
        )

    def test_login_required(self):
        """ログイン必須のページに未ログインでアクセスするとリダイレクトされる"""

        response = self.client.get(reverse('customer_list'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_users_can_see_list(self):
        """ログインしているユーザーは顧客一覧を閲覧できる"""

        self.client.force_login(self.user)

        response = self.client.get(reverse('customer_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "自分の担当顧客")

    def test_cannot_see_others_data(self):
        """他人の顧客データは表示されない"""

        self.client.force_login(self.other_user)

        response = self.client.get(reverse('customer_list'))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "自分の担当顧客")
