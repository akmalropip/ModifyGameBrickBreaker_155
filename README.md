1. Kontrol di dalam game:

- SPASI : Memulai permainan (melepaskan bola).

- Mouse / Panah ← → / A & D : Menggerakkan mobil.

- F atau F11 : Buka mode Layar Penuh (Fullscreen).

- Esc : Keluar dari mode Fullscreen.

- R : Restart / Mengulang game dari awal.

- M : Minimize layar game.

2. Buat yang mau mengubah bentuk atau warna gamenya, kodenya sudah dibagi menjadi beberapa "blok" (Class) agar gampang dicari:

- class Ball
Tempat ngatur bola listrik. Kalau mau bolanya lebih cepat dari awal atau mau ganti warna pendaran listriknya, cari di sini.

- class CarPaddle
Tempat ngatur mobil. Mobil ini digambar dari gabungan bentuk-bentuk kotak dan oval. Tinggal ubah kode warna HEX-nya (misal dari biru #1269d3 jadi merah #ff0000) kalau mau ganti cat mobil.

- class LavaBrick
Tempat ngatur balok rintangan. Baloknya punya level nyawa (ada yang sekali pukul hancur, ada yang butuh 2 kali pukul). Kamu bisa ganti komposisi warna baloknya di bagian ini.

- class BrickBreaker
Ini adalah "otak" gamenya. Segala hal tentang skor, ngurangin nyawa, membaca tombol keyboard, sampai deteksi tabrakan (apakah bola nyentuh balok/mobil) diatur di dalam class ini.
