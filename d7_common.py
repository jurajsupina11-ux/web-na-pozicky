from d6_common import base  # noqa: F401  (re-export)

NAVFIX = ("body .logo-full-img{height:70px;}body{--nav-gap:12px;}"
          "body .main-nav a{font-size:13px;padding:8px 2px;}"
          "body .main-nav .btn-primary{padding:11px 18px;}\n")


def poly(pts):
    return ' '.join('%g,%g' % p for p in pts)


def svg(w, h, body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" fill="none" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (w, h, body))
