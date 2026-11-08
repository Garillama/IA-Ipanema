"""Comparación PNG RGB/RGBA 8-bit y métricas sin dependencias externas."""
from __future__ import annotations

from pathlib import Path
import struct
import zlib

from .core import IpanemaError, read_json


def paeth(a, b, c):
    p = a + b - c
    pa, pb, pc = abs(p-a), abs(p-b), abs(p-c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c


def read_png(path: Path):
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise IpanemaError("La comparación visual admite PNG, no JPEG/WebP.")
    position, compressed, header = 8, bytearray(), None
    while position + 12 <= len(data):
        length = struct.unpack(">I", data[position:position+4])[0]
        kind = data[position+4:position+8]
        payload = data[position+8:position+8+length]
        if len(payload) != length or position + 12 + length > len(data):
            raise IpanemaError("PNG truncado.")
        expected_crc = struct.unpack(">I", data[position+8+length:position+12+length])[0]
        if zlib.crc32(kind+payload) & 0xffffffff != expected_crc:
            raise IpanemaError("PNG con checksum inválido.")
        if kind == b"IHDR":
            header = struct.unpack(">IIBBBBB", payload)
        elif kind == b"IDAT":
            compressed.extend(payload)
        elif kind == b"IEND":
            break
        position += length + 12
    if not header:
        raise IpanemaError("PNG sin IHDR.")
    width, height, depth, color, comp, filtering, interlace = header
    if depth != 8 or color not in (2, 6) or comp or filtering or interlace or not 0 < width * height <= 20_000_000:
        raise IpanemaError("PNG no soportado: se requiere RGB/RGBA 8-bit, sin interlace, hasta 20 MP.")
    channels = 3 if color == 2 else 4
    stride = width * channels
    size = (stride+1) * height
    decoder = zlib.decompressobj()
    raw = decoder.decompress(bytes(compressed), size+1)
    if len(raw) != size or not decoder.eof:
        raise IpanemaError("Datos PNG inválidos o mayores que sus dimensiones.")
    previous = bytearray(stride)
    pixels = bytearray()
    for y in range(height):
        offset = y * (stride+1)
        mode = raw[offset]
        row = bytearray(raw[offset+1:offset+1+stride])
        if mode > 4:
            raise IpanemaError("Filtro PNG no soportado.")
        for x in range(stride):
            a = row[x-channels] if x >= channels else 0
            b = previous[x]
            c = previous[x-channels] if x >= channels else 0
            predictor = (0, a, b, (a+b)//2, paeth(a, b, c))[mode]
            row[x] = (row[x]+predictor) & 255
        if channels == 4:
            pixels.extend(row)
        else:
            for x in range(0, stride, 3):
                pixels.extend(row[x:x+3] + b"\xff")
        previous = row
    return width, height, pixels


def write_png(path: Path, width: int, height: int, rgba: bytes):
    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind+payload) & 0xffffffff)
    raw = b"".join(b"\0" + rgba[y*width*4:(y+1)*width*4] for y in range(height))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) +
                     chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def visual(before: Path, after: Path, *, pixel_threshold=12, max_changed_ratio=0.005, masks=None, diff_path=None):
    if not 0 <= pixel_threshold <= 255 or not 0 <= max_changed_ratio <= 1:
        raise IpanemaError("Umbrales visuales inválidos.")
    w, h, a = read_png(before)
    w2, h2, b = read_png(after)
    if (w, h) != (w2, h2):
        return {"status": "failed", "reason": "dimensions_changed", "before": [w, h], "after": [w2, h2]}
    rectangles = masks or []
    if any(len(rect) != 4 or any(type(n) is not int for n in rect) or rect[2] < 0 or rect[3] < 0 for rect in rectangles):
        raise IpanemaError("Las máscaras son rectángulos [x,y,ancho,alto].")
    changed, tested = 0, 0
    diff = bytearray(a) if diff_path else None
    for y in range(h):
        for x in range(w):
            if any(rx <= x < rx+rw and ry <= y < ry+rh for rx, ry, rw, rh in rectangles):
                continue
            offset = (y*w+x)*4
            differs = max(abs(a[offset+c]-b[offset+c]) for c in range(4)) > pixel_threshold
            tested += 1
            changed += differs
            if diff is not None and differs:
                diff[offset:offset+4] = b"\xff\x00\x7f\xff"
    if tested == 0:
        raise IpanemaError("Todas las áreas están enmascaradas; no existe una comparación válida.")
    ratio = changed / tested
    if diff_path:
        if diff_path.exists() or diff_path.resolve() in (before.resolve(), after.resolve()):
            raise IpanemaError("El diff debe tener un destino nuevo.")
        write_png(diff_path, w, h, diff)
    return {"status": "passed" if ratio <= max_changed_ratio else "failed", "changed_pixels": changed,
            "tested_pixels": tested, "changed_ratio": ratio, "pixel_threshold": pixel_threshold,
            "max_changed_ratio": max_changed_ratio, "masked_rectangles": rectangles,
            "interpretation": "Una diferencia excedida requiere revisión; no demuestra por sí sola una regresión."}


def metrics(before: Path, after: Path, tolerances=None):
    a, b = read_json(before), read_json(after)
    if not a.get("page") or not a.get("profile") or any(a.get(k) != b.get(k) for k in ("profile", "page", "config", "lighthouse_version", "network_policy")):
        raise IpanemaError("Perfiles o páginas distintos: comparación de rendimiento inválida.")
    tolerances = tolerances or {key: .1 for key in sorted(set(a.get("metrics", {})) | set(b.get("metrics", {})))}
    changes = []
    for key, tolerance in tolerances.items():
        old, new = a.get("metrics", {}).get(key), b.get("metrics", {}).get(key)
        if old is None or new is None:
            changes.append({"metric": key, "status": "not_measured"})
        else:
            limit = old * (1+tolerance)
            changes.append({"metric": key, "before": old, "after": new, "delta": new-old,
                            "status": "regression_candidate" if new > limit else "within_threshold"})
    status = "not_measured" if not changes or all(c["status"] == "not_measured" for c in changes) else "failed" if any(c["status"] == "regression_candidate" for c in changes) else "passed"
    return {"status": status,
            "changes": changes, "field_inp_measured": False, "single_sample_limit": True}
