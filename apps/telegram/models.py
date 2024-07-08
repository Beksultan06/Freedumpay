from django.db import models

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    download_limit = models.IntegerField()

    def __str__(self):
        return self.name
    
    # class Meta:
    #     verbose_name_plural = ''

class UserDownload(models.Model):
    user_id = models.BigIntegerField(unique=True)
    download_count = models.IntegerField(default=0)

    # class MEta:
    #     verbose_name_plural = ''  