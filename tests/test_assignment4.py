import os
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from cms.models import Project, ProjectImage

User = get_user_model()

class Assignment4Tests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            email='admin4@example.com',
            password='password123',
            first_name='Admin',
            last_name='User',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        self.project = Project.objects.create(
            title="School Construction in Village X",
            description="Building 5 new classrooms.",
            status="Ongoing",
            location="Village X, State Y"
        )

    def test_project_model_creation(self):
        """Test that Project model can be created and string representation is correct."""
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(str(self.project), "School Construction in Village X")

    def test_project_image_model(self):
        """Test ProjectImage model relation to Project."""
        image = ProjectImage.objects.create(
            project=self.project,
            image_url='test_image.jpg'
        )
        self.assertEqual(self.project.images.count(), 1)
        self.assertEqual(image.project.title, self.project.title)

    def test_public_projects_view(self):
        """Test that the public projects page loads and filters properly."""
        response = self.client.get(reverse('home:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'School Construction in Village X')

        # Test filtering
        response_ongoing = self.client.get(reverse('home:projects') + '?status=Ongoing')
        self.assertContains(response_ongoing, 'School Construction in Village X')

        response_completed = self.client.get(reverse('home:projects') + '?status=Completed')
        self.assertNotContains(response_completed, 'School Construction in Village X')

    def test_cms_project_list_access(self):
        """Test that admin can access project CMS but unauthenticated cannot."""
        # Unauthenticated
        response = self.client.get(reverse('cms:project_list'))
        self.assertNotEqual(response.status_code, 200)
        
        # Authenticated Admin
        self.client.login(email='admin4@example.com', password='password123')
        response = self.client.get(reverse('cms:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'School Construction in Village X')
