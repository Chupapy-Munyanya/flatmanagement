from django.shortcuts import render, HttpResponse

from django.db.models import Count
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView, Response

from .serializers import *

# Create your views here.


class BuildingCompaniesAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BuildingCompanySerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return BuildingCompany.objects.all().order_by('name')


class BuildingCompanyAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = BuildingCompanySerializer

    def get(self, request, company_id):
        serializer = self.serializer_class(BuildingCompany.objects.get(pk=company_id))
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ApartmentsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ApartmentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Apartment.objects.all().order_by('builder')


class ApartmentViewAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, apart_id):
        apart = Apartment.objects.get(pk=apart_id)
        houses = House.objects.filter(apartment=apart)
        data = {
            'name': apart.name,
            'image': apart.image.url,
            'descr': apart.descr,
            'houses': []
        }
        for house in houses:
            data['houses'].append({
                'id': house.pk,
                'name': house.name,
                'descr': house.descr,
                'flat_count': Flat.objects.filter(house=house).count(),
                'free_flat_count': Flat.objects.filter(house=house).filter(owner_id=None).count(),
                'all_commercial': Commercial.objects.filter(house=house).count(),
                'free_commercial': Commercial.objects.filter(house=house).filter(owner_id=None).count()
            })
        return Response(data=data, status=status.HTTP_200_OK)


class HouseAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = HouseSerializer

    def get(self, request, house_id):
        serializer = self.serializer_class(House.objects.get(pk=house_id))
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FlatAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FlatSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        house_id = self.kwargs['house_id']
        return Flat.objects.filter(house=House.objects.get(pk=house_id))


class CommercialAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FlatSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        house_id = self.kwargs['house_id']
        return Commercial.objects.filter(house=House.objects.get(pk=house_id))


