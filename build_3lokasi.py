"""
Maryam Journey - Build 3 Lokasi Sekaligus
Taman Logika + Kebun Karakter + Rumah Maryam
python build_3lokasi.py
"""
import os, subprocess

BASE = os.getcwd()
SCRIPT_PATH = os.path.abspath(__file__)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Build 3 Lokasi")
print("=" * 52)

# ═══════════════════════════════════════════════════
# 1. TAMAN LOGIKA — Cocokkan bentuk & warna
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "locations", "TamanScene.gd"), """\
# =============================================================
#  scripts/locations/TamanScene.gd
#  Taman Logika — Cocokkan warna & bentuk
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

# Soal: cocokkan nama warna dengan warna yang benar
const SOAL : Array[Dictionary] = [
\t{"nama": "MERAH",   "warna": Color(0.92, 0.20, 0.20, 1), "salah": [Color(0.20,0.55,0.92,1), Color(0.20,0.82,0.35,1), Color(0.92,0.78,0.10,1)]},
\t{"nama": "BIRU",    "warna": Color(0.20, 0.50, 0.92, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.82,0.45,0.10,1), Color(0.55,0.20,0.82,1)]},
\t{"nama": "HIJAU",   "warna": Color(0.15, 0.78, 0.35, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.92,0.78,0.10,1)]},
\t{"nama": "KUNING",  "warna": Color(0.95, 0.82, 0.10, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.55,0.20,0.82,1)]},
\t{"nama": "UNGU",    "warna": Color(0.55, 0.18, 0.85, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.92,0.78,0.10,1)]},
\t{"nama": "ORANYE",  "warna": Color(0.95, 0.52, 0.10, 1), "salah": [Color(0.20,0.50,0.92,1), Color(0.15,0.78,0.35,1), Color(0.55,0.18,0.85,1)]},
\t{"nama": "PINK",    "warna": Color(0.95, 0.35, 0.65, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.20,0.50,0.92,1), Color(0.95,0.52,0.10,1)]},
\t{"nama": "COKLAT",  "warna": Color(0.55, 0.32, 0.12, 1), "salah": [Color(0.92,0.20,0.20,1), Color(0.15,0.78,0.35,1), Color(0.95,0.35,0.65,1)]},
]

var _idx_soal    : int  = 0
var _benar       : int  = 0
var _selesai     : bool = false

@onready var _lbl_soal      : Label  = $UI/SoalPanel/LblSoal
@onready var _lbl_warna     : Label  = $UI/SoalPanel/LblWarna
@onready var _kotak_soal    : Panel  = $UI/SoalPanel/KotakWarna
@onready var _lbl_progress  : Label  = $UI/TopBar/LblProgress
@onready var _lbl_feedback  : Label  = $UI/LblFeedback
@onready var _btn_back      : Button = $UI/TopBar/BtnBack
@onready var _panel_selesai : Panel  = $UI/PanelSelesai
@onready var _btn_keluar    : Button = $UI/PanelSelesai/VBox/BtnKeluar
@onready var _pilihan_box   : HBoxContainer = $UI/PilihanBox


func _ready() -> void:
\t_panel_selesai.visible = false
\t_lbl_feedback.visible  = false
\t_btn_back.pressed.connect(_on_back)
\t_btn_keluar.pressed.connect(_on_back)
\t_tampil_soal()


func _tampil_soal() -> void:
\tif _idx_soal >= SOAL.size():
\t\t_selesai_semua()
\t\treturn

\tvar soal : Dictionary = SOAL[_idx_soal]
\t_lbl_soal.text = "Pilih warna:"
\t_lbl_warna.text = soal["nama"]
\t_lbl_warna.add_theme_color_override("font_color", soal["warna"])
\t_lbl_progress.text = str(_idx_soal + 1) + " / " + str(SOAL.size())
\t_lbl_feedback.visible = false

\t# Bersihkan pilihan lama
\tfor child in _pilihan_box.get_children():
\t\tchild.queue_free()

\t# Buat 4 pilihan (1 benar + 3 salah) dan acak urutannya
\tvar semua : Array[Dictionary] = []
\tsemua.append({"warna": soal["warna"], "benar": true})
\tfor w : Color in soal["salah"]:
\t\tsemua.append({"warna": w, "benar": false})
\tsemua.shuffle()

\tfor item : Dictionary in semua:
\t\tvar btn     : Button       = Button.new()
\t\tvar w       : Color        = item["warna"]
\t\tvar is_benar : bool        = item["benar"]
\t\tvar sb      : StyleBoxFlat = StyleBoxFlat.new()
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
\t\tbtn.pressed.connect(func(): _on_pilih(is_benar))
\t\t_pilihan_box.add_child(btn)


func _on_pilih(is_benar: bool) -> void:
\tif _selesai:
\t\treturn
\t_lbl_feedback.visible = true
\tif is_benar:
\t\t_benar += 1
\t\t_lbl_feedback.text = "✅  Betul! Hebat Maryam!"
\t\t_lbl_feedback.add_theme_color_override("font_color", Color(0.20, 0.90, 0.40, 1))
\telse:
\t\t_lbl_feedback.text = "❌  Coba lagi ya!"
\t\t_lbl_feedback.add_theme_color_override("font_color", Color(0.95, 0.35, 0.35, 1))
\tawait get_tree().create_timer(0.8).timeout
\t_idx_soal += 1
\t_tampil_soal()


func _selesai_semua() -> void:
\t_selesai = true
\tGameManager.add_star(3)
\t_panel_selesai.visible = true
\t$UI/PanelSelesai/VBox/LblSkor.text = "Benar: " + str(_benar) + " / " + str(SOAL.size())


func _on_back() -> void:
\tTransitionManager.go_to(WORLD_SCENE)
""")

