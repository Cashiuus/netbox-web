
from django.db import models






class CPE(models.Model):
    """
    A Common Platform Enumeration (CPE) object string for use with automation.
    """
    cpe = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('cpe',)
    
    def __str__(self):
        self.cpe
