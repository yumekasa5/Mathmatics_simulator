# *-* coding: utf-8 *-*
# 3D座標系を定義するクラス

class CoordinateSystem:
    def __init__(self, origin, x, y, z):
        self.origin = origin
        self.x = x
        self.y = y
        self.z = z

    def get_origin(self):
        return self.origin

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z