"""
Maryam Journey - Project Structure Setup
Jalankan script ini di dalam folder project Godot kamu:
  C:/Users/[nama]/maryam-journey/
  
Cara pakai:
  1. Copy file ini ke folder project Godot
  2. Buka terminal / cmd di folder itu
  3. Ketik: python setup_maryam_journey.py
"""

import os

# Daftar semua folder yang perlu dibuat
folders = [
    # Scenes
    "scenes/world",
    "scenes/locations/masjid",
    "scenes/locations/pondok_baca",
    "scenes/locations/taman_logika",
    "scenes/locations/kebun_karakter",
    "scenes/locations/rumah_maryam",
    "scenes/ui",
    "scenes/characters",

    # Scripts
    "scripts/player",
    "scripts/locations",
    "scripts/ui",
    "scripts/managers",

    # Assets
    "assets/sprites/character",
    "assets/sprites/world",
    "assets/sprites/ui",
    "assets/audio/music",
    "assets/audio/sfx",
    "assets/audio/voice",
    "assets/fonts",
    "assets/animations",

    # Data
    "data/hijaiyah",
    "data/stories",
    "data/quests",
    "data/progress",

    # Addons
    "addons",
]

# File .gdignore kosong supaya Godot tidak scan folder data mentah
gdignore_folders = ["data"]

def setup():
    print("=" * 50)
    print("  Maryam Journey - Project Setup")
    print("=" * 50)

    created = 0
    skipped = 0

    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            # Tambah file .gitkeep supaya folder masuk ke Git
            open(os.path.join(folder, ".gitkeep"), "w").close()
            print(f"  ✅ Dibuat : {folder}")
            created += 1
        else:
            print(f"  ⏭️  Ada    : {folder}")
            skipped += 1

    # Buat file README singkat di root
    readme = """# 🌙 Maryam Journey

Game edukasi Islam untuk Maryam — dibuat dengan cinta oleh Ayah.

## Struktur Project

- `scenes/`   → Scene Godot (.tscn)
- `scripts/`  → GDScript (.gd) dan C++ (.cpp/.h)
- `assets/`   → Gambar, audio, font
- `data/`     → Data konten (huruf, cerita, quest)
- `addons/`   → Plugin Godot

## Tech Stack

- Engine : Godot 4.7
- Bahasa : GDScript + C++ (GDExtension)
- Target  : PC (Windows) → Android

## Roadmap

- [ ] Fase 1 : Dunia & Karakter Maryam
- [ ] Fase 2 : Masjid An-Nur (Hijaiyah)
- [ ] Fase 3 : Pondok Baca
- [ ] Fase 4 : Taman Logika
- [ ] Fase 5 : Kebun Karakter
- [ ] Fase 6 : Polish & Android Export
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"\n  📄 README.md dibuat")

    print("\n" + "=" * 50)
    print(f"  Selesai! {created} folder dibuat, {skipped} sudah ada.")
    print("  Sekarang refresh FileSystem di Godot (klik ikon reload).")
    print("=" * 50)

if __name__ == "__main__":
    setup()
