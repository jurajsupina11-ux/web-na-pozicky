def notifications(request):
    """Dostupné v každej šablóne: posledné nezobrazené notifikácie a ich počet
    pre zobrazenie zvončeka v hlavičke (investorské aj dlžnícke prostredie)."""
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {'unread_notifications_count': 0, 'recent_notifications': []}

    from .models import Notification
    qs = Notification.objects.filter(user=user)
    return {
        'unread_notifications_count': qs.filter(is_read=False).count(),
        'recent_notifications': qs[:6],
    }
