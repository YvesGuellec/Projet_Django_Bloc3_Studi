from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from vitrine import views
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Sport


class SportModelTest(TestCase):

    def test_creation_sport_sans_image(self):
        # Vérifie qu’un sport peut être créé sans image
        sport = Sport.objects.create(
            titre="Tennis",
            contenu="Sport individuel"
        )

        self.assertEqual(sport.titre, "Tennis")
        self.assertEqual(sport.contenu, "Sport individuel")
        self.assertIn(sport.image.name, [None, ''])
        self.assertFalse(sport.image)
        self.assertIn("Titre : Tennis", str(sport))

    def test_creation_sport_avec_image(self):
        # Vérifie qu’un sport peut être créé avec une image
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'image_test_content',
            content_type='image/jpeg'
        )

        sport = Sport.objects.create(
            titre="Basketball",
            contenu="Sport d’équipe",
            image=image
        )

        self.assertEqual(sport.titre, "Basketball")
        self.assertIn("test_image", sport.image.name)
        self.assertIn("Basketball", str(sport))

class TestComptesUrls(SimpleTestCase):
    # Vérifie que chaque vu pointe vers la bonne vue.

    def test_register_url_resolves(self):
        url = reverse('vitrine:accueil')
        self.assertEqual(resolve(url).func, views.Accueil)
    

