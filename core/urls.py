from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import GENZAuthenticationForm

urlpatterns = [
    path('', views.index, name='index'),

    # Auth
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        authentication_form=GENZAuthenticationForm,
    ), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='core/password_change.html',
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='core/password_change_done.html',
    ), name='password_change_done'),

    # Main app
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chat/', views.chat, name='chat'),
    path('chat/<int:user_id>/', views.chat_conversation, name='chat_conversation'),
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:pk>/task/create/', views.task_create, name='task_create'),
    path('projects/<int:project_pk>/task/<int:task_pk>/toggle/', views.task_toggle, name='task_toggle'),
    path('teams/', views.teams, name='teams'),
    path('teams/create/', views.team_create, name='team_create'),
    path('analytics/', views.analytics, name='analytics'),
    path('ai/', views.ai_assistant, name='ai_assistant'),
    path('marketplace/', views.marketplace, name='marketplace'),
    path('community/', views.community, name='community'),
    path('community/post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('community/post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/<int:notif_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('settings/', views.settings_view, name='settings'),
    path('settings/save/', views.settings_save, name='settings_save'),
    path('settings/profile/', views.profile_settings, name='profile_settings'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.public_profile, name='public_profile'),
    path('files/', views.file_manager, name='file_manager'),
    path('activity/', views.activity_center, name='activity_center'),
]
