from django.db import models
from django.utils import timezone


class Area(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='都道府県名',
    )

    def __str__(self):
        return self.name


class Place(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='場所',
    )
    area_name = models.ForeignKey(
        Area,
        verbose_name='都道府県名',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='店舗名',
    )
    place_name = models.ForeignKey(
        Place,
        verbose_name='場所',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='ジャンル',
    )

    def __str__(self):
        return self.name


class FeelLog(models.Model):
    user = models.CharField(
        max_length=50,
        verbose_name='ユーザー名',
    )
    food = models.ForeignKey(
        Food,
        verbose_name='食ジャンル',
        on_delete=models.CASCADE,
    )
    shop_name = models.ForeignKey(
        Shop,
        verbose_name='お店',
        on_delete=models.CASCADE,
    )
    list = [
        (1, "☆"),
        (2, "☆☆"),
        (3, "☆☆☆"),
        (4, "☆☆☆☆"),
        (5, "☆☆☆☆☆")
    ]
    evaluation = models.IntegerField(
        choices=list,
        verbose_name='評価',
    )
    comment = models.TextField(
        verbose_name='コメント',
        max_length=500,
        blank=True, null=True,
    )
    image = models.ImageField(
        verbose_name='画像',
        blank=True, null=True,
    )

    date = models.DateTimeField(
        default=timezone.now(),
        verbose_name='日付'
    )
