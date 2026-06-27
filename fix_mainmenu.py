"""
Maryam Journey - Fix MainMenu (node path mismatch)
Jalankan: python fix_mainmenu.py
"""
import os, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Fix MainMenu")
print("=" * 52)

# ── MainMenu.gd — pakai @onready yang sesuai path tscn ───────
write(os.path.join(BASE, "scripts", "ui", "MainMenu.gd"), """\
# =============================================================
#  scripts/ui/MainMenu.gd
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

@onready var _btn_start    : Button = $UI/VBox/Card/Inner/BtnStart
@onready var _btn_continue : Button = $UI/VBox/Card/Inner/BtnContinue
@onready var _btn_reset    : Button = $UI/VBox/Card/Inner/BtnReset
@onready var _lbl_stars    : Label  = $UI/VBox/Card/Inner/LblStars


func _ready() -> void:
\tvar has_save := SaveManager.has_save()
\t_btn_continue.visible = has_save
\t_btn_reset.visible    = has_save
\tif has_save:
\t\tSaveManager.load_save()
\t\t_lbl_stars.text = "⭐ " + str(GameManager.total_stars) + " bintang tersimpan"
\telse:
\t\t_lbl_stars.text = "Petualangan baru menantimu!"
\t_btn_start.pressed.connect(_on_start)
\t_btn_continue.pressed.connect(_on_continue)
\t_btn_reset.pressed.connect(_on_reset)


func _on_start() -> void:
\tSaveManager.delete_save()
\tGameManager.total_stars        = 0
\tGameManager.unlocked_locations = ["masjid","pondok","taman","kebun","rumah"]
\tTransitionManager.go_to(WORLD_SCENE)


func _on_continue() -> void:
\tTransitionManager.go_to(WORLD_SCENE)


func _on_reset() -> void:
\tSaveManager.delete_save()
\tGameManager.total_stars        = 0
\tGameManager.unlocked_locations = ["masjid","pondok","taman","kebun","rumah"]
\t_btn_continue.visible = false
\t_btn_reset.visible    = false
\t_lbl_stars.text       = "Petualangan baru menantimu!"
""")

