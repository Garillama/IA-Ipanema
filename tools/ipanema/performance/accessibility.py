"""Auditoría determinista Better Accessibility (WCAG 2.2 Nivel A y AA) para Shopify Liquid, Hydrogen/Remix, React y Tiendanube/Ipanema."""
from __future__ import annotations

import difflib
import math
import re
from typing import Any

from . import html_liquid
from . import model as perf_model

_HEX_COLOR_RE = re.compile(r'^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$')
_RGB_COLOR_RE = re.compile(r'^rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})(?:\s*,\s*[\d.]+\s*)?\)$')

ECOMMERCE_SURFACE_PATTERNS: dict[str, re.Pattern[str]] = {
    'shopify-pdp': re.compile(r'(?:/cart/add|product-form|main-product|product\.title|js-product-form|CartForm)', re.I),
    'variant-selector': re.compile(r'(?:variant|swatch|data-option|selectVariant|option-value)', re.I),
    'cart-drawer': re.compile(r'(?:cart-drawer|CartDrawer|js-cart-drawer|cart__drawer)', re.I),
    'mobile-menu': re.compile(r'(?:mobile-menu|menu-drawer|nav-drawer|header__menu)', re.I),
    'search-bar': re.compile(r'(?:type=["\']search["\']|role=["\']search["\']|predictive-search|action=["\']/search)', re.I),
    'contact-form': re.compile(r'(?:contact|newsletter|customer_posted|email)', re.I),
    'collection-filters': re.compile(r'(?:facet|sort_by|collection-filter|filter-form)', re.I),
    'carousel': re.compile(r'(?:carousel|slider|swiper|splide|carrusel)', re.I),
    'modal-dialog': re.compile(r'(?:<dialog\b|role=["\']dialog["\']|aria-modal)', re.I),
    'availability-and-errors': re.compile(r'(?:sold out|agotado|out of stock|aria-invalid|form-error|role=["\']alert["\'])', re.I),
}

USER_AUTOCOMPLETE_FIELDS: dict[str, str] = {
    'email': 'email',
    'correo': 'email',
    'phone': 'tel',
    'tel': 'tel',
    'telefono': 'tel',
    'name': 'name',
    'nombre': 'name',
    'postal': 'postal-code',
    'zip': 'postal-code',
    'address': 'street-address',
    'direccion': 'street-address',
}

INTERACTIVE_ARIA_ROLES = frozenset({'button', 'tab', 'switch', 'menuitem', 'checkbox', 'radio', 'option', 'link'})


