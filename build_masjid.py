"""
Maryam Journey - Build Masjid An-Nur
Scene lengkap dengan 28 huruf Hijaiyah
python build_masjid.py
"""
import os, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🕌 Maryam Journey — Build Masjid An-Nur")
print("=" * 52)

# ── 1. MasjidScene.gd ────────────────────────────────────────
write(os.path.join(BASE, "scripts", "locations", "MasjidScene.gd"), """\
# =============================================================
#  scripts/locations/MasjidScene.gd
#  Scene interior Masjid An-Nur — Belajar Hijaiyah
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

# 28 huruf Hijaiyah lengkap
const HIJAIYAH : Array = [
\t{"arab": "ا", "nama": "Alif",  "warna": Color(0.95,0.30,0.30,1)},
\t{"arab": "ب", "nama": "Ba",    "warna": Color(0.95,0.50,0.20,1)},
\t{"arab": "ت", "nama": "Ta",    "warna": Color(0.95,0.75,0.15,1)},
\t{"arab": "ث", "nama": "Tsa",   "warna": Color(0.60,0.85,0.25,1)},
\t{"arab": "ج", "nama": "Jim",   "warna": Color(0.20,0.78,0.45,1)},
\t{"arab": "ح", "nama": "Ha",    "warna": Color(0.15,0.75,0.75,1)},
\t{"arab": "خ", "nama": "Kha",   "warna": Color(0.20,0.55,0.95,1)},
\t{"arab": "د", "nama": "Dal",   "warna": Color(0.40,0.30,0.90,1)},
\t{"arab": "ذ", "nama": "Dzal",  "warna": Color(0.65,0.25,0.90,1)},
\t{"arab": "ر", "nama": "Ra",    "warna": Color(0.90,0.25,0.65,1)},
\t{"arab": "ز", "nama": "Zai",   "warna": Color(0.95,0.30,0.30,1)},
\t{"arab": "س", "nama": "Sin",   "warna": Color(0.95,0.55,0.18,1)},
\t{"arab": "ش", "nama": "Syin",  "warna": Color(0.90,0.78,0.12,1)},
\t{"arab": "ص", "nama": "Shad",  "warna": Color(0.55,0.88,0.20,1)},
\t{"arab": "ض", "nama": "Dhad",  "warna": Color(0.18,0.80,0.48,1)},
\t{"arab": "ط", "nama": "Tha",   "warna": Color(0.12,0.78,0.78,1)},
\t{"arab": "ظ", "nama": "Zha",   "warna": Color(0.18,0.58,0.95,1)},
\t{"arab": "ع", "nama": "Ain",   "warna": Color(0.38,0.28,0.92,1)},
\t{"arab": "غ", "nama": "Ghain", "warna": Color(0.62,0.22,0.92,1)},
\t{"arab": "ف", "nama": "Fa",    "warna": Color(0.92,0.22,0.62,1)},
\t{"arab": "ق", "nama": "Qaf",   "warna": Color(0.95,0.32,0.32,1)},
\t{"arab": "ك", "nama": "Kaf",   "warna": Color(0.95,0.52,0.18,1)},
\t{"arab": "ل", "nama": "Lam",   "warna": Color(0.88,0.80,0.10,1)},
\t{"arab": "م", "nama": "Mim",   "warna": Color(0.52,0.88,0.18,1)},
\t{"arab": "ن", "nama": "Nun",   "warna": Color(0.15,0.82,0.50,1)},
\t{"arab": "و", "nama": "Wau",   "warna": Color(0.12,0.80,0.80,1)},
\t{"arab": "ه", "nama": "Ha",    "warna": Color(0.18,0.60,0.95,1)},
\t{"arab": "ي", "nama": "Ya",    "warna": Color(0.60,0.22,0.92,1)},
]

# State
var _total_kartu    : int  = 28
var _sudah_diklik   : int  = 0
var _kartu_selesai  : Array = []
var _selesai_semua  : bool = false

# Node refs
@onready var _kartu_container : GridContainer = $UI/Scroll/Grid
@onready var _lbl_progress    : Label         = $UI/TopBar/LblProgress
@onready var _lbl_nama        : Label         = $UI/NamaPanel/LblNama
@onready var _btn_back        : Button        = $UI/TopBar/BtnBack
@onready var _panel_selesai   : Panel         = $UI/PanelSelesai
@onready var _btn_keluar      : Button        = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
\t_lbl_progress.text  = "0 / 28 huruf"
\t_lbl_nama.text      = "Sentuh huruf untuk belajar!"
\t_panel_selesai.visible = false
\t_btn_back.pressed.connect(_on_back)
\t_btn_keluar.pressed.connect(_on_back)
\t_build_kartu()


func _build_kartu() -> void:
\tfor i in HIJAIYAH.size():
\t\tvar data   : Dictionary = HIJAIYAH[i]
\t\tvar btn    := Button.new()
\t\tvar idx    := i

\t\tbtn.custom_minimum_size = Vector2(90, 90)
\t\tbtn.text                = data["arab"]
\t\tbtn.tooltip_text        = data["nama"]

\t\t# Style normal
\t\tvar sb_normal := StyleBoxFlat.new()
\t\tsb_normal.bg_color             = data["warna"]
\t\tsb_normal.corner_radius_top_left    = 14
\t\tsb_normal.corner_radius_top_right   = 14
\t\tsb_normal.corner_radius_bottom_left = 14
\t\tsb_normal.corner_radius_bottom_right= 14
\t\tsb_normal.border_width_left   = 3
\t\tsb_normal.border_width_top    = 3
\t\tsb_normal.border_width_right  = 3
\t\tsb_normal.border_width_bottom = 3
\t\tsb_normal.border_color        = Color(1,1,1,0.40)
\t\tsb_normal.content_margin_left   = 4
\t\tsb_normal.content_margin_right  = 4
\t\tsb_normal.content_margin_top    = 4
\t\tsb_normal.content_margin_bottom = 4

\t\t# Style sudah diklik (lebih gelap)
\t\tvar sb_done := StyleBoxFlat.new()
\t\tsb_done.bg_color = Color(
\t\t\tdata["warna"].r * 0.55,
\t\t\tdata["warna"].g * 0.55,
\t\t\tdata["warna"].b * 0.55,
\t\t\t1.0
\t\t)
\t\tsb_done.corner_radius_top_left    = 14
\t\tsb_done.corner_radius_top_right   = 14
\t\tsb_done.corner_radius_bottom_left = 14
\t\tsb_done.corner_radius_bottom_right= 14
\t\tsb_done.border_width_left   = 3
\t\tsb_done.border_width_top    = 3
\t\tsb_done.border_width_right  = 3
\t\tsb_done.border_width_bottom = 3
\t\tsb_done.border_color        = Color(1,1,1,0.80)

\t\tbtn.add_theme_stylebox_override("normal",   sb_normal)
\t\tbtn.add_theme_stylebox_override("hover",    sb_done)
\t\tbtn.add_theme_stylebox_override("pressed",  sb_done)
\t\tbtn.add_theme_font_size_override("font_size", 36)
\t\tbtn.add_theme_color_override("font_color", Color(1,1,1,1))

\t\tbtn.pressed.connect(func(): _on_kartu_pressed(idx, btn, sb_done))
\t\t_kartu_container.add_child(btn)


func _on_kartu_pressed(idx: int, btn: Button, sb_done: StyleBoxFlat) -> void:
\tif _selesai_semua:
\t\treturn
\tvar data : Dictionary = HIJAIYAH[idx]
\t_lbl_nama.text = data["arab"] + "  —  " + data["nama"]

\t# Tandai selesai jika belum
\tif idx not in _kartu_selesai:
\t\t_kartu_selesai.append(idx)
\t\t_sudah_diklik += 1
\t\tbtn.add_theme_stylebox_override("normal", sb_done)
\t\t# Tambah centang kecil
\t\tvar lbl_check := Label.new()
\t\tlbl_check.text = "✓"
\t\tlbl_check.add_theme_font_size_override("font_size", 14)
\t\tlbl_check.add_theme_color_override("font_color", Color(1,1,1,0.9))
\t\tlbl_check.position = Vector2(66, 4)
\t\tbtn.add_child(lbl_check)
\t\t_lbl_progress.text = str(_sudah_diklik) + " / 28 huruf"

\tif _sudah_diklik >= _total_kartu and not _selesai_semua:
\t\t_selesai_semua = true
\t\tawait get_tree().create_timer(0.5).timeout
\t\t_show_selesai()


func _show_selesai() -> void:
\tGameManager.add_star(3)
\t_panel_selesai.visible = true


func _on_back() -> void:
\tTransitionManager.go_to(WORLD_SCENE)
""")

