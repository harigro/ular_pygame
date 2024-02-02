import pygame as pg
import sys
from random import choice

def main():
    pg.init()
    fps = pg.time.Clock()
    lebar = 600
    tinggi = 400

    layar = pg.display.set_mode((lebar, tinggi), pg.NOFRAME)
    
    # Muat gambar dan perkecil ukurannya
    img = pg.image.load("assets/head_left.png")  # Ganti dengan nama file gambar ular Anda
    img_kecil = pg.transform.scale(img, (20, 20))  # Misalnya, ukuran baru 10x10 piksel
    
    kotak = pg.Rect(200, 100, img_kecil.get_width(), img_kecil.get_height())  # Buat kotak dengan ukuran yang sesuai dengan gambar
    ambil_sembarang_posisi = lambda: [choice(range(20, lebar//2, 30)), choice(range(20, tinggi//2, 30))]
    kotak.topleft = ambil_sembarang_posisi()
    segments = [kotak.copy()]
    length = 1

    makanan = kotak.copy()
    makanan.topleft = ambil_sembarang_posisi()

    target_position = kotak.topleft
    MOVE_DISTANCE = 20  # Jarak pergerakan

    arah = None
    jalan = True
    while jalan:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                jalan = False
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    if arah != 'bawah':  # Ular tidak bisa langsung berbalik arah
                        arah = 'atas'
                elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                    if arah != 'kiri':
                        arah = 'kanan'
                elif event.key == pg.K_DOWN or event.key == pg.K_s:
                    if arah != 'atas':
                        arah = 'bawah'
                elif event.key == pg.K_LEFT or event.key == pg.K_a:
                    if arah != 'kanan':
                        arah = 'kiri'

        if arah == 'atas':
            kotak.move_ip(0, -MOVE_DISTANCE)
        elif arah == 'kanan':
            kotak.move_ip(MOVE_DISTANCE, 0)
        elif arah == 'bawah':
            kotak.move_ip(0, MOVE_DISTANCE)
        elif arah == 'kiri':
            kotak.move_ip(-MOVE_DISTANCE, 0)

        # Periksa jika ular menyentuh tepi layar, maka ular muncul dari sisi yang berlawanan
        if kotak.left >= lebar:
            kotak.right = 0
        elif kotak.right <= 0:
            kotak.left = lebar
        elif kotak.top >= tinggi:
            kotak.bottom = 0
        elif kotak.bottom <= 0:
            kotak.top = tinggi

        # Periksa jika ular menyentuh makanan
        if kotak.colliderect(makanan):
            length += 1
            makanan.topleft = ambil_sembarang_posisi()
            
            # Tambahkan segmen baru sebanyak panjang tambahan yang diperlukan
            for _ in range(length - len(segments)):
                segments.append(segments[-1].copy())

        # Update posisi setiap segmen kecuali yang pertama
        for i in range(length - 1, 0, -1):
            segments[i] = segments[i - 1].copy()
        
        segments[0] = kotak.copy()

        layar.fill('black')
        for seg in segments:
            # Gambar ular pada setiap segmen
            layar.blit(img_kecil, seg)
        
        pg.draw.rect(layar, 'green', makanan)
        
        pg.display.flip()
        fps.tick(9)

if __name__ == '__main__':
    main()
