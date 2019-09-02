from main.models import Employee
from rest_framework import viewsets, permissions, generics, renderers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from knox.models import AuthToken
from main.serializers import EmployeeSerializer, UserLoginSerializer,  EmployeeRegisterSerializer

class EmployeeViewSets(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Employee.objects.annotate(number_of_bookings=Count('main_bookings')).all()
    serializer_class = EmployeeSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)

    def list(self, request):
        queryset = Employee.objects.annotate(number_of_bookings=Count('main_bookings')).all()
        return Response(EmployeeSerializer(queryset, many=True).data)

    def retrieve(self, request, pk=None):
        queryset = Employee.objects.get(pk=pk)
        return Response(EmployeeSerializer(queryset).data)

    def partial_update(self, request, pk=None):
        instance = Employee.objects.get(pk=pk)
        serializer = EmployeeSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)
 
    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_employee(self, request, *args, **kwargs):
        #get Employee by year
        queryset = Employee.objects.filter(category__id__iexact=kwargs['category'])
        return Response(EmployeeSerializer(queryset, many=True).data , status=status.HTTP_200_OK)
    
    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_category(self, request, pk, type):
        #get Employee by year
        queryset = Employee.objects.filter(category_id__iexact=pk)
        return Response(EmployeeSerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_search_category(self, request,  *args, **kwargs):
        #get Employee by year
        queryset = Employee.objects.filter(category__id__iexact=kwargs['category'], is_active=True)
        return Response(EmployeeSerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_search_value(self, request,  *args, **kwargs):
        #get Employee by year
        queryset = Employee.objects.filter(fullname__icontains=kwargs['category'], is_active=True)
        return Response(EmployeeSerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_password(self, reqest, pk=None):
        # set or change password
        # set password
        # set Employee activated
        # send password email
        obj = Employee.objects.get(pk=pk)
        obj.set_password()
        obj.save()
        return obj

    @action(detail=True, methods=['post'])
    def set_deactivated(self, request, pk=None):
        #deactivate a user
        queryset = Employee.objects.get(pk=pk)
        pos = not queryset.is_active
        queryset.is_active = pos
        queryset.save()
        return Response({'is_active': pos, 'id': pk} , status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def set_about(self, request, pk=None):
        #deactivate a user
        queryset = Employee.objects.get(pk=pk)
        queryset.about = request.about
        queryset.save()
        return Response({'id': pk} , status=status.HTTP_200_OK)


    
#ALUMNI REGISTER API
class EmployeeRegisterAPI(generics.GenericAPIView):
    serializer_class = EmployeeRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Employee.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)

class UserLoginAPI(generics.GenericAPIView):
    #permission_classes = (AllowAny,)
    #renderer_classes = (UserJSONRenderer,)
    serializer_class = UserLoginSerializer
 
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            'user' : EmployeeSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            "msg": 'You are logged in..'
        })