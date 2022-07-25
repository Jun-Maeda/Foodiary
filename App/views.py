from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm, FeelLogForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Food, Area, Place, Shop, FeelLog
from django.contrib.auth.models import User


class HomeView(LoginRequiredMixin, generic.TemplateView):
    # トップページ
    template_name = 'Foodiary/top.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['area'] = Area.objects.all()
        context['food'] = Food.objects.all()
        return context


# エリアごとの場所一覧
class PlaceList(generic.TemplateView):
    template_name = 'Foodiary/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area_n = Area.objects.get(pk=self.kwargs['pk'])
        data_list = Place.objects.filter(area_name=area_n)  # pkを指定してデータを絞り込む
        context['data_list'] = data_list
        context['title'] = "場所"
        context['url_name'] = "App:shop_list"
        return context


# 場所ごとのお店一覧
class ShopList(generic.TemplateView):
    template_name = 'Foodiary/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_n = Place.objects.get(pk=self.kwargs['pk'])
        data_list = Shop.objects.filter(place_name=place_n)  # pkを指定してデータを絞り込む
        context['data_list'] = data_list
        context['title'] = "店舗"
        context['url_name'] = "App:shop_detail"
        return context


# お店の詳細
class ShopDetail(generic.DetailView):
    model = Shop
    template_name = 'Foodiary/detail.html'
    context_object_name = 'ob_name'


# お店ごとの日記一覧
class ShopDiary(generic.TemplateView):
    template_name = 'Foodiary/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop_n = Shop.objects.get(pk=self.kwargs['pk'])
        data_list = FeelLog.objects.filter(shop_name=shop_n).order_by(
            'date').reverse()  # pkを指定してデータを絞り込む
        context['data_list'] = data_list
        context['title'] = f"{shop_n.name}の日記"
        context['url_name'] = "App:diary_detail"
        return context


# 日記の内容
class DiaryDetail(generic.DetailView):
    model = FeelLog
    template_name = 'Foodiary/log_detail.html'


class Login(LoginView):
    """ログインページ"""
    template_name = 'Foodiary/login.html'
    form_class = LoginForm


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = "Foodiary/login.html"


class AllDiarys(generic.ListView):
    model = FeelLog
    template_name = 'Foodiary/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = FeelLog.objects.all().order_by('date').reverse()
        context['data_list'] = data_list
        context['title'] = f"日記一覧"
        context['url_name'] = "App:diary_detail"
        return context


# 評価フォームのビュー
class FeelLogView(generic.CreateView):
    model = FeelLog
    form_class = FeelLogForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        return reverse_lazy('App:feel_log')

    def form_valid(self, form):
        form = form.save(commit=False, )
        return super(FeelLogView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # ログインユーザー取得
        login_user = self.request.user
        context = super().get_context_data(**kwargs)
        # それぞれの項目をユーザーが登録したもののみ取得
        context['form'].fields['food'].queryset = Food.objects.filter(user__username=login_user)
        context['form'].fields['shop_name'].queryset = Shop.objects.filter(
            user__username=login_user)
        return context


# ユーザーページ
class UserPage(generic.TemplateView):
    template_name = 'Foodiary/user.html'
