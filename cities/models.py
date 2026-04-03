from django.db import models

from participants.choises import DistrictChoice


# Create your models here.

class Cities(models.Model):
    name = models.CharField(max_length=20,unique=True,error_messages={
                                'required': 'Моля въведете име на град или село.',
                                'unique': 'Такъв град вече съществува.',
                            })

    district = models.CharField(max_length=20, choices=DistrictChoice.choices,
                                error_messages={
                                    'required': 'Моля въведете име на град или село.',
                                })

    class Meta:
        verbose_name = "Град/Село"
        verbose_name_plural = "Населени места"

    def __str__(self):
        return self.name + ' , ' + self.district
