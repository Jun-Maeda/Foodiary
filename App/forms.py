from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import FeelLog, Food


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs[
                'placeholder'] = field.label  # 全てのフォームの部品にplaceholderを定義して、入力フォームにフォーム名が表示されるように指定する


class FeelLogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FeelLogForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FeelLog
        fields = '__all__'
        widgets = {
            'date': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

        # labels = {
        #     'user': 'ユーザー名',
        #     'shop_name': 'お店',
        #     'food': '食ジャンル',
        #     'evaluation': '評価',
        #     'image': '写真',
        #     'comment': 'コメント',
        #     'next_comment': '次回へのコメント'
        # }
        # help_texts = {
        #     'name': '名前を入力',
        #     'age': '年齢を入力'
        # }
