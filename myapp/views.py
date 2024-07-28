import json
import os
from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View


def trigger_node_event(request):
    data = {'data': 'example data'}
    response = requests.post(f'{os.environ["NODE_JS_API_URL"]}/triggerEventFromDjango', json=data)
    return JsonResponse(response.json())


@method_decorator(csrf_exempt, name='dispatch')
class SendMessageView(View):
    def post(self, request, *args, **kwargs):
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Define the URL of your Node.js server
        node_url = f'{os.environ["NODE_JS_API_URL"]}/send-message'
        
        # Forward the request data to the Node.js server
        try:
            response = requests.post(node_url, json=data)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class ReceiveMessageView(View):
    def post(self, request, *args, **kwargs):
        node_url = f'{os.environ["NODE_JS_API_URL"]}/receive-message'
        try:
            response = requests.post(node_url, json=request.data)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

 
@method_decorator(csrf_exempt, name='dispatch')
class FileUploadStatusView(View):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')  # Get the uploaded file

        # Notify Node.js about the file upload
        node_url = f'{os.environ["NODE_JS_API_URL"]}/file-upload-status'
        try:
            response = requests.post(node_url, json={'file_name': file.name})
            return JsonResponse(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)


def send_message(request):
    if request.method == 'GET':
        context = {
            'node_js_api_url': os.environ["NODE_JS_API_URL"]
        }
        # Render the HTML page
        return render(request, "myapp/test1.html", context)
    
    if request.method == 'POST':
        # Parse JSON data from request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # Define the URL of your Node.js server
        node_url = f'{os.environ["NODE_JS_API_URL"]}/send-message'
        
        # Forward the request data to the Node.js server
        try:
            response = requests.post(node_url, json=data)
            return JsonResponse(response.json(), status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    return JsonResponse({'error': 'Invalid method'}, status=405)
