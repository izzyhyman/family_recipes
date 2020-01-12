from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import io
import os

from PIL import Image

class Recipe(models.Model):
    '''Represent a recipe'''
    # image if exists, or default
    # later add comments and tags
    # add date submitted
    title = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        default="images/default_recipe_img_01.jpg",
        )
    thumbnail = models.ImageField(
        upload_to="thumbs/",
        editable=False,
        default="thumbs/default_receipe_img_01_thumb.jpg",
    )
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date",]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.image:
            self.image = self.compress_image(self.image)
            self.thumbnail = self.make_thumbnail(self.image)
        super(Recipe, self).save(*args, **kwargs)
    
    
    def compress_image(self, image):
        if image:
            image1 = Image.open(image)
            image_width, image_height = image1.size
            aspect_ratio = image_width/image_height
            new_width = 640
            new_size = (new_width, int(new_width/aspect_ratio))
            image1_resized = image1.resize(new_size, Image.ANTIALIAS)
            output = io.BytesIO()
            image1_resized.save(output, format="JPEG", quality=85)
            output.seek(0)
            return InMemoryUploadedFile(
                output, 'ImageField', image.name, 'image/jpg', sys.getsizeof(output), None)
        else:
            return None

    def make_thumbnail(self, image):
        if image:
            thumb1 = Image.open(image)
            thumb1.thumbnail((160,160), Image.ANTIALIAS)
            output = io.BytesIO()
            thumb1.save(output, format="JPEG", quality=85)
            output.seek(0)

            # name and extension
            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_extension = thumb_extension.lower()
            thumb_filename = thumb_name + '_thumb' + thumb_extension

            # save thumbnail
            return InMemoryUploadedFile(
                output, 'ImageField', thumb_filename, 'image/jpg', sys.getsizeof(output), None)
        else:
            return None


class Comment(models.Model):
    # add date submitted
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return f"{self.text[:20]}..."