# ── 2. MasjidScene.tscn ──────────────────────────────────────
write(os.path.join(BASE, "scenes", "locations", "MasjidScene.tscn"), """\
[gd_scene load_steps=8 format=3]

[ext_resource type="Script" path="res://scripts/locations/MasjidScene.gd" id="1_masjid"]

[sub_resource type="StyleBoxFlat" id="SB_bg"]
bg_color = Color(0.08, 0.06, 0.22, 1)

[sub_resource type="StyleBoxFlat" id="SB_topbar"]
bg_color = Color(0.05, 0.04, 0.16, 0.95)
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 0.60)

[sub_resource type="StyleBoxFlat" id="SB_namapanel"]
bg_color = Color(0.10, 0.08, 0.28, 0.96)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 0.70)
corner_radius_top_left = 14
corner_radius_top_right = 14
corner_radius_bottom_right = 14
corner_radius_bottom_left = 14

[sub_resource type="StyleBoxFlat" id="SB_selesai"]
bg_color = Color(0.06, 0.18, 0.10, 0.97)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(0.20, 0.80, 0.35, 1.0)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[sub_resource type="StyleBoxFlat" id="SB_btn_back"]
bg_color = Color(0.18, 0.14, 0.40, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 0.80)
corner_radius_top_left = 10
corner_radius_top_right = 10
corner_radius_bottom_right = 10
corner_radius_bottom_left = 10
content_margin_left = 16.0
content_margin_right = 16.0
content_margin_top = 8.0
content_margin_bottom = 8.0

[sub_resource type="StyleBoxFlat" id="SB_btn_keluar"]
bg_color = Color(0.14, 0.55, 0.25, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.20, 0.90, 0.40, 0.90)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 12.0
content_margin_bottom = 12.0

[node name="MasjidScene" type="Node2D"]
script = ExtResource("1_masjid")

[node name="BgDecor" type="ColorRect" parent="."]
color = Color(0.08, 0.06, 0.22, 1)
size = Vector2(1280, 720)

[node name="DomeDecorL" type="Polygon2D" parent="."]
color = Color(0.12, 0.22, 0.15, 0.60)
polygon = PackedVector2Array(0,720, 0,480, 60,420, 120,380, 180,420, 240,480, 240,720)

[node name="DomeDecorR" type="Polygon2D" parent="."]
color = Color(0.12, 0.22, 0.15, 0.60)
polygon = PackedVector2Array(1280,720, 1280,480, 1220,420, 1160,380, 1100,420, 1040,480, 1040,720)

[node name="UI" type="CanvasLayer" parent="."]

[node name="TopBar" type="Panel" parent="UI"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
theme_override_styles/panel = SubResource("SB_topbar")

[node name="LblJudul" type="Label" parent="UI/TopBar"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
text = "🕌  Masjid An-Nur  —  Belajar Hijaiyah"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(1.0, 0.90, 0.38, 1)

[node name="LblProgress" type="Label" parent="UI/TopBar"]
position = Vector2(900, 0)
size = Vector2(300, 60)
text = "0 / 28 huruf"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 14
theme_override_colors/font_color = Color(0.80, 0.80, 0.95, 1)

[node name="BtnBack" type="Button" parent="UI/TopBar"]
position = Vector2(12, 10)
size = Vector2(80, 40)
text = "← Balik"
theme_override_styles/normal = SubResource("SB_btn_back")
theme_override_styles/hover = SubResource("SB_btn_back")
theme_override_styles/pressed = SubResource("SB_btn_back")
theme_override_font_sizes/font_size = 13

[node name="NamaPanel" type="Panel" parent="UI"]
position = Vector2(340, 68)
size = Vector2(600, 52)
theme_override_styles/panel = SubResource("SB_namapanel")

[node name="LblNama" type="Label" parent="UI/NamaPanel"]
position = Vector2(0, 0)
size = Vector2(600, 52)
text = "Sentuh huruf untuk belajar!"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 18
theme_override_colors/font_color = Color(1.0, 0.96, 0.80, 1)

[node name="Scroll" type="ScrollContainer" parent="UI"]
position = Vector2(20, 130)
size = Vector2(1240, 560)

[node name="Grid" type="GridContainer" parent="UI/Scroll"]
columns = 7
theme_override_constants/h_separation = 12
theme_override_constants/v_separation = 12

[node name="PanelSelesai" type="Panel" parent="UI"]
position = Vector2(390, 185)
size = Vector2(500, 350)
visible = false
theme_override_styles/panel = SubResource("SB_selesai")

[node name="VBox" type="VBoxContainer" parent="UI/PanelSelesai"]
position = Vector2(32, 32)
size = Vector2(436, 286)
theme_override_constants/separation = 20

[node name="LblMasyaAllah" type="Label" parent="UI/PanelSelesai/VBox"]
text = "مَاشَاءَ اللّٰهُ"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 32
theme_override_colors/font_color = Color(1.0, 0.90, 0.20, 1)

[node name="LblSelesai" type="Label" parent="UI/PanelSelesai/VBox"]
text = "🌟 Maryam Hebat! 🌟"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 24
theme_override_colors/font_color = Color(0.90, 0.95, 0.80, 1)

[node name="LblDesc" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Kamu sudah mengenal\nsemua 28 huruf Hijaiyah!"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 16
theme_override_colors/font_color = Color(0.80, 0.90, 0.85, 1)

[node name="LblBintang" type="Label" parent="UI/PanelSelesai/VBox"]
text = "⭐ ⭐ ⭐  +3 Bintang!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="BtnKeluar" type="Button" parent="UI/PanelSelesai/VBox"]
text = "🏠  Kembali ke Dunia"
theme_override_styles/normal = SubResource("SB_btn_keluar")
theme_override_styles/hover = SubResource("SB_btn_keluar")
theme_override_styles/pressed = SubResource("SB_btn_keluar")
theme_override_font_sizes/font_size = 16
""")