def _parse_rgb(color: str | None) -> tuple[int, int, int] | None:
    if not isinstance(color, str):
        return None
    raw = color.strip()
    if _HEX_COLOR_RE.match(raw):
        h = raw[1:]
        if len(h) == 3:
            h = ''.join(ch * 2 for ch in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    m = _RGB_COLOR_RE.match(raw)
    if m:
        vals = tuple(int(g) for g in m.groups())
        if all(0 <= v <= 255 for v in vals):
            return vals  # type: ignore[return-value]
    return None


def _relative_luminance(rgb: tuple[int, int, int]) -> float:
    def channel(c: int) -> float:
        srgb = c / 255.0
        return srgb / 12.92 if srgb <= 0.03928 else math.pow((srgb + 0.055) / 1.055, 2.4)

    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg: str | None, bg: str | None) -> float | None:
    """Calcula la razón de contraste WCAG 2.2 (1.0 a 21.0) para dos colores válidos."""
    c1, c2 = _parse_rgb(fg), _parse_rgb(bg)
    if c1 is None or c2 is None:
        return None
    l1 = _relative_luminance(c1)
    l2 = _relative_luminance(c2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


def _detect_ecommerce_surfaces(files: dict[str, str], rendered: dict | None) -> list[str]:
    corpus = '\n'.join(f'{k}\n{v}' for k, v in files.items() if isinstance(v, str))
    if isinstance(rendered, dict):
        corpus += '\n' + str(rendered)
    return sorted(name for name, pat in ECOMMERCE_SURFACE_PATTERNS.items() if pat.search(corpus))


def _make_finding(
    *,
    issue_id: str,
    classification: str,
    category: str,
    wcag_criterion: str,
    wcag_level: str,
    severity: str,
    evidence_type: str,
    title: str,
    element: str,
    location: str,
    file_path: str | None,
    impact: str,
    evidence: Any,
    recommendation: str,
    required_verification: str,
) -> dict[str, Any]:
    # Las recomendaciones generales o AAA nunca pueden emitirse como violación WCAG ni severidad HIGH
    effective_severity = severity
    if classification == 'best_practice_recommendation' and effective_severity == 'HIGH':
        effective_severity = 'MEDIUM'
    return {
        'id': issue_id,
        'classification': classification,
        'category': category,
        'wcag_criterion': wcag_criterion,
        'wcag_level': wcag_level,
        'severity': effective_severity,
        'evidence_type': evidence_type,
        'title': title,
        'element': element,
        'location': location,
        'candidate_files': [file_path] if file_path else [],
        'impact': impact,
        'evidence': perf_model.sanitize(evidence),
        'recommendation': recommendation,
        'fix': recommendation,
        'required_verification': required_verification,
    }


def _audit_rendered_dom(
    rendered: dict,
    candidates_map: dict[str, list[str]],
    files: dict[str, str],
) -> tuple[list[dict], list[dict]]:
    verified: list[dict] = []
    recs: list[dict] = []
    default_file = next(iter(sorted(files)), (candidates_map.get('accessibility') or ['rendered-dom'])[0])

    def record(item: dict) -> None:
        if not item['candidate_files']:
            item['candidate_files'] = candidates_map.get('accessibility', [default_file])
        if item['classification'] == 'wcag_violation':
            verified.append(item)
        else:
            recs.append(item)

    # 1. Idioma del documento (3.1.1 A) y título descriptivo (2.4.2 A)
    if 'lang' in rendered and not str(rendered.get('lang') or '').strip():
        record(_make_finding(
            issue_id='A11Y-SEM-MISSING-LANG',
            classification='wcag_violation',
            category='semantics',
            wcag_criterion='3.1.1 Language of Page',
            wcag_level='A',
            severity='HIGH',
            evidence_type='verified_by_tool',
            title='Elemento <html> sin atributo lang válido',
            element='<html>',
            location=f'{default_file}:1',
            file_path=default_file,
            impact='Los lectores de pantalla no pueden seleccionar la pronunciación del idioma correcto.',
            evidence={'observed_lang': rendered.get('lang')},
            recommendation='Declarar atributo lang válido en la raíz HTML (ej. <html lang="es">).',
            required_verification='Confirmar en DOM renderizado tras el cambio.',
        ))
    if 'title' in rendered and not str(rendered.get('title') or '').strip():
        record(_make_finding(
            issue_id='A11Y-STRUCT-MISSING-TITLE',
            classification='wcag_violation',
            category='navigation_structure',
            wcag_criterion='2.4.2 Page Titled',
            wcag_level='A',
            severity='HIGH',
            evidence_type='verified_by_tool',
            title='Documento sin etiqueta <title> descriptiva',
            element='<title>',
            location=f'{default_file}:1',
            file_path=default_file,
            impact='Dificulta orientarse entre pestañas y en cambios de ruta SPA.',
            evidence={'observed_title': rendered.get('title')},
            recommendation='Renderizar un <title> único que identifique el producto o página actual.',
            required_verification='Comprobar el título anunciado al cargar la vista.',
        ))

    # 2. Landmarks y estructura de encabezados (1.3.1 A / 2.4.1 A vs recomendación de outline)
    landmarks = rendered.get('landmarks')
    if isinstance(landmarks, dict):
        if not landmarks.get('main'):
            record(_make_finding(
                issue_id='A11Y-STRUCT-MISSING-MAIN',
                classification='wcag_violation',
                category='navigation_structure',
                wcag_criterion='2.4.1 Bypass Blocks / 1.3.1 Info and Relationships',
                wcag_level='A',
                severity='MEDIUM',
                evidence_type='verified_by_tool',
                title='Página sin landmark principal <main> visible',
                element='<main>',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Usuarios de lector de pantalla no pueden saltar directamente al contenido principal.',
                evidence={'landmarks': landmarks},
                recommendation='Exponer un único <main id="main"> visible y un enlace "Saltar al contenido" como primer foco.',
                required_verification='Verificar atajo de landmarks en lector de pantalla.',
            ))
        if (perf_model.numeric(landmarks.get('nav_count')) or 0) > 1 and not landmarks.get('nav_all_labeled'):
            record(_make_finding(
                issue_id='A11Y-STRUCT-UNLABELED-MULTIPLE-NAV',
                classification='wcag_violation',
                category='semantics',
                wcag_criterion='1.3.1 Info and Relationships',
                wcag_level='A',
                severity='MEDIUM',
                evidence_type='verified_by_tool',
                title='Múltiples regiones <nav> sin etiqueta distintiva aria-label',
                element='<nav>',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Impide distinguir la navegación principal de breadcrumbs o menús del pie.',
                evidence={'nav_count': landmarks.get('nav_count')},
                recommendation='Añadir aria-label descriptivo a cada <nav> (ej. aria-label="Principal", aria-label="Migas de pan").',
                required_verification='Confirmar lista de regiones en árbol de accesibilidad.',
            ))

    headings = [h for h in (rendered.get('headings') or []) if isinstance(h, dict)]
    if headings:
        h1_count = sum(1 for h in headings if str(h.get('tag') or '').upper() == 'H1' and str(h.get('text') or '').strip())
        if h1_count > 1:
            record(_make_finding(
                issue_id='A11Y-REC-MULTIPLE-H1',
                classification='best_practice_recommendation',
                category='navigation_structure',
                wcag_criterion='Recommendation (One H1 Outline — Not a strict WCAG 2.2 AA failure)',
                wcag_level='Heuristic',
                severity='LOW',
                evidence_type='verified_by_tool',
                title=f'Múltiples encabezados <h1> detectados ({h1_count})',
                element='<h1>',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Puede hacer más confusa la navegación rápida por encabezados.',
                evidence={'h1_count': h1_count},
                recommendation='Reservar un único <h1> para el título principal si la estructura del tema lo permite.',
                required_verification='Revisar jerarquía de encabezados sin exigir regla estricta por diseño.',
            ))
        prev_lvl = 0
        for h in headings:
            tag = str(h.get('tag') or '').upper()
            if tag.startswith('H') and tag[1:].isdigit():
                lvl = int(tag[1:])
                if prev_lvl and lvl > prev_lvl + 1:
                    record(_make_finding(
                        issue_id='A11Y-REC-HEADING-SKIP',
                        classification='best_practice_recommendation',
                        category='navigation_structure',
                        wcag_criterion='Recommendation (No-skipped Heading Levels — Not a strict WCAG 2.2 AA failure)',
                        wcag_level='Heuristic',
                        severity='LOW',
                        evidence_type='verified_by_tool',
                        title=f'Salto de nivel en encabezados (H{prev_lvl} -> H{lvl})',
                        element=f'<h{lvl}>',
                        location=f'{default_file}:1',
                        file_path=default_file,
                        impact='Convención estructural; usar clases CSS para tamaño visual en lugar de saltar niveles.',
                        evidence={'from_level': prev_lvl, 'to_level': lvl},
                        recommendation='Ordenar niveles semánticos secuencialmente manteniendo la apariencia con CSS.',
                        required_verification='Revisar árbol de encabezados.',
                    ))
                    break
                prev_lvl = lvl

    # 3. Viewport Zoom (1.4.4 AA) y Reflow 320px (1.4.10 AA)
    for m in (rendered.get('metadata') or []):
        if isinstance(m, dict) and str(m.get('name') or '').lower() == 'viewport':
            vc = str(m.get('content') or '').lower()
            if 'user-scalable=no' in vc or 'user-scalable=0' in vc or re.search(r'maximum-scale\s*=\s*1(?:\.0)?\b', vc):
                record(_make_finding(
                    issue_id='A11Y-ZOOM-VIEWPORT-LOCKED',
                    classification='wcag_violation',
                    category='zoom_and_reflow',
                    wcag_criterion='1.4.4 Resize Text',
                    wcag_level='AA',
                    severity='HIGH',
                    evidence_type='verified_by_tool',
                    title='Meta viewport bloquea zoom de usuario (user-scalable=no / maximum-scale=1)',
                    element='<meta name="viewport">',
                    location=f'{default_file}:1',
                    file_path=default_file,
                    impact='Impide ampliar el texto y los detalles de producto hasta 200% en dispositivos móviles.',
                    evidence={'viewport_content': m.get('content')},
                    recommendation='Usar content="width=device-width, initial-scale=1" sin limitar el escalado.',
                    required_verification='Comprobar pellizco/zoom 200% en móvil.',
                ))

    vp = rendered.get('viewport') or {}
    iw, sw = perf_model.numeric(vp.get('innerWidth')), perf_model.numeric(vp.get('scrollWidth'))
    if iw and sw and sw > iw:
        record(_make_finding(
            issue_id='A11Y-REFLOW-HORIZONTAL-OVERFLOW',
            classification='wcag_violation',
            category='zoom_and_reflow',
            wcag_criterion='1.4.10 Reflow',
            wcag_level='AA',
            severity='HIGH',
            evidence_type='verified_by_tool',
            title=f'Desbordamiento horizontal detectado (scrollWidth {int(sw)}px > innerWidth {int(iw)}px)',
            element='document.documentElement',
            location=f'{default_file}:1',
            file_path=default_file,
            impact='Fuerza desplazamiento bidimensional en anchos estrechos / zoom 400% (320px).',
            evidence={'innerWidth': iw, 'scrollWidth': sw},
            recommendation='Asegurar flujo vertical en una sola columna hasta 320px usando flex-wrap/min-w-0 sin anchos fijos.',
            required_verification='Probar reflow real en viewport de 320px y zoom de texto 200%.',
        ))

    if vp.get('focusObscured'):
        record(_make_finding(
            issue_id='A11Y-FOCUS-OBSCURED-BY-STICKY',
            classification='wcag_violation',
            category='focus',
            wcag_criterion='2.4.11 Focus Not Obscured (Minimum)',
            wcag_level='AA',
            severity='HIGH',
            evidence_type='verified_by_tool',
            title='Elemento con foco queda completamente oculto detrás de cabecera o barra sticky',
            element='focused element',
            location=f'{default_file}:1',
            file_path=default_file,
            impact='Usuarios de teclado no ven el control actualmente enfocado al tabular.',
            evidence={'focus_obscured': True, 'sticky_chrome_px': vp.get('stickyHeight')},
            recommendation='Añadir scroll-padding-block-start / scroll-padding-block-end equivalente al alto sticky.',
            required_verification='Recorrer todo el flujo con Tab/Shift+Tab verificando visibilidad del anillo.',
        ))

    # 4. Controles, nombres accesibles, Label in Name (2.5.3 A) y Target Size (2.5.8 AA vs 44px recomendación)
    for btn in (rendered.get('buttons') or []):
        if not isinstance(btn, dict):
            continue
        btext = str(btn.get('text') or '').strip()
        baria = str(btn.get('ariaLabel') or '').strip()
        bid = btn.get('id') or btn.get('class') or '<button>'
        if not btext and not baria and not btn.get('ariaLabelledby'):
            record(_make_finding(
                issue_id='A11Y-NAME-BUTTON-MISSING',
                classification='wcag_violation',
                category='accessible_names',
                wcag_criterion='4.1.2 Name, Role, Value',
                wcag_level='A',
                severity='HIGH',
                evidence_type='verified_by_tool',
                title='Botón sin nombre accesible (texto visible ni aria-label)',
                element=f'<button id="{bid}">',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Lector de pantalla solo anuncia "botón" sin indicar la acción.',
                evidence={'id': btn.get('id'), 'class': btn.get('class')},
                recommendation='Añadir aria-label descriptivo al <button> y aria-hidden="true" en el icono SVG.',
                required_verification='Inspeccionar nombre calculado en el árbol de accesibilidad.',
            ))
        elif btext and baria and btext.lower() not in baria.lower():
            record(_make_finding(
                issue_id='A11Y-NAME-LABEL-MISMATCH',
                classification='wcag_violation',
                category='accessible_names',
                wcag_criterion='2.5.3 Label in Name',
                wcag_level='A',
                severity='MEDIUM',
                evidence_type='verified_by_tool',
                title=f'El aria-label ("{baria}") omite la etiqueta visible ("{btext}")',
                element=f'<button id="{bid}">',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Usuarios de control por voz no pueden activar el control dictando el texto visible.',
                evidence={'visible_text': btext, 'aria_label': baria},
                recommendation=f'Iniciar aria-label con el texto visible exacto ("{btext}...") o usar texto sr-only adicional.',
                required_verification='Comprobar nombre calculado frente a etiqueta visible.',
            ))
        if btn.get('focusVisible') is False:
            record(_make_finding(
                issue_id='A11Y-FOCUS-NOT-VISIBLE-RENDERED',
                classification='wcag_violation',
                category='focus',
                wcag_criterion='2.4.7 Focus Visible',
                wcag_level='AA',
                severity='HIGH',
                evidence_type='verified_by_tool',
                title=f'Control interactivo sin indicador de foco visible al recibir :focus-visible',
                element=f'<button id="{bid}">',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Impide saber qué botón o variante está seleccionada al navegar por teclado.',
                evidence={'id': btn.get('id'), 'focus_visible': False},
                recommendation='Conservar outline nativo o definir :focus-visible con anillo visible de contraste >= 3:1.',
                required_verification='Tabular con teclado en navegador real y validar anillo de foco.',
            ))
        w, h = perf_model.numeric(btn.get('width')), perf_model.numeric(btn.get('height'))
        if (w is not None and 0 < w < 24) or (h is not None and 0 < h < 24):
            record(_make_finding(
                issue_id='A11Y-TARGET-BELOW-24PX',
                classification='wcag_violation',
                category='touch_targets',
                wcag_criterion='2.5.8 Target Size (Minimum)',
                wcag_level='AA',
                severity='MEDIUM',
                evidence_type='verified_by_tool',
                title=f'Área clicable inferior al mínimo WCAG 2.2 de 24×24px ({int(w or 0)}×{int(h or 0)}px)',
                element=f'<button id="{bid}">',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Dificulta pulsar selectores de talla/color o cerrar drawers sin activar controles vecinos.',
                evidence={'width_px': w, 'height_px': h, 'wcag_min_px': 24},
                recommendation='Ampliar el hit area a mínimo 24×24px (preferible 44×44px en táctil) mediante padding o pseudo-elemento sin solapamientos.',
                required_verification='Medir bounding box y comprobar ausencia de solapamiento entre objetivos.',
            ))
        elif (w is not None and 24 <= w < 44) or (h is not None and 24 <= h < 44):
            record(_make_finding(
                issue_id='A11Y-REC-TARGET-ERGONOMICS-44PX',
                classification='best_practice_recommendation',
                category='touch_targets',
                wcag_criterion='Recommendation (2.5.5 Target Size Enhanced AAA / Touch 44x44px — Passes 2.5.8 AA)',
                wcag_level='AAA/Heuristic',
                severity='LOW',
                evidence_type='verified_by_tool',
                title=f'Objetivo táctil cumple 2.5.8 AA (24px) pero es menor al objetivo recomendado de 44×44px ({int(w or 0)}×{int(h or 0)}px)',
                element=f'<button id="{bid}">',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Recomendación ergonómica táctil; no constituye incumplimiento WCAG 2.2 AA.',
                evidence={'width_px': w, 'height_px': h, 'recommended_px': 44},
                recommendation='Si la densidad visual lo permite, extender el hit area mediante pseudo-elemento ::after a 44×44px.',
                required_verification='Opcional; verificar que no colisione con selectores adyacentes.',
            ))

    # 5. Imágenes (1.1.1 A) y Formularios (3.3.2 A, 3.3.1 A, 1.3.5 AA)
    for img in (rendered.get('images') or []):
        if isinstance(img, dict) and img.get('alt') is None:
            record(_make_finding(
                issue_id='A11Y-ALT-IMG-MISSING',
                classification='wcag_violation',
                category='alt_text',
                wcag_criterion='1.1.1 Non-text Content',
                wcag_level='A',
                severity='HIGH',
                evidence_type='verified_by_tool',
                title='Imagen renderizada sin atributo alt',
                element='<img>',
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Los lectores de pantalla leen la ruta del archivo en lugar del propósito de la imagen.',
                evidence={'src': img.get('currentSrc') or img.get('src')},
                recommendation='Definir alt descriptivo para fotos de producto/funcionales o alt="" si es decorativa.',
                required_verification='Confirmar atributo alt en DOM final.',
            ))

    for form in (rendered.get('forms') or []):
        if not isinstance(form, dict):
            continue
        for inp in (form.get('inputs') or []):
            if not isinstance(inp, dict):
                continue
            itype = str(inp.get('type') or '').lower()
            if itype in ('hidden', 'submit', 'button', 'reset', 'image'):
                continue
            if not inp.get('hasLabel') and not inp.get('ariaLabel') and not inp.get('ariaLabelledby'):
                record(_make_finding(
                    issue_id='A11Y-FORM-INPUT-UNLABELED',
                    classification='wcag_violation',
                    category='forms',
                    wcag_criterion='3.3.2 Labels or Instructions & 4.1.2 Name, Role, Value',
                    wcag_level='A',
                    severity='HIGH',
                    evidence_type='verified_by_tool',
                    title='Control de formulario sin <label> asociado ni aria-label',
                    element=f'<input name="{inp.get("name") or ""}">',
                    location=f'{default_file}:1',
                    file_path=default_file,
                    impact='El usuario no conoce el propósito del campo con lector de pantalla ni tiene hit target ampliado en su etiqueta.',
                    evidence={'tag': inp.get('tag'), 'type': itype, 'name': inp.get('name')},
                    recommendation='Asociar <label for="..."> o envolver en <label>; nunca depender solo de placeholder.',
                    required_verification='Comprobar clic en etiqueta y anuncio de nombre en lector de pantalla.',
                ))

    # 6. Contraste SOLO cuando existe evidencia medible (1.4.3 AA / 1.4.11 AA)
    for sample in (rendered.get('contrast_samples') or []):
        if not isinstance(sample, dict):
            continue
        ratio = contrast_ratio(sample.get('fg'), sample.get('bg'))
        if ratio is None:
            continue
        kind = str(sample.get('kind') or 'text').lower()
        size_px = perf_model.numeric(sample.get('fontSizePx')) or 16.0
        bold = bool(sample.get('bold'))
        is_large = size_px >= 24.0 or (bold and size_px >= 18.67)
        if kind in ('ui', 'focus', 'border'):
            threshold = 3.0
            crit = '1.4.11 Non-text Contrast'
            msg_kind = 'componente UI o indicador de foco'
        else:
            threshold = 3.0 if is_large else 4.5
            crit = '1.4.3 Contrast (Minimum)'
            msg_kind = 'texto grande' if is_large else 'texto normal'
        if ratio < threshold:
            record(_make_finding(
                issue_id='A11Y-CONTRAST-BELOW-MINIMUM',
                classification='wcag_violation',
                category='contrast',
                wcag_criterion=crit,
                wcag_level='AA',
                severity='HIGH',
                evidence_type='verified_by_tool',
                title=f'Contraste medido insuficiente en {msg_kind} ({ratio}:1 < {threshold}:1)',
                element=str(sample.get('element') or kind),
                location=f'{default_file}:1',
                file_path=default_file,
                impact='Texto o borde difícil de percibir para usuarios con baja visión.',
                evidence={'measured_ratio': ratio, 'required_ratio': threshold, 'fg': sample.get('fg'), 'bg': sample.get('bg')},
                recommendation=f'Ajustar el par fg/bg hasta alcanzar >= {threshold}:1 respetando los tokens de marca.',
                required_verification='Re-medición de contraste tras ajuste autorizado.',
            ))

    # 7. Violaciones axe-core si están presentes en rendered
    for v in ((rendered.get('axe') or {}).get('violations') or []):
        if isinstance(v, dict):
            sev = 'HIGH' if str(v.get('impact') or '').lower() in ('critical', 'serious') else 'MEDIUM'
            record(_make_finding(
                issue_id='A11Y-AXE-' + str(v.get('id') or 'VIOLATION').upper(),
                classification='wcag_violation',
                category='semantics',
                wcag_criterion='WCAG 2.2 (axe-core verified)',
                wcag_level='AA',
                severity=sev,
                evidence_type='verified_by_tool',
                title=f'Violación verificada por axe-core: {v.get("id")}',
                element=str(v.get('id') or 'dom-node'),
                location=f'{default_file}:1',
                file_path=default_file,
                impact=v.get('description') or v.get('help') or 'Barrera de accesibilidad detectada por axe-core.',
                evidence={'rule_id': v.get('id'), 'impact_level': v.get('impact')},
                recommendation=v.get('help') or 'Corregir siguiendo criterios WCAG 2.2 AA.',
                required_verification='Re-ejecutar axe-core sobre el DOM actualizado.',
            ))

    return verified, recs


def _scan_jsx_tags(content: str, tag_name: str) -> list[dict[str, Any]]:
    """Escáner léxico JSX consciente de llaves { ... } y cadenas para diagnóstico multilínea (solo lectura)."""
    out: list[dict[str, Any]] = []
    n = len(content)
    open_re = re.compile(r'<' + re.escape(tag_name) + r'(?=[\s/>])', re.I)
    close_token = f'</{tag_name}>'
    pos = 0

    while pos < n:
        m = open_re.search(content, pos)
        if not m:
            break
        start = m.start()
        i = m.end()
        brace_depth = 0
        quote: str | None = None
        tag_end = None
        self_closing = False
        while i < n:
            ch = content[i]
            if quote is not None:
                if ch == '\\' and i + 1 < n:
                    i += 2
                    continue
                if ch == quote:
                    quote = None
                i += 1
                continue
            if ch in ('"', "'", '`'):
                quote = ch
                i += 1
                continue
            if ch == '{':
                brace_depth += 1
            elif ch == '}':
                if brace_depth > 0:
                    brace_depth -= 1
            elif ch == '>' and brace_depth == 0:
                tag_end = i + 1
                prev = content[m.end():i].rstrip()
                self_closing = prev.endswith('/')
                break
            i += 1
        if tag_end is None:
            pos = m.end()
            continue

        attrs_raw = content[m.end():tag_end - (2 if self_closing else 1)]
        inner = ''
        if not self_closing and tag_name.lower() not in html_liquid.VOID_HTML_TAGS:
            same_open = re.compile(r'<' + re.escape(tag_name) + r'(?=[\s/>])', re.I)
            same_close = re.compile(r'</\s*' + re.escape(tag_name) + r'\s*>', re.I)
            depth = 1
            cur = tag_end
            c_idx = -1
            while cur < n and depth > 0:
                mo = same_open.search(content, cur)
                mc = same_close.search(content, cur)
                if not mc:
                    break
                if mo and mo.start() < mc.start():
                    # Ignore self-closing inner tags <tag .../>
                    depth += 1
                    cur = mo.end()
                else:
                    depth -= 1
                    if depth == 0:
                        c_idx = mc.start()
                        break
                    cur = mc.end()
            if c_idx != -1:
                inner = content[tag_end:c_idx]
        line = content.count('\n', 0, start) + 1
        out.append({
            'line': line,
            'attrs': attrs_raw,
            'inner': inner,
            'self_closing': self_closing,
            'full_open': content[start:tag_end],
        })
        pos = tag_end
    return out


def _jsx_has_attr(attrs: str, attr_name: str) -> bool:
    return bool(re.search(r'(?:^|\s)' + re.escape(attr_name) + r'(?:\s*=|\s|$)', attrs, re.I))


def _jsx_get_attr(attrs: str, attr_name: str) -> str | None:
    m = re.search(
        r'(?:^|\s)' + re.escape(attr_name) + r'\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|\{([^}]*)\})',
        attrs,
        re.I,
    )
    if not m:
        return None
    for grp in m.groups():
        if grp is not None:
            return grp
    return None


def _button_accessible_assessment_jsx(attrs: str, inner: str) -> tuple[bool, str | None, str]:
    """Evalúa si un <button> JSX posee nombre accesible (aria-label, aria-labelledby, title o texto/expresión)."""
    aria_label = _jsx_get_attr(attrs, 'aria-label')
    aria_labelledby = _jsx_get_attr(attrs, 'aria-labelledby')
    title_attr = _jsx_get_attr(attrs, 'title')
    # Quitar subárboles <svg ...>...</svg> o <svg .../> marcados o iconos decorativos antes de evaluar texto visible
    inner_no_svg = re.sub(r'<svg\b[^>]*?(?:/>|>.*?</svg>)', '', inner, flags=re.I | re.S)
    # También quitar hijos explícitamente ocultos aria-hidden="true"
    inner_visible = re.sub(r'<([a-zA-Z0-9_-]+)\b[^>]*aria-hidden\s*=\s*["\'{]?true["\'}]?[^>]*>.*?</\1>', '', inner_no_svg, flags=re.I | re.S)
    # Comprobar si hay img con alt no vacío dentro del botón
    img_alts = re.findall(r'<img\b[^>]*\balt\s*=\s*(?:"([^"]+)"|\'([^\']+)\')', inner_visible, re.I)
    has_img_alt = any((a or b).strip() for a, b in img_alts)
    text_only = re.sub(r'<[^>]+>', ' ', inner_visible).strip()
    has_dynamic_expr = bool(re.search(r'\{[^}]+\}', text_only))
    has_name = bool(
        (aria_label and aria_label.strip())
        or (aria_labelledby and aria_labelledby.strip())
        or (title_attr and title_attr.strip())
        or bool(text_only)
        or has_img_alt
        or has_dynamic_expr
    )
    static_visible = '' if (has_dynamic_expr or '<' in inner_visible or not text_only) else text_only
    return has_name, (aria_label.strip() if isinstance(aria_label, str) else None), static_visible


def _audit_source_files(files: dict[str, str]) -> tuple[list[dict], list[dict]]:
    hypotheses: list[dict] = []
    recs: list[dict] = []
    seen_keys: set[tuple[str, str]] = set()

    def add_src(item: dict) -> None:
        key = (item['id'], item['location'])
        if key in seen_keys:
            return
        seen_keys.add(key)
        if item['classification'] == 'wcag_violation':
            hypotheses.append(item)
        else:
            recs.append(item)

    for path, content in sorted(files.items()):
        if not isinstance(content, str):
            continue
        parsed = html_liquid.parse_structural_document(path, content)
        lines = content.splitlines()
        lower = content.lower()
        has_focus_visible = ':focus-visible' in lower or 'focus-visible:' in lower
        has_reduced_motion = 'prefers-reduced-motion' in lower or 'motion-safe:' in lower or 'motion-reduce:' in lower
        has_sticky_chrome = 'position: sticky' in lower or 'position:fixed' in lower or 'position: fixed' in lower or ' sticky ' in lower
        has_scroll_padding = 'scroll-padding' in lower or 'scroll-margin' in lower

        # 1. Estructura base <main> / skip-link
        is_doc_shell = '<html' in lower or '<body' in lower or path.endswith(('layout.tpl', 'theme.liquid', 'root.tsx', 'index.html'))
        if is_doc_shell:
            if '<main' not in lower:
                add_src(_make_finding(
                    issue_id='A11Y-SRC-MISSING-MAIN-LANDMARK',
                    classification='wcag_violation',
                    category='navigation_structure',
                    wcag_criterion='2.4.1 Bypass Blocks / 1.3.1 Info and Relationships',
                    wcag_level='A',
                    severity='MEDIUM',
                    evidence_type='code_hypothesis',
                    title='Plantilla base sin landmark <main>',
                    element='<body>',
                    location=f'{path}:1',
                    file_path=path,
                    impact='Impide a tecnologías de asistencia saltar directamente al bloque principal de contenido.',
                    evidence={'code_excerpt': 'No <main> tag observed'},
                    recommendation='Envolver el contenido principal con <main id="main"> e incluir enlace "Saltar al contenido" como primer elemento enfocable.',
                    required_verification='Verificar árbol de landmarks y recorrido con Tab desde el inicio de la página.',
                ))
            if ('<nav' in lower or '<header' in lower) and 'skip' not in lower and 'saltar' not in lower and '#main' not in lower:
                add_src(_make_finding(
                    issue_id='A11Y-SRC-MISSING-SKIP-LINK',
                    classification='wcag_violation',
                    category='navigation_structure',
                    wcag_criterion='2.4.1 Bypass Blocks',
                    wcag_level='A',
                    severity='MEDIUM',
                    evidence_type='code_hypothesis',
                    title='Navegación/cabecera sin enlace de salto ("Saltar al contenido")',
                    element='<header> / <nav>',
                    location=f'{path}:1',
                    file_path=path,
                    impact='Usuarios de teclado deben tabular por toda la cabecera repetida en cada página.',
                    evidence={'code_excerpt': 'Navigation chrome without #main skip link'},
                    recommendation='Añadir <a class="skip-link" href="#main">Saltar al contenido</a> oculto visualmente hasta :focus.',
                    required_verification='Confirmar con Tab que es el primer foco y mueve el foco a #main.',
                ))

        declared_ids = set(re.findall(r'\bid\s*=\s*["\']([a-zA-Z0-9_-]+)["\']', content))

        # 2. Inspección estructural (multilínea real) según el tipo de archivo
        if parsed.file_kind in ('html', 'liquid'):
            for node in parsed.nodes:
                loc = f'{path}:{node.line}'
                # A. <div onClick> / <span onClick> (multilínea y anidado)
                if node.tag in ('div', 'span') and any(k in node.attr_map for k in ('onclick', 'ng-click', '@click')):
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-NON-SEMANTIC-CLICKABLE',
                        classification='wcag_violation',
                        category='semantics',
                        wcag_criterion='2.1.1 Keyboard & 4.1.2 Name, Role, Value',
                        wcag_level='A',
                        severity='HIGH',
                        evidence_type='code_hypothesis',
                        title='Elemento no semántico <div>/<span> con manejador click en lugar de <button> o <a href>',
                        element=f'<{node.tag}>',
                        location=loc,
                        file_path=path,
                        impact='Inaccesible desde teclado (sin Tab/Enter/Space) y sin rol interactivo en lector de pantalla.',
                        evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                        recommendation='Reemplazar por <button type="button"> para acciones (ej. selector de variante, abrir drawer) o <a href="..."> si navega.',
                        required_verification='Confirmar operación con Tab, Enter y Space y rol anunciado.',
                    ))

                # B. Botón multilínea: nombre accesible + Label in Name (2.5.3) + role redundante + disabled+aria-disabled
                if node.tag == 'button':
                    if (node.get_attr('role') or '').lower() == 'button':
                        add_src(_make_finding(
                            issue_id='A11Y-REC-REDUNDANT-BUTTON-ROLE',
                            classification='best_practice_recommendation',
                            category='aria',
                            wcag_criterion='Recommendation (Redundant ARIA — No ARIA better than redundant ARIA)',
                            wcag_level='Heuristic',
                            severity='LOW',
                            evidence_type='code_hypothesis',
                            title='Rol redundante role="button" en elemento <button> nativo',
                            element='<button role="button">',
                            location=loc,
                            file_path=path,
                            impact='Añade ruido innecesario manteniendo la semántica nativa.',
                            evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                            recommendation='Eliminar role="button" redundante de <button>.',
                            required_verification='Inspeccionar markup limpio.',
                        ))
                    if node.has_attr('disabled') and node.has_attr('aria-disabled'):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-BOTH-DISABLED-AND-ARIA-DISABLED',
                            classification='best_practice_recommendation',
                            category='semantics',
                            wcag_criterion='Recommendation (Avoid mixing native disabled and aria-disabled)',
                            wcag_level='Heuristic',
                            severity='LOW',
                            evidence_type='code_hypothesis',
                            title='Uso simultáneo de `disabled` nativo y `aria-disabled` en el mismo control',
                            element='<button>',
                            location=loc,
                            file_path=path,
                            impact='El atributo disabled nativo saca el control del orden de foco anulando el propósito de aria-disabled.',
                            evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                            recommendation='Elegir native `disabled` o solo `aria-disabled="true"`.',
                            required_verification='Tabular hasta el control deshabilitado para confirmar comportamiento esperado.',
                        ))
                    aria_label = (node.get_attr('aria-label') or '').strip()
                    aria_labelledby = (node.get_attr('aria-labelledby') or '').strip()
                    title_attr = (node.get_attr('title') or '').strip()
                    visible_txt = node.collect_visible_text()
                    # No marcar falta de nombre si hay etiqueta Liquid dinámica o texto/aria válido
                    if not (aria_label or aria_labelledby or title_attr or visible_txt):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-ICON-BUTTON-NO-NAME',
                            classification='wcag_violation',
                            category='accessible_names',
                            wcag_criterion='4.1.2 Name, Role, Value',
                            wcag_level='A',
                            severity='HIGH',
                            evidence_type='code_hypothesis',
                            title='Botón sin nombre accesible visible ni `aria-label`/`aria-labelledby`',
                            element='<button>',
                            location=loc,
                            file_path=path,
                            impact='El usuario con lector de pantalla no conoce la función del botón (cerrar drawer, carrito, buscar).',
                            evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                            recommendation='Añadir `aria-label="..."` claro en <button> (o texto visible / .sr-only) y `aria-hidden="true"` en SVG decorativo.',
                            required_verification='Comprobar nombre accesible calculado en árbol de accesibilidad.',
                        ))
                    elif visible_txt and aria_label and '{{' not in aria_label and '{{' not in visible_txt and '{%' not in visible_txt:
                        if visible_txt.lower() not in aria_label.lower():
                            add_src(_make_finding(
                                issue_id='A11Y-SRC-LABEL-IN-NAME',
                                classification='wcag_violation',
                                category='accessible_names',
                                wcag_criterion='2.5.3 Label in Name',
                                wcag_level='A',
                                severity='MEDIUM',
                                evidence_type='code_hypothesis',
                                title=f'Discrepancia Label in Name: texto visible "{visible_txt}" ausente en aria-label "{aria_label}"',
                                element='<button>',
                                location=loc,
                                file_path=path,
                                impact='Rompe comandos por voz ("hacer clic en ...") porque el nombre accesible no incluye el texto visible.',
                                evidence={'visible_text': visible_txt, 'aria_label': aria_label},
                                recommendation=f'Iniciar aria-label con "{visible_txt}" o eliminar el aria-label si el texto visible basta.',
                                required_verification='Comprobar nombre calculado en árbol de accesibilidad.',
                            ))

                # C. <img> multilínea sin alt
                if node.tag == 'img' and not node.has_attr('alt'):
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-IMG-MISSING-ALT',
                        classification='wcag_violation',
                        category='alt_text',
                        wcag_criterion='1.1.1 Non-text Content',
                        wcag_level='A',
                        severity='HIGH',
                        evidence_type='code_hypothesis',
                        title='Etiqueta <img> sin atributo `alt`',
                        element='<img>',
                        location=loc,
                        file_path=path,
                        impact='Lectores de pantalla anuncian la URL o nombre de archivo en lugar del contenido o acción.',
                        evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                        recommendation='Añadir alt descriptivo del producto/acción o alt="" si la imagen es decorativa.',
                        required_verification='Revisar atributo alt renderizado en PDP y tarjetas.',
                    ))

                # D. Controles de formulario <input>/<select>/<textarea>
                if node.tag in ('input', 'select', 'textarea'):
                    itype = (node.get_attr('type') or '').lower()
                    if not (node.tag == 'input' and itype in ('hidden', 'submit', 'button', 'reset', 'image')):
                        has_aria = bool((node.get_attr('aria-label') or '').strip() or (node.get_attr('aria-labelledby') or '').strip())
                        id_val = node.get_attr('id')
                        has_for = bool(
                            id_val
                            and (
                                re.search(r'for\s*=\s*["\']' + re.escape(id_val) + r'["\']', content, re.I)
                                or re.search(r'htmlFor\s*=\s*["\']' + re.escape(id_val) + r'["\']', content, re.I)
                            )
                        )
                        if not has_aria and not has_for and not node.has_ancestor('label'):
                            add_src(_make_finding(
                                issue_id='A11Y-SRC-FORM-MISSING-LABEL',
                                classification='wcag_violation',
                                category='forms',
                                wcag_criterion='3.3.2 Labels or Instructions & 4.1.2 Name, Role, Value',
                                wcag_level='A',
                                severity='HIGH',
                                evidence_type='code_hypothesis',
                                title=f'Control <{node.tag}> sin <label for>, <label> envolvente ni `aria-label`',
                                element=f'<{node.tag}>',
                                location=loc,
                                file_path=path,
                                impact='El usuario no recibe etiqueta permanente ni área clicable ampliada para el campo.',
                                evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                                recommendation='Vincular <label for="..."> explícito o envolver el control dentro de <label>.',
                                required_verification='Verificar anuncio de nombre y activación al pulsar el texto del label.',
                            ))
                        field_key = (node.get_attr('name') or itype or '').lower()
                        matched_ac = next((ac for k, ac in USER_AUTOCOMPLETE_FIELDS.items() if k in field_key), None)
                        if matched_ac and not node.has_attr('autocomplete'):
                            add_src(_make_finding(
                                issue_id='A11Y-SRC-MISSING-AUTOCOMPLETE',
                                classification='wcag_violation',
                                category='forms',
                                wcag_criterion='1.3.5 Identify Input Purpose',
                                wcag_level='AA',
                                severity='MEDIUM',
                                evidence_type='code_hypothesis',
                                title=f'Campo de usuario sin atributo `autocomplete="{matched_ac}"`',
                                element=f'<{node.tag} name="{field_key}">',
                                location=loc,
                                file_path=path,
                                impact='Impide autocompletado de navegadores y tecnologías de asistencia en formularios de contacto o checkout.',
                                evidence={'expected_autocomplete': matched_ac, 'code_excerpt': node.start_tag_raw.strip()[:120]},
                                recommendation=f'Añadir autocomplete="{matched_ac}" al control.',
                                required_verification='Probar autocompletado de navegador sobre el formulario.',
                            ))

                # E. aria-hidden="true" en elemento enfocable o conteniendo elementos enfocables
                if (node.get_attr('aria-hidden') or '').lower() == 'true':
                    focusable_inside = node.tag in ('button', 'a', 'input', 'select', 'textarea') or any(
                        d.tag in ('button', 'a', 'input', 'select', 'textarea') for d in node.iter_descendants()
                    )
                    if focusable_inside:
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-ARIA-HIDDEN-FOCUSABLE',
                            classification='wcag_violation',
                            category='aria',
                            wcag_criterion='4.1.2 Name, Role, Value & 2.4.3 Focus Order',
                            wcag_level='A',
                            severity='HIGH',
                            evidence_type='code_hypothesis',
                            title='Atributo `aria-hidden="true"` aplicado sobre o alrededor de elemento enfocable',
                            element=f'<{node.tag} aria-hidden="true">',
                            location=loc,
                            file_path=path,
                            impact='Crea paradas de tabulación fantasma invisibles para lectores de pantalla.',
                            evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                            recommendation='Retirar aria-hidden del contenedor interactivo o usar `inert`.',
                            required_verification='Verificar tabulación y árbol de accesibilidad con NVDA/VoiceOver.',
                        ))

                # F. Roles ARIA interactivos sin soporte teclado / nav role="menu" / aria-label en div genérico
                role_val = (node.get_attr('role') or '').lower()
                if role_val in INTERACTIVE_ARIA_ROLES and node.tag not in ('button', 'a', 'input', 'select'):
                    if not (node.has_attr('onkeydown') or node.has_attr('onkeyup') or node.has_attr('tabindex')):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-ARIA-ROLE-MISSING-KEYBOARD',
                            classification='wcag_violation',
                            category='kb_and_focus',
                            wcag_criterion='2.1.1 Keyboard & 4.1.2 Name, Role, Value',
                            wcag_level='A',
                            severity='HIGH',
                            evidence_type='code_hypothesis',
                            title=f'Elemento <{node.tag} role="{role_val}"> sin tabindex ni manejador de teclado (onKeyDown)',
                            element=f'<{node.tag} role="{role_val}">',
                            location=loc,
                            file_path=path,
                            impact='Promete un control interactivo al lector de pantalla pero no se puede enfocar ni activar por teclado.',
                            evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                            recommendation='Usar elemento HTML nativo (<button>/<a href>) o implementar el patrón completo APG con tabindex="0" y onKeyDown.',
                            required_verification='Probar navegación por teclado (Tab/Enter/Space/Flechas).',
                        ))
                if node.tag == 'nav' and role_val == 'menu':
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-NAV-USING-ROLE-MENU',
                        classification='wcag_violation',
                        category='aria',
                        wcag_criterion='4.1.2 Name, Role, Value',
                        wcag_level='A',
                        severity='MEDIUM',
                        evidence_type='code_hypothesis',
                        title='Navegación web marcada incorrectamente con role="menu"',
                        element='<nav role="menu">',
                        location=loc,
                        file_path=path,
                        impact='El rol "menu" anuncia menú de aplicación de escritorio e induce atajos inesperados en navegación web.',
                        evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                        recommendation='Usar <nav aria-label="..."> con lista <ul>/<li> y enlaces <a href>.',
                        required_verification='Comprobar rol landmark de navegación en lector de pantalla.',
                    ))
                if node.tag in ('div', 'span') and not role_val and node.has_attr('aria-label'):
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-ARIA-LABEL-ON-GENERIC',
                        classification='wcag_violation',
                        category='aria',
                        wcag_criterion='4.1.2 Name, Role, Value',
                        wcag_level='A',
                        severity='MEDIUM',
                        evidence_type='code_hypothesis',
                        title='Atributo aria-label colocado en <div>/<span> genérico sin rol',
                        element=f'<{node.tag}>',
                        location=loc,
                        file_path=path,
                        impact='ARIA 1.2 prohíbe nombrar elementos genéricos y muchos lectores de pantalla lo ignoran.',
                        evidence={'code_excerpt': node.start_tag_raw.strip()[:120]},
                        recommendation='Mover el nombre accesible a un elemento semántico (<button>, <a>, <section aria-labelledby>) o texto visible.',
                        required_verification='Leer árbol de accesibilidad del contenedor.',
                    ))
        else:
            # Diagnóstico consciente de JSX/TSX multilínea mediante escáner léxico con profundidad de llaves
            for btn in _scan_jsx_tags(content, 'button'):
                attrs, inner = btn['attrs'], btn['inner']
                loc = f'{path}:{btn["line"]}'
                if (_jsx_get_attr(attrs, 'role') or '').lower() == 'button':
                    add_src(_make_finding(
                        issue_id='A11Y-REC-REDUNDANT-BUTTON-ROLE',
                        classification='best_practice_recommendation',
                        category='aria',
                        wcag_criterion='Recommendation (Redundant ARIA — No ARIA better than redundant ARIA)',
                        wcag_level='Heuristic',
                        severity='LOW',
                        evidence_type='code_hypothesis',
                        title='Rol redundante role="button" en elemento <button> nativo',
                        element='<button role="button">',
                        location=loc,
                        file_path=path,
                        impact='Añade ruido innecesario manteniendo la semántica nativa.',
                        evidence={'code_excerpt': btn['full_open'][:120]},
                        recommendation='Eliminar role="button" redundante de <button>.',
                        required_verification='Inspeccionar markup limpio.',
                    ))
                if _jsx_has_attr(attrs, 'disabled') and _jsx_has_attr(attrs, 'aria-disabled'):
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-BOTH-DISABLED-AND-ARIA-DISABLED',
                        classification='best_practice_recommendation',
                        category='semantics',
                        wcag_criterion='Recommendation (Avoid mixing native disabled and aria-disabled)',
                        wcag_level='Heuristic',
                        severity='LOW',
                        evidence_type='code_hypothesis',
                        title='Uso simultáneo de `disabled` nativo y `aria-disabled` en el mismo control',
                        element='<button>',
                        location=loc,
                        file_path=path,
                        impact='El atributo disabled nativo saca el control del orden de foco anulando el propósito de aria-disabled.',
                        evidence={'code_excerpt': btn['full_open'][:120]},
                        recommendation='Elegir native `disabled` o solo `aria-disabled="true"`.',
                        required_verification='Tabular hasta el control deshabilitado para confirmar comportamiento esperado.',
                    ))
                has_name, aria_val, static_vis = _button_accessible_assessment_jsx(attrs, inner)
                if not btn['self_closing'] and inner and not has_name:
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-ICON-BUTTON-NO-NAME',
                        classification='wcag_violation',
                        category='accessible_names',
                        wcag_criterion='4.1.2 Name, Role, Value',
                        wcag_level='A',
                        severity='HIGH',
                        evidence_type='code_hypothesis',
                        title='Botón sin nombre accesible visible ni `aria-label`',
                        element='<button>',
                        location=loc,
                        file_path=path,
                        impact='El usuario con lector de pantalla no conoce la función del botón.',
                        evidence={'code_excerpt': btn['full_open'][:120]},
                        recommendation='Añadir `aria-label="..."` claro en <button> y `aria-hidden="true"` en SVG decorativo.',
                        required_verification='Comprobar nombre accesible calculado en árbol de accesibilidad.',
                    ))
                elif static_vis and aria_val and static_vis.lower() not in aria_val.lower():
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-LABEL-IN-NAME',
                        classification='wcag_violation',
                        category='accessible_names',
                        wcag_criterion='2.5.3 Label in Name',
                        wcag_level='A',
                        severity='MEDIUM',
                        evidence_type='code_hypothesis',
                        title=f'Discrepancia Label in Name: texto visible "{static_vis}" ausente en aria-label "{aria_val}"',
                        element='<button>',
                        location=loc,
                        file_path=path,
                        impact='Rompe comandos por voz ("hacer clic en ...") porque el nombre accesible no incluye el texto visible.',
                        evidence={'visible_text': static_vis, 'aria_label': aria_val},
                        recommendation=f'Iniciar aria-label con "{static_vis}" o eliminar el aria-label si el texto visible basta.',
                        required_verification='Comprobar nombre calculado en árbol de accesibilidad.',
                    ))

            for im in _scan_jsx_tags(content, 'img'):
                if not _jsx_has_attr(im['attrs'], 'alt') and '...' not in im['attrs']:
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-IMG-MISSING-ALT',
                        classification='wcag_violation',
                        category='alt_text',
                        wcag_criterion='1.1.1 Non-text Content',
                        wcag_level='A',
                        severity='HIGH',
                        evidence_type='code_hypothesis',
                        title='Etiqueta <img> sin atributo `alt`',
                        element='<img>',
                        location=f'{path}:{im["line"]}',
                        file_path=path,
                        impact='Lectores de pantalla anuncian la URL o nombre de archivo en lugar del contenido o acción.',
                        evidence={'code_excerpt': im['full_open'][:120]},
                        recommendation='Añadir alt descriptivo del producto/acción o alt="" si la imagen es decorativa.',
                        required_verification='Revisar atributo alt renderizado.',
                    ))

            for tag_k in ('div', 'span'):
                for node in _scan_jsx_tags(content, tag_k):
                    if _jsx_has_attr(node['attrs'], 'onclick') or _jsx_has_attr(node['attrs'], 'onClick'):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-NON-SEMANTIC-CLICKABLE',
                            classification='wcag_violation',
                            category='semantics',
                            wcag_criterion='2.1.1 Keyboard & 4.1.2 Name, Role, Value',
                            wcag_level='A',
                            severity='HIGH',
                            evidence_type='code_hypothesis',
                            title='Elemento no semántico <div>/<span> con manejador click en lugar de <button> o <a href>',
                            element=f'<{tag_k}>',
                            location=f'{path}:{node["line"]}',
                            file_path=path,
                            impact='Inaccesible desde teclado (sin Tab/Enter/Space) y sin rol interactivo en lector de pantalla.',
                            evidence={'code_excerpt': node['full_open'][:120]},
                            recommendation='Reemplazar por <button type="button"> para acciones o <a href="..."> si navega.',
                            required_verification='Confirmar operación con Tab, Enter y Space.',
                        ))
                    role_val = (_jsx_get_attr(node['attrs'], 'role') or '').lower()
                    if role_val in INTERACTIVE_ARIA_ROLES and not (
                        _jsx_has_attr(node['attrs'], 'onKeyDown') or _jsx_has_attr(node['attrs'], 'onkeydown') or _jsx_has_attr(node['attrs'], 'tabIndex') or _jsx_has_attr(node['attrs'], 'tabindex')
                    ):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-ARIA-ROLE-MISSING-KEYBOARD',
                            classification='wcag_violation',
                            category='kb_and_focus',
                            wcag_criterion='2.1.1 Keyboard & 4.1.2 Name, Role, Value',
                            wcag_level='A',
                            severity='HIGH',
                            evidence_type='code_hypothesis',
                            title=f'Elemento <{tag_k} role="{role_val}"> sin tabindex ni manejador de teclado (onKeyDown)',
                            element=f'<{tag_k} role="{role_val}">',
                            location=f'{path}:{node["line"]}',
                            file_path=path,
                            impact='Promete un control interactivo sin operabilidad por teclado.',
                            evidence={'code_excerpt': node['full_open'][:120]},
                            recommendation='Usar elemento HTML nativo (<button>/<a href>) o implementar patrón APG con tabIndex y onKeyDown.',
                            required_verification='Probar navegación por teclado.',
                        ))
                    if not role_val and _jsx_has_attr(node['attrs'], 'aria-label'):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-ARIA-LABEL-ON-GENERIC',
                            classification='wcag_violation',
                            category='aria',
                            wcag_criterion='4.1.2 Name, Role, Value',
                            wcag_level='A',
                            severity='MEDIUM',
                            evidence_type='code_hypothesis',
                            title='Atributo aria-label colocado en <div>/<span> genérico sin rol',
                            element=f'<{tag_k}>',
                            location=f'{path}:{node["line"]}',
                            file_path=path,
                            impact='ARIA 1.2 prohíbe nombrar elementos genéricos.',
                            evidence={'code_excerpt': node['full_open'][:120]},
                            recommendation='Mover el nombre accesible a un elemento semántico.',
                            required_verification='Leer árbol de accesibilidad.',
                        ))
                    if (_jsx_get_attr(node['attrs'], 'aria-hidden') or '').lower() == 'true' and re.search(r'<(?:button|a\b|input|select|textarea)', node['inner'], re.I):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-ARIA-HIDDEN-FOCUSABLE',
                            classification='wcag_violation',
                            category='aria',
                            wcag_criterion='4.1.2 Name, Role, Value & 2.4.3 Focus Order',
                            wcag_level='A',
                            severity='HIGH',
                            evidence_type='code_hypothesis',
                            title='Atributo `aria-hidden="true"` alrededor de elemento enfocable',
                            element='[aria-hidden="true"]',
                            location=f'{path}:{node["line"]}',
                            file_path=path,
                            impact='Crea paradas de tabulación fantasma invisibles para lectores de pantalla.',
                            evidence={'code_excerpt': node['full_open'][:120]},
                            recommendation='Retirar aria-hidden del contenedor interactivo o usar `inert`.',
                            required_verification='Verificar tabulación.',
                        ))

            for tag_f in ('input', 'select', 'textarea'):
                for fc in _scan_jsx_tags(content, tag_f):
                    attrs = fc['attrs']
                    itype = (_jsx_get_attr(attrs, 'type') or '').lower()
                    if tag_f == 'input' and itype in ('hidden', 'submit', 'button', 'reset', 'image'):
                        continue
                    has_aria = _jsx_has_attr(attrs, 'aria-label') or _jsx_has_attr(attrs, 'aria-labelledby') or '...' in attrs
                    fid = _jsx_get_attr(attrs, 'id')
                    has_for = bool(fid and (re.search(r'for\s*=\s*["\']' + re.escape(fid) + r'["\']', content, re.I) or re.search(r'htmlFor\s*=\s*["\']' + re.escape(fid) + r'["\']', content, re.I)))
                    if not has_aria and not has_for and not re.search(r'<label\b[^>]*>[\s\S]*?' + re.escape(fc['full_open'][:30]), content, re.I):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-FORM-MISSING-LABEL',
                            classification='wcag_violation',
                            category='forms',
                            wcag_criterion='3.3.2 Labels or Instructions & 4.1.2 Name, Role, Value',
                            wcag_level='A',
                            severity='HIGH',
                            evidence_type='code_hypothesis',
                            title=f'Control <{tag_f}> sin <label for> ni `aria-label`',
                            element=f'<{tag_f}>',
                            location=f'{path}:{fc["line"]}',
                            file_path=path,
                            impact='El usuario no recibe etiqueta permanente para el campo.',
                            evidence={'code_excerpt': fc['full_open'][:120]},
                            recommendation='Vincular <label htmlFor="..."> o aria-label.',
                            required_verification='Verificar anuncio de nombre.',
                        ))
                    field_key = (_jsx_get_attr(attrs, 'name') or itype or '').lower()
                    matched_ac = next((ac for k, ac in USER_AUTOCOMPLETE_FIELDS.items() if k in field_key), None)
                    if matched_ac and not (_jsx_has_attr(attrs, 'autocomplete') or _jsx_has_attr(attrs, 'autoComplete')):
                        add_src(_make_finding(
                            issue_id='A11Y-SRC-MISSING-AUTOCOMPLETE',
                            classification='wcag_violation',
                            category='forms',
                            wcag_criterion='1.3.5 Identify Input Purpose',
                            wcag_level='AA',
                            severity='MEDIUM',
                            evidence_type='code_hypothesis',
                            title=f'Campo de usuario sin atributo `autoComplete="{matched_ac}"`',
                            element=f'<{tag_f} name="{field_key}">',
                            location=f'{path}:{fc["line"]}',
                            file_path=path,
                            impact='Impide autocompletado de navegadores.',
                            evidence={'expected_autocomplete': matched_ac},
                            recommendation=f'Añadir autoComplete="{matched_ac}" al control.',
                            required_verification='Probar autocompletado.',
                        ))

            for nav in _scan_jsx_tags(content, 'nav'):
                if (_jsx_get_attr(nav['attrs'], 'role') or '').lower() == 'menu':
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-NAV-USING-ROLE-MENU',
                        classification='wcag_violation',
                        category='aria',
                        wcag_criterion='4.1.2 Name, Role, Value',
                        wcag_level='A',
                        severity='MEDIUM',
                        evidence_type='code_hypothesis',
                        title='Navegación web marcada incorrectamente con role="menu"',
                        element='<nav role="menu">',
                        location=f'{path}:{nav["line"]}',
                        file_path=path,
                        impact='Anuncia menú de aplicación de escritorio.',
                        evidence={'code_excerpt': nav['full_open'][:120]},
                        recommendation='Usar <nav aria-label="..."> con lista <ul>/<li>.',
                        required_verification='Comprobar rol landmark.',
                    ))

        # 3. Reglas por línea comunes (CSS, tabindex, onPaste, aria-live, viewport, drag, overlays)
        for idx, line in enumerate(lines, start=1):
            llower = line.lower()

            tab_m = re.search(r'\btabindex\s*=\s*(?:["\'](\d+)["\']|\{(\d+)\})', llower)
            if tab_m:
                tab_val = int(tab_m.group(1) or tab_m.group(2))
                if tab_val > 0:
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-POSITIVE-TABINDEX',
                        classification='wcag_violation',
                        category='kb_and_focus',
                        wcag_criterion='2.4.3 Focus Order',
                        wcag_level='A',
                        severity='HIGH',
                        evidence_type='code_hypothesis',
                        title=f'Valor positivo de tabindex ({tab_val}) altera el orden natural de tabulación',
                        element=f'[tabindex="{tab_val}"]',
                        location=f'{path}:{idx}',
                        file_path=path,
                        impact='Hace saltar el foco de forma errática antes de la navegación estándar.',
                        evidence={'tab_order_value': tab_val, 'code_excerpt': line.strip()[:120]},
                        recommendation='Corregir el orden en el DOM y emplear exclusivamente tabindex="0" o "-1".',
                        required_verification='Recorrer toda la página con Tab en navegador.',
                    ))

            if ('outline: none' in llower or 'outline:none' in llower or 'outline: 0' in llower or 'outline-none' in llower) and 'focus-visible' not in llower and not has_focus_visible:
                add_src(_make_finding(
                    issue_id='A11Y-SRC-OUTLINE-REMOVED',
                    classification='wcag_violation',
                    category='focus',
                    wcag_criterion='2.4.7 Focus Visible',
                    wcag_level='AA',
                    severity='HIGH',
                    evidence_type='code_hypothesis',
                    title='Eliminación del anillo de foco (`outline: none` / `outline-none`) sin reemplazo `:focus-visible`',
                    element='button / a / input CSS',
                    location=f'{path}:{idx}',
                    file_path=path,
                    impact='Los usuarios de teclado quedan ciegos sobre el elemento activo en PDP, variantes y checkout.',
                    evidence={'code_excerpt': line.strip()[:120]},
                    recommendation='Conservar indicador nativo o definir `:focus-visible { outline: 2px solid var(--focus-ring, currentColor); outline-offset: 2px; }`.',
                    required_verification='Tabular por todos los controles y comprobar contraste >= 3:1 en bordes de foco.',
                ))

            if 'onpaste' in llower and ('preventdefault' in llower or 'return false' in llower):
                add_src(_make_finding(
                    issue_id='A11Y-SRC-PASTE-BLOCKED',
                    classification='wcag_violation',
                    category='forms',
                    wcag_criterion='3.3.8 Accessible Authentication (Minimum)',
                    wcag_level='AA',
                    severity='HIGH',
                    evidence_type='code_hypothesis',
                    title='Evento `onPaste` bloqueado con `preventDefault()`',
                    element='<input>',
                    location=f'{path}:{idx}',
                    file_path=path,
                    impact='Impide pegar contraseñas, códigos 2FA, cupones o correos desde gestores de contraseñas.',
                    evidence={'code_excerpt': line.strip()[:120]},
                    recommendation='Permitir el pegado libremente y validar tras ingresar o enviar.',
                    required_verification='Comprobar Ctrl/Cmd+V en el campo.',
                ))

            if re.search(r'<button\b[^>]*type\s*=\s*["\']submit["\'][^>]*disabled=\{!', llower) or re.search(r'disabled=\{![a-zA-Z0-9_]*valid', llower):
                add_src(_make_finding(
                    issue_id='A11Y-REC-SUBMIT-DISABLED-UNTIL-VALID',
                    classification='best_practice_recommendation',
                    category='forms',
                    wcag_criterion='Recommendation (Validate on submit instead of disabled={!isValid})',
                    wcag_level='Heuristic',
                    severity='LOW',
                    evidence_type='code_hypothesis',
                    title='Botón de envío deshabilitado dinámicamente antes de enviar (`disabled={!isValid}`)',
                    element='<button type="submit">',
                    location=f'{path}:{idx}',
                    file_path=path,
                    impact='Saca al botón del orden de tabulación y oculta qué campo falta antes de validar.',
                    evidence={'code_excerpt': line.strip()[:120]},
                    recommendation='Mantener el botón habilitado, validar al enviar y enfocar el primer campo con error vinculado vía aria-invalid y aria-describedby.',
                    required_verification='Enviar formulario incompleto y verificar foco al primer error.',
                ))

            for ref_m in re.finditer(r'aria-(?:describedby|labelledby)\s*=\s*["\']([a-zA-Z0-9_-]+)["\']', line, re.I):
                target_id = ref_m.group(1)
                if declared_ids and target_id not in declared_ids and '{' not in target_id:
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-BROKEN-ARIA-REF',
                        classification='wcag_violation',
                        category='aria',
                        wcag_criterion='1.3.1 Info and Relationships & 3.3.1 Error Identification',
                        wcag_level='A',
                        severity='HIGH',
                        evidence_type='code_hypothesis',
                        title=f'Referencia `{ref_m.group(0)}` apunta a ID `#${target_id}` no encontrado en el archivo'.replace('$', ''),
                        element=f'[id="{target_id}"]',
                        location=f'{path}:{idx}',
                        file_path=path,
                        impact='El lector de pantalla no anunciará la descripción ni el mensaje de error asociado.',
                        evidence={'missing_id': target_id},
                        recommendation=f'Asegurar que exista un elemento con id="{target_id}" renderizado en el DOM.',
                        required_verification='Validar en árbol de accesibilidad que la descripción se resuelve.',
                    ))

            if re.search(r'\{\s*\w+\s*&&\s*<[^>]*(?:role\s*=\s*["\']status["\']|aria-live\s*=\s*["\']polite["\'])', line):
                add_src(_make_finding(
                    issue_id='A11Y-SRC-CONDITIONAL-LIVE-REGION',
                    classification='wcag_violation',
                    category='live_announcements',
                    wcag_criterion='4.1.3 Status Messages',
                    wcag_level='AA',
                    severity='MEDIUM',
                    evidence_type='code_hypothesis',
                    title='Región `role="status"` montada condicionalmente junto con su mensaje',
                    element='<div role="status">',
                    location=f'{path}:{idx}',
                    file_path=path,
                    impact='Varios lectores de pantalla ignoran anuncios si el contenedor live region no existía previamente vacío en el DOM.',
                    evidence={'code_excerpt': line.strip()[:120]},
                    recommendation='Renderizar la región vacía `<div role="status">` de forma estable y actualizar únicamente su texto interno.',
                    required_verification='Probar con lector de pantalla real al añadir al carrito o filtrar.',
                ))

            if 'aria-live="assertive"' in llower or "aria-live='assertive'" in llower:
                if any(ok_w in llower for ok_w in ('success', 'saved', 'added', 'agregado', 'guardado', 'cart', 'status')):
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-ASSERTIVE-ON-STATUS',
                        classification='best_practice_recommendation',
                        category='live_announcements',
                        wcag_criterion='Recommendation (Prefer role="status" / polite for non-urgent updates)',
                        wcag_level='Heuristic',
                        severity='LOW',
                        evidence_type='code_hypothesis',
                        title='Uso de `aria-live="assertive"` para una actualización de estado no urgente',
                        element='[aria-live="assertive"]',
                        location=f'{path}:{idx}',
                        file_path=path,
                        impact='Interrumpe abruptamente lo que el lector de pantalla estaba leyendo al usuario.',
                        evidence={'code_excerpt': line.strip()[:120]},
                        recommendation='Cambiar a `role="status"` (`aria-live="polite"`) reservando `role="alert"` solo para errores urgentes.',
                        required_verification='Comprobar anuncios secuenciales en lector de pantalla.',
                    ))

            if 'user-scalable=no' in llower or 'user-scalable=0' in llower or re.search(r'maximum-scale\s*=\s*1(?:\.0)?\b', llower):
                add_src(_make_finding(
                    issue_id='A11Y-SRC-ZOOM-BLOCKED',
                    classification='wcag_violation',
                    category='zoom_and_reflow',
                    wcag_criterion='1.4.4 Resize Text',
                    wcag_level='AA',
                    severity='HIGH',
                    evidence_type='code_hypothesis',
                    title='Meta viewport bloquea zoom (`user-scalable=no` / `maximum-scale=1`)',
                    element='<meta name="viewport">',
                    location=f'{path}:{idx}',
                    file_path=path,
                    impact='Impide a usuarios con baja visión hacer zoom a 200%.',
                    evidence={'code_excerpt': line.strip()[:120]},
                    recommendation='Eliminar `user-scalable=no` y `maximum-scale=1`.',
                    required_verification='Verificar zoom 200% y reflow 320px.',
                ))

            if 'ondragstart' in llower or 'draggable="true"' in llower or "draggable='true'" in llower:
                has_pointer_alt = bool(re.search(
                    r'<button\b[^>]*>[^<]*(?:move|mover|subir|bajar|up|down|prev|next|anterior|siguiente|reorder|reordenar)',
                    lower,
                ))
                if not has_pointer_alt:
                    add_src(_make_finding(
                        issue_id='A11Y-SRC-DRAG-WITHOUT-POINTER-ALT',
                        classification='wcag_violation',
                        category='touch_targets',
                        wcag_criterion='2.5.7 Dragging Movements',
                        wcag_level='AA',
                        severity='HIGH',
                        evidence_type='code_hypothesis',
                        title='Interacción basada en arrastre sin alternativa de puntero simple ni teclado',
                        element='draggable element',
                        location=f'{path}:{idx}',
                        file_path=path,
                        impact='Impide operar la función a usuarios que no pueden mantener un gesto de arrastre.',
                        evidence={'code_excerpt': line.strip()[:120]},
                        recommendation='Añadir botones de acción simple (anterior/siguiente o mover) accesibles por clic y teclado.',
                        required_verification='Probar acción completa con un solo toque/clic y mediante Tab/Enter.',
                    ))

            if ('glow' in llower or 'scrim' in llower or 'sheen' in llower) and 'inset-0' in llower and 'pointer-events-none' not in llower:
                add_src(_make_finding(
                    issue_id='A11Y-SRC-DECORATIVE-LAYER-BLOCKS-HITS',
                    classification='wcag_violation',
                    category='touch_targets',
                    wcag_criterion='2.1.1 Keyboard & Pointer Hit Area Integrity',
                    wcag_level='A',
                    severity='MEDIUM',
                    evidence_type='code_hypothesis',
                    title='Capa decorativa superpuesta sin `pointer-events-none`',
                    element='decorative overlay',
                    location=f'{path}:{idx}',
                    file_path=path,
                    impact='Puede interceptar clics/toques dirigidos al control subyacente.',
                    evidence={'code_excerpt': line.strip()[:120]},
                    recommendation='Añadir `pointer-events: none` (y `aria-hidden="true"` si es elemento DOM).',
                    required_verification='Confirmar pulsación sobre toda el área visual del control.',
                ))

        # 4. Chequeos a nivel de componente / archivo
        if any(k in lower for k in ('cart-drawer', 'cartdrawer', 'role="dialog"', "role='dialog'", 'modal-overlay', 'mobile-menu-drawer')):
            is_native_dialog = '<dialog' in lower and 'showmodal(' in lower
            has_dialog_aria = 'role="dialog"' in lower or "role='dialog'" in lower
            has_modal_attr = 'aria-modal="true"' in lower or "aria-modal='true'" in lower or "aria-modal={'true'}" in lower
            has_name = 'aria-labelledby' in lower or 'aria-label' in lower
            has_escape_or_inert = 'escape' in lower or '.inert' in lower or 'inert=' in lower
            if not is_native_dialog and (not has_dialog_aria or not has_modal_attr or not has_name or not has_escape_or_inert):
                missing_parts = []
                if not has_dialog_aria:
                    missing_parts.append('role="dialog"')
                if not has_modal_attr:
                    missing_parts.append('aria-modal="true"')
                if not has_name:
                    missing_parts.append('aria-labelledby / aria-label')
                if not has_escape_or_inert:
                    missing_parts.append('Escape + inert/focus-trap')
                add_src(_make_finding(
                    issue_id='A11Y-SRC-DRAWER-MODAL-FOCUS-INCOMPLETE',
                    classification='wcag_violation',
                    category='dialogs',
                    wcag_criterion='2.1.2 No Keyboard Trap, 2.4.3 Focus Order & 4.1.2 Name, Role, Value',
                    wcag_level='A',
                    severity='HIGH',
                    evidence_type='code_hypothesis',
                    title=f'Modal / cart drawer personalizado incompleto: falta {", ".join(missing_parts)}',
                    element='dialog / drawer container',
                    location=f'{path}:1',
                    file_path=path,
                    impact='Sin trampa/restauración de foco ni atributo modal, el teclado escapa al fondo oculto.',
                    evidence={'missing_dialog_contracts': missing_parts},
                    recommendation='Preferir <dialog> con showModal() o añadir role="dialog", aria-modal="true", nombre accesible, inert al fondo, cierre con Escape y restauración de foco al disparador.',
                    required_verification='Abrir drawer con teclado, recorrer con Tab, pulsar Escape y validar retorno del foco.',
                ))

        if ('@keyframes' in lower or 'animation:' in lower or 'animate-' in lower) and not has_reduced_motion:
            add_src(_make_finding(
                issue_id='A11Y-SRC-MISSING-REDUCED-MOTION',
                classification='wcag_violation',
                category='reduced_motion',
                wcag_criterion='2.3.3 Animation from Interactions / Reduced Motion Trigger',
                wcag_level='AA',
                severity='HIGH',
                evidence_type='code_hypothesis',
                title='Animación CSS/UI sin `@media (prefers-reduced-motion)` ni variantes `motion-reduce`/`motion-safe`',
                element='@keyframes / animation',
                location=f'{path}:1',
                file_path=path,
                impact='Mantiene desplazamientos y escalados animados para usuarios con preferencia de movimiento reducido.',
                evidence={'prefers_reduced_motion_detected': False},
                recommendation='Envolver movimiento/escala/blur en `@media (prefers-reduced-motion: no-preference)` o sustituir por transición de opacidad.',
                required_verification='Activar prefers-reduced-motion: reduce en DevTools y verificar ausencia de movimiento vestibular.',
            ))

        if ('<video' in lower and 'autoplay' in lower or 'autoplay: true' in lower or 'autoplay=true' in lower) and not any(p in lower for p in ('pause', 'stop', 'pausar', 'detener', 'controls')):
            add_src(_make_finding(
                issue_id='A11Y-SRC-AUTOPLAY-NO-PAUSE-CONTROL',
                classification='wcag_violation',
                category='reduced_motion',
                wcag_criterion='2.2.2 Pause, Stop, Hide',
                wcag_level='A',
                severity='HIGH',
                evidence_type='code_hypothesis',
                title='Contenido multimedia o carrusel automático (`autoplay`) sin control visible para pausar/detener',
                element='<video autoplay> / carousel',
                location=f'{path}:1',
                file_path=path,
                impact='Causa distracción continua o incapacidad de leer contenido móvil >5s.',
                evidence={'autoplay_detected': True, 'pause_control_detected': False},
                recommendation='Proporcionar botón accesible de Pausa/Reproducción o iniciar el carrusel pausado.',
                required_verification='Comprobar control visible y operable por teclado tras 5 segundos.',
            ))

        if has_sticky_chrome and not has_scroll_padding:
            add_src(_make_finding(
                issue_id='A11Y-SRC-STICKY-NO-SCROLL-PADDING',
                classification='wcag_violation',
                category='focus',
                wcag_criterion='2.4.11 Focus Not Obscured (Minimum)',
                wcag_level='AA',
                severity='MEDIUM',
                evidence_type='code_hypothesis',
                title='Cabecera o barra `sticky`/`fixed` sin `scroll-padding-block-start` / `scroll-margin`',
                element='sticky header / scroller',
                location=f'{path}:1',
                file_path=path,
                impact='Al tabular hacia atrás o saltar a anclas, el elemento enfocado puede quedar tapado por el header.',
                evidence={'has_sticky_chrome': True, 'has_scroll_padding': False},
                recommendation='Definir `scroll-padding-block-start` igual a la altura de la cabecera sticky en el contenedor desplazable.',
                required_verification='Tabular de abajo hacia arriba en viewport móvil/desktop verificando visibilidad completa.',
            ))

        if ('border-color: red' in lower or 'border-red-' in lower or 'color: red' in lower) and 'aria-invalid' not in lower and 'error' in lower:
            add_src(_make_finding(
                issue_id='A11Y-SRC-ERROR-BY-COLOR-ONLY',
                classification='wcag_violation',
                category='forms',
                wcag_criterion='1.4.1 Use of Color & 3.3.1 Error Identification',
                wcag_level='A',
                severity='MEDIUM',
                evidence_type='code_hypothesis',
                title='Indicación visual de error apoyada únicamente en color rojo sin texto/icono ni `aria-invalid`',
                element='form error styling',
                location=f'{path}:1',
                file_path=path,
                impact='Inaccesible para personas con daltonismo o lectores de pantalla.',
                evidence={'color_only_error_hint': True},
                recommendation='Acompañar el error con mensaje textual vinculado vía `aria-describedby`, `aria-invalid="true"` e icono.',
                required_verification='Validar envío fallido y lectura por tecnología de asistencia.',
            ))

    return hypotheses, recs


