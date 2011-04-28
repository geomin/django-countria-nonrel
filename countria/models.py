from django.db import models
from lingua import translation
from decimal import Decimal
from django.conf import settings

from djangotoolbox import fields
from django_mongodb_engine.contrib import MongoDBManager

class Currency(models.Model):
    class Translation(translation.Translation):
        name   = models.CharField(max_length=16)
    code   = models.CharField(max_length=3) 

    class Meta:
        unique_together = (('name','code'), )

    def __unicode__(self):
        return unicode(self.name)

class Continent(models.Model):
    class Translation(translation.Translation):
        name   = models.CharField(max_length=16)
    code   = models.CharField(max_length=2) 

    class Meta:
        unique_together = (('name','code'), )

    def __unicode__(self):
        return unicode(self.name)

class Country(models.Model):
    class Translation(translation.Translation):
        name      = models.CharField(max_length=64, unique=True)
        full_name = models.CharField(max_length=64)

    currency        = fields.EmbeddedModelField(Currency, null=True)
    capital         = fields.EmbeddedModelField('City', null=True)   
    idc             = models.PositiveIntegerField(null=True) # Iternational Dialing Code
    iso_2           = models.CharField(max_length=2, null=True)
    iso_3           = models.CharField(max_length=3, null=True)
    iso_number      = models.PositiveIntegerField(null=True)
    tld             = models.CharField(max_length=7, null=True)
    geo             = fields.ListField(models.FloatField(), null=True)
    population      = models.PositiveIntegerField(null=True)
    continent       = fields.EmbeddedModelField(Continent, null=True)

    @property
    def calling_code(self):
        return '00%d' % self.idc
    
    def __unicode__(self):
        if hasattr(settings, 'MAX_COUNTRY_NAME_LENGTH'):
            if len(self.name) > settings.MAX_COUNTRY_NAME_LENGTH:
                return self.name[:settings.MAX_COUNTRY_NAME_LENGTH] + '...'
        return unicode(self.name)

class City(models.Model):
    class Translation(translation.Translation):
        name = models.CharField(max_length=64)

    country     = fields.EmbeddedModelField(Country, null=True)
    state       = fields.EmbeddedModelField('State', null=True)
    population  = models.PositiveIntegerField(null=True)
    geo         = fields.ListField(models.FloatField(), null=True)

    objects = MongoDBManager()

    def __unicode__(self):
        return unicode(self.name)

class State(models.Model):
    class Translation(translation.Translation):
        name = models.CharField(max_length=64)

    capital     = fields.EmbeddedModelField('City', null=True)
    country     = fields.EmbeddedModelField(Country, null=True)
    geo         = fields.ListField(models.FloatField(), null=True)
    code        = models.CharField(max_length=2)

    def __unicode__(self):
        return unicode(self.name)

class IpRange(models.Model):
    city  = models.ForeignKey(City)
    range = fields.DictField()

    def __unicode__(self):
        return unicode(self.name)

