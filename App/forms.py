from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import FeelLog, Food, Area, Place, Shop


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs[
                'placeholder'] = field.label  # 全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する


class FeelLogForm(forms.ModelForm):
    # 登録したメニューにない場合に追加する項目
    add_menu = forms.CharField(label="メニュー追加", required=False)

    def __init__(self, *args, **kwargs):
        super(FeelLogForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FeelLog
        fields = [
            'user',
            'shop_name',
            'food',
            'image',
            'food_menu',
            'add_menu',
            'evaluation',
            'comment',
            'next_comment',
        ]

        widgets = {
            'date': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        # labels = {
        #     'user': forms.TextInput(attrs={'type': 'hidden'},)
        # }
        # help_texts = {
        #     'name': '名前を入力',
        #     'age': '年齢を入力'
        # }


class AreaAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AreaAddForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Area
        fields = '__all__'


class PlaceAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlaceAddForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Place
        fields = '__all__'


class ShopAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShopAddForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Shop
        fields = ['user', 'name', 'place_name', 'menu', 'memo']


class AreaShopAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AreaShopAddForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Shop
        fields = ['user', 'name', 'place_name', 'menu', 'memo']


class FoodAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FoodAddForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Food
        fields = ['user', 'name']
