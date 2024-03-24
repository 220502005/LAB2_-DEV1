# AYBÜKE TÜRİDİ 220502005 ELİF BEYZA BEYAZ 220502033
# -*- coding: utf-8 -*-
import pygame
import sys
import random

#                                   DÜNYA BOYUTU AYARLARI
# Sabit değerler:
WIDTH, HEIGHT = 700, 700  #Ekran boyutu
matris_sinir1 = 8
matris_sinir2 = 32

while True:
    try:
        boyut = int(input(f"\nMatris boyutunu seçiniz ({matris_sinir1} -  {matris_sinir2} ):"))
        if matris_sinir1 <= boyut <= matris_sinir2:
            break
        else:
            print(f"Boyut girişleri {matris_sinir1} ile {matris_sinir2} arasında bir değer olmalıdır.")
    except ValueError:
        print("Geçersiz giriş. Lütfen sayı ifadesi giriniz:")

ROWS, COLS = boyut, boyut  # Matrisin satır sütunları
oyun_penceresi = WIDTH // COLS  # Pencerenin boyutları
kazanma_kosulu = ROWS * COLS * 0.6  # Tüm alanın yüzde 60'ı = Kazanma durumu için belirlenen bir değişken

# Renkler:
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

#                                   OYUN İÇİN GEREKLİ KARAKTER SINIFLARI
# Savaşçı sınıfları
class Savasci:
    def __init__(self, ad, can, saldiri, renk):
        self.ad = ad
        self.can = can
        self.saldiri = saldiri
        self.renk = renk

class Okcu(Savasci):
    def __init__(self, renk):
        super().__init__("Okçu", 30, 60, renk)

class Muhafiz(Savasci):
    def __init__(self, renk):
        super().__init__("Muhafız", 80, 20, renk)

class Atli(Savasci):
    def __init__(self, renk):
        super().__init__("Atlı", 40, 30, renk)

class Saglikci(Savasci):
    def __init__(self, renk):
        super().__init__("Sağlıkçı", 100, 50, renk)

class Topcu(Savasci):
    def __init__(self, renk):
        super().__init__("Topçu", 30, 100, renk)

# Oyuncu sınıfı
class Oyuncu:
    def __init__(self, ad, renk):
        self.ad = ad
        self.savascilar = []
        self.renk = renk

        # Rastgele bir köşeye Muhafız yerleştirme = Oyunun başlangıçı
        kose_x = random.choice([0, COLS - 1])
        kose_y = random.choice([0, ROWS - 1])
        oyun_alani[kose_y][kose_x] = 1 if ad == "Player 1" else 0  # Oyun alanına yerleştirme

    def savasci_ekleme(self, savasci_tipi):
        self.savascilar.append(savasci_tipi)

    def savasci_secimi(self):
        if self.ad == "Player 1":
            print("\nLütfen savaşçı seçin:")
            for i, s in enumerate(self.savascilar):
                print(f"{i + 1}. {s.ad}")  # Savaşçı listesi
            while True:
                try:
                    secim = int(input("Savaşçı seçiniz:(1 - {}): ".format(len(self.savascilar))))
                    if 1 <= secim <= len(self.savascilar):
                        return self.savascilar[secim - 1]  # Liste indeksi
                    else:
                        print("Seçim yapılamadı.")
                except ValueError:
                    print("Geçersiz giriş.Lütfen sayı ifadesi giriniz:")
        else:  # Oyuncu 2 ise rastgele bir savaşçı seç = Yapay zeka mantığı için
            return random.choice(self.savascilar)


# Izgara oluşturma (Satır-sütun)
oyun_alani = [[0 for _ in range(COLS)] for _ in range(ROWS)]  # Satırlar sütunlar başlangıç değeri olarak 0 belirlenir,
# sisteme göre 1 veya -1 olma durumunda değişim gösterir

def tablo_doldurma(tablo):
    for row in range(ROWS):
        for col in range(COLS):
            if oyun_alani[row][col] == 1:
                color = RED  # Oyuncu 1 için renk
            elif oyun_alani[row][col] == -1:
                color = BLUE  # Oyuncu 2 için renk
            else:
                color = BLACK

            pygame.draw.rect(tablo, color, (col * oyun_penceresi, row * oyun_penceresi, oyun_penceresi, oyun_penceresi))
            pygame.draw.rect(tablo, WHITE, (col * oyun_penceresi, row * oyun_penceresi, oyun_penceresi, oyun_penceresi), 1)  # Oyun alanı ızgarası için
        pygame.display.update()


def check_winner():
    player1_count = sum(row.count(1) for row in oyun_alani)
    player2_count = sum(row.count(-1) for row in oyun_alani)

    # EK OYUNU KAZANMA DURUMU = Yan yana kareleri dolduran ilk oyuncu kazanır.
    for row in oyun_alani:
        for i in range(len(row) - 2):
            if abs(sum(row[i:i + 3])) == 3:
                if row[i] == 1:
                    return 1
                else:
                    return -1

    # %60 alan doldurma ile kazanma durumu
    if player1_count >= kazanma_kosulu:
        return 1
    elif player2_count >= kazanma_kosulu:
        return -1
    return 0

