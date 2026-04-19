from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    POST_TYPES = [
        ('RECIPE', 'Recipe'),
        ('DISCOVERY', 'Discovery'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(
        max_length=10, 
        choices=POST_TYPES, 
        default='DISCOVERY'
    )
    
    # Recipe specific fields
    carbs_per_serving = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fiber = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    net_carbs = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, editable=False)
    glycemic_index = models.CharField(max_length=20, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically calculate net carbs before saving
        if self.post_type == 'RECIPE':
            carbs = self.carbs_per_serving or 0
            fiber = self.fiber or 0
            self.net_carbs = carbs - fiber
        else:
            self.net_carbs = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_post_type_display()}] {self.title}"


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"
