# test_views.py
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Teacher, School, User
from rest_framework.authtoken.models import Token

class TeacherViewSetTest(APITestCase):
    def setUp(self):
        # Create test User, Token, and School
        self.user = User.objects.create(username="johndoe", email="johndoe@example.com")
        self.user.set_password("password")
        self.user.save()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.school = School.objects.create(name="Test School")
        self.teacher = Teacher.objects.create(user=self.user, school=self.school, department="Math")

    def test_list_teachers(self):
        """
        Test the list endpoint for teachers.
        """
        response = self.client.get("/teachers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['department'], "Math")

    def test_retrieve_teacher(self):
        """
        Test the retrieve endpoint for a single teacher.
        """
        response = self.client.get(f"/teachers/{self.teacher.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department'], "Math")

    def test_create_teacher(self):
        """
        Test the create endpoint for a teacher.
        """
        new_user = User.objects.create(username="janedoe", email="janedoe@example.com")
        data = {
            "user": new_user.id,
            "school": self.school.id,
            "department": "Science"
        }
        response = self.client.post("/teachers/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['department'], "Science")

    def test_update_teacher(self):
        """
        Test the update endpoint for a teacher.
        """
        data = {"department": "Physics"}
        response = self.client.patch(f"/teachers/{self.teacher.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.department, "Physics")

    def test_delete_teacher(self):
        """
        Test the delete endpoint for a teacher.
        """
        response = self.client.delete(f"/teachers/{self.teacher.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Teacher.objects.filter(id=self.teacher.id).exists())
