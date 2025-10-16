from django.db import models

class Sport(models.Model):
    titre = models.CharField(max_length=50)
    contenu = models.TextField(blank=True)
    image = models.ImageField(upload_to='sport_media',blank=True, null=True)

    def __str__(self):
        return f'Titre : {self.titre } | Contenu : {self.contenu}'