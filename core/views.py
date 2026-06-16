from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Profile, Team, Project, Task, Message, Notification, Post, Comment, Badge
from .forms import (
    GENZUserCreationForm, ProfileForm, UserUpdateForm, TeamForm,
    ProjectForm, TaskForm, PostForm, CommentForm, MessageForm
)


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    total_users = User.objects.count()
    total_projects = Project.objects.count()
    total_teams = Team.objects.count()
    team_members = Profile.objects.select_related('user').all()
    featured_projects = Project.objects.all()[:6]
    context = {
        'total_users': total_users,
        'total_projects': total_projects,
        'total_teams': total_teams,
        'team_members': team_members,
        'featured_projects': featured_projects,
    }
    return render(request, 'core/index.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = GENZUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Welcome to KHIZEX, {user.first_name}! Your account is live.')
            return redirect('login')
    else:
        form = GENZUserCreationForm()
    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def dashboard(request):
    user = request.user
    projects = Project.objects.filter(Q(owner=user) | Q(team__members=user)).distinct()[:6]
    recent_tasks = Task.objects.filter(
        Q(assignee=user) | Q(project__owner=user)
    ).exclude(status='done').order_by('-project__created_at')[:8]
    unread_notifications = Notification.objects.filter(user=user, is_read=False).count()

    context = {
        'projects': projects,
        'recent_tasks': recent_tasks,
        'unread_notifications': unread_notifications,
        'total_projects': Project.objects.filter(Q(owner=user) | Q(team__members=user)).distinct().count(),
        'active_tasks': Task.objects.filter(
            Q(assignee=user) | Q(project__owner=user)
        ).exclude(status='done').count(),
        'completed_tasks': Task.objects.filter(
            Q(assignee=user) | Q(project__owner=user), status='done'
        ).count(),
        'team_count': Team.objects.filter(members=user).count(),
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def chat(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')
    context = {
        'users': users,
        'other_user': None,
        'messages': [],
        'current_user': request.user,
    }
    return render(request, 'core/chat.html', context)


@login_required
def chat_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_conversation', user_id=user_id)

    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    users = User.objects.exclude(id=request.user.id).order_by('username')

    context = {
        'other_user': other_user,
        'messages': messages_list,
        'users': users,
        'current_user': request.user,
    }
    return render(request, 'core/chat.html', context)


@login_required
def projects(request):
    user = request.user
    user_projects = Project.objects.filter(
        Q(owner=user) | Q(team__members=user)
    ).distinct().order_by('-created_at')

    total_tasks = Task.objects.filter(project__in=user_projects).count()
    done_tasks = Task.objects.filter(project__in=user_projects, status='done').count()

    context = {
        'projects': user_projects,
        'total_projects': user_projects.count(),
        'active_projects': user_projects.exclude(tasks__status='done').distinct().count(),
        'total_tasks': total_tasks,
        'done_tasks': done_tasks,
    }
    return render(request, 'core/projects.html', context)


@login_required
def project_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        desc = request.POST.get('description', '').strip()
        team_id = request.POST.get('team')
        if name:
            team = Team.objects.filter(id=team_id).first() if team_id else None
            Project.objects.create(name=name, description=desc, owner=request.user, team=team)
            messages.success(request, f'Project "{name}" created!')
            return redirect('projects')
    teams = Team.objects.all()
    return render(request, 'core/project_create.html', {'teams': teams})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all().order_by('-id')

    context = {
        'project': project,
        'tasks': tasks,
        'todo_tasks': tasks.filter(status='todo'),
        'in_progress_tasks': tasks.filter(status='in_progress'),
        'done_tasks': tasks.filter(status='done'),
    }
    return render(request, 'core/project_detail.html', context)


@login_required
def task_create(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        desc = request.POST.get('description', '').strip()
        status = request.POST.get('status', 'todo')
        assignee_id = request.POST.get('assignee')
        if title:
            assignee = User.objects.filter(id=assignee_id).first() if assignee_id else None
            task = Task.objects.create(title=title, description=desc, project=project, assignee=assignee, status=status)
            if assignee and assignee != request.user:
                Notification.objects.create(user=assignee, message=f'You were assigned to "{task.title}" in {project.name}')
            messages.success(request, f'Task "{title}" created!')
    return redirect('project_detail', pk=pk)


@login_required
def task_toggle(request, project_pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk, project_id=project_pk)
    cycle = {'todo': 'in_progress', 'in_progress': 'done', 'done': 'todo'}
    task.status = cycle.get(task.status, 'todo')
    task.save()
    return redirect('project_detail', pk=project_pk)


@login_required
def teams(request):
    user_teams = Team.objects.all().order_by('-created_at')
    all_users = User.objects.all().order_by('username')

    context = {
        'teams': user_teams,
        'all_users': all_users,
    }
    return render(request, 'core/teams.html', context)


@login_required
def team_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        member_ids = request.POST.getlist('members')
        if name:
            team = Team.objects.create(name=name)
            team.members.add(request.user)
            for mid in member_ids:
                u = User.objects.filter(id=mid).first()
                if u:
                    team.members.add(u)
            messages.success(request, f'Team "{name}" created!')
            return redirect('teams')
    all_users = User.objects.all().order_by('username')
    return render(request, 'core/team_create.html', {'all_users': all_users})


@login_required
def analytics(request):
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    done_tasks = Task.objects.filter(status='done').count()
    team_count = Team.objects.count()

    context = {
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'done_tasks': done_tasks,
        'team_count': team_count,
        'nodes': [
            {'id': '#NX-104', 'location': 'Lahore, PK', 'status': 'Active', 'load': 85, 'uptime': 342},
            {'id': '#NX-205', 'location': 'Karachi, PK', 'status': 'Active', 'load': 42, 'uptime': 120},
            {'id': '#NX-301', 'location': 'Islamabad, PK', 'status': 'Maint.', 'load': 0, 'uptime': 5},
            {'id': '#NX-404', 'location': 'Rawalpindi, PK', 'status': 'Active', 'load': 98, 'uptime': 890},
        ],
    }
    return render(request, 'core/analytics.html', context)


@login_required
def ai_assistant(request):
    return render(request, 'core/ai_assistant.html')


@login_required
def marketplace(request):
    return render(request, 'core/marketplace.html')


@login_required
def community(request):
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()

    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Post.objects.create(author=request.user, content=content)
            return redirect('community')

    trending = [
        {'tag': '#KHIZEX', 'count': '2.4k posts'},
        {'tag': '#PythonDev', 'count': '1.8k posts'},
        {'tag': '#MachineLearning', 'count': '1.5k posts'},
        {'tag': '#CyberpunkAesthetic', 'count': '980 posts'},
        {'tag': '#OpenSource', 'count': '750 posts'},
    ]

    context = {
        'posts': posts,
        'post_form': post_form,
        'trending': trending,
    }
    return render(request, 'core/community.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
            if post.author != request.user:
                Notification.objects.create(user=post.author, message=f'{request.user.first_name} commented on your post')
    return redirect('community')


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('community')


@login_required
def notifications(request):
    user_notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST':
        user_notifs.filter(is_read=False).update(is_read=True)
        return redirect('notifications')

    context = {
        'notifications_list': user_notifs,
        'unread_count': user_notifs.filter(is_read=False).count(),
    }
    return render(request, 'core/notifications.html', context)


@login_required
def mark_notification_read(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications')


@login_required
def settings_view(request):
    return render(request, 'core/settings.html')


@login_required
def profile_settings(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        bio = request.POST.get('bio', '')
        profile.bio = bio
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('settings')

    return render(request, 'core/profile_settings.html')


@login_required
def admin_panel(request):
    recent_users = User.objects.all().order_by('-date_joined')[:10]
    total_users = User.objects.count()
    total_projects = Project.objects.count()
    total_teams = Team.objects.count()

    from django.contrib.admin.models import LogEntry
    recent_logs = LogEntry.objects.all().order_by('-action_time')[:10]

    context = {
        'recent_users': recent_users,
        'total_users': total_users,
        'total_projects': total_projects,
        'total_teams': total_teams,
        'recent_logs': recent_logs,
    }
    return render(request, 'core/admin_panel.html', context)


@login_required
def profile(request):
    user = request.user
    profile_obj = user.profile
    user_projects = Project.objects.filter(owner=user).order_by('-created_at')[:5]
    user_badges = profile_obj.badges.all()

    context = {
        'profile_user': user,
        'profile_obj': profile_obj,
        'user_projects': user_projects,
        'user_badges': user_badges,
        'total_commits': 850,
        'followers': 1200,
    }
    return render(request, 'core/profile.html', context)


@login_required
def public_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile_obj = profile_user.profile
    user_projects = Project.objects.filter(owner=profile_user).order_by('-created_at')[:5]

    context = {
        'profile_user': profile_user,
        'profile_obj': profile_obj,
        'user_projects': user_projects,
        'user_badges': profile_obj.badges.all(),
    }
    return render(request, 'core/profile.html', context)


@login_required
def file_manager(request):
    return render(request, 'core/file_manager.html')


@login_required
def activity_center(request):
    return render(request, 'core/activity_center.html')


@login_required
def settings_save(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        bio = request.POST.get('bio', '')
        if bio is not None:
            profile = user.profile
            profile.bio = bio
            profile.save()
        messages.success(request, 'Profile updated successfully!')
    return redirect('settings')
