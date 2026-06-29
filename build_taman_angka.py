"""
Maryam Journey - Upgrade Taman Logika
Tambah modul Belajar Angka 1-10
python build_taman_angka.py
"""
import os, subprocess

BASE = os.getcwd()
SCRIPT_PATH = os.path.abspath(__file__)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🧩 Maryam Journey — Upgrade Taman Logika + Angka")
print("=" * 52)

# Taman sekarang punya 2 tab:
# Tab 1: Cocokkan Warna (sudah ada, dipertahankan)
# Tab 2: Belajar Angka 1-10 (baru)
# Keduanya dalam satu TamanScene.gd

write(os.path.join(BASE, "scripts", "locations", "TamanScene.gd"), """\
# =============================================================
#  scripts/locations/TamanScene.gd
#  Taman Logika — Warna & Angka
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

# ── Data Warna ───────────────────────────────────────────────
const SOAL_WARNA : Array[Dictionary] = [
\t{"nama": "MERAH",  "warna": Color(0.92,0.20,0.20,1), "salah": [Color(0.20,0.55,0.92,1), Color(0.20,0.82,0.35,1), Color(0.92,0.78,0.10,1)]},
\t{"nama": "BIRU",   "warna": Color(0.20,0.50,0.92,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.82,0.45,0.10,1), Color(0.55,0.20,0.82,1)]},
\t{"nama": "HIJAU",  "warna": Color(0.15,0.78,0.35,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.92,0.78,0.10,1)]},
\t{"nama": "KUNING", "warna": Color(0.95,0.82,0.10,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.55,0.20,0.82,1)]},
\t{"nama": "UNGU",   "warna": Color(0.55,0.18,0.85,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.92,0.78,0.10,1)]},
\t{"nama": "ORANYE", "warna": Color(0.95,0.52,0.10,1), "salah": [Color(0.20,0.50,0.92,1), Color(0.15,0.78,0.35,1), Color(0.55,0.18,0.85,1)]},
\t{"nama": "PINK",   "warna": Color(0.95,0.35,0.65,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.95,0.52,0.10,1)]},
\t{"nama": "COKLAT", "warna": Color(0.55,0.32,0.12,1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.95,0.35,0.65,1)]},
]

# ── Data Angka ───────────────────────────────────────────────
const ANGKA : Array[Dictionary] = [
\t{"angka": 1,  "arab": "١", "emoji": "🌙",  "nama": "Satu"},
\t{"angka": 2,  "arab": "٢", "emoji": "⭐⭐", "nama": "Dua"},
\t{"angka": 3,  "arab": "٣", "emoji": "🍎🍎🍎", "nama": "Tiga"},
\t{"angka": 4,  "arab": "٤", "emoji": "🐟🐟🐟🐟", "nama": "Empat"},
\t{"angka": 5,  "arab": "٥", "emoji": "🌺🌺🌺🌺🌺", "nama": "Lima"},
\t{"angka": 6,  "arab": "٦", "emoji": "🐝🐝🐝🐝🐝🐝", "nama": "Enam"},
\t{"angka": 7,  "arab": "٧", "emoji": "🌈", "nama": "Tujuh"},
\t{"angka": 8,  "arab": "٨", "emoji": "🎵🎵🎵🎵🎵🎵🎵🎵", "nama": "Delapan"},
\t{"angka": 9,  "arab": "٩", "emoji": "🌟🌟🌟🌟🌟🌟🌟🌟🌟", "nama": "Sembilan"},
\t{"angka": 10, "arab": "١٠","emoji": "🎉", "nama": "Sepuluh"},
]

const WARNA_KARTU : Array[Color] = [
\tColor(0.92,0.25,0.25,1), Color(0.92,0.55,0.15,1),
\tColor(0.88,0.82,0.10,1), Color(0.22,0.80,0.35,1),
\tColor(0.12,0.75,0.75,1), Color(0.18,0.50,0.92,1),
\tColor(0.50,0.22,0.88,1), Color(0.88,0.22,0.60,1),
\tColor(0.22,0.75,0.50,1), Color(0.92,0.50,0.15,1),
]

# ── State ─────────────────────────────────────────────────────
var _mode            : String = "menu"  # "menu" | "warna" | "angka"
var _idx_warna       : int    = 0
var _benar_warna     : int    = 0
var _selesai_warna   : bool   = false
var _angka_klik      : Array  = []
var _selesai_angka   : bool   = false

# ── Node refs ─────────────────────────────────────────────────
@onready var _btn_back       : Button        = $UI/TopBar/BtnBack
@onready var _lbl_progress   : Label         = $UI/TopBar/LblProgress

# Panel Menu
@onready var _panel_menu     : Panel         = $UI/PanelMenu
@onready var _btn_warna      : Button        = $UI/PanelMenu/VBox/BtnWarna
@onready var _btn_angka      : Button        = $UI/PanelMenu/VBox/BtnAngka

# Panel Warna
@onready var _panel_warna    : Panel         = $UI/PanelWarna
@onready var _lbl_soal_w     : Label         = $UI/PanelWarna/LblSoal
@onready var _lbl_nama_w     : Label         = $UI/PanelWarna/LblNamaWarna
@onready var _lbl_feedback_w : Label         = $UI/PanelWarna/LblFeedback
@onready var _pilihan_w      : HBoxContainer = $UI/PanelWarna/PilihanBox

# Panel Angka
@onready var _panel_angka    : Panel         = $UI/PanelAngka
@onready var _grid_angka     : GridContainer = $UI/PanelAngka/GridAngka
@onready var _lbl_info_a     : Label         = $UI/PanelAngka/LblInfo

# Panel Selesai
@onready var _panel_selesai  : Panel         = $UI/PanelSelesai
@onready var _lbl_selesai    : Label         = $UI/PanelSelesai/VBox/LblSelesai
@onready var _lbl_bintang    : Label         = $UI/PanelSelesai/VBox/LblBintang
@onready var _btn_menu_lagi  : Button        = $UI/PanelSelesai/VBox/BtnMenuLagi
@onready var _btn_keluar     : Button        = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
\t_panel_menu.visible    = true
\t_panel_warna.visible   = false
\t_panel_angka.visible   = false
\t_panel_selesai.visible = false
\t_lbl_progress.text     = "🧩 Taman Logika"
\t_btn_back.pressed.connect(_on_back)
\t_btn_warna.pressed.connect(_start_warna)
\t_btn_angka.pressed.connect(_start_angka)
\t_btn_menu_lagi.pressed.connect(_kembali_menu)
\t_btn_keluar.pressed.connect(_on_back)


# ── MENU ─────────────────────────────────────────────────────
func _kembali_menu() -> void:
\t_panel_menu.visible    = true
\t_panel_warna.visible   = false
\t_panel_angka.visible   = false
\t_panel_selesai.visible = false
\t_lbl_progress.text     = "🧩 Taman Logika"


# ── MODUL WARNA ──────────────────────────────────────────────
func _start_warna() -> void:
\t_idx_warna     = 0
\t_benar_warna   = 0
\t_selesai_warna = false
\t_panel_menu.visible  = false
\t_panel_warna.visible = true
\t_tampil_soal_warna()


func _tampil_soal_warna() -> void:
\tif _idx_warna >= SOAL_WARNA.size():
\t\t_selesai("warna")
\t\treturn
\tvar soal : Dictionary = SOAL_WARNA[_idx_warna]
\t_lbl_soal_w.text = "Pilih warna:"
\t_lbl_nama_w.text = soal["nama"]
\t_lbl_nama_w.add_theme_color_override("font_color", soal["warna"])
\t_lbl_progress.text = "Warna " + str(_idx_warna + 1) + " / " + str(SOAL_WARNA.size())
\t_lbl_feedback_w.visible = false
\tfor c in _pilihan_w.get_children():
\t\tc.queue_free()
\tvar pilihan : Array[Dictionary] = []
\tpilihan.append({"warna": soal["warna"], "benar": true})
\tfor w : Color in soal["salah"]:
\t\tpilihan.append({"warna": w, "benar": false})
\tpilihan.shuffle()
\tfor item : Dictionary in pilihan:
\t\tvar btn      : Button       = Button.new()
\t\tvar w        : Color        = item["warna"]
\t\tvar is_benar : bool         = item["benar"]
\t\tvar sb       : StyleBoxFlat = StyleBoxFlat.new()
\t\tsb.bg_color                   = w
\t\tsb.corner_radius_top_left     = 20
\t\tsb.corner_radius_top_right    = 20
\t\tsb.corner_radius_bottom_left  = 20
\t\tsb.corner_radius_bottom_right = 20
\t\tsb.border_width_left          = 4
\t\tsb.border_width_top           = 4
\t\tsb.border_width_right         = 4
\t\tsb.border_width_bottom        = 4
\t\tsb.border_color               = Color(1,1,1,0.40)
\t\tsb.shadow_color               = Color(0,0,0,0.30)
\t\tsb.shadow_size                = 6
\t\tbtn.custom_minimum_size = Vector2(140, 140)
\t\tbtn.add_theme_stylebox_override("normal",  sb)
\t\tbtn.add_theme_stylebox_override("hover",   sb)
\t\tbtn.add_theme_stylebox_override("pressed", sb)
\t\tbtn.pressed.connect(func(): _on_pilih_warna(is_benar))
\t\t_pilihan_w.add_child(btn)


func _on_pilih_warna(is_benar: bool) -> void:
\tif _selesai_warna:
\t\treturn
\t_lbl_feedback_w.visible = true
\tif is_benar:
\t\t_benar_warna += 1
\t\t_lbl_feedback_w.text = "✅  Betul! Hebat Maryam!"
\t\t_lbl_feedback_w.add_theme_color_override("font_color", Color(0.20,0.90,0.40,1))
\telse:
\t\t_lbl_feedback_w.text = "❌  Coba lagi ya!"
\t\t_lbl_feedback_w.add_theme_color_override("font_color", Color(0.95,0.35,0.35,1))
\tawait get_tree().create_timer(0.8).timeout
\t_idx_warna += 1
\t_tampil_soal_warna()


# ── MODUL ANGKA ──────────────────────────────────────────────
func _start_angka() -> void:
\t_angka_klik   = []
\t_selesai_angka = false
\t_panel_menu.visible  = false
\t_panel_angka.visible = true
\t_lbl_info_a.text     = "Sentuh angka untuk belajar!"
\t_lbl_progress.text   = "0 / 10 angka"
\t_build_kartu_angka()


func _build_kartu_angka() -> void:
\tfor c in _grid_angka.get_children():
\t\tc.queue_free()
\tfor i in ANGKA.size():
\t\tvar data  : Dictionary = ANGKA[i]
\t\tvar warna : Color      = WARNA_KARTU[i]
\t\tvar btn   : Button     = Button.new()
\t\tvar idx   : int        = i
\t\tbtn.custom_minimum_size = Vector2(108, 108)

\t\tvar lbl_angka : Label = Label.new()
\t\tlbl_angka.text = str(data["angka"])
\t\tlbl_angka.add_theme_font_size_override("font_size", 42)
\t\tlbl_angka.add_theme_color_override("font_color", Color(1,1,1,1))
\t\tlbl_angka.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\t\tlbl_angka.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
\t\tlbl_angka.offset_bottom = -28.0

\t\tvar lbl_nama : Label = Label.new()
\t\tlbl_nama.text = data["nama"]
\t\tlbl_nama.add_theme_font_size_override("font_size", 11)
\t\tlbl_nama.add_theme_color_override("font_color", Color(1,1,1,0.90))
\t\tlbl_nama.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
\t\tlbl_nama.vertical_alignment   = VERTICAL_ALIGNMENT_BOTTOM
\t\tlbl_nama.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
\t\tlbl_nama.offset_bottom = -4.0

\t\tvar sb : StyleBoxFlat = StyleBoxFlat.new()
\t\tsb.bg_color                   = warna
\t\tsb.corner_radius_top_left     = 16
\t\tsb.corner_radius_top_right    = 16
\t\tsb.corner_radius_bottom_left  = 16
\t\tsb.corner_radius_bottom_right = 16
\t\tsb.border_width_left          = 3
\t\tsb.border_width_top           = 3
\t\tsb.border_width_right         = 3
\t\tsb.border_width_bottom        = 3
\t\tsb.border_color               = Color(1,1,1,0.35)
\t\tsb.shadow_color               = Color(0,0,0,0.25)
\t\tsb.shadow_size                = 4

\t\tvar sb_done : StyleBoxFlat = StyleBoxFlat.new()
\t\tsb_done.bg_color                   = Color(warna.r*0.50,warna.g*0.50,warna.b*0.50,1)
\t\tsb_done.corner_radius_top_left     = 16
\t\tsb_done.corner_radius_top_right    = 16
\t\tsb_done.corner_radius_bottom_left  = 16
\t\tsb_done.corner_radius_bottom_right = 16
\t\tsb_done.border_width_left          = 3
\t\tsb_done.border_width_top           = 3
\t\tsb_done.border_width_right         = 3
\t\tsb_done.border_width_bottom        = 3
\t\tsb_done.border_color               = Color(1,1,1,0.85)

\t\tbtn.add_theme_stylebox_override("normal",  sb)
\t\tbtn.add_theme_stylebox_override("hover",   sb_done)
\t\tbtn.add_theme_stylebox_override("pressed", sb_done)
\t\tbtn.add_child(lbl_angka)
\t\tbtn.add_child(lbl_nama)
\t\tbtn.pressed.connect(func(): _on_kartu_angka(idx, btn, sb_done, data))
\t\t_grid_angka.add_child(btn)


func _on_kartu_angka(idx: int, btn: Button, sb_done: StyleBoxFlat, data: Dictionary) -> void:
\tif _selesai_angka:
\t\treturn
\t_lbl_info_a.text = str(data["angka"]) + "  —  " + data["nama"] + "  " + data["emoji"]
\tif idx not in _angka_klik:
\t\t_angka_klik.append(idx)
\t\tbtn.add_theme_stylebox_override("normal", sb_done)
\t\tvar chk : Label = Label.new()
\t\tchk.text = "✓"
\t\tchk.add_theme_font_size_override("font_size", 14)
\t\tchk.add_theme_color_override("font_color", Color(1,1,1,0.95))
\t\tchk.position = Vector2(84, 4)
\t\tbtn.add_child(chk)
\t\t_lbl_progress.text = str(_angka_klik.size()) + " / 10 angka"
\tif _angka_klik.size() >= 10 and not _selesai_angka:
\t\t_selesai_angka = true
\t\tawait get_tree().create_timer(0.5).timeout
\t\t_selesai("angka")


# ── SELESAI ──────────────────────────────────────────────────
func _selesai(mode: String) -> void:
\tGameManager.add_star(3)
\t_panel_warna.visible   = false
\t_panel_angka.visible   = false
\t_panel_selesai.visible = true
\tif mode == "warna":
\t\t_lbl_selesai.text  = "🌈 Maryam Kenal Semua Warna!"
\t\t_lbl_bintang.text  = "Benar: " + str(_benar_warna) + " / " + str(SOAL_WARNA.size()) + "\\n⭐ ⭐ ⭐  +3 Bintang!"
\telse:
\t\t_lbl_selesai.text  = "🔢 Maryam Bisa Berhitung!"
\t\t_lbl_bintang.text  = "Angka 1 sampai 10 sudah dikuasai!\\n⭐ ⭐ ⭐  +3 Bintang!"


func _on_back() -> void:
\tTransitionManager.go_to(WORLD_SCENE)
""")