def audit_better_accessibility(
    source_files: dict[str, str] | None = None,
    *,
    rendered: dict | None = None,
    framework: str | None = None,
    quality_audit_report: dict | None = None,
    design_report: dict | None = None,
) -> dict[str, Any]:
    """Auditoría WCAG 2.2 A/AA Better Accessibility (Etapa 7/9) con análisis estructural multilínea."""
    files = source_files or {}
    detected_fw = perf_model.infer_framework(framework, files)
    candidates_map = perf_model.FRAMEWORK_CANDIDATES.get(detected_fw, perf_model.FRAMEWORK_CANDIDATES['tiendanube-ipanema'])

    verified_by_tool: list[dict] = []
    code_hypothesis: list[dict] = []
    recommendations: list[dict] = []
    requires_external_verification: list[dict] = []
    reused_findings: list[str] = []
    reused_engines: list[str] = []

    if isinstance(quality_audit_report, dict) and quality_audit_report.get('skill') == 'web-quality-audit':
        reused_engines.append('web-quality-audit')
        for item in quality_audit_report.get('verified_issues') or []:
            if isinstance(item, dict) and item.get('category') in ('accessibility', 'interaction') and item.get('id'):
                reused_findings.append(str(item['id']))
    if isinstance(design_report, dict) and design_report.get('skill') == 'web-design-guidelines':
        reused_engines.append('web-design-guidelines')
        for item in (design_report.get('verified_by_tool') or []) + (design_report.get('code_hypothesis') or []):
            if isinstance(item, dict) and item.get('id'):
                reused_findings.append(str(item['id']))

    if isinstance(rendered, dict):
        r_verified, r_recs = _audit_rendered_dom(rendered, candidates_map, files)
        verified_by_tool.extend(r_verified)
        recommendations.extend(r_recs)
        if not rendered.get('contrast_samples'):
            requires_external_verification.append({
                'id': 'A11Y-EXT-COMPUTED-CONTRAST',
                'category': 'contrast',
                'evidence_type': 'requires_external_verification',
                'title': 'Medición computada de contraste (1.4.3 / 1.4.11 AA) sobre estilos finales e imágenes',
                'reason': 'No se aportaron pares fg/bg computados del navegador; no se infiere ni inventa incumplimiento sin medición.',
                'required_check': 'Medir relación de contraste (4.5:1 texto, 3:1 texto grande y bordes UI/foco) en DevTools.',
            })
    else:
        requires_external_verification.append({
            'id': 'A11Y-EXT-COMPUTED-CONTRAST',
            'category': 'contrast',
            'evidence_type': 'requires_external_verification',
            'title': 'Medición computada de contraste (1.4.3 / 1.4.11 AA)',
            'reason': 'El análisis estático de plantillas no calcula el contraste renderizado real de colores finales.',
            'required_check': 'Medir pares de color renderizados en navegador real antes de reportar fallos 1.4.3 / 1.4.11.',
        })

    has_manual_walks = isinstance(rendered, dict) and bool(rendered.get('keyboard_walk_verified')) and bool(rendered.get('screen_reader_walk_verified'))
    if not has_manual_walks:
        requires_external_verification.append({
            'id': 'A11Y-EXT-KEYBOARD-AND-SCREEN-READER-WALKS',
            'category': 'keyboard_nav',
            'evidence_type': 'requires_external_verification',
            'title': 'Recorrido completo por teclado y lector de pantalla (NVDA / VoiceOver)',
            'reason': 'El análisis estático o automático no certifica que todo el flujo de compra, variantes y cart drawer sea operable con lector de pantalla real.',
            'required_check': 'Ejecutar recorrido Keyboard-only Walk (Tab, Shift+Tab, Enter, Space, Escape, flechas) y Screen-reader Walk sobre el navegador real.',
        })

    s_hypotheses, s_recs = _audit_source_files(files)
    code_hypothesis.extend(s_hypotheses)
    recommendations.extend(s_recs)

    detected_css_variables = sorted({
        tok
        for content in files.values()
        if isinstance(content, str)
        for tok in re.findall(r'--(?:color|font|space|radius|shadow|btn|text|bg|focus)-[a-zA-Z0-9_-]+', content)
    })
    protected_contracts = []
    for path, content in sorted(files.items()):
        if isinstance(content, str):
            hits = sorted(set(perf_model.DESIGN_COMMERCE_CONTRACT_MARKERS.findall(content)))
            if hits:
                protected_contracts.append({'file': path, 'contracts': hits})

    severity_rank = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    verified_by_tool.sort(key=lambda x: (severity_rank.get(x['severity'], 9), x['wcag_criterion'], x['id']))
    code_hypothesis.sort(key=lambda x: (severity_rank.get(x['severity'], 9), x['wcag_criterion'], x['id']))
    recommendations.sort(key=lambda x: (severity_rank.get(x['severity'], 9), x['id']))

    wcag_breakdown: dict[str, int] = {}
    for item in verified_by_tool + code_hypothesis:
        crit = item['wcag_criterion']
        wcag_breakdown[crit] = wcag_breakdown.get(crit, 0) + 1

    has_high = any(f['severity'] == 'HIGH' for f in verified_by_tool + code_hypothesis)
    verdict = 'Block' if has_high else 'Needs_External_Verification' if requires_external_verification else 'Approve'

    return perf_model.sanitize({
        'kind': 'better-accessibility-audit',
        'skill': 'better-accessibility',
        'framework': detected_fw,
        'ecommerce_surfaces': _detect_ecommerce_surfaces(files, rendered),
        'rules_source': {
            'repository': 'jakubkrehel/skills',
            'path': 'skills/better-accessibility',
            'commit': '547d415dc10a23e66088eba5aa6664e6e772432c',
            'skill_git_blob_sha1': 'b5293ecc20e4356a50a55e1a1eadd3db9a0019a7',
            'license': 'MIT',
            'static_verification_only': True,
        },
        'reused_engines': list(dict.fromkeys(reused_engines)) + ['ipanema-visual-qa'],
        'reused_prior_findings': list(dict.fromkeys(reused_findings)),
        'brand_and_commerce_guards': {
            'preserve_brand_identity': True,
            'preserve_cart_checkout_variants': True,
            'detected_css_variables': detected_css_variables,
            'protected_commerce_contracts': protected_contracts,
            'note': 'Las correcciones de accesibilidad conservan selectores js-*, data-store, LS.*, /cart/add, variantes, tokens CSS y diseño visual de marca.',
        },
        'verified_by_tool': verified_by_tool,
        'code_hypothesis': code_hypothesis,
        'best_practice_recommendations': recommendations,
        'requires_external_verification': requires_external_verification,
        'wcag_criteria_breakdown': wcag_breakdown,
        'verdict': verdict,
        'static_certification_claimed': False,
        'counts': {
            'wcag_violations_verified': len(verified_by_tool),
            'wcag_violations_hypothesis': len(code_hypothesis),
            'wcag_violations_total': len(verified_by_tool) + len(code_hypothesis),
            'recommendations': len(recommendations),
            'requires_external_verification': len(requires_external_verification),
            'high': sum(1 for i in verified_by_tool + code_hypothesis if i['severity'] == 'HIGH'),
            'medium': sum(1 for i in verified_by_tool + code_hypothesis if i['severity'] == 'MEDIUM'),
            'low': sum(1 for i in verified_by_tool + code_hypothesis + recommendations if i['severity'] == 'LOW'),
        },
        'limitations': [
            'El análisis estático o automático no certifica cumplimiento completo WCAG 2.2 AA sin prueba real de teclado y lector de pantalla.',
            'Las preferencias visuales y criterios AAA/heurísticos (ej. objetivo táctil 44x44px o único H1) se reportan como recomendaciones y nunca como fallos WCAG AA.',
            'El contraste (1.4.3 / 1.4.11) solo se declara incumplido cuando existe evidencia medible de pares fg/bg.',
        ],
    })


