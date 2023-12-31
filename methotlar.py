from collections import deque

class Koordinatlar:
    def __init__(self):
        self.S1_koordinat = deque(maxlen=10)
        self.S2_koordinat = deque(maxlen=10)
        self.S3_koordinat = deque(maxlen=10)
        self.S4_koordinat = deque(maxlen=10)

    def set_S1_koordinat(self, koordinat):
        self.S1_koordinat.append(koordinat)

    def set_S2_koordinat(self, koordinat):
        self.S2_koordinat.append(koordinat)

    def set_S3_koordinat(self, koordinat):
        self.S3_koordinat.append(koordinat)

    def set_S4_koordinat(self, koordinat):
        self.S4_koordinat.append(koordinat)

    def get_S1_koordinat(self):
        return [int((80 * (500 + i) / 100) + 20) for i in self.S1_koordinat]

    def get_S2_koordinat(self):
        return [int((80 * (500 + i) / 100) + 20) for i in self.S2_koordinat]

    def get_S3_koordinat(self):
        return [int((80 * (500 - i) / 100) + 20) for i in self.S3_koordinat]

    def get_S4_koordinat(self):
        return [int((80 * (500 - i) / 100) + 20) for i in self.S4_koordinat]
