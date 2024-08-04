import numpy as np

# Ortam boyutlarını tanımlıyoruz (11x11 ızgara)
ortam_satir_sayisi = 11
ortam_sutun_sayisi = 11

# Ödül değerleri için minimum ve maksimum değerler
min_deger = -100.
max_deger = 100.

# Başlangıç ve hedef konumlarını belirliyoruz
baslangic_konumu = (0, 0)
hedef_konumu = (0, 5)

# Hareket yönlerini ve sayısını belirliyoruz
hareketler = ['yukari', 'sag', 'asagi', 'sol']
hareket_sayisi = len(hareketler)

# Q-değerleri matrisini ve ödül matrisini oluşturuyoruz
q_degerleri = np.zeros((ortam_satir_sayisi, ortam_sutun_sayisi, hareket_sayisi))
oduller = np.full((ortam_satir_sayisi, ortam_sutun_sayisi), min_deger)
oduller[hedef_konumu] = max_deger

# Geçit noktalarını tanımlıyoruz (robotun geçebileceği yerler)
gecitler = {}
gecitler[1] = [i for i in range(1, 10)]
gecitler[2] = [1, 7, 9]
gecitler[3] = [i for i in range(1, 8)]
gecitler[3].append(9)
gecitler[4] = [3, 7]
gecitler[5] = [i for i in range(11)]
gecitler[6] = [5]
gecitler[7] = [i for i in range(1, 10)]
gecitler[8] = [3, 7]
gecitler[9] = [i for i in range(11)]

# Geçit noktalarının ödüllerini -1 olarak güncelliyoruz
for satir_indeks in range(1, 10):
    for sutun_indeks in gecitler[satir_indeks]:
        oduller[satir_indeks, sutun_indeks] = -1.

# Ödül matrisini yazdırıyoruz
for satir in oduller:
    print(satir)

# Bir konumun engel olup olmadığını kontrol eden fonksiyon
def engel_mi(konum):
    return oduller[konum] != min_deger

# Rastgele bir başlangıç konumu belirleyen fonksiyon
def baslangic_belirle():
    while True:
        konum = (np.random.randint(ortam_satir_sayisi), np.random.randint(ortam_sutun_sayisi))
        if not engel_mi(konum):
            return konum

# Bir sonraki hareketi belirleyen fonksiyon (epsilon-greedy stratejisi)
def sonraki_hareket_belirle(gecerli_konum, epsilon):
    if np.random.random() < epsilon:
        return np.argmax(q_degerleri[gecerli_konum])
    else:
        return np.random.randint(hareket_sayisi)

# Bir sonraki konuma gitmek için hareketi gerçekleştiren fonksiyon
def sonraki_noktaya_git(gecerli_konum, hareket_indeks):
    y, x = gecerli_konum
    if hareketler[hareket_indeks] == 'yukari' and y > 0:
        y -= 1
    elif hareketler[hareket_indeks] == 'sag' and x < ortam_sutun_sayisi - 1:
        x += 1
    elif hareketler[hareket_indeks] == 'asagi' and y < ortam_satir_sayisi - 1:
        y += 1
    elif hareketler[hareket_indeks] == 'sol' and x > 0:
        x -= 1
    return (y, x)

# En kısa mesafeyi hesaplayan fonksiyon
def en_kisa_mesafe(basla_konum):
    if engel_mi(basla_konum):
        return []
    else:
        gecerli_konum = basla_konum
        en_kisa = []
        en_kisa.append(gecerli_konum)
        while not engel_mi(gecerli_konum):
            hareket_indeks = sonraki_hareket_belirle(gecerli_konum, 1.)
            gecerli_konum = sonraki_noktaya_git(gecerli_konum, hareket_indeks)
            en_kisa.append(gecerli_konum)
        return en_kisa

# Eğitim parametrelerini tanımlıyoruz
epsilon = 0.9
azalma_degeri = 0.9
ogrenme_orani = 0.9

# Q-öğrenme eğitim döngüsü
for adim in range(1000):
    gecerli_konum = baslangic_belirle()
    while not engel_mi(gecerli_konum):
        hareket_indeks = sonraki_hareket_belirle(gecerli_konum, epsilon)
        eski_konum = gecerli_konum
        gecerli_konum = sonraki_noktaya_git(gecerli_konum, hareket_indeks)
        odul = oduller[gecerli_konum]
        eski_q_degeri = q_degerleri[eski_konum][hareket_indeks]
        fark = odul + (azalma_degeri * np.max(q_degerleri[gecerli_konum])) - eski_q_degeri
        yeni_q_degeri = eski_q_degeri + (ogrenme_orani * fark)
        q_degerleri[eski_konum][hareket_indeks] = yeni_q_degeri

print('Eğitim tamamlandı.')

# Kullanıcıdan robotun harekete başlayacağı konumu alıyoruz
ogr_sonrasi_satir = int(input('Robotun harekete başlayacağı satır indeksini giriniz:'))
ogr_sonrasi_sutun = int(input('Robotun harekete başlayacağı sutun indeksini giriniz:'))

# En kısa mesafeyi hesaplayıp yazdırıyoruz
print('Kargo noktasına giden rota:', en_kisa_mesafe((ogr_sonrasi_satir, ogr_sonrasi_sutun)))
