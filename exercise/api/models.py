from django.contrib.auth.models import User
from django.contrib.gis.db import models

class Incident(models.Model):
    # Não há necessidade de definir id = models.AutoField(primary_key=True)
    # O Django trata deste field automaticamente por nós :)
    description = models.TextField()
    location = models.PointField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) # FIXME: Referenciar username ou id? Check Paulo, check.
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('VALIDATE','Validate'),    # FIXME: VALIDATE e VALIDATED parecem ambíguos e podem induzir em erro?
        ('VALIDATED','Validated'),
        ('RESOLVED', 'Resolved')
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='VALIDATE')

    CATEGORY_CHOICES = [
        ('CONSTRUCTION', 'Construction'),
        ('SPECIAL_EVENT', 'Special event'),
        ('INCIDENT', 'Incident'),
        ('WEATHER_CONDITION', 'Weather condition'),
        ('ROAD_CONDITION', 'Road condition')
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    class Meta:
        ordering = ['created']
