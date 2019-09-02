from main.models import Category
from rest_framework import viewsets, permissions, generics, renderers, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import action
from knox.models import AuthToken
from main.serializers import CategorySerializer

class CategoryViewSets(viewsets.ViewSet):
    permission_classes = [
        permissions.AllowAny
    ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def list(self, request):
        queryset = Category.objects.all()
        return Response(CategorySerializer(queryset, many=True).data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.get(pk=pk)
        return Response(CategorySerializer(queryset).data)

    def destroy(self, request, pk=None):
        instance = Category.objects.get(pk=pk).delete()
        return Response({'id': pk} , status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        instance = Category.objects.get(pk=pk)
        serializer = CategorySerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_306_RESERVED)
 
    @action(detail=False, renderer_classes=[renderers.JSONRenderer])
    def get_category(self, request, year):
        #get Category by year
        queryset = Category.objects.filter(year__iexact=year)
        return Response(CategorySerializer(queryset, many=True).data , status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_deactivated(self, request, pk=None):
        #deactivate a user
        queryset = Category.objects.get(pk=pk)
        pos = not queryset.is_active
        queryset.is_active = pos
        queryset.save()
        return Response({'is_active': pos, 'id': pk} , status=status.HTTP_200_OK)

#ALUMNI REGISTER API
class CategoryRegisterAPI(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)