# ── 3. Update WorldMap.tscn — tambah scene_path ke ZoneMasjid
wmap_path = os.path.join(BASE, "scenes", "world", "WorldMap.tscn")
with open(wmap_path, "r", encoding="utf-8") as f:
    wmap = f.read()

# Tambah scene_path ke ZoneMasjid
if 'scene_path = "res://scenes/locations/MasjidScene.tscn"' not in wmap:
    wmap = wmap.replace(
        'location_name = "Masjid An-Nur"\nlocation_key = "masjid"',
        'location_name = "Masjid An-Nur"\nlocation_key = "masjid"\nscene_path = "res://scenes/locations/MasjidScene.tscn"'
    )
    with open(wmap_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(wmap)
    print("  ✅  WorldMap.tscn — scene_path Masjid ditambahkan")

# ── 4. Git commit ─────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "feat: Masjid An-Nur scene — 28 huruf Hijaiyah interaktif"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

print("\n" + "=" * 52)
print("  SELESAI!")
print("  1. Godot → Project → Reload Current Project")
print("  2. F5 → jalan ke Masjid → tekan Enter")
print("  3. 28 kartu Hijaiyah muncul berwarna-warni")
print("  4. Klik semua → Masyaallah + 3 bintang!")
print("=" * 52 + "\n")
