from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from users.models import User

image_file = SimpleUploadedFile(
    name='C#.png',
    content=open('images/C#.png', 'rb').read(),
    content_type='image/png'
)


class MaterialTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        self.user.save()

    def test_create_course(self):
        """Тест создания курса"""
        data = {
            'name': 'Programming on C#',
            'description': 'Learn the C# language',
            'image': image_file,
            'owner': self.user.id
        }
        response = self.client.post(
            '/courses/',
            data=data
        )

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
