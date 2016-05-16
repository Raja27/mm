__author__ = 'rajaprasanna'

from rest_framework import serializers, pagination
from bridegroom import models


class LimitTenPaginator(pagination.PageNumberPagination):
    default_limit = 10
    page_size_query_param = 'limit'


class Cityserializer(serializers.ModelSerializer):

    class Meta:
        model = models.City

class Castserializer(serializers.ModelSerializer):

    class Meta:
        model = models.Casts


class FamilySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Family


class BrideGroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BrideGroom


class FamilyDetailserializer(serializers.ModelSerializer):
    cast = serializers.ReadOnlyField(source='cast.name')
    native_place = serializers.ReadOnlyField(source='native_place.name')
    gothram = serializers.ReadOnlyField(source='gothram.name')
    religion = serializers.ReadOnlyField(source='religion.name')
    language = serializers.ReadOnlyField(source='language.name')

    class Meta:
        model = models.Family


class BrideGroomDetailSerializer(serializers.ModelSerializer):

    family = FamilyDetailserializer(read_only=True)
    higher_degree = serializers.ReadOnlyField(source='higher_degree.name')
    occupations = serializers.ReadOnlyField(source='occupations.name')
    raasi = serializers.ReadOnlyField(source='raasi.name')
    star = serializers.ReadOnlyField(source='star.name')
    living_city = serializers.ReadOnlyField(source='living_city.name')

    class Meta:
        model = models.BrideGroom


class BrideGroomListSerializer(serializers.ModelSerializer):

    higher_degree = serializers.ReadOnlyField(source='higher_degree.name')
    occupations = serializers.ReadOnlyField(source='occupations.name')
    raasi = serializers.ReadOnlyField(source='raasi.name')
    star = serializers.ReadOnlyField(source='star.name')
    living_city = serializers.ReadOnlyField(source='living_city.name')

    cast = serializers.ReadOnlyField(source='cast.name')
    religion = serializers.ReadOnlyField(source='religion.name')

    class Meta:
        model = models.BrideGroom
        fields = ('name', 'height', 'date_of_birth',
                  'higher_degree', 'occupations', 'raasi',
                  'star', 'living_city', 'cast', 'religion')


class PhoneSeenserializer(serializers.ModelSerializer):

    class Meta:
        model = models.PhoneSeen