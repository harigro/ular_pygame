import pygame as pg
import sys
from random import choice

class Makanan:
    def __init__(self, lebar, tinggi, ukuran_grid, pembatas):
        self.lebar = lebar
        self.tinggi = tinggi
        self.pembatas = pembatas
        self.ukuran_grid = ukuran_grid
        self.kotak = pg.Rect(0, 0, ukuran_grid, ukuran_grid)
        self.kotak.topleft = self.posisi_acak()

    def posisi_acak(self):
        return [choice(range(self.pembatas, self.lebar-self.pembatas, self.ukuran_grid)), 
                choice(range(self.pembatas, self.tinggi-self.pembatas, self.ukuran_grid))]

    def pindah(self, ular_segmen):
        while True:
            posisi_baru = self.posisi_acak()
            self.kotak.topleft = posisi_baru
            if self.kotak not in ular_segmen:
                break

class Ular(Makanan):
    def __init__(self, lebar, tinggi, ukuran_grid, pembatas):
        super().__init__(lebar, tinggi, ukuran_grid, pembatas)
        self.segmen = []
        self.panjang = 1
        self.arah = "kanan"

    def gerak(self):
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

    def pindahkan_ke_sisi_berlawanan(self):
        if self.kotak.right <= 0:
            self.kotak.left = self.lebar
        elif self.kotak.left >= self.lebar:
            self.kotak.right = 0

        # Tangani jika kepala ular melewati batas vertikal
        elif self.kotak.top < self.pembatas:
            # Jika melewati batas atas, pindahkan ke bawah layar
            self.kotak.top = self.tinggi - self.ukuran_grid
        elif self.kotak.bottom > self.tinggi:
            # Jika melewati batas bawah, pindahkan ke atas layar
            self.kotak.top = self.pembatas

        # Perbarui segmen agar sinkron dengan posisi kepala
        self.segmen[-1] = self.kotak.copy()

    def reset(self):
        self.segmen.clear()
        self.panjang = 1
        self.kotak.topleft = self.posisi_acak()
        self.bekukan = False

class Game:
    def __init__(self):
        pg.init()
        self.lebar, self.tinggi = 600, 400
        self.ukuran_grid = 20
        self.layar = pg.display.set_mode((self.lebar, self.tinggi), pg.NOFRAME)
        pg.display.set_caption('Ular')
        self.fps = pg.time.Clock()
        self.ular = Ular(self.lebar, self.tinggi, self.ukuran_grid, self.tinggi//5)
        self.makanan = Makanan(self.lebar, self.tinggi, self.ukuran_grid, self.tinggi//5)
        self.skor = 0
        self.font = pg.font.SysFont('Arial', 24)
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
        # Warna untuk membedakan area
        warna_skor = (50, 50, 50)  # Abu-abu gelap untuk latar skor
        warna_latar_permainan = 'black'

        # Area skor (20% dari tinggi layar)
        tinggi_skor = self.tinggi // 5
        rect_skor = pg.Rect(0, 0, self.lebar, tinggi_skor)

        # Area permainan (80% dari tinggi layar)
        rect_permainan = pg.Rect(0, tinggi_skor, self.lebar, self.tinggi - tinggi_skor)

        # Isi warna untuk setiap area
        pg.draw.rect(self.layar, warna_skor, rect_skor)
        pg.draw.rect(self.layar, warna_latar_permainan, rect_permainan)

        # Gambar grid secara manual di area permainan
        for x in range(rect_permainan.left, rect_permainan.right, self.ukuran_grid):
            pg.draw.line(self.layar, (255, 255, 0, 50), (x, rect_permainan.top), (x, rect_permainan.bottom))
        for y in range(rect_permainan.top, rect_permainan.bottom, self.ukuran_grid):
            pg.draw.line(self.layar, (255, 255, 0, 50), (rect_permainan.left, y), (rect_permainan.right, y))

        # Gambar teks skor di area skor
        teks_skor = pg.font.Font(None, 36).render(f'Skor: {self.ular.panjang - 1}', True, 'white')
        self.layar.blit(teks_skor, (10, 10))

        # Gambar elemen permainan di area permainan
        for segmen in self.ular.segmen:
            pg.draw.rect(self.layar, 'red', segmen)
        pg.draw.rect(self.layar, 'green', self.makanan.kotak)

        # Perbarui tampilan layar
        pg.display.flip()


    def cek_tabrakan(self):
        if self.ular.kotak.colliderect(self.makanan.kotak):
            self.ular.panjang += 1
            self.skor += 10
            self.makanan.pindah(self.ular.segmen)

        if self.ular.segmen[0] in self.ular.segmen[1:]:
            pg.time.wait(2000)
            self.ular.reset()
            self.skor = 0

    def loop(self):
        while self.jalan:
            self.kontrol()
            self.gambar()
            self.ular.gerak()
            # self.ular.cek_keluar_layar()
            self.ular.pindahkan_ke_sisi_berlawanan()
            self.cek_tabrakan()
            self.fps.tick(9)

if __name__ == '__main__':
    game = Game()
    game.loop()
