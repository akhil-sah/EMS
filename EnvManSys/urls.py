"""EnvManSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from my_app import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
#    path('my_app/',include('my_app.urls')),
    path('', views.index_view, name = 'index'),
#    path('survey_data/<int:survey_id>/',views.survey_data_view, name = 'survey_data'),

    path('password_reset/',auth_views.PasswordResetView.as_view(),name = 'password_reset'),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register'),
    path('edit/',views.edit_view, name = 'edit'),
    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),
    path('home/', views.home_view, name = 'home'),

#    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),
#    path('profile/',views.profile_view, name='profile'),
#    path('password_change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
#    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(),name = 'password_change_done'),
 
    #PasswordReset
#    path('password_reset/',auth_views.PasswordResetView.as_view(),name = 'password_reset'),
#    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name = 'password_reset_done'),
#    path('reset/uidb64/<token>/',auth_views.PasswordResetConfirmView.as_view(),name = 'password_reset_confirm'),
#    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name = 'password_reset_complete'),
]
