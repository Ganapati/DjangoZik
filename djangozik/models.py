from django.template.defaultfilters import slugify
from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=250)
    picture = models.CharField(max_length=256, null=True)
    text = models.TextField(null=True)
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Artist, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Style(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Style, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Album(models.Model):
    name = models.CharField(max_length=250)
    date = models.DateField('date released', null=True)
    picture = models.CharField(max_length=256, null=True)
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Song(models.Model):
    title = models.CharField(max_length=250)
    artist = models.ForeignKey(Artist, related_name="song")
    style = models.ForeignKey(Style, related_name="song")
    album = models.ForeignKey(Album, related_name="song")
    filepath = models.CharField(max_length=256)
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Song, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Playlist(models.Model):
    name = models.CharField(max_length=250)
    songs = models.ManyToManyField(Song, related_name="playlist")
    slug = models.SlugField(db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Playlist, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Radio(models.Model):
    url = models.CharField(max_length=256)

    def __unicode__(self):
        return self.url
