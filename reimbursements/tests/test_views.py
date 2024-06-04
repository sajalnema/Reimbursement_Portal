from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, Department
from reimbursements.models import Reimbursement

class ReimbursementViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.department = Department.objects.create(name='HR')
        self.superuser = CustomUser.objects.create_superuser(
            username='admin', email='admin@nucleusteq.com', password='adminpass'
        )
        self.manager = CustomUser.objects.create_user(
            username='manager', email='manager@nucleusteq.com', password='managerpass', is_manager=True, department=self.department
        )
        self.employee = CustomUser.objects.create_user(
            username='employee', email='employee@nucleusteq.com', password='employeepass', is_employee=True, department=self.department, manager=self.manager
        )
        self.reimbursement = Reimbursement.objects.create(
            employee=self.employee,
            category='travel',
            amount=100.00,
            description='Travel expenses'
        )

    def test_submit_reimbursement_view(self):
        self.client.login(username='employee', password='employeepass')
        response = self.client.get(reverse('reimbursements:submit_reimbursement'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reimbursements/submit_reimbursement.html')

        response = self.client.post(reverse('reimbursements:submit_reimbursement'), {
            'category': 'travel',
            'amount': 100.00,
            'description': 'Travel expenses',
            'document': None
        })
        self.assertRedirects(response, reverse('accounts:employee_home'))

    def test_reimbursement_list_view(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('reimbursements:reimbursement_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reimbursements/reimbursement_list.html')

    def test_reimbursement_detail_view(self):
        self.client.login(username='manager', password='managerpass')
        response = self.client.get(reverse('reimbursements:reimbursement_detail', args=[self.reimbursement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reimbursements/reimbursement_detail.html')

    def test_approve_reimbursement_view(self):
        self.client.login(username='manager', password='managerpass')
        response = self.client.post(reverse('reimbursements:approve_reimbursement', args=[self.reimbursement.id]), {
            'action': 'approve',
            'manager_comments': 'Approved'
        })
        self.assertRedirects(response, reverse('accounts:manager_home'))
        self.reimbursement.refresh_from_db()
        self.assertEqual(self.reimbursement.status, 'approved')
        self.assertEqual(self.reimbursement.manager_comments, 'Approved')

    def test_decline_reimbursement_view(self):
        self.client.login(username='manager', password='managerpass')
        response = self.client.post(reverse('reimbursements:decline_reimbursement', args=[self.reimbursement.id]), {
            'manager_comments': 'Declined'
        })
        self.assertRedirects(response, reverse('accounts:manager_home'))
        self.reimbursement.refresh_from_db()
        self.assertEqual(self.reimbursement.status, 'declined')
        self.assertEqual(self.reimbursement.manager_comments, 'Declined')