write(os.path.join(BASE, "scenes", "locations", "TamanScene.tscn"), """\
[gd_scene load_steps=9 format=3]

[ext_resource type="Script" path="res://scripts/locations/TamanScene.gd" id="1_taman"]

[sub_resource type="StyleBoxFlat" id="SB_topbar"]
bg_color = Color(0.05, 0.14, 0.08, 0.97)
border_width_bottom = 2
border_color = Color(0.22, 0.78, 0.35, 0.70)

[sub_resource type="StyleBoxFlat" id="SB_menu"]
bg_color = Color(0.06, 0.16, 0.09, 0.96)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(0.22, 0.78, 0.35, 0.75)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[sub_resource type="StyleBoxFlat" id="SB_panel"]
bg_color = Color(0.06, 0.16, 0.09, 0.94)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.22, 0.70, 0.30, 0.65)
corner_radius_top_left = 16
corner_radius_top_right = 16
corner_radius_bottom_right = 16
corner_radius_bottom_left = 16

[sub_resource type="StyleBoxFlat" id="SB_selesai"]
bg_color = Color(0.05, 0.16, 0.09, 0.97)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(0.22, 0.85, 0.40, 1.0)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[sub_resource type="StyleBoxFlat" id="SB_btn_back"]
bg_color = Color(0.10, 0.22, 0.12, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.22, 0.78, 0.35, 0.80)
corner_radius_top_left = 10
corner_radius_top_right = 10
corner_radius_bottom_right = 10
corner_radius_bottom_left = 10
content_margin_left = 16.0
content_margin_right = 16.0
content_margin_top = 8.0
content_margin_bottom = 8.0

[sub_resource type="StyleBoxFlat" id="SB_btn_modul"]
bg_color = Color(0.12, 0.42, 0.18, 0.95)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(0.30, 0.90, 0.40, 0.90)
corner_radius_top_left = 16
corner_radius_top_right = 16
corner_radius_bottom_right = 16
corner_radius_bottom_left = 16
content_margin_left = 28.0
content_margin_right = 28.0
content_margin_top = 20.0
content_margin_bottom = 20.0

[sub_resource type="StyleBoxFlat" id="SB_btn_keluar"]
bg_color = Color(0.14, 0.55, 0.25, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.22, 0.85, 0.40, 0.90)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 12.0
content_margin_bottom = 12.0

[sub_resource type="StyleBoxFlat" id="SB_info"]
bg_color = Color(0.06, 0.18, 0.09, 0.92)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.22, 0.70, 0.30, 0.60)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12

[node name="TamanScene" type="Node2D"]
script = ExtResource("1_taman")

[node name="BgSky" type="ColorRect" parent="."]
color = Color(0.07, 0.14, 0.09, 1)
size = Vector2(1280, 720)

[node name="GlowGreen" type="Polygon2D" parent="."]
color = Color(0.10, 0.45, 0.18, 0.18)
polygon = PackedVector2Array(0,0, 1280,0, 1280,400, 0,400)

[node name="UI" type="CanvasLayer" parent="."]

[node name="TopBar" type="Panel" parent="UI"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
theme_override_styles/panel = SubResource("SB_topbar")

[node name="LblJudul" type="Label" parent="UI/TopBar"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
text = "🧩  Taman Logika"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 22
theme_override_colors/font_color = Color(0.55, 0.95, 0.55, 1)

[node name="LblProgress" type="Label" parent="UI/TopBar"]
position = Vector2(880, 0)
size = Vector2(320, 60)
text = "🧩 Taman Logika"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 14
theme_override_colors/font_color = Color(0.80, 0.95, 0.80, 1)

[node name="BtnBack" type="Button" parent="UI/TopBar"]
position = Vector2(12, 10)
size = Vector2(80, 40)
text = "← Balik"
theme_override_styles/normal = SubResource("SB_btn_back")
theme_override_styles/hover = SubResource("SB_btn_back")
theme_override_styles/pressed = SubResource("SB_btn_back")
theme_override_font_sizes/font_size = 13

[node name="PanelMenu" type="Panel" parent="UI"]
position = Vector2(340, 100)
size = Vector2(600, 520)
theme_override_styles/panel = SubResource("SB_menu")

[node name="VBox" type="VBoxContainer" parent="UI/PanelMenu"]
position = Vector2(48, 48)
size = Vector2(504, 424)
theme_override_constants/separation = 28

[node name="LblTitle" type="Label" parent="UI/PanelMenu/VBox"]
size_flags_horizontal = 3
text = "🌿 Pilih Modul Belajar"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 26
theme_override_colors/font_color = Color(0.75, 0.98, 0.60, 1)

[node name="LblDesc" type="Label" parent="UI/PanelMenu/VBox"]
size_flags_horizontal = 3
text = "Hari ini mau belajar apa, Maryam?"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 15
theme_override_colors/font_color = Color(0.75, 0.90, 0.75, 1)

[node name="Sep" type="HSeparator" parent="UI/PanelMenu/VBox"]
size_flags_horizontal = 3

[node name="BtnWarna" type="Button" parent="UI/PanelMenu/VBox"]
size_flags_horizontal = 3
text = "🌈  Belajar Warna"
theme_override_styles/normal = SubResource("SB_btn_modul")
theme_override_styles/hover = SubResource("SB_btn_modul")
theme_override_styles/pressed = SubResource("SB_btn_modul")
theme_override_font_sizes/font_size = 20

[node name="LblWarna" type="Label" parent="UI/PanelMenu/VBox"]
size_flags_horizontal = 3
text = "Cocokkan nama warna dengan warnanya!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 13
theme_override_colors/font_color = Color(0.65, 0.88, 0.65, 1)

[node name="BtnAngka" type="Button" parent="UI/PanelMenu/VBox"]
size_flags_horizontal = 3
text = "🔢  Belajar Angka 1-10"
theme_override_styles/normal = SubResource("SB_btn_modul")
theme_override_styles/hover = SubResource("SB_btn_modul")
theme_override_styles/pressed = SubResource("SB_btn_modul")
theme_override_font_sizes/font_size = 20

[node name="LblAngka" type="Label" parent="UI/PanelMenu/VBox"]
size_flags_horizontal = 3
text = "Kenali angka 1 sampai 10 dengan emoji!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 13
theme_override_colors/font_color = Color(0.65, 0.88, 0.65, 1)

[node name="PanelWarna" type="Panel" parent="UI"]
position = Vector2(0, 60)
size = Vector2(1280, 660)
visible = false
theme_override_styles/panel = SubResource("SB_panel")

[node name="LblSoal" type="Label" parent="UI/PanelWarna"]
position = Vector2(0, 30)
size = Vector2(1280, 36)
text = "Pilih warna:"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 18
theme_override_colors/font_color = Color(0.80, 0.95, 0.80, 1)

[node name="LblNamaWarna" type="Label" parent="UI/PanelWarna"]
position = Vector2(0, 72)
size = Vector2(1280, 90)
text = "MERAH"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 58

[node name="LblFeedback" type="Label" parent="UI/PanelWarna"]
position = Vector2(0, 172)
size = Vector2(1280, 44)
text = "✅  Betul!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 22
visible = false

[node name="PilihanBox" type="HBoxContainer" parent="UI/PanelWarna"]
position = Vector2(100, 228)
size = Vector2(1080, 160)
theme_override_constants/separation = 30
alignment = 1

[node name="PanelAngka" type="Panel" parent="UI"]
position = Vector2(0, 60)
size = Vector2(1280, 660)
visible = false
theme_override_styles/panel = SubResource("SB_panel")

[node name="LblInfo" type="Panel" parent="UI/PanelAngka"]
position = Vector2(240, 16)
size = Vector2(800, 48)
theme_override_styles/panel = SubResource("SB_info")

[node name="LblInfo" type="Label" parent="UI/PanelAngka/LblInfo"]
position = Vector2(0, 0)
size = Vector2(800, 48)
text = "Sentuh angka untuk belajar!"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 17
theme_override_colors/font_color = Color(0.90, 0.98, 0.82, 1)

[node name="GridAngka" type="GridContainer" parent="UI/PanelAngka"]
position = Vector2(30, 80)
size = Vector2(1220, 560)
columns = 5
theme_override_constants/h_separation = 16
theme_override_constants/v_separation = 16

[node name="PanelSelesai" type="Panel" parent="UI"]
position = Vector2(390, 160)
size = Vector2(500, 380)
visible = false
theme_override_styles/panel = SubResource("SB_selesai")

[node name="VBox" type="VBoxContainer" parent="UI/PanelSelesai"]
position = Vector2(32, 32)
size = Vector2(436, 316)
theme_override_constants/separation = 18

[node name="LblEmoji" type="Label" parent="UI/PanelSelesai/VBox"]
text = "🧩 🌟 🎉"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 36

[node name="LblSelesai" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Maryam Cerdas!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 22
theme_override_colors/font_color = Color(0.80, 1.0, 0.80, 1)

[node name="LblBintang" type="Label" parent="UI/PanelSelesai/VBox"]
text = "⭐ ⭐ ⭐  +3 Bintang!"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 16
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="BtnMenuLagi" type="Button" parent="UI/PanelSelesai/VBox"]
text = "🧩  Modul Lain"
theme_override_styles/normal = SubResource("SB_btn_keluar")
theme_override_styles/hover = SubResource("SB_btn_keluar")
theme_override_styles/pressed = SubResource("SB_btn_keluar")
theme_override_font_sizes/font_size = 15

[node name="BtnKeluar" type="Button" parent="UI/PanelSelesai/VBox"]
text = "🏠  Kembali ke Dunia"
theme_override_styles/normal = SubResource("SB_btn_keluar")
theme_override_styles/hover = SubResource("SB_btn_keluar")
theme_override_styles/pressed = SubResource("SB_btn_keluar")
theme_override_font_sizes/font_size = 15
""")

