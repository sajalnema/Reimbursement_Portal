from django.test import TestCase
from accounts.models import CustomUser, Department

class ModelsTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="HR")

    def test_create_department(self):
        department = Department.objects.create(name="Finance")
        self.assertEqual(department.name, "Finance")
        self.assertEqual(str(department), "Finance")

    def test_create_custom_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@nucleusteq.com',
            password='password123',
            is_employee=True,
            department=self.department
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@nucleusteq.com')
        self.assertTrue(user.is_employee)
        self.assertEqual(user.department.name, 'HR')
        self.assertEqual(str(user), 'testuser')

    def test_promote_to_manager(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@nucleusteq.com',
            password='password123',
            is_employee=True,
            department=self.department
        )
        user.promote_to_manager()
        self.assertTrue(user.is_manager)
        self.assertFalse(user.is_employee)
