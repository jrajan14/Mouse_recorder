import numpy as np
import struct

class MouseData:
    def __init__(self, points: np.ndarray):
        self.points = points

    def pack(self) -> bytes:
        size = self.points.shape[0]*self.points.shape[1]
        buf = bytearray(size * 8 + 4)
        buf[4:] = self.points.flatten().tobytes(order="C")
        buf[:4] = struct.pack("<i", size)
        return buf

    @staticmethod
    def Parse(buf: bytes):
        _ = struct.unpack("<i", buf[:4])
        points = np.frombuffer(buf[4:], dtype=np.float64)
        points = points.reshape(-1, 2)
        return MouseData(points)