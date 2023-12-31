import threading
import serial
import time
from collections import deque

class Arduino:
    def __init__(self, port="COM4", baud_rate=9600, port_bt="COM1"):
        self.calisiyor = True
        self.veri_kuyrugu = deque(maxlen=8)
        self.ser_usb = None
        self.ser_bt = None

        # USB bağlantısını kurmaya çalış
        try:
            self.ser_usb = serial.Serial(port, baud_rate)
        except serial.SerialException:
            print("USB bağlantısı başarısız.")

        # Bluetooth bağlantısını kurmaya çalış
        try:
            self.ser_bt = serial.Serial(port_bt, baud_rate)
        except serial.SerialException:
            print("Bluetooth bağlantısı başarısız.")

        if not self.ser_usb and not self.ser_bt:
            print("Hiçbir bağlantı kurulamadı.")
            self.calisiyor = False
            return

        threading.Thread(target=self.arduinoVeriOku, daemon=True).start()

    def arduinoVeriOku(self):
        while self.calisiyor:
            ser = None
            if self.ser_bt is not None and self.ser_bt.in_waiting > 0:
                ser = self.ser_bt
            elif self.ser_usb is not None and self.ser_usb.in_waiting > 0:
                ser = self.ser_usb
            else:
                time.sleep(0.1)
                continue

            try:
                veri = ser.readline().decode('utf-8').strip()
                # Virgülle ayrılmış veriyi ayır
                veriler = veri.split(',')
                # Verileri tam sayıya dönüştür ve kuyruğa ekle
                if len(veriler) == 4:
                    veri_tuple = tuple(map(int, veriler))
                    self.veri_kuyrugu.append(veri_tuple)
                else:
                    print("Beklenen veri formatı dışında veri alındı.")
            except ValueError:
                print("Geçersiz veri okundu.")
            except serial.SerialException:
                # Bağlantı hatası durumunda işlenecek kodlar
                pass

            time.sleep(0.1)  # İsteğe bağlı bekleme süresi

    def kapat(self):
        self.calisiyor = False
        if self.ser_usb:
            self.ser_usb.close()
        if self.ser_bt:
            self.ser_bt.close()
