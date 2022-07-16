from django.shortcuts import render, HttpResponse

from django.db.models import Count
from rest_framework import authentication, status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.views import APIView, Response
import requests

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
            'builder': apart.builder.name,
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


class FlatTypeAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FlatTypeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        house_id = self.kwargs['house_id']
        return FlatType.objects.filter(house=House.objects.get(pk=house_id))


class FlatsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FlatSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        house_id = self.kwargs['house_id']
        return Flat.objects.filter(house=House.objects.get(pk=house_id))


class CommercialsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FlatSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        house_id = self.kwargs['house_id']
        return Commercial.objects.filter(house=House.objects.get(pk=house_id))


AUTHENTICATION_HEADER_PREFIX = 'Token'
BASE_URL = 'http://localhost:5000/'


def check_auth(request):
    auth_header = authentication.get_authorization_header(request).split()
    auth_header_prefix = AUTHENTICATION_HEADER_PREFIX.lower()

    if not auth_header:
        return

    if len(auth_header) == 1:
        return

    elif len(auth_header) > 2:
        return

    prefix = auth_header[0].decode('utf-8')
    token = auth_header[1].decode('utf-8')

    if prefix.lower() != auth_header_prefix:
        return

    res = requests.get(headers={'Authorization': f'{prefix} {token}'}, url=BASE_URL+'user/')
    return res.json()


class CreateServiceType(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ServiceTypeSerializer

    def post(self, request):
        user_data = check_auth(request)
        if user_data.get("pk"):
            if user_data['is_staff']:
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ServiceTypesAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ServiceTypeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return ServiceType.objects.all().order_by('name')


class CreateServiceAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ServiceSerializer

    def post(self, request):
        user_data = check_auth(request)
        if user_data.get("pk"):
            data = request.data
            data |= {'performer_id': str(user_data['pk'])}
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AllServicesAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ServiceSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Service.objects.all()


class CategoryServicesAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ServiceSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        type_id = self.kwargs['type_id']
        return Service.objects.filter(service_type=ServiceType.objects.get(pk=type_id))


class UserPlacementsAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PlacementSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Placement.objects.filter(owner_id=user_id)


class DealStatusAPIView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DealStatusSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return DealStatus.objects.all()


class CreateDealAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = DealSerializer

    def post(self, request):
        user_data = check_auth(request)
        if user_data.get("pk"):
            data = request.data
            data |= {'user_id': str(user_data['pk'])}
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UpdateDealStatusAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        deal = Deal.objects.get(pk=data["pk"])
        deal.status = DealStatus.objects.get(pk=data["status_id"])
        deal.save(updated_fields=['status'])
        return Response(status=status.HTTP_200_OK)
