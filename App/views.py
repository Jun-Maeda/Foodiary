from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm, FeelLogForm, AreaAddForm, PlaceAddForm, ShopAddForm, FoodAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Food, Area, Place, Shop, FeelLog, User, Food_menu
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse


# お店の平均を計算してオーバーライドする
def shop_ave(shop_id):
    all_ev = FeelLog.objects.filter(shop_name_id=shop_id)
    q = len(all_ev)
    al_av = 0
    # 評価をすべて合計
    for a in all_ev:
        al_av += a.evaluation
    # 評価の合計をすべての記事数で割る
    av = al_av / q

    now = Shop.objects.get(id=shop_id)
    now.average = round(av, 2)
    now.time = q
    now.save()


class HomeView(LoginRequiredMixin, generic.TemplateView):
    # トップページ
    template_name = 'Foodiary/top.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        shop_time = Shop.objects.filter(user=self.request.user).order_by('time')[:3]
        shop_a = Shop.objects.filter(user=self.request.user).order_by('average')[:3]

        context = super().get_context_data()
        context['area'] = Area.objects.filter(user=self.request.user)
        context['food'] = Food.objects.filter(user=self.request.user)
        context['shop_time'] = shop_time
        context['shop_a'] = shop_a
        return context


# エリアごとの場所一覧
class PlaceList(generic.TemplateView):
    template_name = 'Foodiary/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area_n = Area.objects.get(pk=self.kwargs['pk'])
        data_list = Place.objects.filter(area_name=area_n,
                                         user=self.request.user)  # pkを指定してデータを絞り込む
        context['data_list'] = data_list
        context['title'] = "場所"
        context['url_name'] = "App:shop_list"
        context['add_place'] = area_n
        return context


# 場所ごとのお店一覧
class ShopList(generic.TemplateView):
    template_name = 'Foodiary/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        place_n = Place.objects.get(pk=self.kwargs['pk'])
        data_list = Shop.objects.filter(place_name=place_n,
                                        user=self.request.user)  # pkを指定してデータを絞り込む
        context['data_list'] = data_list
        context['title'] = "店舗"
        context['url_name'] = "App:shop_detail"
        context['add'] = place_n
        return context


# お店の詳細
class ShopDetail(generic.DetailView):
    model = Shop
    template_name = 'Foodiary/detail.html'
    context_object_name = 'ob_name'

    def get_context_data(self, **kwargs):
        context = super(ShopDetail, self).get_context_data(**kwargs)
        # 登録されているメニューを表示
        menus = Food_menu.objects.filter(shop_id=self.kwargs['pk'])
        context['menus'] = menus
        return context


# お店ごとの日記一覧
class ShopDiary(generic.TemplateView):
    template_name = 'Foodiary/list.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop_n = Shop.objects.get(pk=self.kwargs['pk'])
        data_list = FeelLog.objects.filter(shop_name=shop_n, user=self.request.user).order_by(
            'date').reverse()  # pkを指定してデータを絞り込む
        paginator = Paginator(data_list, 15)
        p = self.request.GET.get('p')
        articles = paginator.get_page(p)
        context['data_list'] = articles
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


# 全ての日記一覧
class AllDiarys(generic.ListView):
    model = FeelLog
    template_name = 'Foodiary/list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data_list = FeelLog.objects.filter(user=self.request.user).order_by('date').reverse()
        paginator = Paginator(data_list, 15)
        p = self.request.GET.get('p')
        articles = paginator.get_page(p)
        context['data_list'] = articles
        context['title'] = f"日記一覧"
        context['url_name'] = "App:diary_detail"
        return context


# カテゴリごとのお店一覧
class FoodShopList(generic.TemplateView):
    template_name = 'Foodiary/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        food_n = Food.objects.get(pk=self.kwargs['pk'])  # pkを指定してデータを絞り込む
        data_list = food_n.shops.all
        context['data_list'] = data_list
        context['title'] = "店舗"
        context['url_name'] = "App:shop_detail"
        context['check'] = False
        return context


