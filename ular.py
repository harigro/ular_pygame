import pygame as pg
import sys
from random import choice
from pygame_grid import draw_grid

class Ular:
    def __init__(self, lebar, tinggi, ukuran_grid):
        self.lebar = lebar
        self.tinggi = tinggi
        self.ukuran_grid = ukuran_grid
        self.kotak = pg.Rect(0, 0, ukuran_grid, ukuran_grid)
        self.kotak.topleft = self.posisi_acak()
        self.segmen = []
        self.panjang = 1
        self.arah = "kanan"
        self.bekukan = False  # Tambahkan atribut untuk membekukan pergerakan

    def posisi_acak(self):
        return [choice(range(0, self.lebar, self.ukuran_grid)), choice(range(0, self.tinggi, self.ukuran_grid))]

    def gerak(self):
        if self.bekukan:
            return

        if self.arah == 'atas':
            self.kotak.move_ip(0, -self.ukuran_grid)
        elif self.arah == 'kanan':
            self.kotak.move_ip(self.ukuran_grid, 0)
        elif self.arah == 'bawah':
            self.kotak.move_ip(0, self.ukuran_grid)
        elif self.arah == 'kiri':
            self.kotak.move_ip(-self.ukuran_grid, 0)

        self.segmen.append(self.kotak.copy())
        if len(self.segmen) > self.panjang:
            self.segmen.pop(0)

    def cek_keluar_layar(self):
        # Periksa apakah seluruh segmen keluar dari layar
        keluar_horizontal = all(seg.right <= 0 or seg.left >= self.lebar for seg in self.segmen)
        keluar_vertical = all(seg.bottom <= 0 or seg.top >= self.tinggi for seg in self.segmen)

        if keluar_horizontal or keluar_vertical:
            self.bekukan = True

    def pindahkan_ke_sisi_berlawanan(self):
        if not self.bekukan:
            return

        # Pindahkan seluruh segmen ke sisi berlawanan
        for seg in self.segmen:
            if seg.right <= 0:
                seg.left = self.lebar
            elif seg.left >= self.lebar:
                seg.right = 0
            elif seg.bottom <= 0:
                seg.top = self.tinggi
            elif seg.top >= self.tinggi:
                seg.bottom = 0

        self.bekukan = False

    def reset(self):
        self.segmen.clear()
        self.panjang = 1
        self.kotak.topleft = self.posisi_acak()
        self.bekukan = False

class Makanan:
    def __init__(self, lebar, tinggi, ukuran_grid):
        self.lebar = lebar
        self.tinggi = tinggi
        self.ukuran_grid = ukuran_grid
        self.rect = pg.Rect(0, 0, ukuran_grid, ukuran_grid)
        self.rect.topleft = self.posisi_acak()

    def posisi_acak(self):
        return [choice(range(0, self.lebar, self.ukuran_grid)), choice(range(0, self.tinggi, self.ukuran_grid))]

    def pindah(self, ular_segmen):
        while True:
            posisi_baru = self.posisi_acak()
            self.rect.topleft = posisi_baru
            if self.rect not in ular_segmen:
                break

class Game:
    def __init__(self):
        pg.init()
        self.lebar, self.tinggi = 600, 400
        self.ukuran_grid = 20
        self.layar = pg.display.set_mode((self.lebar, self.tinggi), pg.NOFRAME)
        pg.display.set_caption('Ular')
        self.fps = pg.time.Clock()
        self.ular = Ular(self.lebar, self.tinggi, self.ukuran_grid)
        self.makanan = Makanan(self.lebar, self.tinggi, self.ukuran_grid)
        self.jalan = True

    def kontrol(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.jalan = False
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))
                elif event.key == pg.K_w and self.ular.arah != 'bawah':
                    self.ular.arah = 'atas'
                elif event.key == pg.K_d and self.ular.arah != 'kiri':
                    self.ular.arah = 'kanan'
                elif event.key == pg.K_s and self.ular.arah != 'atas':
                    self.ular.arah = 'bawah'
                elif event.key == pg.K_a and self.ular.arah != 'kanan':
                    self.ular.arah = 'kiri'

    def gambar(self):
        self.layar.fill('black')
        draw_grid(x_dist=self.ukuran_grid, y_dist=self.ukuran_grid, 
                  x_minor_dist=self.ukuran_grid, y_minor_dist=self.ukuran_grid, 
                  color="yellow", opacity=0.2)
        for segmen in self.ular.segmen:
            pg.draw.rect(self.layar, 'red', segmen)
        pg.draw.rect(self.layar, 'green', self.makanan.rect)
        pg.display.flip()

    def cek_tabrakan(self):
        if self.ular.kotak.colliderect(self.makanan.rect):
            self.ular.panjang += 1
            self.makanan.pindah(self.ular.segmen)

        if self.ular.segmen[0] in self.ular.segmen[1:]:
            self.ular.reset()

    def loop(self):
        while self.jalan:
            self.kontrol()
            self.ular.cek_keluar_layar()
            self.ular.gerak()
            self.ular.pindahkan_ke_sisi_berlawanan()
            self.cek_tabrakan()
            self.gambar()
            self.fps.tick(9)

if __name__ == '__main__':
    game = Game()
    game.loop()
