import pygame as pg
import sys
from random import choice

def main():
    pg.init()
    fps = pg.time.Clock()
    lebar, tinggi = 600, 400
    layar = pg.display.set_mode((lebar, tinggi), pg.NOFRAME)
    # variabel untuk mengatur posisi acak
    posis_acak = lambda: [choice(range(20, lebar//2, 30)), choice(range(20, tinggi//2, 30))]
    kotak = pg.Rect(200, 100, 20, 20)
    kotak.topleft = posis_acak()
    # variabel untuk menambah panjang ular
    segmen = []
    panjang = 1
    # variabel makanan
    makanan = kotak.copy()
    makanan.topleft = posis_acak()
    # variabel kecepatan
    kecepatan = 20
    # variabel arah
    arah = "kanan"
    # perulangan
    jalan = True
    while jalan:
        # atur tombol gerak dan keluar dari permainan
        for event in pg.event.get():
            if event.type == pg.QUIT:
                jalan = False
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))
                elif event.key == pg.K_w and arah != 'bawah':
                    arah = 'atas'
                elif event.key == pg.K_d and arah != 'kiri':
                    arah = 'kanan'
                elif event.key == pg.K_s and arah != 'atas':
                    arah = 'bawah'
                elif event.key == pg.K_a and arah != 'kanan': 
                    arah = 'kiri'
        # atur kecepatan dan arah gerak ular
        if arah == 'atas':
            kotak.move_ip(0, -kecepatan)
        elif arah == 'kanan':
            kotak.move_ip(kecepatan, 0)
        elif arah == 'bawah':
            kotak.move_ip(0, kecepatan)
        elif arah == 'kiri':
            kotak.move_ip(-kecepatan, 0)
        # Periksa jika ular menyentuh tepi layar
        if kotak.left >= lebar:
            kotak.right = 0
        elif kotak.right <= 0:
            kotak.left = lebar
        elif kotak.top >= tinggi:
            kotak.bottom = 0
        elif kotak.bottom <= 0:
            kotak.top = tinggi
        # tambahkan kotak ke segmen dan periksa panjangnya
        segmen.append(kotak.copy())
        if len(segmen) > panjang:
            segmen.pop(0)
        # beri warna ke layar dan gambar semua objek 
        layar.fill('black')
        for s in segmen:
            pg.draw.rect(layar, 'red', s)
        pg.draw.rect(layar, 'green', makanan)
        # Periksa jika ular menyentuh makanan
        if kotak.colliderect(makanan):
            panjang += 1
            makanan.topleft = posis_acak()
        # Periksa jika kepala menabrak tubunya:
        if segmen[0] in segmen[1:]:
            segmen.clear()
            panjang = 1
            kotak.topleft = posis_acak()
        # periksa posisi makanan dengan badan ular
        if makanan in segmen:
            makanan.topleft = posis_acak()
        pg.display.flip()
        fps.tick(9)

if __name__ == '__main__':
    main()
