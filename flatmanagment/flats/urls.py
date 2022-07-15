from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from .views import *


app_name = 'flats'
urlpatterns = [
    path('buildingcompanies/', BuildingCompaniesAPIView.as_view()),
    path('buildingcompany/<int:company_id>/', BuildingCompanyAPIView.as_view()),
    path('apartments/', ApartmentsAPIView.as_view()),
    path('apartment/<int:apart_id>/', ApartmentViewAPI.as_view()),
    path('house/<int:house_id>/', HouseAPIView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
