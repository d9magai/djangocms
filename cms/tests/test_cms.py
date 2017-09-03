# coding: utf-8
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.compat import get_user_model
from rest_framework_jwt.settings import api_settings


class CmsTest(APITestCase):
    def setUp(self):
        # アクセストークンの発行
        User = get_user_model()
        self.username = 'test_user'
        self.email = 'test_user@gmail.com'
        self.user = User.objects.create_user(self.username, self.email)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(self.user)
        token = jwt_encode_handler(payload)
        self.auth = 'JWT {0}'.format(token)
        self.url = '/api/book/'


    def test_cms_api(self):
        # POST
        data = {
            "id": 1,
            "name": "book1",
            "publisher": "pub2",
            "page": 100,
        }
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)

        # GET
        expected_get_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "name": "book1",
                    "publisher": "pub2",
                    "page": 100,
                }
            ]
        }
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_get_data)

        # PUT
        data2 = {
            "id": 1,
            "name": "book2",
            "publisher": "pub2",
            "page": 200,
        }
        response = self.client.put(self.url + '1/', data2, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data2)

        # DELETE
        response = self.client.delete(self.url + '1/', HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
