from . import models
from . import serializers
from . import utils
from django.http.response import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
import os
from dotenv import load_dotenv
from rest_framework.response import Response
from loguru import logger
import requests

dotenv_path = 'PATH/TO/.ENV'
load_dotenv(dotenv_path=dotenv_path)
logger.add(sink='debug.log', format="{time} - {level} - {message}", filter=__name__, level="DEBUG", rotation='100 MB', compression='zip')

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def fetch_and_display_data(request):
    counter = 0
    isNotOver = True
    while isNotOver:
        API_URL = f'YOUR_API_FROM_WHERE_YOU_TAKE_INFORMATION'
        HEADERS = {
            'Authorization': f'Bearer {os.getenv("API_TOKEN")}'
        }
        response = requests.get(url=API_URL, headers=HEADERS)
        data = response.json()
        utils.save_data_to_model(data=data)
        counter += 1
        if len(data['orders']) != 10:
            isNotOver = False

    order_with_products = models.Order.objects.all()

    serializer = serializers.OrderSerializer(data=order_with_products, many=True)
    serializer.is_valid()
    
    return JsonResponse({'orders': serializer.data}, safe=False)

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def courier_list(request):

    if request.method == 'GET':
        logger.debug('Request GET courier-list | GET all couriers')
        couriers = models.Courier.objects.all()
        serializer = serializers.CourierSerializer(couriers, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        logger.debug('Request POST courier-list | Create new courier')
        serializer = serializers.CourierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def courier_detail(request, telegram_id):

    try:
        courier = models.Courier.objects.get(telegram_id=telegram_id)
    except models.Courier.DoesNotExist:
        logger.warning('models.Courier Does Not Exist, Invalid credentials or user doesn\'t have an account')
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        logger.debug('Request GET courier-detail | GET courier telegram_id based')
        serializer = serializers.CourierSerializer(courier)
        return JsonResponse(serializer.data)
    
    if request.method == 'PUT':
        logger.debug('Request PUT courier-detail | Change models.Courier information')
        serializer = serializers.CourierSerializer(courier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        logger.debug('Request DELETE courier-detail | DELETE models.Courier')
        courier.delete()
        serializer = serializers.CourierSerializer(courier)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def order_list(request):

    if request.method == 'GET':
        logger.debug('Request GET order-list | GET all orders')
        orders = models.Order.objects.all()
        serializer = serializers.OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data)
    
    if request.method == 'POST':
        logger.debug('Request POST order-list | Create new order')
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_available_orders(request):
    if request.method == 'GET':
        logger.debug('Request GET available orders | GET orders that active and have no couriers')
        orders = models.Order.objects.filter(active=1).filter(courier=None)
        serializer = serializers.OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_available_orders(request, page):

    start = 0 + page*3
    end = 3 + page*3
    if request.method == 'GET':
        logger.debug('Request GET available orders | GET orders that active and have no couriers')
        orders = models.Order.objects.filter(active=1).filter(courier=None)[start:end]
        serializer = serializers.OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_my_active(request, telegram_id):

    try:
        courier_obj = models.Courier.objects.get(telegram_id=telegram_id)
    except models.Courier.DoesNotExist:
        logger.warning('models.Courier Does Not Exist, Invalid credentials or user doesn\'t have an account')
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        logger.debug('Request GET get_my_active | GET my active orders')
        orders = models.Order.objects.filter(courier=courier_obj.pk).filter(active=True)
        serializer = serializers.OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_my_history(request, telegram_id):

    try:
        courier_obj = models.Courier.objects.get(telegram_id=telegram_id)
    except models.Courier.DoesNotExist:
        logger.warning('models.Courier Does Not Exist, Invalid credentials or user doesn\'t have an account')
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        logger.debug('Request GET get_my_history | GET courier\'s history of finished orders')
        orders = models.Order.objects.filter(courier=courier_obj.pk).filter(active=False)

        if len(orders) < 5:
            serializer = serializers.OrderSerializer(orders, many=True)
        else:
            serializer = serializers.OrderSerializer(orders[:5], many=True)
        
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET','PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request, id):
    
    try:
        order = models.Order.objects.get(pk=id)
    except models.Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = serializers.OrderSerializer(order)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = serializers.OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        order.delete()
        serializer = serializers.OrderSerializer(order)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def assign_courier_to_order(request):

    telegram_id = request.data.get('telegram_id')
    order_id = request.data.get('order_id')

    try:
        courier = models.Courier.objects.get(telegram_id=int(telegram_id))
    except models.Courier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        order = models.Order.objects.get(pk=int(order_id))
    except models.Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        if order.courier is None:
            order.courier = courier
            order.save()
            serializer = serializers.OrderSerializer(order)
            return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_courier_from_order(request):

    order_id = request.data.get('order_id')

    try:
        order = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        if order.courier is not None:
            order.courier = None
            order.save()
    
    serializer = serializers.OrderSerializer(order)
    return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def finish_delivery(request):

    order_id = request.data.get('order_id')

    try:
        order = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        logger.debug(f'Request PUT finish_delivery | Order of ID:{order_id} is finished')
        if order.active == True:
            order.active = False
            order.save()

    serializer = serializers.OrderSerializer(order)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_orders_product_set(request, order_id):

    try:
        order = models.Order.objects.get(pk=order_id)
    except models.Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        logger.debug(f'Request GET get_orders_product_set | Requested Order: {order_id}')
        product_sets = order.products
        serializer = serializers.ProductSetSerializer(product_sets, many=True)
        return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_product(request, product_id):

    try:
        product = models.Product.objects.get(pk=product_id)
    except models.Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        logger.debug(f'Request GET get_product | Requested Product: {product_id}')
        serializer = serializers.ProductSerializer(product)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_branches(request):

    if request.method == 'GET':
        logger.debug('Request GET get_branches | GET all branches')
        branches = models.Branch.objects.all()
        serializer = serializers.BranchSerializer(branches, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == 'POST':
        logger.debug('Request POST get_branches | Added new branch')
        serializer = serializers.BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
