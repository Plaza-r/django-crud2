from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Snack


# Create your tests here.
class SnacksTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username="tester", password="tester")
        self.snack = Snack.objects.create(title="flan", purchaser=self.user, description="Test")

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "flan")

    def test_snack_list_status(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_snack_list_template(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_list.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_snack_list_content(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        snacks = response.context['object_list']
        self.assertEqual(len(snacks), 1)
        self.assertEqual(snacks[0].title, "flan")
        self.assertEqual(snacks[0].description, "Test")
        self.assertEqual(snacks[0].purchaser.username, "tester")

    def test_snack_detail_status(self):
        url = reverse('snack_detail', args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_snack_detail_template(self):
        url = reverse('snack_detail', args=(1,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_detail.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_snack_detail_content(self):
        url = reverse('snack_detail', args=(1,))
        response = self.client.get(url)
        snack = response.context['snack']
        self.assertEqual(snack.title, "flan")
        self.assertEqual(snack.description, "Test")
        self.assertEqual(snack.purchaser.username, "tester")

    def test_snack_create(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "title": "Tamper",
                "description": "Poundy poundy",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "Details about Tamper")

    def test_snack_update_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"title": "Updated name", "description": "low on calories", "purchaser": self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))