# test that helper function for our model can create new user

from django.test import TestCase
# import get user model helper function that comes with django, you can
# directly import the models from django , but this is not recommended
# if everywhere get_user_model is used then any changes made could be easily
# imported
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating a new user with email is successful'''
        email = 'trial@trial.com'
        password = 'trial123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)  # make sure email of user created
        # is same as email passed in
        self.assertTrue(user.check_password(password))  # returns T if pwd good

    def test_new_user_email_normalized(self):
        '''Test the email for new user is normalized'''
        email = 'trial@TRIAL.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_invalid_email(self):
        '''Test creating user with no email raises err'''
        with self.assertRaises(ValueError):  # anything in the following section
            # should raise ValueError if not this test fails
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        '''Test creating superuser'''
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)  # is_superuser is included as part
        # permissionsmixin
        self.assertTrue(user.is_staff)