def _attr_insert_offset(content: str, node: html_liquid.HtmlNode) -> int:
    """Devuelve el offset exacto antes de espacios+('/>'|'>') en la apertura para conservar formato limpio."""
    raw = node.start_tag_raw
    stripped_end = len(raw.rstrip())
    closing_len = 2 if raw[:stripped_end].endswith('/>') else 1
    before_close = raw[:stripped_end - closing_len]
    ws_tail = len(before_close) - len(before_close.rstrip(' \t'))
    return node.open_start + stripped_end - closing_len - ws_tail


def _has_open_dynamic_liquid_spread(node: html_liquid.HtmlNode, content: str) -> bool:
    """Detecta {{ ... }} o {% ... %} sueltos en la cabecera del tag fuera de valores de atributo comillados."""
    if not node.has_liquid_attr:
        return False
    masked, _ = html_liquid.mask_liquid_constructs(node.start_tag_raw)
    without_quoted = re.sub(r'=\s*(?:"[^"]*"|\'[^\']*\')', '=""', masked)
    return 'LIQOUT' in without_quoted or '{%' in without_quoted or '{{' in without_quoted


def _safe_css_transforms(css_text: str, base_offset: int) -> tuple[list[tuple[int, int, str]], list[str]]:
    """Propone ediciones CSS idempotentes y seguras dentro de <style> o archivo CSS sin romper Liquid."""
    edits: list[tuple[int, int, str]] = []
    notes: list[str] = []
    # Enmascarar Liquid dentro de CSS antes de analizar
    masked, _ = html_liquid.mask_liquid_constructs(css_text)
    lower = masked.lower()

    if re.search(r'outline\s*:\s*none\s*;?', lower) and ':focus-visible' not in lower:
        for m in re.finditer(r'outline\s*:\s*none\s*;?', lower):
            edits.append((base_offset + m.start(), base_offset + m.end(), '/* outline:none replaced with :focus-visible */'))
        edits.append((base_offset + len(css_text), base_offset + len(css_text), '\n:focus-visible { outline: 2px solid var(--focus-ring, currentColor); outline-offset: 2px; }\n'))
        notes.append('2.4.7 Focus Visible')

    if '@keyframes' in lower and 'prefers-reduced-motion' not in lower:
        edits.append((
            base_offset + len(css_text),
            base_offset + len(css_text),
            '\n@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; } }\n',
        ))
        notes.append('Reduced Motion')

    return edits, notes


