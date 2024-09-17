from django.shortcuts import render
from django.db import connections
from django.core.paginator import Paginator
from rest_framework import viewsets
from django.views import View
from ..serializers import FileHandOverSerializer
from App_db.models.file_handover_mt import FileHandOver
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status,permissions
from ..serializers import LoginSerializer
from django.conf import settings
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from  django.http import JsonResponse


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            print("Access Token:", access_token)

            return Response({
                "access": access_token,
                "refresh": refresh_token,
                
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LoginUnit(APIView):
        def get(self, request):
                sql_query2 = """ 
                             SELECT
                               id AS UnitID,
                               name AS Unit
                               FROM location_master
                            """
            
                with connections['intellisync_db'].cursor() as cursor:
                    cursor.execute(sql_query2)
                    Units = cursor.fetchall()
                    
                unit_data = [{'id': unit[0], 'name': unit[1]} for unit in Units]
                return JsonResponse({
                                  'Units': unit_data},
                                   safe=False)
                
     
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.is_authenticated:
                user = request.user
                print("User data ----------------------------------",user)
                context ={
                        'username':user.username,
                        'user_id' :user.id,
                        'full_name':user.full_name,
                        'location': user.location
                        
                    }
        return JsonResponse(context,safe=False)
    
    
    
class UserLogoutView(APIView):
    def post(self, request):
        # Extract tokens from the request
        refresh_token = request.data.get('refresh')
        access_token = request.headers.get('Authorization', '').split(' ')[1]

        if not refresh_token:
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()


            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        
        except (TokenError, InvalidToken) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)