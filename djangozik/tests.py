from django.test import TestCase, Client
from django.contrib.auth.models import User


class HomeViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class SongsViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/songs/albums/test_value')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class ArtistsViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/artists/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class AlbumsViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/albums/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class StylesViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/styles/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class PlaylistViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/playlists/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class RadioViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/radios/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class SearchViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/search/test_value')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()


class AjaxViewTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='test_user',
                                 email='test@foo.bar',
                                 password='test_password')

    def test_view(self):
        c = Client()
        c.login(username='test_user', password='test_password')
        response = c.head('/ajax/test_value/foo')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()
