from django.utils import timezone
from django.shortcuts import render
from order.models import Shop, Menu, Order, Orderfood
from order.serializer import ShopSerializer, MenuSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser


# Shop객체들을 다 serialize한 결과를 json으로 parsing해서 json형태로 이를 반응하겠다
@csrf_exempt
def shop(request):
    if request.method == 'GET':
        # shop = Shop.objects.all()
        # serializer = ShopSerializer(shop, many=True)
        # return JsonResponse(serializer.data, safe=False)

        shop = Shop.objects.all()
        return render(request, 'order/shop_list.html', {'shop_list': shop})

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def menu(request, shop):
    if request.method == 'GET':
        # get으로 하게 되면 menu1개 밖에 불러오지 못하게 된다.
        # 모든 menu를 불러오고 싶을 떄는 배열로서 filter를 사용해 주면 된다.
        menu = Menu.objects.filter(shop=shop)
        # many=True는 값이 여러개여도 상관하지 않겠다는 의미이다.

        # serializer = MenuSerializer(menu, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return render(request, 'order/menu_list.html', {'menu_list': menu, 'shop': shop})

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def order(request):
    if request.method == 'POST':
        address = request.POST['address']
        shop = request.POST['shop']
        food_list = request.POST.getlist('menu')
        order_date = timezone.now()

        shop_item = Shop.objects.get(pk=int(shop))
        shop_item.order_set.create(
            order_date=order_date, address=address, shop=int(shop))
        
        shop_item.save()
        order_item = Order.objects.get(
            pk=int(shop_item.order_set.latest('id').id))
        
        for food in food_list:
            order_item.orderfood_set.create(food_name=food)

        return render(request, 'order/success.html')
    elif request.method == 'GET':
        order_list = Order.objects.all()
        return render(request, 'order/order_list.html', {'order_list': order_list})