# ── MainMenu.tscn — node path harus identik dengan @onready ──
write(os.path.join(BASE, "scenes", "ui", "MainMenu.tscn"), """\
[gd_scene load_steps=5 format=3]

[ext_resource type="Script" path="res://scripts/ui/MainMenu.gd" id="1_menu"]

[sub_resource type="StyleBoxFlat" id="SB_btn"]
bg_color = Color(0.10, 0.08, 0.25, 0.95)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 1.0)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 10.0
content_margin_bottom = 10.0

[sub_resource type="StyleBoxFlat" id="SB_hover"]
bg_color = Color(0.22, 0.16, 0.42, 0.98)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.92, 0.40, 1.0)
corner_radius_top_left = 12
corner_radius_top_right = 12
corner_radius_bottom_right = 12
corner_radius_bottom_left = 12
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 10.0
content_margin_bottom = 10.0

[sub_resource type="StyleBoxFlat" id="SB_card"]
bg_color = Color(0.05, 0.04, 0.18, 0.90)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 0.80)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20

[node name="MainMenu" type="Node2D"]
script = ExtResource("1_menu")

[node name="BgSky" type="ColorRect" parent="."]
color = Color(0.10, 0.08, 0.28, 1)
size = Vector2(1280, 720)

[node name="GlowTop" type="Polygon2D" parent="."]
color = Color(0.28, 0.18, 0.58, 0.30)
polygon = PackedVector2Array(0,0, 1280,0, 1280,380, 0,380)

[node name="Star1" type="Polygon2D" parent="."]
color = Color(1,1,1,0.90)
polygon = PackedVector2Array(120,80, 122,86, 128,86, 123,90, 125,96, 120,92, 115,96, 117,90, 112,86, 118,86)

[node name="Star2" type="Polygon2D" parent="."]
color = Color(1,1,0.8,0.80)
polygon = PackedVector2Array(300,40, 301,44, 305,44, 302,47, 303,51, 300,48, 297,51, 298,47, 295,44, 299,44)

[node name="Star3" type="Polygon2D" parent="."]
color = Color(1,1,1,0.85)
polygon = PackedVector2Array(600,60, 602,66, 608,66, 603,70, 605,76, 600,72, 595,76, 597,70, 592,66, 598,66)

[node name="Star4" type="Polygon2D" parent="."]
color = Color(1,1,0.8,0.75)
polygon = PackedVector2Array(900,35, 901,39, 905,39, 902,42, 903,46, 900,43, 897,46, 898,42, 895,39, 899,39)

[node name="Star5" type="Polygon2D" parent="."]
color = Color(1,1,1,0.88)
polygon = PackedVector2Array(1100,90, 1102,96, 1108,96, 1103,100, 1105,106, 1100,102, 1095,106, 1097,100, 1092,96, 1098,96)

[node name="MoonGlow" type="Polygon2D" parent="."]
color = Color(1.0, 0.95, 0.70, 0.14)
polygon = PackedVector2Array(1040,10, 1180,10, 1220,110, 1000,110)

[node name="Moon" type="Polygon2D" parent="."]
color = Color(1.0, 0.96, 0.80, 1.0)
polygon = PackedVector2Array(1100,28, 1110,32, 1122,32, 1130,42, 1130,56, 1122,66, 1110,70, 1100,72, 1088,66, 1078,56, 1076,42, 1084,32, 1096,32)

[node name="MoonCut" type="Polygon2D" parent="."]
color = Color(0.10, 0.08, 0.28, 1)
polygon = PackedVector2Array(1112,30, 1120,34, 1128,44, 1128,56, 1120,66, 1112,70, 1108,58, 1108,42)

[node name="HillFar" type="Polygon2D" parent="."]
color = Color(0.12, 0.20, 0.16, 0.75)
polygon = PackedVector2Array(0,720, 0,560, 180,480, 420,518, 660,468, 900,508, 1100,472, 1280,498, 1280,720)

[node name="HillNear" type="Polygon2D" parent="."]
color = Color(0.10, 0.16, 0.12, 1)
polygon = PackedVector2Array(0,720, 0,615, 130,572, 320,592, 540,558, 780,584, 1020,554, 1280,574, 1280,720)

[node name="SilMasjidL" type="Node2D" parent="."]
position = Vector2(60, 0)

[node name="Body" type="ColorRect" parent="SilMasjidL"]
color = Color(0.08, 0.13, 0.10, 1)
position = Vector2(0, 524)
size = Vector2(110, 196)

[node name="Dome" type="Polygon2D" parent="SilMasjidL"]
color = Color(0.07, 0.11, 0.09, 1)
polygon = PackedVector2Array(0,528, 18,494, 40,478, 55,474, 70,478, 92,494, 110,528)

[node name="Minaret" type="ColorRect" parent="SilMasjidL"]
color = Color(0.08, 0.13, 0.10, 1)
position = Vector2(118, 504)
size = Vector2(20, 216)

[node name="MinaretTop" type="Polygon2D" parent="SilMasjidL"]
color = Color(0.07, 0.11, 0.09, 1)
polygon = PackedVector2Array(118,508, 128,484, 138,508)

[node name="SilMasjidR" type="Node2D" parent="."]
position = Vector2(1080, 0)

[node name="Body" type="ColorRect" parent="SilMasjidR"]
color = Color(0.08, 0.13, 0.10, 1)
position = Vector2(0, 534)
size = Vector2(95, 186)

[node name="Dome" type="Polygon2D" parent="SilMasjidR"]
color = Color(0.07, 0.11, 0.09, 1)
polygon = PackedVector2Array(0,538, 16,506, 36,492, 47,488, 58,492, 78,506, 95,538)

[node name="Minaret" type="ColorRect" parent="SilMasjidR"]
color = Color(0.08, 0.13, 0.10, 1)
position = Vector2(-20, 514)
size = Vector2(17, 206)

[node name="MinaretTop" type="Polygon2D" parent="SilMasjidR"]
color = Color(0.07, 0.11, 0.09, 1)
polygon = PackedVector2Array(-20,518, -11,496, -3,518)

[node name="UI" type="CanvasLayer" parent="."]

[node name="VBox" type="VBoxContainer" parent="UI"]
anchors_preset = 15
offset_right = 1280.0
offset_bottom = 720.0
alignment = 1

[node name="Card" type="Panel" parent="UI/VBox"]
custom_minimum_size = Vector2(440, 0)
size_flags_horizontal = 4
theme_override_styles/panel = SubResource("SB_card")

[node name="Inner" type="VBoxContainer" parent="UI/VBox/Card"]
anchors_preset = 15
offset_left = 28.0
offset_top = 28.0
offset_right = -28.0
offset_bottom = -28.0
theme_override_constants/separation = 16

[node name="LblTitle" type="Label" parent="UI/VBox/Card/Inner"]
text = "🌙 Maryam Journey"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 34

[node name="LblBismillah" type="Label" parent="UI/VBox/Card/Inner"]
text = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 17
theme_override_colors/font_color = Color(1.0, 0.90, 0.38, 1)

[node name="LblDesc" type="Label" parent="UI/VBox/Card/Inner"]
text = "Jelajahi dunia bersama Maryam\nBelajar, bermain, dan tumbuh bersama Islam 🌟"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 14
theme_override_colors/font_color = Color(0.82, 0.82, 0.95, 1)

[node name="LblStars" type="Label" parent="UI/VBox/Card/Inner"]
text = "Petualangan baru menantimu!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 13
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="Sep" type="HSeparator" parent="UI/VBox/Card/Inner"]

[node name="BtnStart" type="Button" parent="UI/VBox/Card/Inner"]
text = "✨  Mulai Petualangan Baru"
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 15

[node name="BtnContinue" type="Button" parent="UI/VBox/Card/Inner"]
text = "▶  Lanjutkan Petualangan"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 15

[node name="BtnReset" type="Button" parent="UI/VBox/Card/Inner"]
text = "🗑  Hapus Progress"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 13
theme_override_colors/font_color = Color(1, 0.50, 0.50, 1)
""")

# ── Git commit ───────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "fix: MainMenu node path mismatch — semua @onready sesuai tscn"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

print("\n" + "=" * 52)
print("  SELESAI!")
print("  1. Godot → Project → Reload Current Project")
print("  2. Tekan F5 → Main Menu muncul tanpa error")
print("=" * 52 + "\n")
