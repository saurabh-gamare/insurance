from rest_framework.views import APIView
from .serializers import ProfileSerializer, UserSerializer, PolicySerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from .models import Profile, PolicyDetail
from datetime import datetime
import random


class Registration(APIView):

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if not user_serializer.is_valid():
            return Response(user_serializer.errors, status=400)
        user = user_serializer.save()
        
        request_data = request.data
        request_data.update({
            'mobile': "****" + request.data['mobile'][-4:] if request.data.get('mobile') else None,
            'full_name': request.data['full_name'].split()[-1][0] + "****" + request.data['full_name'].split()[-1][-1] if request.data.get('full_name') else None
        })
        profile_serializer = ProfileSerializer(data=request_data)
        if not profile_serializer.is_valid():
            return Response(profile_serializer.errors, status=400)
        profile = profile_serializer.save(user=user)

        return Response({"profile": profile.user.username})
    

class Login(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful!',
                'response': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }
            })
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        

class PolicyCreateList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"error": "No profile found!"}, status=status.HTTP_401_UNAUTHORIZED)
        request.data.update({'profile': profile.id})
        serializer = PolicySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        policy = serializer.save()
        return Response({'policy': policy.id})
    
    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"error": "No profile found!"}, status=status.HTTP_401_UNAUTHORIZED)
        policies = PolicyDetail.objects.filter(profile=profile)
        serializer = PolicySerializer(policies, many=True)
        return Response({'policies': serializer.data})
    

class PolicyGetUpdateDestroy(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        instance = PolicyDetail.objects.filter(id=pk).first()
        if not instance:
            return Response({"error": "No policy found!"}, status=404)
        serializer = PolicySerializer(instance)
        return Response({'policy': serializer.data})
    
    def put(self, request, pk):
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            return Response({"error": "No profile found!"}, status=status.HTTP_401_UNAUTHORIZED)
        request.data.update({'profile': profile.id})
        instance = PolicyDetail.objects.filter(id=pk).first()
        if not instance:
            return Response({"error": "No policy found!"}, status=404)
        serializer = PolicySerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  
            return Response({
                'policy': pk
            })
        
    def delete(self, request, pk):
        instance = PolicyDetail.objects.filter(id=pk).first()
        if not instance:
            return Response({"error": "No policy found!"}, status=404)
        instance.delete()
        return Response({
            'policy': pk
        })
    

class ProjectedBenefits(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_bonus_rate(self, dob, pt):
        dob = datetime.strptime(dob, "%Y-%m-%d").date()
        today = datetime.now()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 25:
            bonus_rates = [3.5, 4, 4.5, 5, 5.5]
        elif age < 35:
            bonus_rates = [2, 2.5, 3, 3.5]
        else:
            bonus_rates = [0.5, 1, 1.5, 2]
        return [random.choice(bonus_rates) for _ in range(pt)]
    
    def get(self, request, pk):
        instance = PolicyDetail.objects.filter(id=pk).first()
        if not instance:
            return Response({"error": "No policy found!"}, status=404)
        serializer = PolicySerializer(instance)
        data = serializer.data
        dob = data['profile_details']['dob']
        pt = data['pt']
        sum_assured = data['sum_assured']

        bonus_rates = self.get_bonus_rate(dob, pt)
        total_benefit = sum([sum_assured * bonus_rate / 100 for bonus_rate in bonus_rates]) + sum_assured
        return Response({'total_benefits': total_benefit})

