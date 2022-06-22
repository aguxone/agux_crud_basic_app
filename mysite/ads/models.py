from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

#Django4w5
from taggit.managers import TaggableManager # We need a tag manager, it integrates with search
# This is a django extension and is installed separadetely, pip install django-taggit
# and added to the project's setting.py in installed apps.

class Ad(models.Model) :
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Comment field which is manytomany, Django 4w2
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
    through='Comment', related_name='comments_owned')

    # Picture field, Django4w2
    picture = models.BinaryField(null=True, editable=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    # Favorites field for favorite icon, Django 4w4
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Fav', related_name='favorite_ads')

    # Django4w5 Tag field, just shown text in detail view in order to have a better search criteria
    tags = TaggableManager(blank=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title

# We'll add a model called comment, the table

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'

# Now for Django4w4, The Fav Class for fav icon, it's a through table

class Fav(models.Model) :
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.2/ref/models/options/#unique-together
    class Meta:
        unique_together = ('ad', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.ad.title[:10])

