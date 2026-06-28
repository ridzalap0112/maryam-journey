"""
Maryam Journey - Build Pondok Baca
Huruf A-Z + kata pertama untuk anak 3-5 tahun
python build_pondok.py
"""
import os, subprocess, sys

BASE = os.getcwd()
SCRIPT_PATH = os.path.abspath(__file__)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n📚 Maryam Journey — Build Pondok Baca")
print("=" * 52)

# ── 1. PondokScene.gd ────────────────────────────────────────
write(os.path.join(BASE, "scripts", "locations", "PondokScene.gd"), """\
# =============================================================
#  scripts/locations/PondokScene.gd
#  Pondok Baca — Belajar Huruf A-Z + Kata Pertama
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

# 26 huruf A-Z dengan contoh kata & emoji
const HURUF : Array = [
\t{"huruf": "A", "kata": "Apel",    "emoji": "🍎"},
\t{"huruf": "B", "kata": "Buku",    "emoji": "📚"},
\t{"huruf": "C", "kata": "Cincin",  "emoji": "💍"},
\t{"huruf": "D", "kata": "Domba",   "emoji": "🐑"},
\t{"huruf": "E", "kata": "Elang",   "emoji": "🦅"},
\t{"huruf": "F", "kata": "Foto",    "emoji": "📷"},
\t{"huruf": "G", "kata": "Gajah",   "emoji": "🐘"},
\t{"huruf": "H", "kata": "Harimau", "emoji": "🐯"},
\t{"huruf": "I", "kata": "Ikan",    "emoji": "🐟"},
\t{"huruf": "J", "kata": "Jeruk",   "emoji": "🍊"},
\t{"huruf": "K", "kata": "Kucing",  "emoji": "🐱"},
\t{"huruf": "L", "kata": "Lampu",   "emoji": "💡"},
\t{"huruf": "M", "kata": "Mangga",  "emoji": "🥭"},
\t{"huruf": "N", "kata": "Nanas",   "emoji": "🍍"},
\t{"huruf": "O", "kata": "Onta",    "emoji": "🐪"},
\t{"huruf": "P", "kata": "Pisang",  "emoji": "🍌"},
\t{"huruf": "Q", "kata": "Quran",   "emoji": "📖"},
\t{"huruf": "R", "kata": "Roti",    "emoji": "🍞"},
\t{"huruf": "S", "kata": "Singa",   "emoji": "🦁"},
\t{"huruf": "T", "kata": "Topi",    "emoji": "🎩"},
\t{"huruf": "U", "kata": "Ulat",    "emoji": "🐛"},
\t{"huruf": "V", "kata": "Vas",     "emoji": "🏺"},
\t{"huruf": "W", "kata": "Wortel",  "emoji": "🥕"},
\t{"huruf": "X", "kata": "Xilofon", "emoji": "🎵"},
\t{"huruf": "Y", "kata": "Yogurt",  "emoji": "🥛"},
\t{"huruf": "Z", "kata": "Zebra",   "emoji": "🦓"},
]

# Warna kartu per huruf (pastel cerah)
const WARNA : Array = [
\tColor(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
\tColor(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
\tColor(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
\tColor(0.18,0.55,0.95,1), Color(0.42,0.28,0.92,1),
\tColor(0.65,0.22,0.92,1), Color(0.92,0.22,0.65,1),
\tColor(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
\tColor(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
\tColor(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
\tColor(0.18,0.55,0.95,1), Color(0.42,0.28,0.92,1),
\tColor(0.65,0.22,0.92,1), Color(0.92,0.22,0.65,1),
\tColor(0.95,0.35,0.35,1), Color(0.95,0.55,0.20,1),
\tColor(0.92,0.80,0.12,1), Color(0.55,0.88,0.22,1),
\tColor(0.18,0.80,0.50,1), Color(0.12,0.78,0.80,1),
]

var _sudah_klik   : int   = 0
var _klik_list    : Array = []
var _selesai      : bool  = false

@onready var _grid          : GridContainer = $UI/Scroll/Grid
@onready var _lbl_progress  : Label         = $UI/TopBar/LblProgress
@onready var _lbl_info      : Label         = $UI/InfoPanel/LblInfo
@onready var _btn_back      : Button        = $UI/TopBar/BtnBack
@onready var _panel_selesai : Panel         = $UI/PanelSelesai
@onready var _btn_keluar    : Button        = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
\t_lbl_progress.text  = "0 / 26 huruf"
\t_lbl_info.text      = "Sentuh huruf untuk belajar!"
\t_panel_selesai.visible = false
\t_btn_back.pressed.connect(_on_back)
\t_btn_keluar.pressed.connect(_on_back)
\t_build_kartu()


func _build_kartu() -> void:
\tfor i in HURUF.size():
\t\tvar data := HURUF[i]
\t\tvar warna := WARNA[i]
\t\tvar btn   := Button.new()
\t\tvar idx   := i

\t\tbtn.custom_minimum_size = Vector2(100, 100)

\t\t# Isi tombol: huruf besar + emoji + kata
\t\tvar lbl_huruf := Label.new()
\t\tlbl_huruf.text = data["huruf"]
\t\tlbl_huruf.add_theme_font_size_override("font_size", 38)
\t\tlbl_huruf.add_theme_color_override("font_color", Color(1,1,1,1))
\t\tlbl_huruf.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\t\tlbl_huruf.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)

\t\tvar lbl_kata := Label.new()
\t\tlbl_kata.text = data["emoji"] + " " + data["kata"]
\t\tlbl_kata.add_theme_font_size_override("font_size", 10)
\t\tlbl_kata.add_theme_color_override("font_color", Color(1,1,1,0.90))
\t\tlbl_kata.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\t\tlbl_kata.vertical_alignment   = VERTICAL_ALIGNMENT_BOTTOM
\t\tlbl_kata.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
\t\tlbl_kata.offset_bottom = -6.0

\t\t# StyleBox normal
\t\tvar sb := StyleBoxFlat.new()
\t\tsb.bg_color = warna
\t\tsb.corner_radius_top_left     = 16
\t\tsb.corner_radius_top_right    = 16
\t\tsb.corner_radius_bottom_left  = 16
\t\tsb.corner_radius_bottom_right = 16
\t\tsb.border_width_left   = 3
\t\tsb.border_width_top    = 3
\t\tsb.border_width_right  = 3
\t\tsb.border_width_bottom = 3
\t\tsb.border_color        = Color(1,1,1,0.35)
\t\tsb.shadow_color        = Color(0,0,0,0.25)
\t\tsb.shadow_size         = 4

\t\t# StyleBox sudah diklik
\t\tvar sb_done := StyleBoxFlat.new()
\t\tsb_done.bg_color = Color(warna.r*0.50, warna.g*0.50, warna.b*0.50, 1)
\t\tsb_done.corner_radius_top_left     = 16
\t\tsb_done.corner_radius_top_right    = 16
\t\tsb_done.corner_radius_bottom_left  = 16
\t\tsb_done.corner_radius_bottom_right = 16
\t\tsb_done.border_width_left   = 3
\t\tsb_done.border_width_top    = 3
\t\tsb_done.border_width_right  = 3
\t\tsb_done.border_width_bottom = 3
\t\tsb_done.border_color        = Color(1,1,1,0.85)

\t\tbtn.add_theme_stylebox_override("normal",  sb)
\t\tbtn.add_theme_stylebox_override("hover",   sb_done)
\t\tbtn.add_theme_stylebox_override("pressed", sb_done)
\t\tbtn.add_child(lbl_huruf)
\t\tbtn.add_child(lbl_kata)
\t\tbtn.pressed.connect(func(): _on_kartu(idx, btn, sb_done))
\t\t_grid.add_child(btn)


func _on_kartu(idx: int, btn: Button, sb_done: StyleBoxFlat) -> void:
\tif _selesai:
\t\treturn
\tvar data := HURUF[idx]
\t_lbl_info.text = data["huruf"] + "  —  " + data["emoji"] + "  " + data["kata"]

\tif idx not in _klik_list:
\t\t_klik_list.append(idx)
\t\t_sudah_klik += 1
\t\tbtn.add_theme_stylebox_override("normal", sb_done)
\t\tvar chk := Label.new()
\t\tchk.text = "✓"
\t\tchk.add_theme_font_size_override("font_size", 14)
\t\tchk.add_theme_color_override("font_color", Color(1,1,1,0.95))
\t\tchk.position = Vector2(76, 4)
\t\tbtn.add_child(chk)
\t\t_lbl_progress.text = str(_sudah_klik) + " / 26 huruf"

\tif _sudah_klik >= 26 and not _selesai:
\t\t_selesai = true
\t\tawait get_tree().create_timer(0.5).timeout
\t\t_show_selesai()


func _show_selesai() -> void:
\tGameManager.add_star(3)
\t_panel_selesai.visible = true


func _on_back() -> void:
\tTransitionManager.go_to(WORLD_SCENE)
""")

