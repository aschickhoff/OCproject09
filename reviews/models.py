from PIL import Image
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='books_img')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    if image is True:
        def save(self, *args, **kwargs):
            super(Ticket, self).save(*args, **kwargs)
            img = Image.open(self.image.path)
            if img.height > 200 or img.width > 125:
                output_size = (200, 125)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('ticket-detail', kwargs={'pk': self.pk})


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        return reverse('review-detail', kwargs={'pk': self.pk})
