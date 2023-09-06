from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from .cab_map import getCab
from .tweet import main_tweet
from django.http import HttpResponse
from .clustercab import cluster
from .get_traffic import get_cars
from .predict_dublinbikes import pred_bikes
import json



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def Tweet(request):
    #Return the tweet geojson 
    try:
        return Response(main_tweet())
    except JSONDecodeError:
        return JsonResponse({"result": "error","message": "Error has occured in Tweet"}, status= 400)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def showGeoJson(request):
    #Retuen geojson for simulated cab
    cab = getCab()
    return JsonResponse(cab)



@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def returnTraffic(request,id):
    #Return the Traffic prediction
    try:
        return Response(json.loads(get_cars(id)))

    except JSONDecodeError:
        return JsonResponse({"result": "error","message": "Error has occured in return TRaffic"}, status= 400)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def predictionDublinBikes(request,id):
    #Return the Bike prediction
    try:

        return Response(pred_bikes(id))

    except JSONDecodeError:
        return JsonResponse({"result": "error","message": "Error has occured in erturn TRaffic"}, status= 400)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def returnClusterCab(request):
    #Return the clustering information
    try:
        taxi = request.data
        return Response(cluster(taxi))
    except Exception as e:
        return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
