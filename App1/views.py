from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import urljoin
from .models import DataModel
from .serializers import DataSerializer
from .forms import DataForm

def home(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data_to_save = form.cleaned_data['data']
            data_object = DataModel.objects.create(data=data_to_save)
            print("Data object:", data_object)
    else:
        form = DataForm()
    return render(request, 'callback_data.html', {'form': form})

@api_view(['POST'])
def callback_view(request):
    serializer = DataSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data['data']
        callback_url_relative = reverse('callback_listener')
        base_url = request.build_absolute_uri('/')
        callback_url_absolute = urljoin(base_url, callback_url_relative)
        DataModel.objects.create(data=data)
        response_data = {
            'message': "Data Triggered successfully",
            'callback_url': callback_url_absolute
        }
        return Response(response_data)
    else:
        return Response(serializer.errors, status=400)


def callback_listener_view(request):
    data_from_callback = DataModel.objects.all()
    serializer = DataSerializer(data_from_callback, many=True)

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(serializer.data, safe=False)
    else:
        return render(request, 'receive_data.html', {'data_from_callback': serializer.data})


# @api_view(['POST'])
# @authentication_classes([TokenAuthentication]) 
# @permission_classes([IsAuthenticated])  
# def webhook_callback(request):
#     submission_data = {
#         "submission_id": 123,
#         "test_result": "passed",
#         "timestamp": "2023-08-04T12:34:56"
#     }
#     response_data = {
#         "message": "Webhook received successfully.",
#         "submission_data": submission_data
#     }
#     return Response(response_data, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def callback_listener_view(request):
#     data_from_callback = DataModel.objects.all()
#     serializer = DataSerializer(data_from_callback, many=True)
#     return render(request,'receive_data.html', 'data_from_callback': serializer.data)
#     # return Response({'message': 'Data received and saved successfully', 'data_from_callback': serializer.data})
