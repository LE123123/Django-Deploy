from django.db import models

# pk는 자동으로 생성된다.


class Shop(models.Model):
    shop_name = models.CharField(max_length=20)
    shop_address = models.CharField(max_length=40)

# 이렇게 하면 Menu에는 1번 sho에 해당하는 많은 음식 메뉴들이 있을 것이다.


class Menu(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=20)


class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order_date = models.DateTimeField('date ordered')
    address = models.CharField(max_length=40)

    # 일단 estimated_time의 defualt값은 -1인데 가게 사장님이 예상 소요시간을 입력하지 않았기 때문
    estimated_time = models.IntegerField(default=-1)
    deliver_finish = models.BooleanField(default=0)


class Orderfood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=20)
