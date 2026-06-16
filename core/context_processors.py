from .models import Notification


def global_notifications(request):
    if request.user.is_authenticated:
        unread = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notifications': unread if unread > 0 else None}
    return {'unread_notifications': None}
