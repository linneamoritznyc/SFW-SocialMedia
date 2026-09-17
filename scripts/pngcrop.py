"""Crop a PNG to an exact height, in pure Python.

Headless Chromium reserves about 87px of the window for browser chrome, so a
--window-size of exactly 1080x1080 renders the page into a 1080x993 viewport
and the bottom of the frame is lost. We render tall and crop back here.
"""
import zlib, struct, sys

def decode(path):
    d = open(path, 'rb').read(); i = 8; idat = b''
    while i < len(d):
        ln = struct.unpack('>I', d[i:i+4])[0]; typ = d[i+4:i+8]
        if typ == b'IHDR': w, h, bd, ct = struct.unpack('>IIBB', d[i+8:i+18])
        if typ == b'IDAT': idat += d[i+8:i+8+ln]
        i += 12 + ln
    raw = zlib.decompress(idat); bpp = {0:1, 2:3, 3:1, 4:2, 6:4}[ct]
    stride = w * bpp; prev = bytearray(stride); rows = []; pos = 0
    for _ in range(h):
        f = raw[pos]; pos += 1
        line = bytearray(raw[pos:pos+stride]); pos += stride
        for x in range(stride):
            a = line[x-bpp] if x >= bpp else 0
            b = prev[x]
            c = prev[x-bpp] if x >= bpp else 0
            if f == 1:   line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a+b)//2) & 255
            elif f == 4:
                pa, pb, pc = abs(b-c), abs(a-c), abs(a+b-2*c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        prev = line; rows.append(bytes(line))
    return w, h, bpp, ct, rows

def chunk(typ, data):
    return (struct.pack('>I', len(data)) + typ + data
            + struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff))

def write(path, w, h, ct, rows):
    body = b''.join(b'\x00' + r for r in rows)
    out = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, ct, 0, 0, 0))
           + chunk(b'IDAT', zlib.compress(body, 9))
           + chunk(b'IEND', b''))
    open(path, 'wb').write(out)

if __name__ == '__main__':
    src, keep = sys.argv[1], int(sys.argv[2])
    w, h, bpp, ct, rows = decode(src)
    if h != keep:
        write(src, w, keep, ct, rows[:keep])
