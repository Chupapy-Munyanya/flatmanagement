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
    path('house/<int:house_id>/', HouseAPIView.as_view()),
    path('flats/<int:house_id>/', FlatsAPIView.as_view()),
    path('commercials/<int:house_id>/', CommercialsAPIView.as_view()),
    path('types/<int:house_id>/', FlatTypeAPIView.as_view()),
    path('createservicetype/', CreateServiceType.as_view()),
    path('servicetypes/', ServiceTypesAPIView.as_view()),
    path('createservice/', CreateServiceAPIView.as_view()),
    path('services/<int:type_id>/', CategoryServicesAPIView.as_view()),
    path('services/', AllServicesAPIView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
