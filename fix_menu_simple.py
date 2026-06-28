"""
Maryam Journey - Fix Menu Simple & Final
python fix_menu_simple.py
"""
import os, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Fix Menu Simple & Final")
print("=" * 40)

# Strategi: TIDAK pakai Container apapun
# Card Panel diposisi manual X=410, Y=160 (center dari 1280x720)
# Card size = 460 x 400
# Center X = (1280 - 460) / 2 = 410
# Center Y = (720 - 400) / 2 = 160
#
# @onready path: $UI/Card/Inner/[NodeName]

write(os.path.join(BASE, "scripts", "ui", "MainMenu.gd"), """\
# =============================================================
#  scripts/ui/MainMenu.gd
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

@onready var _btn_start    : Button = $UI/Card/Inner/BtnStart
@onready var _btn_continue : Button = $UI/Card/Inner/BtnContinue
@onready var _btn_reset    : Button = $UI/Card/Inner/BtnReset
@onready var _lbl_stars    : Label  = $UI/Card/Inner/LblStars


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

write(os.path.join(BASE, "scenes", "ui", "MainMenu.tscn"), """\
[gd_scene load_steps=4 format=3]

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
content_margin_left = 20.0
content_margin_right = 20.0
content_margin_top = 12.0
content_margin_bottom = 12.0

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
content_margin_left = 20.0
content_margin_right = 20.0
content_margin_top = 12.0
content_margin_bottom = 12.0

[sub_resource type="StyleBoxFlat" id="SB_card"]
bg_color = Color(0.05, 0.04, 0.18, 0.94)
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
color = Color(0.09, 0.07, 0.26, 1)
size = Vector2(1280, 720)

[node name="GlowTop" type="Polygon2D" parent="."]
color = Color(0.26, 0.16, 0.55, 0.28)
polygon = PackedVector2Array(0,0, 1280,0, 1280,360, 0,360)

[node name="S1" type="Polygon2D" parent="."]
color = Color(1,1,1,0.92)
polygon = PackedVector2Array(140,75, 142,82, 150,82, 144,87, 146,94, 140,89, 134,94, 136,87, 130,82, 138,82)

[node name="S2" type="Polygon2D" parent="."]
color = Color(1,1,0.85,0.80)
polygon = PackedVector2Array(320,38, 321,42, 325,42, 322,45, 323,49, 320,46, 317,49, 318,45, 315,42, 319,42)

[node name="S3" type="Polygon2D" parent="."]
color = Color(1,1,1,0.88)
polygon = PackedVector2Array(560,65, 562,72, 570,72, 564,77, 566,84, 560,79, 554,84, 556,77, 550,72, 558,72)

[node name="S4" type="Polygon2D" parent="."]
color = Color(1,1,0.85,0.74)
polygon = PackedVector2Array(760,32, 761,36, 765,36, 762,39, 763,43, 760,40, 757,43, 758,39, 755,36, 759,36)

[node name="S5" type="Polygon2D" parent="."]
color = Color(1,1,1,0.85)
polygon = PackedVector2Array(980,82, 982,89, 990,89, 984,94, 986,101, 980,96, 974,101, 976,94, 970,89, 978,89)

[node name="MoonGroup" type="Node2D" parent="."]
position = Vector2(940, 80)

[node name="MoonGlow" type="Polygon2D" parent="MoonGroup"]
color = Color(1.0, 0.95, 0.70, 0.13)
polygon = PackedVector2Array(-80,-50, 80,-50, 100,80, -100,80)

[node name="MoonBody" type="Polygon2D" parent="MoonGroup"]
color = Color(1.0, 0.96, 0.82, 1.0)
polygon = PackedVector2Array(0,-44, 14,-40, 28,-28, 36,-12, 36,4, 28,20, 14,32, 0,36, -14,32, -28,20, -36,4, -36,-12, -28,-28, -14,-40)

[node name="MoonCut" type="Polygon2D" parent="MoonGroup"]
color = Color(0.09, 0.07, 0.26, 1)
polygon = PackedVector2Array(14,-42, 28,-28, 36,-10, 36,6, 28,22, 14,34, 22,28, 30,14, 34,0, 30,-14, 22,-30)

[node name="MoonStar" type="Polygon2D" parent="MoonGroup"]
color = Color(1.0, 0.90, 0.20, 1.0)
polygon = PackedVector2Array(20,-18, 22,-12, 28,-12, 23,-8, 25,-2, 20,-6, 15,-2, 17,-8, 12,-12, 18,-12)

[node name="HillFar" type="Polygon2D" parent="."]
color = Color(0.11, 0.18, 0.14, 0.72)
polygon = PackedVector2Array(0,720, 0,558, 160,484, 380,522, 620,472, 860,512, 1080,476, 1280,502, 1280,720)

[node name="HillNear" type="Polygon2D" parent="."]
color = Color(0.09, 0.15, 0.11, 1)
polygon = PackedVector2Array(0,720, 0,618, 110,576, 290,596, 500,562, 740,588, 980,558, 1280,578, 1280,720)

[node name="SilL" type="Node2D" parent="."]
position = Vector2(50, 0)

[node name="Minaret" type="ColorRect" parent="SilL"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(112, 440)
size = Vector2(20, 280)

[node name="MinaretTop" type="Polygon2D" parent="SilL"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(112,444, 122,418, 132,444)

[node name="Body" type="ColorRect" parent="SilL"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(0, 520)
size = Vector2(112, 200)

[node name="Dome" type="Polygon2D" parent="SilL"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(0,524, 20,488, 44,470, 56,466, 68,470, 92,488, 112,524)

[node name="SilR" type="Node2D" parent="."]
position = Vector2(1108, 0)

[node name="Minaret" type="ColorRect" parent="SilR"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(-18, 450)
size = Vector2(18, 270)

[node name="MinaretTop" type="Polygon2D" parent="SilR"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(-18,454, -9,430, 0,454)

[node name="Body" type="ColorRect" parent="SilR"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(0, 530)
size = Vector2(100, 190)

[node name="Dome" type="Polygon2D" parent="SilR"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(0,534, 18,500, 38,484, 50,480, 62,484, 82,500, 100,534)

[node name="UI" type="CanvasLayer" parent="."]

[node name="Card" type="Panel" parent="UI"]
position = Vector2(410, 160)
size = Vector2(460, 400)
theme_override_styles/panel = SubResource("SB_card")

[node name="Inner" type="VBoxContainer" parent="UI/Card"]
position = Vector2(32, 28)
size = Vector2(396, 344)
theme_override_constants/separation = 12

[node name="LblTitle" type="Label" parent="UI/Card/Inner"]
size_flags_horizontal = 3
text = "🌙 Maryam Journey"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 28

[node name="LblBismillah" type="Label" parent="UI/Card/Inner"]
size_flags_horizontal = 3
text = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 15
theme_override_colors/font_color = Color(1.0, 0.90, 0.38, 1)

[node name="LblDesc" type="Label" parent="UI/Card/Inner"]
size_flags_horizontal = 3
text = "Jelajahi dunia bersama Maryam 🌟"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 12
theme_override_colors/font_color = Color(0.80, 0.80, 0.94, 1)

[node name="LblStars" type="Label" parent="UI/Card/Inner"]
size_flags_horizontal = 3
text = "Petualangan baru menantimu!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 11
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="Sep" type="HSeparator" parent="UI/Card/Inner"]
size_flags_horizontal = 3

[node name="BtnStart" type="Button" parent="UI/Card/Inner"]
size_flags_horizontal = 3
text = "✨  Mulai Petualangan Baru"
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 14

[node name="BtnContinue" type="Button" parent="UI/Card/Inner"]
size_flags_horizontal = 3
text = "▶  Lanjutkan Petualangan"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 14

[node name="BtnReset" type="Button" parent="UI/Card/Inner"]
size_flags_horizontal = 3
text = "🗑  Hapus Progress"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 11
theme_override_colors/font_color = Color(1, 0.50, 0.50, 1)
""")

try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m", "fix: menu simple manual position center"], cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️  Git: {e}")

print("\n  Godot → Reload → F5 → Card tepat di tengah! 🌙\n")
