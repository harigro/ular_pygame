import pygame as pg
import sys
from random import choice
from typing import Union

class Kons:
    def panjang(p: int) -> int:
        return p
    
    def skor(s: int) -> int:
        return s
    
    def batas(b: int) -> int:
        return b
    
class Objek:
    def __init__(self, lebar: int, tinggi: int, ukuran_grid: int, pembatas: int):
        self.lebar = lebar
        self.tinggi = tinggi
        self.ukuran_grid = ukuran_grid
        self.pembatas = pembatas

    def posisi_acak(self):
        return [choice(range(self.pembatas, self.lebar-self.pembatas, self.ukuran_grid)), 
                choice(range(self.pembatas, self.tinggi-self.pembatas, self.ukuran_grid))]
    
class Makanan(Objek):
    def __init__(self, lebar, tinggi, ukuran_grid, pembatas):
        super().__init__(lebar, tinggi, ukuran_grid, pembatas)
        self.kotak = pg.Rect(0, 0, ukuran_grid, ukuran_grid)
        self.kotak.topleft = self.posisi_acak()

    def pindah(self, ular_segmen):
        while True:
            self.kotak.topleft = self.posisi_acak()
            if self.kotak not in ular_segmen:
                break

class Ular(Makanan):
    def __init__(self, lebar, tinggi, ukuran_grid, pembatas):
        super().__init__(lebar, tinggi, ukuran_grid, pembatas)
        self.segmen = []
        self.panjang = Kons.panjang(1)
        self.arah = "kanan"
        self.arah_sebelumnya = None

    def gerak(self):
        self.arah_sebelumnya = self.arah
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
        # Tangani jika kepala ular melewati batas horizontal
        if self.kotak.right <= 0:
            self.kotak.left = self.lebar
        elif self.kotak.left >= self.lebar:
            self.kotak.right = 0
        # Tangani jika kepala ular melewati batas vertikal
        elif self.kotak.top < self.pembatas:
            # Jika melewati batas atas, pindahkan ke bawah layar
            self.kotak.bottom = self.tinggi
        elif self.kotak.bottom > self.tinggi:
            # Jika melewati batas bawah, pindahkan ke atas layar
            self.kotak.top = self.pembatas
        # Perbarui segmen agar sinkron dengan posisi kepala
        self.segmen[-1] = self.kotak.copy()

    def reset(self):
        self.segmen.clear()
        self.panjang = 1
        self.kotak.topleft = self.posisi_acak()

class BelahLayar(Objek):
    def __init__(self, layar: pg.display, lebar: int, tinggi: int, ukuran_grid: int, pembatas: int):
        super().__init__(lebar, tinggi, ukuran_grid, pembatas)
        self.layar = layar

    def daerah_skor(self, warna: Union[tuple[int, int, int], str] = (50, 50, 50)) -> None:
        # Area skor (20% dari tinggi layar)
        rect_skor = pg.Rect(0, 0, self.lebar, self.pembatas)
        pg.draw.rect(self.layar, warna, rect_skor)
        
    def daerah_permainan(self, warna: Union[tuple[int, int, int], str] = 'black', isi_grid = False) -> None:
        # Area permainan (80% dari tinggi layar)
        mainan = pg.Rect(0, self.pembatas, self.lebar, self.tinggi - self.pembatas)
        pg.draw.rect(self.layar, warna, mainan)
        if isi_grid:
            for x in range(mainan.left, mainan.right, self.ukuran_grid):
                pg.draw.line(self.layar, (255, 255, 0, 50), (x, mainan.top), (x, mainan.bottom))
            for y in range(mainan.top, mainan.bottom, self.ukuran_grid):
                pg.draw.line(self.layar, (255, 255, 0, 50), (mainan.left, y), (mainan.right, y))

class Gambar:
    def __init__(self, source: str):
        self.source = source

    def blit(self, screen: pg.display, dest:pg.Rect, transform: int) -> None:
        screen.blit(pg.transform.scale(pg.image.load(self.source), (transform, transform)), dest.topleft)
        

class Game:
    def __init__(self):
        pg.init()
        self.lebar, self.tinggi = 600, 400
        self.ukuran_grid = 20
        self.layar = pg.display.set_mode((self.lebar, self.tinggi), pg.NOFRAME)
        self.catat = []
        self.fps = pg.time.Clock()
        self.pembatasan = Kons.batas(self.tinggi//5)
        self.ular = Ular(self.lebar, self.tinggi, self.ukuran_grid, self.pembatasan)
        self.makanan = Makanan(self.lebar, self.tinggi, self.ukuran_grid, self.pembatasan)
        self.skor = Kons.skor(0)
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
        belah = BelahLayar(self.layar, self.lebar, self.tinggi, self.ukuran_grid, self.pembatasan)
        belah.daerah_skor()
        belah.daerah_permainan()
        buah = Gambar("assets/apple.png")
        # pemangsa
        pemangsa = lambda o, x, y, z: Gambar(o).blit(x, y, z)
        kepala = ["assets/head_left.png"
                  "assets/head_up.png",
                  "assets/head_right.png",
                  "assets/head_down.png"]
        badan = ["assets/body_bottomleft.png",
                "assets/body_bottomright.png",
                "assets/body_horizontal.png",
                "assets/body_topleft.png",
                "assets/body_topright.png"]
        ekor = ["assets/tail_left.png",
                "assets/tail_up.png",
                "assets/tail_right.png",
                "assets/tail_down.png"]

        # Gambar teks skor di area skor
        teks_skor = pg.font.Font(None, 36).render(f'Skor: {self.skor}', True, 'white')
        self.layar.blit(teks_skor, (10, 10))

        # Gambar elemen permainan di area permainan
        # posisi_ekor = self.ular.segmen[-1]
        for i, segmen in enumerate(self.ular.segmen):
            pg.draw.rect(self.layar, 'red', segmen)
            if self.ular.arah != self.ular.arah_sebelumnya and self.ular.panjang > 2:
                if i != 0 and self.ular.segmen[-1] != segmen and len(self.catat) != 0:
                    self.catat.pop(0)
                else:
                    self.catat.append(segmen)
            else:
                if self.ular.segmen[-1] == segmen:
                    self.catat.clear()
            # print(f"{self.ular.arah}, {self.ular.arah_sebelumnya}, {segmen[0]}, {segmen[1]:<5}", end='\r')
            print(f"belokan : {self.catat}:<5", end='\r')
            # print()
        buah.blit(self.layar, pg.Rect(self.makanan.kotak), self.ukuran_grid)

        # Perbarui tampilan layar
        pg.display.flip()

    def cek_tabrakan(self):
        if self.ular.kotak.colliderect(self.makanan.kotak):
            self.ular.panjang += 1
            self.skor += 5
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
            self.ular.pindahkan_ke_sisi_berlawanan()
            self.cek_tabrakan()
            self.fps.tick(6)

if __name__ == '__main__':
    game = Game()
    game.loop()
