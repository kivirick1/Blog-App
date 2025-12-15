from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Kategori Adı")

    class Meta:
        verbose_name = "Kategoriler"

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name="Başlık")
    content = models.TextField(verbose_name="İçerik")
    image = models.CharField(max_length=255, verbose_name="Görsel")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Kategori",
    )
    publish_date = models.DateTimeField(auto_now=True, verbose_name="Yayın Tarihi")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Yazar",
    )
    status = models.CharField(max_length=3, choices=(('d', 'Taslak'), ('p', 'Yayınlandı')), default='d', verbose_name="Yayınlanma Durumu")
    slug = models.SlugField(null=True, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_comment_count(self):
        return self.comments.count()

    def get_like_count(self):
        return self.likes.filter(likes=True).count()

    def get_view_count(self):
        return self.views.count()

    class Meta:
        verbose_name = "Bloglar"

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Kullanıcı",
    )
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name="Tarih")
    content = models.CharField(max_length=255, verbose_name="Yorum")
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name="Blog",
        related_name="comments",
    )

    class Meta:
        verbose_name = "Yorumlar"

    def __str__(self):
        return f"{self.user.username} yorumu (Blog#{self.blog.id})"

class Likes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Kullanıcı",
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name="Blog",
        related_name="likes",
    )
    likes = models.BooleanField(verbose_name="Beğenilme Durumu")

    class Meta:
        verbose_name = "Beğeniler"
        constraints = [
            models.UniqueConstraint(fields=['user', 'blog'], name='unique_like_per_user_blog'),
        ]

    def __str__(self):
        return f"{self.user.username} beğenisi (Blog#{self.blog.id})"

class PostViews(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Kullanıcı",
    )
    post_views = models.BooleanField(verbose_name="Görüntüleme Durumu")
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name="Blog",
        related_name="views",
    )
    time_stamp = models.DateTimeField(auto_now_add=True, verbose_name="Görüntüleme Tarihi")