def _post_patch_verify(path: str, before_text: str, before_parsed: html_liquid.ParsedDocument, after_text: str) -> tuple[bool, str | None]:
    """Valida invariantes estructurales, preservación exacta de Liquid y contratos comerciales tras parchear."""
    after_parsed = html_liquid.parse_structural_document(path, after_text)
    if len(after_parsed.misnested_events) > len(before_parsed.misnested_events):
        return False, 'La transformación introdujo etiquetas HTML cruzadas o mal anidadas.'
    if len(after_parsed.unclosed_tags) > len(before_parsed.unclosed_tags):
        return False, 'La transformación dejó etiquetas HTML sin cerrar.'
    if [s.raw for s in after_parsed.liquid_spans] != [s.raw for s in before_parsed.liquid_spans]:
        return False, 'La transformación alteró expresiones o bloques Liquid existentes.'
    before_contracts = perf_model.DESIGN_COMMERCE_CONTRACT_MARKERS.findall(before_text)
    after_contracts = perf_model.DESIGN_COMMERCE_CONTRACT_MARKERS.findall(after_text)
    if sorted(before_contracts) != sorted(after_contracts):
        return False, 'La transformación alteró selectores o contratos comerciales protegidos.'
    if not after_parsed.balanced and not before_parsed.balanced:
        # Si ya estaba desbalanceado originalmente, exigir mismo número de tags totales clave
        if after_text.count('<button') != after_text.count('</button>'):
            return False, 'Conteo de apertura/cierre de <button> inconsistente tras parchear.'
    return True, None


