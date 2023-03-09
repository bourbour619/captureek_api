import datetime
from django.http import Http404
from django.shortcuts import render

from .models import Record, User
from .serializers import LoginSerializer, VerifySerializer, RegisterSerializer,RecordSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate
# Create your views here.

class LoginView(CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class= LoginSerializer
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        password = request.data['password']
        try:
            user = authenticate(request, username=email, password=password)
            token = AccessToken.for_user(user)
            token.set_exp(lifetime=datetime.timedelta(hours=1))
            user_obj = VerifySerializer(user)
            return Response({
                'user': user_obj.data,
                'token': str(token)
            }) 
        except :
            return Response({'error' : 'wrong password or email'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyView(APIView):
    permission_classes=[IsAuthenticated]
    
    def get(self, request, format=None):
        try:
            serializer = VerifySerializer(request.user, many=False)
            return Response({'user' : serializer.data})
        except KeyError:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
            
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class RecordList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecordSerializer(data=request.data, context= {'request' : request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordDetail(APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [IsAuthenticated]
    
    def get_record(self, pk):
        try:
            return Record.objects.get(pk=pk)
        except Record.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        record = self.get_record(pk)
        serializer = RecordSerializer(record)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        record = self.get_record(pk)
        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

