# djangowiz/repo/templates/test.py.j2

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from test.models import Property
from rest_framework.test import APIClient
import os

class PropertyAPITests(TestCase):
    fixtures = ['property_fixtures.json']

    def setUp(self):
        self.client = APIClient()
        self.model_list_url = reverse('property-list')
        self.model_detail_url = lambda pk: reverse('property-detail', args=[pk])
        self.instances = Property.objects.all()
        self.first_instance = self.instances.first()
        self.second_instance = self.instances[1] if len(self.instances) > 1 else None
        # Dynamically determine the first string field
        self.string_field, self.first_value, self.second_value = self.get_first_string_field_and_values()

    def get_first_string_field_and_values(self):
        for field, value in self.first_instance.__dict__.items():
            if isinstance(value, str):
                second_value = getattr(self.second_instance, field) if self.second_instance else "Updated Value"
                return field, value, second_value
        return 'name', 'Sample Name', 'Updated Name'  # Default if no string field is found

    def test_list_propertys(self):
        response = self.client.get(self.model_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.instances))

    def test_create_property(self):
        # Update data with the correct fields and values for Property
        data = {self.string_field: 'New Value'}  # Replace 'New Value' with actual data
        response = self.client.post(self.model_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), len(self.instances) + 1)

    def test_retrieve_property(self):
        response = self.client.get(self.model_detail_url(self.first_instance.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[self.string_field], getattr(self.first_instance, self.string_field))

    def test_update_property(self):
        if not self.second_instance:
            self.skipTest("Not enough instances for update test")
        data = {self.string_field: self.second_value}
        response = self.client.put(self.model_detail_url(self.first_instance.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.first_instance.refresh_from_db()
        self.assertEqual(getattr(self.first_instance, self.string_field), self.second_value)

    def test_partial_update_property(self):
        if not self.second_instance:
            self.skipTest("Not enough instances for partial update test")
        data = {self.string_field: self.second_value}
        response = self.client.patch(self.model_detail_url(self.first_instance.pk), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.first_instance.refresh_from_db()
        self.assertEqual(getattr(self.first_instance, self.string_field), self.second_value)

    def test_delete_property(self):
        response = self.client.delete(self.model_detail_url(self.first_instance.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), len(self.instances) - 1)

    def test_invalid_create(self):
        # Missing required fields in data
        data = {}  # Add required fields and their values here
        response = self.client.post(self.model_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)