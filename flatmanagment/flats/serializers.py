from rest_framework import serializers

from .models import (
    BuildingCompany, Apartment, House, Entrance, Deal, DealStatus, Service, ServiceType, Flat, FlatType, Commercial, Placement
)


class HouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = House
        fields = ('name', 'apartment', 'descr')


class ApartmentSerializer(serializers.ModelSerializer):
    houses = HouseSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = ('name', 'builder', 'descr', 'houses')


class BuildingCompanySerializer(serializers.ModelSerializer):
    # apartments = ApartmentSerializer(many=True, read_only=True)

    class Meta:
        model = BuildingCompany
        fields = ['name', 'avatar', 'descr', 'apartments']


class EntranceSerializer(serializers.ModelSerializer):
    # house = serializers.StringRelatedField()

    class Meta:
        model = Entrance
        fields = ('number', 'house')


class PlacementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Placement
        fields = ('number', 'floor', 'owner_id')


class FlatTypeSerializer(serializers.ModelSerializer):
    # house = serializers.StringRelatedField()

    class Meta:
        model = FlatType
        fields = ('rooms', 'square', 'descr', 'schema', 'house')


class FlatSerializer(serializers.ModelSerializer):
    # type = serializers.RelatedField()
    # entrance = serializers.StringRelatedField()

    class Meta:
        model = Flat
        fields = ('number', 'floor', 'owner_id', 'type', 'entrance')


class CommercialSerializer(serializers.ModelSerializer):
    # house = serializers.StringRelatedField()

    class Meta:
        model = Commercial
        fields = ('number', 'floor', 'owner_id', 'square', 'house', 'descr')


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('pk', 'name', 'description')


class ServiceSerializer(serializers.ModelSerializer):
    # type = serializers.RelatedField()

    class Meta:
        model = Service
        fields = ('performer_id', 'price', 'description', 'service_type')


class DealStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = DealStatus
        fields = ('name',)


class DealSerializer(serializers.ModelSerializer):
    # service = serializers.StringRelatedField()
    # placement = PlacementSerializer
    # status = serializers.StringRelatedField()

    class Meta:
        model = Deal
        fields = ('service', 'placement', 'status', 'dt')
