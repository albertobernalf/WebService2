from django.shortcuts import render
from rest_framework import serializers, viewsets, routers
from rest_framework.views  import APIView
from rest_framework.response  import Response
from rest_framework.decorators import api_view
from reportes.models import User
# Create your views here.


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


#class UserApiView(APIView):
@api_view(['GET', 'POST'])
def user_api_view(request):
#    def get(self, request):
        if request.method =='GET':

            print("pase")
            queryset = User.objects.all()
            user_serializer = UserSerializer(queryset, many = True)
            print("pase")
            return Response(user_serializer.data)

        elif request.method =='POST':
            user_serializer = UserSerializer(data = request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data)
            return Response(user_serializer.errors)

