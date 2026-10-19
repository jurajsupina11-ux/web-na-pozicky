"""Spolocne pomocne funkcie pre definicie dizajnov v6."""


def art(bg, a, b, c, ink):
    """Ilustracia (graf + mince), prefarbena paletou dizajnu."""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 420" fill="none" '
        'stroke-linecap="round" stroke-linejoin="round">'
        f'<rect x="20" y="20" width="480" height="380" rx="26" fill="{bg}"/>'
        f'<circle cx="400" cy="110" r="70" fill="{c}" fill-opacity=".9"/>'
        f'<circle cx="110" cy="330" r="46" fill="{b}" fill-opacity=".85"/>'
        f'<rect x="80" y="250" width="62" height="110" rx="8" fill="{a}"/>'
        f'<rect x="162" y="200" width="62" height="160" rx="8" fill="{ink}" fill-opacity=".9"/>'
        f'<rect x="244" y="150" width="62" height="210" rx="8" fill="{b}"/>'
        f'<rect x="326" y="96" width="62" height="264" rx="8" fill="{a}"/>'
        f'<path d="M60 230 L190 170 L275 118 L400 56" stroke="{ink}" stroke-width="7"/>'
        f'<circle cx="400" cy="56" r="12" fill="{c}" stroke="{ink}" stroke-width="5"/>'
        f'<g transform="translate(396 292)"><ellipse cx="46" cy="80" rx="46" ry="14" fill="{c}"/>'
        f'<rect x="0" y="52" width="92" height="28" fill="{c}"/>'
        f'<ellipse cx="46" cy="52" rx="46" ry="14" fill="{b}"/>'
        f'<rect x="0" y="24" width="92" height="28" fill="{b}"/>'
        f'<ellipse cx="46" cy="24" rx="46" ry="14" fill="{a}"/></g></svg>'
    )


def base(**kw):
    """Predvolene hodnoty premennych; dizajn ich prepise."""
    d = {
        'radius-sm': '12px', 'brand-ink': '#fff', 'brand-text': 'var(--brand)',
        'inv-ink': '#fff', 'inv-text': 'var(--inv)', 'bor-ink': '#fff', 'bor-text': 'var(--bor)',
        'hdr-top': '5px solid var(--acc)', 'hdr-bd': '1px solid var(--line)',
        'hero-chip': 'var(--acc)', 'hero-chip-ink': 'var(--acc-ink)',
        'hero-btn': 'var(--acc)', 'hero-btn-ink': 'var(--acc-ink)', 'hero-bd': '0',
        'wal-btn': 'var(--acc)', 'wal-btn-ink': 'var(--acc-ink)', 'th-ink': 'var(--muted)',
        'focus': 'rgba(0,0,0,.12)', 'card-bd': '1px solid var(--line)', 'inp-bd': '1.5px solid var(--line)',
        'ft-bd': '0', 'sb-bd': '0', 'h1': '52px',
    }
    d.update({k.replace('_', '-'): v for k, v in kw.items()})
    return d
