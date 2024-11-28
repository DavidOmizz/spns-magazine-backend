from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary_storage.storage import MediaCloudinaryStorage


class User(AbstractUser):
    USER_TYPE = (
        ('subscriber', 'Subscriber'),
        ('contributor', 'Contributor'),
        ('free', 'Free'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='free')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)


class Contributor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='contributors/', storage=MediaCloudinaryStorage(), blank=True, null=True)

    def __str__(self):
        return self.user.username


class Edition(models.Model):
    name = models.CharField(max_length=255)
    # description = models.TextField()
    description = RichTextField()
    editors_desk_speech = RichTextField(blank=True, null=True)
    coverimage = models.ImageField(upload_to='editions/', storage=MediaCloudinaryStorage(), blank=True, null=True)
    release_date = models.DateField()
    pdf_file = models.FileField(upload_to='edition_pdfs/', storage=MediaCloudinaryStorage(), blank=True, null=True)  # PDF upload field


    def __str__(self):
        return self.name


# class Article(models.Model):
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     image = models.ImageField(upload_to='articles/', blank=True, null=True)
#     contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='articles')
#     edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='articles')
#     publication_date = models.DateField()

#     def __str__(self):
#         return self.title


class Article(models.Model):
    INDUSTRY_CHOICES = [
        ('FIN', 'Finance'),
        ('DATA', 'Data Analysis'),
        ('CUB', 'Construction Business'),
        ('ENGR', 'Engineering'),
        ('SME', 'SME Development'),
        ('TM', 'Tourism'),
        ('CUST', 'Customer Care/experience Management'),
    ]
     
    title = models.CharField(max_length=255)
    # content = models.TextField()  # This will hold the short summary
    content = RichTextField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='articles/',storage=MediaCloudinaryStorage(), blank=True, null=True)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='articles')
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='articles')
    publication_date = models.DateField()
    pdf_file = models.FileField(upload_to='article_pdfs/', storage=MediaCloudinaryStorage(), blank=True, null=True)  # PDF upload field
    industry = models.CharField(max_length=10, choices=INDUSTRY_CHOICES, blank=True, null=True)
    def __str__(self):
        return self.title
    

class PDFRequest(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="pdf_requests")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    company = models.CharField(max_length=30)
    job_title = models.CharField(max_length=30)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.article.title} by {self.name}"
    
class EditionRequest(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name="edition_requests")
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    company = models.CharField(max_length=30)
    job_title = models.CharField(max_length=30)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request for {self.edition.name} by {self.name}"

