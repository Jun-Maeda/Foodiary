from django.urls import path, include
from . import views
from django.urls import path

app_name = 'App'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.Login.as_view(), name="login"),
    path('login/', views.Logout.as_view(), name="logout"),
    path('place/<int:pk>/', views.PlaceList.as_view(), name='place_list'),
    path('shop/<int:pk>/', views.ShopList.as_view(), name='shop_list'),
    path('shop_detail/<int:pk>/', views.ShopDetail.as_view(), name='shop_detail'),
    path('shop_diary/<int:pk>/', views.ShopDiary.as_view(), name='shop_diary'),
    path('diary/<int:pk>/', views.DiaryDetail.as_view(), name='diary_detail'),
    path('alldiarys/', views.AllDiarys.as_view(), name='all_diary'),
    path('feellog/', views.FeelLogView.as_view(), name='all_feel_log'),
    path('feellog/<int:pk>', views.ShopFeelLogView.as_view(), name='feel_log'),
    path('userpage/', views.UserPage.as_view(), name='user_page'),
    path('food_cat/<int:pk>/', views.FoodShopList.as_view(), name='food_cat'),
    path('add_area', views.AreaAddView.as_view(), name='area_add'),
    path('add_place', views.PlaceAddView.as_view(), name='place_add'),
    path('add_shop', views.ShopAddView.as_view(), name='shop_add'),
    path('add_food', views.FoodAddView.as_view(), name='food_add'),
    path('update_feellog/<int:pk>/', views.DiaryUpdateView.as_view(), name='update_log'),
    path('update_shop/<int:pk>/', views.ShopUpdateView.as_view(), name='update_shop'),
]
