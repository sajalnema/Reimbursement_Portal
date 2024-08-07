from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import home, register, login_view, manage_departments, manage_employees, admin_home, manager_home, employee_home

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('accounts:home')
        self.assertEquals(resolve(url).func, home)

    def test_register_url_is_resolved(self):
        url = reverse('accounts:signup')
        self.assertEquals(resolve(url).func, register)

    def test_login_url_is_resolved(self):
        url = reverse('accounts:login')
        self.assertEquals(resolve(url).func, login_view)

    def test_manage_departments_url_is_resolved(self):
        url = reverse('accounts:manage_departments')
        self.assertEquals(resolve(url).func, manage_departments)

    def test_manage_employees_url_is_resolved(self):
        url = reverse('accounts:manage_employees')
        self.assertEquals(resolve(url).func, manage_employees)

    def test_admin_home_url_is_resolved(self):
        url = reverse('accounts:admin_home')
        self.assertEquals(resolve(url).func, admin_home)

    def test_manager_home_url_is_resolved(self):
        url = reverse('accounts:manager_home')
        self.assertEquals(resolve(url).func, manager_home)

    def test_employee_home_url_is_resolved(self):
        url = reverse('accounts:employee_home')
        self.assertEquals(resolve(url).func, employee_home)
