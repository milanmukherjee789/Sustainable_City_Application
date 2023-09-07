from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import TwitterSerializer
from rest_framework import permissions
from .models import Twitter
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import views, status
# Create your views here.
# @api_view(['GET'])
# def apiOverview(request):
#     api_urls = {
#         'List': '/product-list/',
#         'Detail View': '/product-detail/<int:id>/',
#         'Create': '/product-create/',
#         'Update': '/product-update/<int:id>/',
#         'Delete': '/product-detail/<int:id>/',
#     }
#     return Response(api_urls)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def ShowAll(request):
    tweet = Twitter.objects.all()
    serializer = TwitterSerializer(tweet, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addTweet(request):
    # serializer = TwitterSerializer(data=request.data)

    # if serializer.is_valid():
    #     serializer.save()

    # return Response(serializer.data)

    
    try:
        data = JSONParser().parse(request)
        serializer = TwitterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except JSONDecodeError:
        return JsonResponse({"result": "error","message": "Json decoding error"}, status= 400)
