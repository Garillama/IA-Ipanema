# Análisis estático H1 — candidato congelado

Estado: revisión externa registrada; candidato original intacto; segunda revisión independiente todavía pendiente. No se repitieron pruebas y no se accedió a producción.

## Identidad comprobada

- Paquete manual: SHA256 `c10cec1d30ff6f609e4f47378f313bb3b89fa034c84087e4a2fb7cef21172123`.
- Diff candidato: SHA256 `ff73a41106aa153e30f0b84bf018ce89f80d693a68551eb39ab021ce1c09406b`.
- `sections/hero.tpl`: SHA256 `1e70c54c4c5bc38711272284843d8881c4354ac7725e9de56c0223b599c3e65d`.
- `snippets/image.tpl`: SHA256 `e4e622e0c561c4450138e7717a1e5af95cf19d0184aee5cbcb89990f7ada767e`.
- CSS local consultado solo para dependencia estática: `static/css/style-critical.css`, SHA256 `25194781ceb4181689a88d76c0d9ab5ca35614d6cc97902ecf1af568a389c845`.
- Fuentes de la tienda local configurada; no se consultó el storefront ni la API administrativa.

## Fragmento candidato relacionado

En `sections/hero.tpl`, rama de hero responsive posterior:

```twig
image_classes: not is_priority_section ? 'fade-in lazyload',
image_lazy: not is_priority_section,
image_lazy_js: false,
```

La misma rama agrega un hermano `.placeholder.placeholder-fade` para las secciones posteriores.

En `snippets/image.tpl`, la salida añade `loading="lazy"` cuando `image_lazy and not image_lazy_js`, pero el `image_classes` entregado por el caller se conserva en el atributo `class`. Por tanto, al retirar solo la clase `lazyload`, el markup conserva `fade-in` y carga nativa, pero pierde el estado `.lazyloaded` que actualmente comunica el fin de la carga al CSS.

## Evidencia CSS exacta

`static/css/style-critical.css`, bloque “Placeholders and preloaders”:

```css
.lazyloaded+.placeholder-shine,
.lazyloaded+.placeholder-fade,
.swiper-lazy-loaded+.placeholder-shine,
.swiper-lazy-loaded+.placeholder-fade,
picture:has(.lazyloaded)+.placeholder-shine,
picture:has(.lazyloaded)+.placeholder-fade,
picture:has(.swiper-lazy-loaded)+.placeholder-shine,
picture:has(.swiper-lazy-loaded)+.placeholder-fade {
  display: none !important;
}

.fade-in {
  opacity: 0;
  transition: opacity .2s;
}

.fade-in.lazyloaded,
.fade-in.swiper-lazy-loaded,
.fade-in.image-priority-high {
  opacity: 1;
}
```

La carga nativa `loading="lazy"` por sí sola no asigna ninguna de esas clases CSS. No aparece una regla alternativa de `opacity: 1` para `.fade-in` después de que el recurso nativo termine.

## Conclusión estática sobre H1

La recomendación de retirar exclusivamente `lazyload` está incompleta: el CSS del tema usa `.lazyloaded` para revelar la imagen `.fade-in` y ocultar su placeholder. Si se elimina `lazyload` sin cambiar esas dependencias, las hero responsive no prioritarias pueden permanecer con `opacity: 0` y el placeholder puede continuar animándose. Esto es una consecuencia estática de las reglas observadas; no se ejecutó navegador para verificar cascada, evento de carga o timings.

## Aceptación necesaria antes de cerrar H1

La corrección futura debe resolver la carga y el estado visual como una sola unidad. Opción nativa mínima para valorar: quitar ambos `lazyload` y `fade-in` de la rama que use carga nativa, y decidir expresamente qué hacer con su placeholder (por ejemplo, retirarlo en esa rama). Si se conserva fade-in y placeholder, debe existir un estado de carga terminado compatible con `loading="lazy"`, sin reactivar accidentalmente LazySizes ni duplicar requests.

Pruebas de aceptación focalizadas, todavía no ejecutadas:

1. Inspección del HTML generado: variante posterior con `loading="lazy"`, sin clase LazySizes si se adopta carga nativa, proporciones reservadas y sin URL duplicadas.
2. Browser fixture con LazySizes empaquetado presente: imagen fuera de viewport, entrada al umbral, request única, imagen finalmente visible (`opacity: 1`) y placeholder oculto o removido.
3. Caso de fallo de carga: placeholder/estado alternativo no queda en animación infinita y no oculta el error.
4. Primera hero prioritaria permanece visible inmediatamente y no recibe lazyload.
5. No cambiar contenido visual ni estado de banners en otras ramas del helper.

El candidato se mantiene congelado hasta recibir la segunda revisión independiente. Esta nota no aplica H1 ni modifica el código.
