from main.models import Client
from rest_framework import viewsets, permissions, generics, renderers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from knox.models import AuthToken
from main.serializers import ClientSerializer, ClientRegisterSerializer, UserLoginSerializer

class ClientViewSets(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def list(self, request):
        queryset = Client.objects.all()
        return Response(ClientSerializer(queryset, many=True).data)

    def retrieve(self, request, pk=None):
        queryset = Client.objects.get(pk=pk)
        return Response(ClientSerializer(queryset).data)

    def partial_update(self, request, pk=None):
        instance = Client.objects.get(pk=pk)
        serializer = ClientSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)
 

    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_client(self, request, year):
        #get Client by year
        queryset = Client.objects.filter(year__iexact=year)
        return Response(ClientSerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_password(self, reqest, pk=None):
        # set or change password
        # set password
        # set Client activated
        # send password email
        obj = Client.objects.get(pk=pk)
        obj.set_password()
        obj.save()
        return obj

    @action(detail=True, methods=['post'])
    def set_deactivated(self, request, pk=None):
        #deactivate a user
        queryset = Client.objects.get(pk=pk)
        pos = not queryset.is_active
        queryset.is_active = pos
        queryset.save()
        return Response({'is_active': pos, 'id': pk} , status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def set_about(self, request, pk=None):
        #deactivate a user
        queryset = Client.objects.get(pk=pk)
        queryset.about = request.about
        queryset.save()
        return Response({'id': pk} , status=status.HTTP_200_OK)


#CLIENT REGISTER API
class ClientRegisterAPI(generics.GenericAPIView):
    serializer_class = ClientRegisterSerializer
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Client.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
            'user' : ClientSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            "msg": 'You are registered..'
            })
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)

class ClientLoginAPI(generics.GenericAPIView):
    #permission_classes = (AllowAny,)
    #renderer_classes = (UserJSONRenderer,)
    serializer_class = UserLoginSerializer
 
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            'user' : ClientSerializer(user, context = self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
            "msg": 'You are logged in..'
        })