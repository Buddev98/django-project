from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=100, validators=[MinLengthValidator(2)])

    def __str__(self):
        return self.caption

class Author(models.Model):
    first_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email_address = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Post(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(5)])
    excerpt = models.CharField(max_length=500, validators=[MinLengthValidator(10)])
    image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    content = models.TextField(validators=[MinLengthValidator(20)])
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    content = models.TextField(validators=[MinLengthValidator(5)])
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"