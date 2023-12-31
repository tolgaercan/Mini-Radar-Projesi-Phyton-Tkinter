import tkinter
import methotlar
import arduino

class Arayüz:
    def __init__(self):
        self.arduino = arduino.Arduino()
        self.koordinatlar = methotlar.Koordinatlar()
        self.ana_pencere = tkinter.Tk()
        self.frame = tkinter.Frame(self.ana_pencere)
        self.butonFrame=tkinter.Frame(self.ana_pencere,width=250,height=200,bg="light gray")
        self.canvas = tkinter.Canvas(self.frame, width=1100, height=820)
        # Tarama başlat butonu ekleme
        self.buton = tkinter.Button(self.butonFrame, text="Tarama Başlat",bg="yellow", font=("Arial", 12, "bold"),command=self.Tarama_baslat)
        self.buton.pack(padx=10,pady=10)
        # Tarama Sonlandır Butonu
        self.buton_durdur = tkinter.Button(self.butonFrame, text="Tarama Sonlandır",bg="orange",font=("Arial", 12, "bold"),command=self.Tarama_durdur)
        self.buton_durdur.pack(padx=10,pady=10)
        # Kapat Butonu
        self.buton_kapat = tkinter.Button(self.butonFrame, text="Kapat",bg="red",font=("Arial", 12, "bold"), command=self.kapat)
        self.buton_kapat.pack(padx=10,pady=10)
        # Dikdörtgen ve artı işareti çizimi
        self.dikdortgen = self.canvas.create_rectangle(20, 20, 820, 820, fill="light green")
        orta_x = 420
        orta_y = 420
        self.canvas.create_line(orta_x - 10, orta_y, orta_x + 10, orta_y, fill="red", width=3)
        self.canvas.create_line(orta_x, orta_y - 10, orta_x, orta_y + 10, fill="red", width=3)
        # Kesikli çizgileri oluşturma
        # x eksenine kesikli çizgi oluşturma
        for i in range(100, 820, 80):
            self.canvas.create_line(20, i, 820, i, dash=(2, 2), fill="red")
            self.canvas.create_line(i, 20, i, 820, dash=(2, 2), fill="red")
        self.butonFrame.place(x=855,y=350)    
        self.canvas.pack()
        self.frame.pack(padx=10, pady=10)
        self.guncelleme_süresi = 50  # Milisaniye cinsinden
        self.tarama_devam_etsin = False
        self.ana_pencere.protocol("WM_DELETE_WINDOW", self.kapat)
        self.ana_pencere.mainloop()
    def Tarama_baslat(self):
        # Taramayı başlat
            self.tarama_devam_etsin = True
            self.veri_guncelle()
            self.tarama_efekti_olustur()
    def Tarama_durdur(self):
        # Taramayı durdur
            self.tarama_devam_etsin = False
            self.canvas.delete("nokta","halka")
    def veri_guncelle(self):
        if self.tarama_devam_etsin and self.arduino.veri_kuyrugu:
            # Kuyruğun en sol elemanını (tuple) al
            veri_tuple = self.arduino.veri_kuyrugu.popleft()
            # Tuple içindeki verileri al
            veri1 = veri_tuple[0]
            veri2 = veri_tuple[1]
            veri3 = veri_tuple[2]
            veri4 = veri_tuple[3]
            # Koordinatları ayarla
            self.koordinatlar.set_S1_koordinat(veri1)
            self.koordinatlar.set_S2_koordinat(veri2)
            self.koordinatlar.set_S3_koordinat(veri3)
            self.koordinatlar.set_S4_koordinat(veri4)
            # Noktaları yenile
            self.nokta_yenileme()
        if self.tarama_devam_etsin:
            # Tarama devam ediyorsa, fonksiyonu tekrar çağır         
            self.ana_pencere.after(self.guncelleme_süresi, self.veri_guncelle)
    def nokta_yenileme(self):
        self.canvas.delete("nokta")
        s1_koordinat = self.koordinatlar.get_S1_koordinat()
        s2_koordinat = self.koordinatlar.get_S2_koordinat()
        s3_koordinat = self.koordinatlar.get_S3_koordinat()
        s4_koordinat = self.koordinatlar.get_S4_koordinat()
        for koordinat in s1_koordinat:
            self.canvas.create_oval(koordinat,420, koordinat + 6, 420 + 6, fill="black", width=4, tags="nokta")
                                    #(x koordinatı,y koordinatı)bir noktanın---diğeride diğer noktanın koordinatı
        for koordinat in s2_koordinat:
             self.canvas.create_oval(420,koordinat, 420 + 6, koordinat + 6, fill="black", width=4, tags="nokta") 
        for koordinat in s3_koordinat:
            self.canvas.create_oval(koordinat,420, koordinat + 6, 420 + 6, fill="black", width=4, tags="nokta")
        for koordinat in s4_koordinat:
             self.canvas.create_oval(420,koordinat, 420 + 6, koordinat + 6, fill="black", width=4, tags="nokta")    
    def kapat(self):
        self.arduino.kapat()
        self.ana_pencere.destroy()
        
    def tarama_efekti_olustur(self, cap=20):
        merkez_x, merkez_y = 420, 420
        self.canvas.delete("halka")

        if cap < 410:  # 800x800 karenin içinde kalmak için çapı kontrol et
            sol_ust_x = merkez_x - cap
            sol_ust_y = merkez_y - cap
            sag_alt_x = merkez_x + cap
            sag_alt_y = merkez_y + cap
            self.canvas.create_oval(sol_ust_x, sol_ust_y, sag_alt_x, sag_alt_y, outline="dark green", width=1, tags="halka")   
        else:
            cap = 20  # Çapı başa döndür
        if self.tarama_devam_etsin:
            self.ana_pencere.after(self.guncelleme_süresi, lambda: self.tarama_efekti_olustur(cap + 20))
if __name__ == "__main__":
    Arayüz()


