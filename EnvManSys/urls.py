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


    path('', views.index_view, name = 'index'),
    path('permissible_emissions/', views.permissible_emissions_view, name = 'permissible_emissions'),
    path('profile/',views.edit_view, name = 'profile'),
    path('home/', views.home_view, name = 'home'),

    #Viewer's urls
    path('lodge_complaint/', views.lodge_complaint_view, name = 'lodge_complaint'),
    path('lodge_complaint/<int:id>', views.complaint_lodged_view, name = 'complaint_lodged'),
    path('track_complaint/', views.track_complaint_view, name = 'track_complaint'),

    # Supervisor's urls
    path('select_session/', views.select_session_page, name = 'select_session'),
    path('enter_emissions/<int:session_id>', views.enter_emissions_page, name = 'enter_emissions'),

    # Surveyer's urls
    path('surveys/', views.surveys_view, name = 'surveys'),
    path('new_survey/', views.new_survey_view, name = 'new_survey'),
    path('surveys/<int:survey_id>/survey_form/', views.survey_form_view, name = 'survey_form'),

    # Auditor's urls
    path('audit_complaints/', views.audit_complaints_view, name = 'audit_complaints'),
    path('audit_complaints/<int:complaint_id>', views.complaint_feedback_view, name = 'complaint_feedback'),
    path('audit_surveys/', views.audit_surveys_view, name = 'audit_surveys'),
    path('audit_surveys/<int:survey_id>/survey_response/<int:response_id>', views.survey_response_view, name = 'survey_response'),
    path('audit_emissions/', views.audit_emissions_view, name = 'audit_emissions'),
    path('audit_emissions/<int:session_id>/update', views.update_emissions_view, name = 'update_emissions'),

    #AuthenticationUrl's
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name = 'register'),
    path('logout/',views.logout_view, name = 'logout'),
    path('password_change/',views.password_change_view, name='password_change'),
    path('password_change/done/',views.password_change_done_view, name = 'password_change_done'),


    #PasswordReset
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password-reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="password-reset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password-reset/password_reset_complete.html'), name='password_reset_complete'),
     path('password-reset/', views.password_reset_view, name="password_reset"),
]
