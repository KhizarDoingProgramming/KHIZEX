from django.contrib import admin
from .models import Profile, Badge, Team, Project, Task, Message, Notification, Post, Comment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']
    filter_horizontal = ['badges']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'icon']
    search_fields = ['name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'member_count']
    search_fields = ['name']
    filter_horizontal = ['members']
    readonly_fields = ['created_at']

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'team', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['team', 'created_at']
    raw_id_fields = ['owner', 'team']
    readonly_fields = ['created_at']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assignee', 'status']
    search_fields = ['title', 'description']
    list_filter = ['status', 'project']
    raw_id_fields = ['project', 'assignee']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp']
    search_fields = ['sender__username', 'receiver__username', 'content']
    list_filter = ['timestamp']
    raw_id_fields = ['sender', 'receiver']
    readonly_fields = ['timestamp']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'is_read', 'created_at']
    search_fields = ['user__username', 'message']
    list_filter = ['is_read', 'created_at']
    raw_id_fields = ['user']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'content_preview', 'created_at']
    search_fields = ['author__username', 'content']
    list_filter = ['created_at']
    raw_id_fields = ['author']
    readonly_fields = ['created_at']

    def content_preview(self, obj):
        return obj.content[:80] + '...' if len(obj.content) > 80 else obj.content
    content_preview.short_description = 'Content'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'created_at']
    search_fields = ['author__username', 'content']
    list_filter = ['created_at']
    raw_id_fields = ['post', 'author']
    readonly_fields = ['created_at']

    def content_preview(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    content_preview.short_description = 'Content'
