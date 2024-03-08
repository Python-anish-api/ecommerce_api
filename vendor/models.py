from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User, Profile
from django.db.models import Max
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import shortuuid    
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="vendor")
    image = models.FileField(upload_to='vendor/', default="shop-image.jpg", blank=True)
    name = models.CharField(max_length=100, help_text="Shop Name", null=True, blank=True)
    email = models.EmailField(max_length=100, help_text="Shop Email", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    mobile = models.CharField(max_length = 150, null=True, blank=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('  <img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.shop_image.url))

    def __str__(self):
        return str(self.name)
        

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.name)
        super(Vendor, self).save(*args, **kwargs) 