write(os.path.join(BASE, "scenes", "locations", "TamanScene.tscn"), """\
[gd_scene load_steps=6 format=3]

[ext_resource type="Script" path="res://scripts/locations/TamanScene.gd" id="1_taman"]

[sub_resource type="StyleBoxFlat" id="SB_topbar"]
bg_color = Color(0.05, 0.14, 0.08, 0.97)
border_width_bottom = 2
border_color = Color(0.22, 0.78, 0.35, 0.70)

[sub_resource type="StyleBoxFlat" id="SB_soal"]
bg_color = Color(0.06, 0.18, 0.10, 0.96)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.22, 0.78, 0.35, 0.70)
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
text = "🧩  Taman Logika  —  Cocokkan Warnanya!"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(0.55, 0.95, 0.55, 1)

[node name="LblProgress" type="Label" parent="UI/TopBar"]
position = Vector2(900, 0)
size = Vector2(300, 60)
text = "1 / 8"
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

[node name="SoalPanel" type="Panel" parent="UI"]
position = Vector2(290, 90)
size = Vector2(700, 200)
theme_override_styles/panel = SubResource("SB_soal")

[node name="LblSoal" type="Label" parent="UI/SoalPanel"]
position = Vector2(0, 20)
size = Vector2(700, 40)
text = "Pilih warna:"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 18
theme_override_colors/font_color = Color(0.80, 0.95, 0.80, 1)

[node name="LblWarna" type="Label" parent="UI/SoalPanel"]
position = Vector2(0, 70)
size = Vector2(700, 80)
text = "MERAH"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 52

[node name="KotakWarna" type="Panel" parent="UI/SoalPanel"]
position = Vector2(310, 150)
size = Vector2(80, 40)
visible = false

[node name="LblFeedback" type="Label" parent="UI"]
position = Vector2(0, 300)
size = Vector2(1280, 50)
text = "✅  Betul!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 24
visible = false

[node name="PilihanBox" type="HBoxContainer" parent="UI"]
position = Vector2(150, 370)
size = Vector2(980, 160)
theme_override_constants/separation = 30
alignment = 1

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
text = "🧩 🌟 🎉"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 40

[node name="LblSelesai" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Maryam Cerdas!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 26
theme_override_colors/font_color = Color(0.80, 1.0, 0.80, 1)

[node name="LblSkor" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Benar: 8 / 8"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 18
theme_override_colors/font_color = Color(0.60, 0.95, 0.65, 1)

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

# ═══════════════════════════════════════════════════
# 2. KEBUN KARAKTER — Cerita nilai Islam
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "locations", "KebunScene.gd"), """\
# =============================================================
#  scripts/locations/KebunScene.gd
#  Kebun Karakter — Cerita nilai Islam untuk anak
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

const CERITA : Array[Dictionary] = [
\t{
\t\t"judul"  : "🌸 Berbagi Itu Indah",
\t\t"cerita" : "Maryam punya 2 apel.\\nTemannya tidak punya apel.\\nMaryam memberi 1 apel kepada temannya.\\n\\nTemannya sangat senang! 😊",
\t\t"nilai"  : "Berbagi membuat hati bahagia! 💝",
\t\t"emoji"  : "🍎"
\t},
\t{
\t\t"judul"  : "🙏 Selalu Berdoa",
\t\t"cerita" : "Sebelum makan, Maryam selalu berdoa.\\n\\n'Bismillahirrahmanirrahim'\\n\\nAllah senang dengan anak yang berdoa. ✨",
\t\t"nilai"  : "Ingat Allah di setiap kegiatan! 🌟",
\t\t"emoji"  : "🤲"
\t},
\t{
\t\t"judul"  : "😊 Jujur Itu Berani",
\t\t"cerita" : "Maryam tidak sengaja memecahkan gelas.\\nMaryam berani berkata jujur kepada Ayah.\\n\\nAyah bangga karena Maryam jujur! 💪",
\t\t"nilai"  : "Jujur adalah sifat orang berani! 🦁",
\t\t"emoji"  : "💎"
\t},
\t{
\t\t"judul"  : "🤝 Tolong Menolong",
\t\t"cerita" : "Teman Maryam membawa tas yang berat.\\nMaryam membantu mengangkat tasnya.\\n\\nMereka berjalan bersama dengan gembira! 🌈",
\t\t"nilai"  : "Membantu sesama adalah kebaikan! 💛",
\t\t"emoji"  : "👫"
\t},
\t{
\t\t"judul"  : "😌 Sabar Itu Kuat",
\t\t"cerita" : "Maryam mengantri dengan tertib.\\nWalaupun lama, Maryam tetap sabar.\\n\\nAllah suka dengan orang yang sabar! ⭐",
\t\t"nilai"  : "Sabar adalah kekuatan sejati! 🌺",
\t\t"emoji"  : "⏳"
\t},
]

var _idx      : int  = 0
var _selesai  : bool = false

@onready var _lbl_judul     : Label  = $UI/CardCerita/LblJudul
@onready var _lbl_emoji     : Label  = $UI/CardCerita/LblEmoji
@onready var _lbl_cerita    : Label  = $UI/CardCerita/LblCerita
@onready var _lbl_nilai     : Label  = $UI/CardCerita/LblNilai
@onready var _btn_next      : Button = $UI/CardCerita/BtnNext
@onready var _lbl_progress  : Label  = $UI/TopBar/LblProgress
@onready var _btn_back      : Button = $UI/TopBar/BtnBack
@onready var _panel_selesai : Panel  = $UI/PanelSelesai
@onready var _btn_keluar    : Button = $UI/PanelSelesai/VBox/BtnKeluar


func _ready() -> void:
\t_panel_selesai.visible = false
\t_btn_back.pressed.connect(_on_back)
\t_btn_keluar.pressed.connect(_on_back)
\t_btn_next.pressed.connect(_on_next)
\t_tampil_cerita()


func _tampil_cerita() -> void:
\tif _idx >= CERITA.size():
\t\t_selesai_semua()
\t\treturn
\tvar c : Dictionary = CERITA[_idx]
\t_lbl_judul.text   = c["judul"]
\t_lbl_emoji.text   = c["emoji"]
\t_lbl_cerita.text  = c["cerita"]
\t_lbl_nilai.text   = c["nilai"]
\t_lbl_progress.text = str(_idx + 1) + " / " + str(CERITA.size())
\tif _idx == CERITA.size() - 1:
\t\t_btn_next.text = "✅  Selesai!"
\telse:
\t\t_btn_next.text = "Cerita Berikutnya →"


func _on_next() -> void:
\tif _selesai:
\t\treturn
\t_idx += 1
\t_tampil_cerita()


func _selesai_semua() -> void:
\tif _selesai:
\t\treturn
\t_selesai = true
\tGameManager.add_star(3)
\t_panel_selesai.visible = true


func _on_back() -> void:
\tTransitionManager.go_to(WORLD_SCENE)
""")

write(os.path.join(BASE, "scenes", "locations", "KebunScene.tscn"), """\
[gd_scene load_steps=6 format=3]

[ext_resource type="Script" path="res://scripts/locations/KebunScene.gd" id="1_kebun"]

[sub_resource type="StyleBoxFlat" id="SB_topbar"]
bg_color = Color(0.06, 0.16, 0.06, 0.97)
border_width_bottom = 2
border_color = Color(0.35, 0.80, 0.25, 0.65)

[sub_resource type="StyleBoxFlat" id="SB_card"]
bg_color = Color(0.06, 0.18, 0.07, 0.96)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(0.35, 0.80, 0.25, 0.75)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[sub_resource type="StyleBoxFlat" id="SB_selesai"]
bg_color = Color(0.05, 0.18, 0.06, 0.97)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(0.35, 0.88, 0.28, 1.0)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[sub_resource type="StyleBoxFlat" id="SB_btn_back"]
bg_color = Color(0.10, 0.24, 0.10, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.35, 0.80, 0.25, 0.80)
corner_radius_top_left = 10
corner_radius_top_right = 10
corner_radius_bottom_right = 10
corner_radius_bottom_left = 10
content_margin_left = 16.0
content_margin_right = 16.0
content_margin_top = 8.0
content_margin_bottom = 8.0

[sub_resource type="StyleBoxFlat" id="SB_btn_next"]
bg_color = Color(0.14, 0.50, 0.14, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.35, 0.88, 0.28, 0.90)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 28.0
content_margin_right = 28.0
content_margin_top = 12.0
content_margin_bottom = 12.0

[node name="KebunScene" type="Node2D"]
script = ExtResource("1_kebun")

[node name="BgSky" type="ColorRect" parent="."]
color = Color(0.07, 0.14, 0.07, 1)
size = Vector2(1280, 720)

[node name="GlowGreen" type="Polygon2D" parent="."]
color = Color(0.10, 0.35, 0.10, 0.20)
polygon = PackedVector2Array(0,0, 1280,0, 1280,400, 0,400)

[node name="UI" type="CanvasLayer" parent="."]

[node name="TopBar" type="Panel" parent="UI"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
theme_override_styles/panel = SubResource("SB_topbar")

[node name="LblJudul" type="Label" parent="UI/TopBar"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
text = "🌿  Kebun Karakter  —  Cerita Nilai Islam"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(0.60, 0.95, 0.45, 1)

[node name="LblProgress" type="Label" parent="UI/TopBar"]
position = Vector2(900, 0)
size = Vector2(300, 60)
text = "1 / 5"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 14
theme_override_colors/font_color = Color(0.75, 0.95, 0.65, 1)

[node name="BtnBack" type="Button" parent="UI/TopBar"]
position = Vector2(12, 10)
size = Vector2(80, 40)
text = "← Balik"
theme_override_styles/normal = SubResource("SB_btn_back")
theme_override_styles/hover = SubResource("SB_btn_back")
theme_override_styles/pressed = SubResource("SB_btn_back")
theme_override_font_sizes/font_size = 13

[node name="CardCerita" type="Panel" parent="UI"]
position = Vector2(190, 80)
size = Vector2(900, 560)
theme_override_styles/panel = SubResource("SB_card")

[node name="LblJudul" type="Label" parent="UI/CardCerita"]
position = Vector2(0, 24)
size = Vector2(900, 50)
text = "🌸 Berbagi Itu Indah"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 26
theme_override_colors/font_color = Color(0.75, 0.98, 0.60, 1)

[node name="LblEmoji" type="Label" parent="UI/CardCerita"]
position = Vector2(0, 82)
size = Vector2(900, 70)
text = "🍎"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 52

[node name="LblCerita" type="Label" parent="UI/CardCerita"]
position = Vector2(60, 162)
size = Vector2(780, 220)
text = "..."
horizontal_alignment = 1
vertical_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(0.90, 0.96, 0.86, 1)

[node name="LblNilai" type="Label" parent="UI/CardCerita"]
position = Vector2(60, 390)
size = Vector2(780, 50)
text = "..."
horizontal_alignment = 1
theme_override_font_sizes/font_size = 17
theme_override_colors/font_color = Color(1.0, 0.88, 0.30, 1)

[node name="BtnNext" type="Button" parent="UI/CardCerita"]
position = Vector2(250, 460)
size = Vector2(400, 52)
text = "Cerita Berikutnya →"
theme_override_styles/normal = SubResource("SB_btn_next")
theme_override_styles/hover = SubResource("SB_btn_next")
theme_override_styles/pressed = SubResource("SB_btn_next")
theme_override_font_sizes/font_size = 16

[node name="PanelSelesai" type="Panel" parent="UI"]
position = Vector2(390, 160)
size = Vector2(500, 400)
visible = false
theme_override_styles/panel = SubResource("SB_selesai")

[node name="VBox" type="VBoxContainer" parent="UI/PanelSelesai"]
position = Vector2(32, 32)
size = Vector2(436, 336)
theme_override_constants/separation = 18

[node name="LblEmoji" type="Label" parent="UI/PanelSelesai/VBox"]
text = "🌿 💚 🌺"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 40

[node name="LblSelesai" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Maryam Berbudi Baik!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 24
theme_override_colors/font_color = Color(0.75, 1.0, 0.65, 1)

[node name="LblDesc" type="Label" parent="UI/PanelSelesai/VBox"]
text = "Kamu sudah belajar\n5 nilai kebaikan Islam!"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 16
theme_override_colors/font_color = Color(0.80, 0.95, 0.75, 1)

[node name="LblBintang" type="Label" parent="UI/PanelSelesai/VBox"]
text = "⭐ ⭐ ⭐  +3 Bintang!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="BtnKeluar" type="Button" parent="UI/PanelSelesai/VBox"]
text = "🏠  Kembali ke Dunia"
theme_override_styles/normal = SubResource("SB_btn_next")
theme_override_styles/hover = SubResource("SB_btn_next")
theme_override_styles/pressed = SubResource("SB_btn_next")
theme_override_font_sizes/font_size = 16
""")

# ═══════════════════════════════════════════════════
# 3. RUMAH MARYAM — Progress & koleksi bintang
# ═══════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "locations", "RumahScene.gd"), """\
# =============================================================
#  scripts/locations/RumahScene.gd
#  Rumah Maryam — Progress & koleksi bintang
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

const LOKASI_INFO : Array[Dictionary] = [
\t{"nama": "🕌 Masjid An-Nur",  "key": "masjid", "maks": 3},
\t{"nama": "📚 Pondok Baca",    "key": "pondok", "maks": 3},
\t{"nama": "🧩 Taman Logika",   "key": "taman",  "maks": 3},
\t{"nama": "🌿 Kebun Karakter", "key": "kebun",  "maks": 3},
]

@onready var _lbl_nama      : Label  = $UI/Card/LblNama
@onready var _lbl_total     : Label  = $UI/Card/LblTotal
@onready var _lbl_pesan     : Label  = $UI/Card/LblPesan
@onready var _vbox_lokasi   : VBoxContainer = $UI/Card/VBoxLokasi
@onready var _btn_back      : Button = $UI/TopBar/BtnBack


func _ready() -> void:
\t_btn_back.pressed.connect(_on_back)
\t_build_ui()


func _build_ui() -> void:
\tvar total : int = GameManager.total_stars
\t_lbl_nama.text  = "Assalamu'alaikum, " + GameManager.player_name + "! 🌙"
\t_lbl_total.text = "⭐  Total Bintang: " + str(total)

\tif total >= 12:
\t\t_lbl_pesan.text = "Subhanallah! Kamu sudah menyelesaikan semuanya! 🏆"
\t\t_lbl_pesan.add_theme_color_override("font_color", Color(1.0, 0.85, 0.10, 1))
\telif total >= 6:
\t\t_lbl_pesan.text = "Alhamdulillah! Terus semangat belajar ya! 💪"
\t\t_lbl_pesan.add_theme_color_override("font_color", Color(0.55, 0.95, 0.55, 1))
\telse:
\t\t_lbl_pesan.text = "Bismillah! Ayo mulai petualangan belajar! 🌟"
\t\t_lbl_pesan.add_theme_color_override("font_color", Color(0.80, 0.85, 1.0, 1))

\t# Bersihkan dulu
\tfor c in _vbox_lokasi.get_children():
\t\tc.queue_free()

\t# Tampilkan progress tiap lokasi
\tfor info : Dictionary in LOKASI_INFO:
\t\tvar row : HBoxContainer = HBoxContainer.new()
\t\trow.custom_minimum_size = Vector2(0, 48)

\t\tvar lbl_nama : Label = Label.new()
\t\tlbl_nama.text = info["nama"]
\t\tlbl_nama.custom_minimum_size = Vector2(280, 0)
\t\tlbl_nama.add_theme_font_size_override("font_size", 16)
\t\tlbl_nama.add_theme_color_override("font_color", Color(0.90, 0.94, 1.0, 1))
\t\tlbl_nama.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

\t\tvar lbl_stars : Label = Label.new()
\t\tvar bintang_lokasi : int = _hitung_bintang(info["key"])
\t\tvar bintang_str    : String = ""
\t\tfor s in info["maks"]:
\t\t\tif s < bintang_lokasi:
\t\t\t\tbintang_str += "⭐"
\t\t\telse:
\t\t\t\tbintang_str += "☆"
\t\tlbl_stars.text = bintang_str
\t\tlbl_stars.add_theme_font_size_override("font_size", 22)
\t\tlbl_stars.vertical_alignment = VERTICAL_ALIGNMENT_CENTER

\t\trow.add_child(lbl_nama)
\t\trow.add_child(lbl_stars)
\t\t_vbox_lokasi.add_child(row)


func _hitung_bintang(key: String) -> int:
\t# Sederhana: kalau sudah pernah masuk lokasi, dapat 3 bintang
\t# Nanti bisa dikembangkan dengan tracking per lokasi
\tif GameManager.total_stars > 0:
\t\tmatch key:
\t\t\t"masjid": return 3 if GameManager.total_stars >= 3 else 0
\t\t\t"pondok": return 3 if GameManager.total_stars >= 6 else 0
\t\t\t"taman":  return 3 if GameManager.total_stars >= 9 else 0
\t\t\t"kebun":  return 3 if GameManager.total_stars >= 12 else 0
\treturn 0


func _on_back() -> void:
\tTransitionManager.go_to(WORLD_SCENE)
""")

write(os.path.join(BASE, "scenes", "locations", "RumahScene.tscn"), """\
[gd_scene load_steps=5 format=3]

[ext_resource type="Script" path="res://scripts/locations/RumahScene.gd" id="1_rumah"]

[sub_resource type="StyleBoxFlat" id="SB_topbar"]
bg_color = Color(0.16, 0.10, 0.06, 0.97)
border_width_bottom = 2
border_color = Color(1.0, 0.78, 0.20, 0.65)

[sub_resource type="StyleBoxFlat" id="SB_card"]
bg_color = Color(0.10, 0.08, 0.22, 0.96)
border_width_left = 3
border_width_top = 3
border_width_right = 3
border_width_bottom = 3
border_color = Color(1.0, 0.84, 0.12, 0.80)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[sub_resource type="StyleBoxFlat" id="SB_row"]
bg_color = Color(0.14, 0.12, 0.30, 0.70)
corner_radius_top_left = 10
corner_radius_top_right = 10
corner_radius_bottom_right = 10
corner_radius_bottom_left = 10

[sub_resource type="StyleBoxFlat" id="SB_btn_back"]
bg_color = Color(0.20, 0.14, 0.06, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.78, 0.20, 0.80)
corner_radius_top_left = 10
corner_radius_top_right = 10
corner_radius_bottom_right = 10
corner_radius_bottom_left = 10
content_margin_left = 16.0
content_margin_right = 16.0
content_margin_top = 8.0
content_margin_bottom = 8.0

[node name="RumahScene" type="Node2D"]
script = ExtResource("1_rumah")

[node name="BgSky" type="ColorRect" parent="."]
color = Color(0.09, 0.07, 0.22, 1)
size = Vector2(1280, 720)

[node name="GlowGold" type="Polygon2D" parent="."]
color = Color(0.40, 0.28, 0.05, 0.18)
polygon = PackedVector2Array(300,0, 980,0, 1100,400, 180,400)

[node name="UI" type="CanvasLayer" parent="."]

[node name="TopBar" type="Panel" parent="UI"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
theme_override_styles/panel = SubResource("SB_topbar")

[node name="LblJudul" type="Label" parent="UI/TopBar"]
position = Vector2(0, 0)
size = Vector2(1280, 60)
text = "⭐  Rumah Maryam  —  Koleksi Bintangku"
horizontal_alignment = 1
vertical_alignment = 1
theme_override_font_sizes/font_size = 20
theme_override_colors/font_color = Color(1.0, 0.88, 0.30, 1)

[node name="BtnBack" type="Button" parent="UI/TopBar"]
position = Vector2(12, 10)
size = Vector2(80, 40)
text = "← Balik"
theme_override_styles/normal = SubResource("SB_btn_back")
theme_override_styles/hover = SubResource("SB_btn_back")
theme_override_styles/pressed = SubResource("SB_btn_back")
theme_override_font_sizes/font_size = 13

[node name="Card" type="Panel" parent="UI"]
position = Vector2(240, 80)
size = Vector2(800, 570)
theme_override_styles/panel = SubResource("SB_card")

[node name="LblNama" type="Label" parent="UI/Card"]
position = Vector2(0, 28)
size = Vector2(800, 44)
text = "Assalamu'alaikum, Maryam! 🌙"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 22
theme_override_colors/font_color = Color(0.95, 0.90, 1.0, 1)

[node name="LblTotal" type="Label" parent="UI/Card"]
position = Vector2(0, 80)
size = Vector2(800, 52)
text = "⭐  Total Bintang: 0"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 30
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="LblPesan" type="Label" parent="UI/Card"]
position = Vector2(40, 140)
size = Vector2(720, 40)
text = "Bismillah! Ayo mulai petualangan belajar! 🌟"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 15

[node name="Sep" type="HSeparator" parent="UI/Card"]
position = Vector2(40, 192)
size = Vector2(720, 8)

[node name="LblProgressTitle" type="Label" parent="UI/Card"]
position = Vector2(0, 208)
size = Vector2(800, 36)
text = "Progress Belajar:"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 16
theme_override_colors/font_color = Color(0.80, 0.82, 1.0, 1)

[node name="VBoxLokasi" type="VBoxContainer" parent="UI/Card"]
position = Vector2(60, 252)
size = Vector2(680, 260)
theme_override_constants/separation = 14
""")

# ── 4. Update WorldMap.tscn — scene_path 3 lokasi ────────────
wmap_path = os.path.join(BASE, "scenes", "world", "WorldMap.tscn")
with open(wmap_path, "r", encoding="utf-8") as f:
    wmap = f.read()

patches = [
    (
        'location_name = "Taman Logika"\nlocation_key = "taman"',
        'location_name = "Taman Logika"\nlocation_key = "taman"\nscene_path = "res://scenes/locations/TamanScene.tscn"'
    ),
    (
        'location_name = "Kebun Karakter"\nlocation_key = "kebun"',
        'location_name = "Kebun Karakter"\nlocation_key = "kebun"\nscene_path = "res://scenes/locations/KebunScene.tscn"'
    ),
    (
        'location_name = "Rumah Maryam"\nlocation_key = "rumah"',
        'location_name = "Rumah Maryam"\nlocation_key = "rumah"\nscene_path = "res://scenes/locations/RumahScene.tscn"'
    ),
]
for old, new in patches:
    if old in wmap and new not in wmap:
        wmap = wmap.replace(old, new)

with open(wmap_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(wmap)
print("  ✅  WorldMap.tscn — scene_path 3 lokasi ditambahkan")

# ── 5. Git commit ─────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "feat: Taman Logika + Kebun Karakter + Rumah Maryam — 5 lokasi lengkap!"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

# ── 6. Auto-delete ────────────────────────────────────────────
try:
    os.remove(SCRIPT_PATH)
    print("  ✅  Script dihapus otomatis")
except:
    pass

print("\n" + "=" * 52)
print("  SEMUA 5 LOKASI LENGKAP!")
print("  Godot → Reload → F5")
print("  🕌 Masjid    — 28 Hijaiyah")
print("  📚 Pondok    — 26 huruf A-Z")
print("  🧩 Taman     — puzzle warna")
print("  🌿 Kebun     — cerita nilai Islam")
print("  ⭐ Rumah     — koleksi bintang")
print("=" * 52 + "\n")
