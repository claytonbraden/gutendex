from django.db import models


class Book(models.Model):
    authors = models.ManyToManyField('Person', related_name='books')
    bookshelves = models.ManyToManyField('Bookshelf')
    copyright = models.BooleanField(null=True)
    download_count = models.PositiveIntegerField(blank=True, null=True)
    gutenberg_id = models.PositiveIntegerField(unique=True, primary_key=True)
    languages = models.ManyToManyField('Language')
    media_type = models.CharField(max_length=16)
    subjects = models.ManyToManyField('Subject')
    title = models.CharField(blank=True, max_length=1024, null=True)
    translators = models.ManyToManyField(
        'Person', related_name='books_translated')
    gutenberg_url = models.URLField(null=True, blank=True)  # Added this field to get URL
    cover_image_url = models.URLField(null=True, blank=True)  # Added this line to get jpg url
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)  # Added this line to get jpg image
    
    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.id)

    def get_formats(self):
        return Format.objects.filter(book_id=self.id)

    def get_summaries(self):
        return Summary.objects.filter(book_id=self.id)


class Bookshelf(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Format(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)

    def __str__(self):
        return "%s (%s)" % (
            self.mime_type,
            self.book.__str__()
        )


class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.code


class Person(models.Model):
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Summary(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        preview_len = 24
        return f'{self.text[:preview_len]}...' if len(self.text) > preview_len else self.text