def propose_safe_accessibility_fixes(source_files: dict[str, str]) -> dict[str, Any]:
    """Genera correcciones estructurales seguras e idempotentes por tipo de archivo; se abstiene ante JSX sin AST o HTML ambiguo."""
    patched_files: dict[str, str] = {}
    changes: list[dict[str, str]] = []
    diffs: list[str] = []
    strategy_by_file: dict[str, dict[str, Any]] = {}
    abstained_files: list[dict[str, str]] = []
    abstained_elements: list[dict[str, Any]] = []
    manual_proposals: list[dict[str, Any]] = []
    post_patch_verified: dict[str, bool] = {}

    for path, content in sorted(source_files.items()):
        if not isinstance(content, str):
            continue
        parsed = html_liquid.parse_structural_document(path, content)
        file_kind = parsed.file_kind

        # 1. Regla estricta JSX / TSX / JS: si no hay parser AST JSX/TSX verificado instalado, deshabilitar escritura automática
        if file_kind in ('jsx', 'tsx', 'js'):
            ast_avail = bool(parsed.jsx_parser_info.get('available'))
            if not ast_avail:
                strategy_by_file[path] = {
                    'file_kind': file_kind,
                    'parser': 'jsx-brace-diagnostic-only',
                    'auto_apply_enabled': False,
                }
                patched_files[path] = content
                post_patch_verified[path] = True
                reason = f'Archivo {file_kind.upper()} omitido de escritura automática: no existe un parser AST JSX/TSX verificado en el entorno autorizado.'
                abstained_files.append({'file': path, 'reason': reason})
                file_diag = _audit_source_files({path: content})[0]
                for diag in file_diag:
                    manual_proposals.append({
                        'file': path,
                        'location': diag['location'],
                        'rule': diag['wcag_criterion'],
                        'element': diag['element'],
                        'proposal': diag['recommendation'],
                        'auto_applied': False,
                    })
                continue

        # 2. CSS puro
        if file_kind == 'css':
            strategy_by_file[path] = {'file_kind': 'css', 'parser': 'liquid-masked-css', 'auto_apply_enabled': True}
            edits, notes = _safe_css_transforms(content, 0)
            updated, ok_edit = html_liquid.apply_text_edits(content, edits)
            if not ok_edit:
                patched_files[path] = content
                post_patch_verified[path] = False
                abstained_files.append({'file': path, 'reason': 'Solapamiento inesperado de rangos CSS.'})
                continue
            for n in notes:
                changes.append({'file': path, 'rule': n, 'change': f'Ajuste CSS seguro ({n}).'})
            patched_files[path] = updated
            post_patch_verified[path] = True
            if updated != content:
                diffs.extend(difflib.unified_diff(content.splitlines(), updated.splitlines(), fromfile=f'a/{path}', tofile=f'b/{path}', lineterm=''))
            continue

        # 3. HTML / Liquid estructural
        strategy_by_file[path] = {'file_kind': file_kind, 'parser': 'stdlib-HTMLParser+LiquidMask', 'auto_apply_enabled': True}
        if not parsed.balanced:
            patched_files[path] = content
            post_patch_verified[path] = False
            abstained_files.append({
                'file': path,
                'reason': 'Estructura HTML desbalanceada o etiquetas cruzadas en archivo origen; se abstiene de aplicar ediciones automáticas.',
            })
            continue

        edits: list[tuple[int, int, str]] = []
        file_changes: list[dict[str, str]] = []
        edited_nodes: set[int] = set()

        for node in parsed.nodes:
            if node.has_jsx_syntax:
                abstained_elements.append({'file': path, 'line': node.line, 'tag': node.tag, 'reason': 'Expresión sintáctica JSX detectada dentro de HTML/Liquid.'})
                manual_proposals.append({'file': path, 'location': f'{path}:{node.line}', 'rule': 'Syntax safety', 'element': f'<{node.tag}>', 'proposal': 'Aplicar cambio manualmente verificando JSX.', 'auto_applied': False})
                continue

            # A. CSS dentro de nodos <style> reales
            if node.tag == 'style' and node.close_start is not None and not node.misnested:
                css_inner = content[node.open_end:node.close_start]
                css_edits, css_notes = _safe_css_transforms(css_inner, node.open_end)
                edits.extend(css_edits)
                for n in css_notes:
                    file_changes.append({'file': path, 'rule': n, 'change': f'Ajuste CSS seguro dentro de <style> ({n}).'})
                continue

            # B. <img> sin alt (respeta /> vs >)
            if node.tag == 'img' and not node.has_attr('alt'):
                if _has_open_dynamic_liquid_spread(node, content):
                    abstained_elements.append({'file': path, 'line': node.line, 'tag': 'img', 'reason': 'Atributo Liquid dinámico sin nombre fijo en <img>.'})
                    continue
                off = _attr_insert_offset(content, node)
                edits.append((off, off, ' alt="Imagen de producto"'))
                file_changes.append({'file': path, 'rule': '1.1.1 Non-text Content', 'change': 'Añadido atributo alt en <img> preservando sintaxis de cierre.'})
                continue

            # C. <input> sin etiqueta ni aria-label
            if node.tag in ('input', 'select', 'textarea'):
                itype = (node.get_attr('type') or '').lower()
                if not (node.tag == 'input' and itype in ('hidden', 'submit', 'button', 'reset', 'image')):
                    has_aria = bool((node.get_attr('aria-label') or '').strip() or (node.get_attr('aria-labelledby') or '').strip())
                    id_val = node.get_attr('id')
                    has_for = bool(id_val and re.search(r'for\s*=\s*["\']' + re.escape(id_val) + r'["\']', content, re.I))
                    if not has_aria and not has_for and not node.has_ancestor('label'):
                        if _has_open_dynamic_liquid_spread(node, content):
                            abstained_elements.append({'file': path, 'line': node.line, 'tag': node.tag, 'reason': 'Atributos Liquid dinámicos en campo de formulario.'})
                            continue
                        label_text = (node.get_attr('name') or 'Campo').replace('"', '')
                        off = _attr_insert_offset(content, node)
                        edits.append((off, off, f' aria-label="{label_text}"'))
                        file_changes.append({'file': path, 'rule': '3.3.2 / 4.1.2 Input Label', 'change': f'Añadido aria-label a <{node.tag}> preservando cierre.'})
                continue

            # D. <button> multilínea/inline de solo icono sin nombre accesible
            if node.tag == 'button' and not node.misnested and node.close_start is not None:
                has_name = bool(
                    (node.get_attr('aria-label') or '').strip()
                    or (node.get_attr('aria-labelledby') or '').strip()
                    or (node.get_attr('title') or '').strip()
                    or node.collect_visible_text()
                )
                has_svg_child = any(c.tag == 'svg' for c in node.iter_descendants())
                if not has_name and has_svg_child and not _has_open_dynamic_liquid_spread(node, content) and not node.spans_liquid_branch:
                    cls_id = ((node.get_attr('class') or '') + ' ' + (node.get_attr('id') or '')).lower()
                    inferred = 'Cerrar' if ('close' in cls_id or 'cerrar' in cls_id) else 'Acción'
                    off = _attr_insert_offset(content, node)
                    edits.append((off, off, f' aria-label="{inferred}"'))
                    for d in node.iter_descendants():
                        if d.tag == 'svg' and not d.has_attr('aria-hidden'):
                            svg_off = _attr_insert_offset(content, d)
                            edits.append((svg_off, svg_off, ' aria-hidden="true"'))
                            break
                    file_changes.append({'file': path, 'rule': '4.1.2 Accessible Name', 'change': 'Añadido aria-label en <button> de icono y aria-hidden="true" en SVG.'})
                continue

            # E. Cart drawer sin role="dialog" / aria-modal
            if node.tag in ('div', 'section', 'aside') and not node.has_attr('role'):
                cls_id = ((node.get_attr('class') or '') + ' ' + (node.get_attr('id') or '')).lower()
                if 'cart-drawer' in cls_id or 'js-cart-drawer' in cls_id:
                    if id(node) not in edited_nodes and not _has_open_dynamic_liquid_spread(node, content):
                        off = _attr_insert_offset(content, node)
                        edits.append((off, off, ' role="dialog" aria-modal="true" aria-label="Carrito de compras"'))
                        file_changes.append({'file': path, 'rule': '4.1.2 / 2.4.3 Dialog Drawer', 'change': 'Añadido role="dialog", aria-modal="true" y aria-label al cart drawer.'})
                        edited_nodes.add(id(node))

            # F. <div onclick="..."> / <span onclick="..."> hoja plano (NUNCA con hijos bloque/interactivos ni JSX ni ramas Liquid)
            if node.tag in ('div', 'span') and node.has_attr('onclick'):
                has_nested_block = any(d.tag in html_liquid.BLOCK_OR_INTERACTIVE_TAGS for d in node.iter_descendants())
                if (
                    not node.misnested
                    and node.close_start is not None
                    and node.close_end is not None
                    and not has_nested_block
                    and not node.spans_liquid_branch
                    and not node.has_attr('role')
                    and not _has_open_dynamic_liquid_spread(node, content)
                    and id(node) not in edited_nodes
                ):
                    edits.append((node.open_start + 1, node.open_start + 1 + len(node.tag), 'button' + ('' if node.has_attr('type') else ' type="button"')))
                    edits.append((node.close_start, node.close_end, '</button>'))
                    file_changes.append({'file': path, 'rule': '2.1.1 / 4.1.2 Native Button', 'change': f'Convertido <{node.tag}> simple sin hijos bloque en <button type="button">.'})
                    edited_nodes.add(id(node))
                else:
                    reason = (
                        'El elemento contiene etiquetas de bloque o interactivas anidadas (riesgo de HTML cruzado o ruptura visual).'
                        if has_nested_block
                        else 'Elemento cruza ramas Liquid o requiere revisión manual del evento.'
                    )
                    abstained_elements.append({'file': path, 'line': node.line, 'tag': node.tag, 'reason': reason})
                    manual_proposals.append({
                        'file': path,
                        'location': f'{path}:{node.line}',
                        'rule': '2.1.1 Keyboard & 4.1.2 Native Button',
                        'element': f'<{node.tag}>',
                        'proposal': 'Refactorizar manualmente a <button type="button"> o patrón interactivo verificando hijos anidados y eventos.',
                        'auto_applied': False,
                    })

            # G. <meta name="viewport"> bloqueando zoom
            if node.tag == 'meta' and (node.get_attr('name') or '').lower() == 'viewport':
                vp_val = node.get_attr('content') or ''
                if 'user-scalable=no' in vp_val.lower() or 'user-scalable=0' in vp_val.lower() or re.search(r'maximum-scale\s*=\s*1(?:\.0)?\b', vp_val, re.I):
                    m_c = re.search(r'(\bcontent\s*=\s*)(["\'])([^"\']*)(\2)', node.start_tag_raw, re.I)
                    if m_c:
                        new_c = re.sub(r',?\s*user-scalable\s*=\s*(?:no|0)', '', m_c.group(3), flags=re.I)
                        new_c = re.sub(r',?\s*maximum-scale\s*=\s*1(?:\.0)?\b', '', new_c, flags=re.I).strip(' ,')
                        c_start = node.open_start + m_c.start(3)
                        c_end = node.open_start + m_c.end(3)
                        edits.append((c_start, c_end, new_c))
                        file_changes.append({'file': path, 'rule': '1.4.4 Resize Text', 'change': 'Retirado bloqueo de zoom del meta viewport.'})

        updated, ok_edit = html_liquid.apply_text_edits(content, edits)
        if not ok_edit:
            patched_files[path] = content
            post_patch_verified[path] = False
            abstained_files.append({'file': path, 'reason': 'Ediciones de rango en conflicto; transformación abortada de forma segura.'})
            continue

        verified, verify_err = _post_patch_verify(path, content, parsed, updated)
        if not verified:
            patched_files[path] = content
            post_patch_verified[path] = False
            abstained_files.append({'file': path, 'reason': verify_err or 'Fallo de invariante post-parche.'})
            continue

        patched_files[path] = updated
        post_patch_verified[path] = True
        changes.extend(file_changes)
        if updated != content:
            diffs.extend(difflib.unified_diff(
                content.splitlines(),
                updated.splitlines(),
                fromfile=f'a/{path}',
                tofile=f'b/{path}',
                lineterm='',
            ))

    return {
        'patched_files': patched_files,
        'applied_changes': changes,
        'diff': '\n'.join(diffs),
        'changed': any(patched_files.get(p) != source_files[p] for p in source_files),
        'strategy_by_file': strategy_by_file,
        'abstained_files': abstained_files,
        'abstained_elements': abstained_elements,
        'manual_proposals': manual_proposals,
        'post_patch_verified': post_patch_verified,
    }

