from main.models import Booking
from rest_framework import viewsets, permissions, generics, renderers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from knox.models import AuthToken
from main.serializers import BookingSerializer, UserLoginSerializer, BookingRegisterSerializer

class BookingViewSets(viewsets.ViewSet):
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Booking.objects.select_related('bempno', 'bcardno').all()
    serializer_class = BookingSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)

    def list(self, request):
        queryset = Booking.objects.select_related('bempno', 'bcardno').all()
        return Response(BookingSerializer(queryset, many=True).data)

    def retrieve(self, request, pk=None):
        queryset = Booking.objects.get(pk=pk)
        return Response(BookingSerializer(queryset).data)

    def partial_update(self, request, pk=None):
        instance = Booking.objects.get(pk=pk)
        serializer = BookingSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)
 
    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_booking(self, request, *args, **kwargs):
        #get Booking by year
        queryset = Booking.objects.filter(category__id__iexact=kwargs['category'])
        return Response(BookingSerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_day(self, request, *args, **kwargs):
        #get Booking by year
        queryset = Booking.objects.filter(date_booked__iexact=kwargs['day'])
        return Response(BookingSerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_personal(self, request, *args, **kwargs):
        #get Booking by user
        queryset = Booking.objects.filter(bcardno=kwargs['id'])
        return Response(BookingSerializer(queryset, many=True).data , status=status.HTTP_200_OK)
    
    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_personal_day(self, request, *args, **kwargs):
        #get Booking by user
        queryset = Booking.objects.filter(bempno__iexact=kwargs['id'], date_booked__iexact=kwargs['day'])
        return Response(BookingSerializer(queryset, many=True).data , status=status.HTTP_200_OK)
    
    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_category(self, request, pk, type):
        #get Booking by year
        queryset = Booking.objects.filter(category_id__iexact=pk)
        return Response(BookingSerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_password(self, reqest, pk=None):
        # set or change password
        # set password
        # set Booking activated
        # send password email
        obj = Booking.objects.get(pk=pk)
        obj.set_password()
        obj.save()
        return obj

    @action(detail=True, methods=['post'])
    def set_deactivated(self, request, pk=None):
        #deactivate a user
        queryset = Booking.objects.get(pk=pk)
        pos = not queryset.is_active
        queryset.is_active = pos
        queryset.save()
        return Response({'is_active': pos, 'id': pk} , status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_state(self, request, pk=None, st=None):
        #deactivate a user
        queryset = Booking.objects.get(pk=pk)
        queryset.is_paid = st
        queryset.save()
        return Response({'is_paid': st, 'id': pk} , status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def set_about(self, request, pk=None):
        #deactivate a user
        queryset = Booking.objects.get(pk=pk)
        queryset.about = request.about
        queryset.save()
        return Response({'id': pk} , status=status.HTTP_200_OK)


    
#ALUMNI REGISTER API
class BookingRegisterAPI(generics.GenericAPIView):
    serializer_class = BookingRegisterSerializer

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
            'user' : BookingSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            "msg": 'You are logged in..'
        })