# Fix node path LblInfo yang duplikat di tscn
tscn_path = os.path.join(BASE, "scenes", "locations", "TamanScene.tscn")
with open(tscn_path, "r", encoding="utf-8") as f:
    content = f.read()
# Perbaiki duplikat nama node LblInfo
content = content.replace(
    '[node name="LblInfo" type="Panel" parent="UI/PanelAngka"]\n',
    '[node name="InfoPanel" type="Panel" parent="UI/PanelAngka"]\n'
)
content = content.replace(
    '[node name="LblInfo" type="Label" parent="UI/PanelAngka/LblInfo"]\n',
    '[node name="LblInfo" type="Label" parent="UI/PanelAngka/InfoPanel"]\n'
)
with open(tscn_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

# Fix @onready di gd sesuai perubahan node name
gd_path = os.path.join(BASE, "scripts", "locations", "TamanScene.gd")
with open(gd_path, "r", encoding="utf-8") as f:
    gd = f.read()
gd = gd.replace(
    '@onready var _lbl_info_a     : Label         = $UI/PanelAngka/LblInfo',
    '@onready var _lbl_info_a     : Label         = $UI/PanelAngka/InfoPanel/LblInfo'
)
with open(gd_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(gd)
print("  ✅  Node path LblInfo fixed")

# ── Git commit ────────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "feat: Taman Logika upgrade — menu 2 modul, Warna + Angka 1-10"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

# ── Auto-delete ───────────────────────────────────────────────
try:
    os.remove(SCRIPT_PATH)
    print("  ✅  Script dihapus otomatis")
except:
    pass

print("\n" + "=" * 52)
print("  SELESAI!")
print("  Godot → Reload → F5")
print("  Masuk Taman Logika → pilih modul:")
print("  🌈 Belajar Warna  — cocokkan warna")
print("  🔢 Belajar Angka  — angka 1-10 + emoji")
print("=" * 52 + "\n")