# ── 2. PondokScene.tscn ──────────────────────────────────────
write(os.path.join(BASE, "scenes", "locations", "PondokScene.tscn"), """\
[gd_scene load_steps=7 format=3]

[ext_resource type="Script" path="res://scripts/locations/PondokScene.gd" id="1_pondok"]

[sub_resource type="StyleBoxFlat" id="SB_topbar"]
bg_color = Color(0.06, 0.10, 0.22, 0.97)
border_width_bottom = 2
border_color = Color(0.95, 0.80, 0.20, 0.60)

[sub_resource type="StyleBoxFlat" id="SB_info"]
bg_color = Color(0.08, 0.12, 0.30, 0.96)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.95, 0.80, 0.20, 0.70)
corner_radius_top_left = 14
corner_radius_top_right = 14
corner_radius_bottom_right = 14
corner_radius_bottom_left = 14

[sub_resource type="StyleBoxFlat" id="SB_selesai"]
bg_color = Color(0.05, 0.14, 0.25, 0.97)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(0.20, 0.65, 0.95, 1.0)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[sub_resource type="StyleBoxFlat" id="SB_btn_back"]
bg_color = Color(0.14, 0.18, 0.40, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.95, 0.80, 0.20, 0.80)
corner_radius_top_left = 10
corner_radius_top_right = 10
corner_radius_bottom_right = 10
corner_radius_bottom_left = 10
content_margin_left = 16.0
content_margin_right = 16.0
content_margin_top = 8.0
content_margin_bottom = 8.0

[sub_resource type="StyleBoxFlat" id="SB_btn_keluar"]
bg_color = Color(0.10, 0.38, 0.70, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.20, 0.65, 0.95, 0.90)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 12.0
content_margin_bottom = 12.0

[node name="PondokScene" type="Node2D"]
script = ExtResource("1_pondok")

[node name="BgSky" type="ColorRect" parent="."]
color = Color(0.07, 0.10, 0.28, 1)
size = Vector2(1280, 720)

[node name="BgGlow" type="Polygon2D" parent="."]
color = Color(0.15, 0.30, 0.60, 0.22)
polygon = PackedVector2Array(200,0, 1080,0, 1280,360, 0,360)

[node name="BookDecorL" type="Polygon2D" parent="."]
color = Color(0.14, 0.22, 0.50, 0.50)
polygon = PackedVector2Array(0,720, 0,500, 50,460, 100,500, 100,720)

[node name="BookDecorR" type="Polygon2D" parent="."]
color = Color(0.14, 0.22, 0.50, 0.50)
polygon = PackedVector2Array(1280,720, 1280,500, 1230,460, 1180,500, 1180,720)

[node name="UI" type="CanvasLayer" parent="."]

[node name="TopBar" type="Panel" parent="UI"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
theme_override_styles/panel = SubResource("SB_topbar")

[node name="LblJudul" type="Label" parent="UI/TopBar"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
text = "📚  Pondok Baca  —  Belajar Huruf A-Z"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(1.0, 0.92, 0.40, 1)

[node name="LblProgress" type="Label" parent="UI/TopBar"]
position = Vector2(900, 0)
size = Vector2(300, 60)
text = "0 / 26 huruf"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 14
theme_override_colors/font_color = Color(0.80, 0.85, 0.95, 1)

[node name="BtnBack" type="Button" parent="UI/TopBar"]
position = Vector2(12, 10)
size = Vector2(80, 40)
text = "← Balik"
theme_override_styles/normal = SubResource("SB_btn_back")
theme_override_styles/hover = SubResource("SB_btn_back")
theme_override_styles/pressed = SubResource("SB_btn_back")
theme_override_font_sizes/font_size = 13

[node name="InfoPanel" type="Panel" parent="UI"]
position = Vector2(240, 68)
size = Vector2(800, 52)
theme_override_styles/panel = SubResource("SB_info")

[node name="LblInfo" type="Label" parent="UI/InfoPanel"]
position = Vector2(0, 0)
size = Vector2(800, 52)
text = "Sentuh huruf untuk belajar!"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 18
theme_override_colors/font_color = Color(1.0, 0.96, 0.80, 1)

[node name="Scroll" type="ScrollContainer" parent="UI"]
position = Vector2(20, 130)
size = Vector2(1240, 570)

[node name="Grid" type="GridContainer" parent="UI/Scroll"]
columns = 7
theme_override_constants/h_separation = 14
theme_override_constants/v_separation = 14

[node name="PanelSelesai" type="Panel" parent="UI"]
position = Vector2(390, 160)
size = Vector2(500, 400)
visible = false
theme_override_styles/panel = SubResource("SB_selesai")

[node name="VBox" type="VBoxContainer" parent="UI/PanelSelesai"]
position = Vector2(32, 32)
size = Vector2(436, 336)
theme_override_constants/separation = 20

[node name="LblEmoji" type="Label" parent="UI/PanelSelesai/VBox"]
text = "📚 ✨ 📖"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 40

[node name="LblSelesai" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Maryam Pintar!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 28
theme_override_colors/font_color = Color(0.90, 0.95, 1.0, 1)

[node name="LblDesc" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Kamu sudah mengenal\nsemua 26 huruf A sampai Z!"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 16
theme_override_colors/font_color = Color(0.80, 0.88, 0.95, 1)

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

# ── 3. Update WorldMap.tscn — tambah scene_path ZonePondok ──
wmap_path = os.path.join(BASE, "scenes", "world", "WorldMap.tscn")
with open(wmap_path, "r", encoding="utf-8") as f:
    wmap = f.read()

if 'scene_path = "res://scenes/locations/PondokScene.tscn"' not in wmap:
    wmap = wmap.replace(
        'location_name = "Pondok Baca"\nlocation_key = "pondok"',
        'location_name = "Pondok Baca"\nlocation_key = "pondok"\nscene_path = "res://scenes/locations/PondokScene.tscn"'
    )
    with open(wmap_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(wmap)
    print("  ✅  WorldMap.tscn — scene_path Pondok ditambahkan")

# ── 4. Git commit ─────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "feat: Pondok Baca — 26 huruf A-Z interaktif dengan kata & emoji"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

# ── 5. Auto-delete script ini ─────────────────────────────────
print("\n  🗑️  Menghapus script ini...")
try:
    os.remove(SCRIPT_PATH)
    print("  ✅  build_pondok.py dihapus otomatis")
except Exception as e:
    print(f"  ⚠️   Gagal hapus: {e}")

print("\n" + "=" * 52)
print("  SELESAI!")
print("  Godot → Project → Reload Current Project → F5")
print("  Jalan ke Pondok Baca → Enter → 26 huruf A-Z!")
print("=" * 52 + "\n")
