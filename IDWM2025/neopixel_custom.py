from machine import Pin, bitstream

class NeoPixel:
    ORDER = (1, 0, 2, 3)  # G R B W for WS2815B
    
    def __init__(self, pin, n, bpp=3, timing=1):
        self.pin = pin
        self.n = n
        self.bpp = bpp
        self.buf = bytearray(n * bpp)
        self.pin.init(Pin.OUT)
        self.timing = ((400, 850, 800, 450) if timing else (800, 1700, 1600, 900))
        self.brightness = 1.0  # Default to full brightness

    def __len__(self):
        return self.n

    def __setitem__(self, i, v):
        offset = i * self.bpp
        for j in range(self.bpp):
            self.buf[offset + self.ORDER[j]] = int(v[j] * self.brightness)

    def __getitem__(self, i):
        offset = i * self.bpp
        return tuple(self.buf[offset + self.ORDER[j]] // self.brightness for j in range(self.bpp))

    def fill(self, v):
        for i in range(self.n):
            self.__setitem__(i, v)

    def write(self):
        bitstream(self.pin, 0, self.timing, self.buf)

    def set_brightness(self, brightness):
        if 0 <= brightness <= 1:
            self.brightness = brightness
            for i in range(self.n):
                self[i] = self[i]  # Reapply current color with new brightness

    def color(self, r, g, b):
        return (g, r, b)


