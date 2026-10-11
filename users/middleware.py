from .models import User


class ImpersonateMiddleware:
    """Umožňuje superuserovi 'zobraziť si prostredie' iného používateľa (investora
    alebo dlžníka) bez toho, aby poznal jeho heslo. Administrátor sa neodhlási -
    len si v session uloží ID cieľového účtu a middleware pre danú požiadavku
    nahradí request.user cieľovým účtom, pričom pôvodný admin účet si ponechá
    v request.real_admin (na zobrazenie banneru a možnosť návratu)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        impersonate_id = request.session.get('impersonate_user_id')
        if impersonate_id and getattr(request.user, 'is_authenticated', False) and request.user.is_superuser:
            target = User.objects.filter(pk=impersonate_id).first()
            if target:
                request.real_admin = request.user
                request.user = target
            else:
                del request.session['impersonate_user_id']
        return self.get_response(request)
