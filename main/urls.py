from rest_framework import routers, renderers
from rest_framework.urlpatterns import format_suffix_patterns
from .api.category import CategoryViewSets, CategoryRegisterAPI
from .api.client import ClientViewSets, ClientRegisterAPI, ClientLoginAPI
from .api.employee import EmployeeViewSets, UserLoginAPI, EmployeeRegisterAPI
from .api.booking import BookingViewSets, BookingRegisterAPI
from django.urls import path, include
from django.conf import  settings
from django.conf.urls.static import static
from  knox import views as knox_views


urlpatterns = format_suffix_patterns([
    path('api', include('knox.urls')),
    path('api/employee/', EmployeeViewSets.as_view({'get' : 'list'}), name='employee-list'),
    path('api/employee/<int:pk>/profile', EmployeeViewSets.as_view({'get' : 'retrieve'}), name='employee-detail'),
    path('api/employee/<int:category>/category', EmployeeViewSets.as_view({'get' : 'get_employee'}), name='get_employee-list'),
    path('api/employee/<int:category>/group', EmployeeViewSets.as_view({'get' : 'get_search_category'}), name='get_search_category-list'),
    path('api/employee/<slug:category>/groups', EmployeeViewSets.as_view({'get' : 'get_search_value'}), name='get_search_value-list'),
    path('api/employee/<int:pk>/set_password', EmployeeViewSets.as_view({'post' : 'set_password'}), name='set_password-list'),
    path('api/employee/<int:pk>/set_deactivated', EmployeeViewSets.as_view({'post' : 'set_deactivated'}), name='set_deactivated-list'),
    path('api/employee/<int:pk>/set_about', EmployeeViewSets.as_view({'patch' : 'set_about'}), name='set_about-details'),
    path('api/employee/<int:pk>/update', EmployeeViewSets.as_view({'patch' : 'partial_update', 'post' : 'partial_update'}), name='partial_update'),
    path('api/employee/<int:pk>/<str:type>', EmployeeViewSets.as_view({'get' : 'get_category'}), name='get_category'),
    path('api/employee-register', EmployeeRegisterAPI.as_view()),
    path('api/employee-login', UserLoginAPI.as_view()),
    path('api/employee-logout', knox_views.LogoutView.as_view(), name='knox_employee_logout'),

    path('api/client/', ClientViewSets.as_view({'get' : 'list'}), name='client-list'),
    path('api/client/<int:pk>/profile', ClientViewSets.as_view({'get' : 'retrieve'}), name='client-detail'),
    path('api/client/<int:category>/category', ClientViewSets.as_view({'get' : 'get_client'}), name='get_client-list'),
    path('api/client/<int:pk>/set_password', ClientViewSets.as_view({'post' : 'set_password'}), name='set_password-list'),
    path('api/client/<int:pk>/set_deactivated', ClientViewSets.as_view({'post' : 'set_deactivated'}), name='set_deactivated-list'),
    path('api/client/<int:pk>/set_about', ClientViewSets.as_view({'patch' : 'set_about'}), name='set_about-details'),
    path('api/client/<int:pk>/update', ClientViewSets.as_view({'patch' : 'partial_update', 'post' : 'partial_update'}), name='partial_update'),
    path('api/client/<int:pk>/<str:type>', ClientViewSets.as_view({'get' : 'get_category'}), name='get_category'),
    path('api/client-register', ClientRegisterAPI.as_view()),
    path('api/client-login', ClientLoginAPI.as_view()),
    path('api/client-logout', knox_views.LogoutView.as_view(), name='knox_client_logout'),

    path('api/category/', CategoryViewSets.as_view({'get' : 'list'}), name='category-list'),
    path('api/category/<int:pk>/profile', CategoryViewSets.as_view({'get' : 'retrieve'}), name='category-detail'),
    path('api/category/<int:pk>/set_deactivated', CategoryViewSets.as_view({'post' : 'set_deactivated'}), name='set_deactivated-list'),
    path('api/category/<int:pk>/set_about', CategoryViewSets.as_view({'patch' : 'set_about'}), name='set_about-details'),
    path('api/category/<int:pk>/update', CategoryViewSets.as_view({'patch' : 'partial_update', 'post' : 'partial_update'}), name='partial_update'),
    path('api/category-register', CategoryRegisterAPI.as_view()),
    path('api/category/<int:pk>/set_delete', CategoryViewSets.as_view({'delete' : 'destroy'}), name='set_delete'),

    path('api/booking/', BookingViewSets.as_view({'get' : 'list'}), name='booking-list'),
    path('api/booking/<int:pk>/profile', BookingViewSets.as_view({'get' : 'retrieve'}), name='booking-detail'),
    path('api/booking/<int:id>/<slug:day>/day', BookingViewSets.as_view({'get' : 'get_day'}), name='get_day-list'),
    path('api/booking/<int:id>/personal', BookingViewSets.as_view({'get' : 'get_personal'}), name='booking-detail'),
    path('api/booking/<int:id>/<slug:day>/personalday', BookingViewSets.as_view({'get' : 'get_personal_day'}), name='get_day-list'),
    path('api/booking/<int:pk>/set_deactivated', BookingViewSets.as_view({'post' : 'set_deactivated'}), name='set_deactivated-list'),
    path('api/booking/<int:pk>/<int:st>/set_state', BookingViewSets.as_view({'post' : 'set_state'}), name='set_deactivated-list'),
    path('api/booking/<int:pk>/set_about', BookingViewSets.as_view({'patch' : 'set_about'}), name='set_about-details'),
    path('api/booking/<int:pk>/update', BookingViewSets.as_view({'patch' : 'partial_update', 'post' : 'partial_update'}), name='partial_update'),
    path('api/booking-register', BookingRegisterAPI.as_view()),
    path('api/booking/<int:pk>/set_delete', BookingViewSets.as_view({'delete' : 'destroy'}), name='set_delete'),
]) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)