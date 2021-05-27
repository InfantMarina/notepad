from django.contrib import admin
from django.urls import path, include, re_path
from notepad import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required

app_name="notepad"


# router = DefaultRouter()
# router.register('storages', views.StorageMViewset)

urlpatterns = [
    # re_path('^', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path('login', views.login_view, name="login"),
    re_path('^logout/', views.logout_view, name="logout"),
    re_path('^index/(?P<user_id>[0-9]{1,4})?/?(?P<action>(create|delete|edit))?/?$', views.Index.as_view(), name='index')
]