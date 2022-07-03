from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from user.serializers import UserSerailizer
from user.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

# Shop객체들을 다 serialize한 결과를 json으로 parsing해서 json형태로 이를 반응하겠다


@csrf_exempt
def user(request):
    if request.method == 'GET':
        shop = User.objects.all()
        return render(request, 'user/user_list.html', {'user_list': shop})
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerailizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        try:
            request.session['user_id'] = User.objects.all().get(user_name=name).id
            print(request.session['user_id'])
            return render(request, 'user/success.html')
        except:
            return render(request, 'user/fail.html')

    elif request.method == 'GET':
        return render(request, 'user/login.html')
