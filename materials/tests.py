from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile

image_file = SimpleUploadedFile(
    name='C#.png',
    content=open('images/C#.png', 'rb').read(),
    content_type='image/png'
)


class MaterialTestCase(APITestCase):

    def setUp(self) -> None:
        pass

    def test_create_course(self):
        """Тест создания курса"""
        data = {
            'name': 'Programming on C#',
            'description': 'Learn the C# language',
            'image': image_file
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
