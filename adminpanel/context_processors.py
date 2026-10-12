def admin_badges(request):
    """Počty čakajúcich položiek pre odznaky v bočnom menu admin prostredia -
    počíta sa len na stránkach /sprava/, aby to nezaťažovalo bežné požiadavky."""
    if not request.path.startswith('/sprava/'):
        return {}
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated or not user.is_superuser:
        return {}

    from auctions.models import Auction, WalletTransaction

    pending_count = Auction.objects.filter(
        status__in=[Auction.Status.PENDING_REVIEW, Auction.Status.COUNTER_OFFER],
    ).count()
    wallet_count = WalletTransaction.objects.filter(status=WalletTransaction.Status.PENDING).count()
    return {'pending_count': pending_count, 'wallet_count': wallet_count}
