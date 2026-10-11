def impersonation(request):
    """Dostupné v každej šablóne: real_admin (ak admin aktuálne 'zobrazuje ako'
    iného používateľa) a is_impersonating flag pre banner s možnosťou návratu."""
    real_admin = getattr(request, 'real_admin', None)
    return {
        'real_admin': real_admin,
        'is_impersonating': real_admin is not None,
    }
