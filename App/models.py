from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Area(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='都道府県名',
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー名',
        on_delete=models.CASCADE,
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
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー名',
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
    menu = models.ImageField(
        verbose_name='メニュー写真',
        blank=True, null=True,
    )
    memo = models.TextField(
        max_length=500,
        verbose_name="おすすめや注意",
    )
    last_history = models.TextField(
        max_length=500,
        verbose_name="前回からのコメント",
        blank=True, null=True,
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー名',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='ジャンル',
    )
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー名',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class FeelLog(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='ユーザー名',
        on_delete=models.CASCADE,
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
        default=timezone.now,
        verbose_name='日付'
    )

    next_comment = models.TextField(
        verbose_name='次回へのコメント',
        max_length=500,
        blank=True, null=True,
    )

    def save(self, *args, **kwargs):
        feel_shop = Shop.objects.get(pk=self.shop_name.pk)

        # 次回へのコメントがあれば更新
        if len(self.next_comment):
            feel_shop.last_history = self.next_comment
            feel_shop.save()

        super(FeelLog, self).save()
