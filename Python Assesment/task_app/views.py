from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from .utils import *
from .models import *
from .serializers import *
from .enums import *
from django.db.models import Q


class TaskAPI(APIView):
    def post(self, request):
        try:
            data = request.data

            task_serializer = TaskSerializer(data=data)

            if task_serializer.is_valid():
                task_serializer.save()
                payload = Common.create_payload(True, "Task Added Sucessfully","", None)
                return JsonResponse(payload, status=status.HTTP_200_OK)
            else:
                payload = Common.create_payload(False, "Some error occurred", "", task_serializer.errors)
                return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            payload = Common.create_payload(False, "Some error occurred.", str(e), None)
            return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):

        try:
            data = request.GET

            pending_task = data.get('pending_task')
            completed_task = data.get('completed_task')
            search = data.get('search')
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 10))


            if pending_task:
                if search:
                    tasks = Task.objects.filter(status=task_state.Pending.value, description__icontains=search)[limit*(page-1) : limit*(page)]
                else:
                    tasks = Task.objects.filter(status=task_state.Pending.value).all()[limit*(page-1) : limit*(page)]
            
            elif completed_task:
                if search:
                    tasks = Task.objects.filter(status=task_state.Completed.value, description__icontains=search)[limit*(page-1) : limit*(page)]
                else:
                    tasks = Task.objects.filter(status=task_state.Completed.value).all()[limit*(page-1) : limit*(page)]
            
            else:
                if search:
                    tasks = Task.objects.filter(description__icontains=search)[limit*(page-1) : limit*(page)]
                else:
                    tasks = Task.objects.all()[limit*(page-1) : limit*(page)]
            
            task_serializer = TaskSerializer(tasks,many=True)
            payload = Common.create_payload(True, "Task List", "", task_serializer.data)
            return JsonResponse(payload, status=status.HTTP_200_OK)

        except Exception as e:
            
            payload = Common.create_payload(False, "Some error occurred.", str(e), None)
            return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        try:
            data = request.data

            task_id = data.get('task_id',None)

            if task_id is None:
                payload = Common.create_payload(False, "Task ID is required", "Task ID is required", None)
                return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)

            task = Task.objects.get(task_id=task_id)

            task_serializer = TaskSerializer(instance=task, data=data, partial=True)

           

            if task_serializer.is_valid():
                task_serializer.save()
                payload = Common.create_payload(True, "Task Updated", "", None)
                return JsonResponse(payload, status=status.HTTP_200_OK)
            else:
                payload = Common.create_payload(False, "Some error occurred", "", task_serializer.errors)
                return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)
        
        except Task.DoesNotExist:
                payload = Common.create_payload(False,"Task Does Not Exsist","Task Does Not Exsist", None)
                return JsonResponse(payload, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            
            payload = Common.create_payload(False, "Some error occurred.", str(e), None)
            return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            data = request.data
            task_id = data.get('task_id', None)

            if task_id is None:
                payload = Common.create_payload(False, "Task ID is required", "Task ID is required", None)
                return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)

            
            task = Task.objects.get(id=task_id)
            

            task.delete()
            payload = Common.create_payload(True, "Task Deleted", "", None)
            return JsonResponse(payload, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            payload = Common.create_payload(False,"Task Does Not Exsist","Task Does Not Exsist", None)
            return JsonResponse(payload, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            payload = {"success": False, "message": "An error occurred", "error": str(e)}
            return JsonResponse(payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


            



        
            