# 評価フォームのビュー
class FeelLogView(generic.CreateView):
    model = FeelLog
    form_class = FeelLogForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        # formからショップ情報を取得
        shop_id = self.request.POST['shop_name']
        # 上で作成した関数を実行して平均を計算して保存
        shop_ave(shop_id)
        # メッセージ表記
        messages.success(self.request, '投稿しました')
        return reverse_lazy('App:all_feel_log')

    def form_valid(self, form):
        # 画像があれば変換して保存
        if self.request.FILES['image']:
            form.cleaned_data['image'] = self.request.FILES['image']
        # オーバーライドして、もし追加のメニューがあれば登録してリレーション
        form = form.save(commit=False, )
        new_menu = self.request.POST['add_menu']
        if new_menu != "":
            menu = Food_menu.objects.create(
                name=new_menu,
                shop=form.shop_name,
                food=form.food,
            )
            form.food_menu = menu

        return super(FeelLogView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # ログインユーザー取得
        login_user = self.request.user
        context = super().get_context_data(**kwargs)
        # それぞれの項目をユーザーが登録したもののみ取得
        context['form'].fields['food'].queryset = Food.objects.filter(user__username=login_user)
        context['form'].fields['shop_name'].queryset = Shop.objects.filter(
            user__username=login_user)
        context['check'] = True
        return context


# お店指定の評価フォームのビュー
class ShopFeelLogView(generic.CreateView):
    model = FeelLog
    form_class = FeelLogForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        # formからショップ情報を取得
        shop_id = self.request.POST['shop_name']
        # 上で作成した関数を実行して記事数と平均を計算して保存
        shop_ave(shop_id)
        # メッセージ表記
        messages.success(self.request, '投稿しました')
        return reverse_lazy('App:shop_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        # 画像があれば変換して保存
        if self.request.FILES['image']:
            form.cleaned_data['image'] = self.request.FILES['image']
        # オーバーライドして、もし追加のメニューがあれば登録してリレーション
        form = form.save(commit=False, )
        new_menu = self.request.POST['add_menu']
        if new_menu != "":
            menu = Food_menu.objects.create(
                name=new_menu,
                shop=form.shop_name,
                food=form.food,
            )
            form.food_menu = menu

        return super(ShopFeelLogView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # ログインユーザー取得
        login_user = self.request.user
        context = super().get_context_data(**kwargs)
        # それぞれの項目をユーザーが登録したもののみ取得
        context['form'].fields['food'].queryset = Food.objects.filter(user__username=login_user)
        context['form'].fields['shop_name'].queryset = Shop.objects.filter(
            pk=self.kwargs['pk'])
        context['form'].fields['food_menu'].queryset = Food_menu.objects.filter(
            shop_id=self.kwargs['pk'])
        return context


# 都道府県の追加フォーム
class AreaAddView(generic.CreateView):
    model = Area
    form_class = AreaAddForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        messages.success(self.request, '追加しました')
        return reverse_lazy('App:area_add')

    def form_valid(self, form):
        form = form.save(commit=False, )
        return super(AreaAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# 場所の追加フォーム
class PlaceAddView(generic.CreateView):
    model = Place
    form_class = PlaceAddForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        messages.success(self.request, '追加しました')
        return reverse_lazy('App:place_add')

    def form_valid(self, form):
        form = form.save(commit=False, )
        return super(PlaceAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['area_name'].queryset = Area.objects.filter(user=self.request.user)
        return context


# エリア指定の場所の追加フォーム
class AleaPlaceAddView(generic.CreateView):
    model = Place
    form_class = PlaceAddForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        messages.success(self.request, '追加しました')
        return reverse_lazy('App:place_add')

    def form_valid(self, form):
        form = form.save(commit=False, )
        return super(AleaPlaceAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['area_name'].queryset = Area.objects.filter(pk=self.kwargs['pk'])
        return context


# お店の追加フォーム
class ShopAddView(generic.CreateView):
    model = Shop
    form_class = ShopAddForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        messages.success(self.request, '追加しました')
        return reverse_lazy('App:shop_add')

    def form_valid(self, form):
        if self.request.FILES['menu']:
            form.cleaned_data['menu'] = self.request.FILES['menu']
        form = form.save(commit=False, )
        return super(ShopAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['place_name'].queryset = Place.objects.filter(user=self.request.user)
        return context


# 場所ごとのお店の追加フォーム
class AreaShopAddView(generic.CreateView):
    model = Shop
    form_class = ShopAddForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        messages.success(self.request, '追加しました')
        return reverse_lazy('App:shop_add')

    def form_valid(self, form):
        # 画像ファイルを指定し直して保存
        if self.request.FILES['menu']:
            form.cleaned_data['menu'] = self.request.FILES['menu']
        form = form.save(commit=False, )
        return super(AreaShopAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['place_name'].queryset = Place.objects.filter(pk=self.kwargs['pk'])
        return context


# ジャンルの追加フォーム
class FoodAddView(generic.CreateView):
    model = Food
    form_class = FoodAddForm
    template_name = 'Foodiary/form.html'

    def get_success_url(self):
        messages.success(self.request, '追加しました')
        return reverse_lazy('App:food_add')

    def form_valid(self, form):
        form = form.save(commit=False, )
        return super(FoodAddView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DiaryUpdateView(generic.UpdateView):
    model = FeelLog
    template_name = 'Foodiary/form.html'
    fields = '__all__'

    def get_success_url(self):
        messages.success(self.request, '更新しました。')
        return reverse('App:diary_detail', kwargs={'pk': self.object.pk})


class ShopUpdateView(generic.UpdateView):
    model = Shop
    template_name = 'Foodiary/form.html'
    fields = ['name', 'place_name', 'menu', 'memo', 'last_history']

    def get_success_url(self):
        messages.success(self.request, '更新しました。')
        return reverse('App:shop_detail', kwargs={'pk': self.object.pk})


# ユーザーページ
class UserPage(generic.TemplateView):
    template_name = 'Foodiary/user.html'
