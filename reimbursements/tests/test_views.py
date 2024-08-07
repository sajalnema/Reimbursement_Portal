from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from reimbursements.models import Reimbursement
from django.utils import timezone

User = get_user_model()

class ReimbursementViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='employee', password='password', is_employee=True)
        self.manager = User.objects.create_user(username='manager', password='password', is_manager=True)
        self.admin = User.objects.create_superuser(username='admin', password='password')
        self.reimbursement = Reimbursement.objects.create(
            employee=self.user,
            category='travel',
            amount=1000,
            description='Travel expenses',
            status='pending',
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    def test_submit_reimbursement_get(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('reimbursements:submit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reimbursements/submit_reimbursement.html')

    def test_submit_reimbursement_post_valid(self):
        self.client.login(username='employee', password='password')
        data = {
            'category': 'travel',
            'amount': 500,
            'description': 'Travel for conference',
            'date': '2024-06-16'
        }
        response = self.client.post(reverse('reimbursements:submit'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:employee_home'))
        self.assertEqual(Reimbursement.objects.count(), 2)

    def test_submit_reimbursement_post_invalid(self):
        self.client.login(username='employee', password='password')
        data = {
            'category': 'travel',
            'amount': 20000,  # Exceeds limit
            'description': 'Travel for conference',
            'date': '2024-06-16'
        }
        response = self.client.post(reverse('reimbursements:submit'), data)
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertFormError(response, 'form', 'amount', 'Amount exceeds the limit for travel category')

    def test_reimbursement_list_superuser(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('reimbursements:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['reimbursements']), Reimbursement.objects.count())

    def test_reimbursement_list_manager(self):
        self.client.login(username='manager', password='password')
        response = self.client.get(reverse('reimbursements:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['reimbursements']), 0)  # No managed employees yet

    def test_reimbursement_list_employee(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('reimbursements:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['reimbursements']), 1)

    def test_reimbursement_detail_get(self):
        self.client.login(username='employee', password='password')
        response = self.client.get(reverse('reimbursements:detail', args=[self.reimbursement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reimbursements/reimbursement_detail.html')

    def test_reimbursement_detail_unauthorized(self):
        self.client.login(username='manager', password='password')
        response = self.client.get(reverse('reimbursements:detail', args=[self.reimbursement.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertRedirects(response, reverse('accounts:manager_home'))

    def test_approve_reimbursement_post(self):
        self.client.login(username='manager', password='password')
        response = self.client.post(reverse('reimbursements:approve', args=[self.reimbursement.id]), {'action': 'approve'})
        self.assertEqual(response.status_code, 302)
        self.reimbursement.refresh_from_db()
        self.assertEqual(self.reimbursement.status, 'approved')

    def test_decline_reimbursement_post(self):
        self.client.login(username='manager', password='password')
        response = self.client.post(reverse('reimbursements:decline', args=[self.reimbursement.id]), {'action': 'decline'})
        self.assertEqual(response.status_code, 302)
        self.reimbursement.refresh_from_db()
        self.assertEqual(self.reimbursement.status, 'declined')

    def test_approve_reimbursement_unauthorized(self):
        self.client.login(username='employee', password='password')
        response = self.client.post(reverse('reimbursements:approve', args=[self.reimbursement.id]), {'action': 'approve'})
        self.assertEqual(response.status_code, 302)
        self.reimbursement.refresh_from_db()
        self.assertEqual(self.reimbursement.status, 'pending')  # Should not change

    def test_decline_reimbursement_unauthorized(self):
        self.client.login(username='employee', password='password')
        response = self.client.post(reverse('reimbursements:decline', args=[self.reimbursement.id]), {'action': 'decline'})
        self.assertEqual(response.status_code, 302)
        self.reimbursement.refresh_from_db()
        self.assertEqual(self.reimbursement.status, 'pending')  # Should not change

    def test_invalid_reimbursement_id(self):
        self.client.login(username='manager', password='password')
        response = self.client.post(reverse('reimbursements:approve', args=[999]), {'action': 'approve'})
        self.assertEqual(response.status_code, 404)

        response = self.client.post(reverse('reimbursements:decline', args=[999]), {'action': 'decline'})
        self.assertEqual(response.status_code, 404)

