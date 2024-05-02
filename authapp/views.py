from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from authapp.serializers import LeadSerializer, UserSerializer, TaskSerializer
from django.contrib.auth import authenticate
from authapp.models import CustomUser, Lead, Task
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from datetime import date


class SignUpViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response({"message": "This is the signup page."})

class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        username_or_email = request.data.get('username_or_email')
        password = request.data.get('password')

        user = authenticate(request, username=username_or_email, password=password)
        
        if user is None:
            try:
                user = CustomUser.objects.get(email=username_or_email)             
                user = authenticate(request, username=user.username, password=password)
               
            except CustomUser.DoesNotExist:
                pass

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),   
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username / email or password'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        return Response({"message": "This is the login page."})

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error_message = {'message': 'User update failed', 'errors': serializer.errors}
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# class lead
class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return Lead.objects.filter(status=status)
        return Lead.objects.all()

    def retrieve(self, request, *args, **kwargs):
        name = kwargs.get('name')
        try:
            lead = Lead.objects.get(name=name)
            serializer = self.get_serializer(lead)
            return Response(serializer.data)
        except Lead.DoesNotExist:
            return Response({'error': 'Lead does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({'message': 'Lead has been successfully added.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'message': 'Lead has been successfully updated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({'message': 'Lead has been partially updated.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Lead has been successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
    
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response({'message': 'Task has been successfully added.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)
        total_leads = Lead.objects.count()
        total_tasks = Task.objects.count()
        today_tasks = Task.objects.filter(from_date=date.today())
        today_tasks_serializer = TaskSerializer(today_tasks, many=True)
        all_tasks = Task.objects.all()
        all_tasks_serializer = TaskSerializer(all_tasks, many=True)

        response_data = {
            'userName': user.username,
            'totalLeads': total_leads,
            'totalTasks': total_tasks,
            'todayTasks': today_tasks_serializer.data,
            'allTasks': all_tasks_serializer.data,
        }
        print(response_data)
        return Response(response_data, status=status.HTTP_200_OK)