#                                           OYUN EKRANI AYARLARI VE OYNAMA SİSTEMİ
def main():
    pygame.init()
    ekran = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("LORDS OF THE POLYWARPHISM")
    font = pygame.font.Font(None, 30)

    # Oyuncular
    player1 = Oyuncu("Player 1", RED)
    player1_kaynak = 200
    player2 = Oyuncu("Player 2", BLUE)

    # Tüm savaşçı çeşitlerini oyuncu renkleriyle uyumlu şekilde listeye eklendi. Seçimler buradan yapılmış olacak.
    # Oyuncu 1
    player1.savasci_ekleme(Okcu(RED))
    player1.savasci_ekleme(Muhafiz(RED))
    player1.savasci_ekleme(Atli(RED))
    player1.savasci_ekleme(Saglikci(RED))
    player1.savasci_ekleme(Topcu(RED))

    # Oyuncu 2
    player2.savasci_ekleme(Okcu(BLUE))
    player2.savasci_ekleme(Muhafiz(BLUE))
    player2.savasci_ekleme(Atli(BLUE))
    player2.savasci_ekleme(Saglikci(BLUE))
    player2.savasci_ekleme(Topcu(BLUE))

    turn = 1  # 1.oyuncudan oyun başlar = El değişimi sağlayan değişken
    passes = [0, 0]  # Her oyuncunun pas geçme sayısını takip etmek için sayaç

    # pygame sistem ekranı için
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        tablo_doldurma(ekran)

        #                                   Oyun oynanıyor.
        if turn == 1:
            text = font.render("Oyuncu 1", True, YELLOW)  # Oyuncu 1 için yazı
        else:
            text = font.render("Oyuncu 2", True, YELLOW)  # Oyuncu 2 için yazı
        ekran.blit(text, (10, HEIGHT - 40))
        # Kaynak ekranı
        kaynak_text = font.render(f"Kaynak: {player1_kaynak}", True, YELLOW)
        ekran.blit(kaynak_text, (10, HEIGHT - 80))
        pygame.display.update()
        player1_kaynak += 10 + sum(row.count(1) for row in oyun_alani if row.count(1) > 0)  # Her el sonundaki savaşçı sayısı+10 kadar kaynak kazanma

        # Koordinat girişi ile tabloda hareket etme durumu
        try:
            x = input('\nx koordinatı girişi (Pas geçmek için enter tuşuna basınız): ')
            if x == "":
                passes[turn - 1] += 1
                print("Pas geçildi.")
                if passes[turn - 1] == 3:
                    print(f"Oyuncu {turn} pas geçme hakkını 3 kez kullandı, Oyuncu {3 - turn} kazandı!")
                    running = False
                turn = 3 - turn  # Sıranın değişimi
                continue
            else:
                x = int(x)

            y = int(input("y koordinatı girişi: "))
        except ValueError:
            print("Geçersiz koordinatlar. Tekrar deneyin.")
            continue

        # Dolu kare durumu ve saldırı
        if 0 <= x < COLS and 0 <= y < ROWS:
            if oyun_alani[y][x] != 0:  # Dolu ise = -1 veya 1 olabilir
                if oyun_alani[y][x] == -1:  # Saldırı sadece oyuncu 1 oyuncu 2 nin karelerinden seçtiğinde başlar.
                    print("\n\n*********************SALDIRI FIRSATI**********************\n\n")
                    cevap = input("Saldırı yapmak istiyor musunuz? (istiyorsanız *evet* yazınız): ").lower()
                    if cevap == 'evet':
                        saldiran = player1.savasci_secimi()
                        saldiri_gucu = saldiran.saldiri
                        if saldiri_gucu > 50:
                            print("\nSALDIRILDI\n")
                            oyun_alani[y][x] = 1
                        else:
                            print("\nSALDIRI YAPILAMADI.\n")
                    else:
                        continue
                else:
                    print("Bu kare zaten dolu. Tekrar deneyin.")
                    continue

            # Savaşçı seçimi
            if turn == 1:
                selected_warrior = player1.savasci_secimi()
            else:
                selected_warrior = player2.savasci_secimi()

            print(f"{selected_warrior.ad} seçildi.")
            oyun_alani[y][x] = turn
            passes = [0, 0]

            # Kazanan bulma
            winner = check_winner()
            if winner != 0:
                print(f"Oyuncu {winner} kazandı!")
                running = False

            turn = 3 - turn  # Sıranın değiştirilmesi

            # İkinci oyuncunun hamlesi ( Koordinatları ve savaşçı türü random seçiliyor = Yapay zeka mantığı )
            if running:
                tablo_doldurma(ekran)
                pygame.display.update()
                x = random.randint(0, COLS - 1)  # -1ler matris indeksleri 0'dan başladığı için
                y = random.randint(0, ROWS - 1)
                while oyun_alani[y][x] != 0:
                    x = random.randint(0, COLS - 1)
                    y = random.randint(0, ROWS - 1)
                selected_warrior = player2.savasci_secimi()
                print("\nOyuncu 2 oynuyor...")
                print(f"\nOyuncu 2'nin koordinatları: {x,y} ")
                print(f"Oyuncu 2'nin savaşçısı: {selected_warrior.ad} ")
                oyun_alani[y][x] = -1
                passes = [0, 0]

                # Kazanan bulma 2
                if winner != 0:
                    print(f"Oyuncu {winner} kazandı!")
                    running = False

                turn = 3 - turn  # Sıranın değişimi



if __name__ == "__main__":
    main()
