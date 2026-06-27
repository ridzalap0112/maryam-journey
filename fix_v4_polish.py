"""
Maryam Journey - Fix V4 Polish
python fix_v4_polish.py
"""
import os, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Fix V4 Polish")
print("=" * 52)

# ── 1. Fix MainMenu.tscn — bulan tidak terpotong, card full ──
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
content_margin_left = 24.0
content_margin_right = 24.0
content_margin_top = 12.0
content_margin_bottom = 12.0

[sub_resource type="StyleBoxFlat" id="SB_card"]
bg_color = Color(0.05, 0.04, 0.18, 0.92)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.84, 0.12, 0.75)
corner_radius_top_left = 20
corner_radius_top_right = 20
corner_radius_bottom_right = 20
corner_radius_bottom_left = 20
content_margin_left = 32.0
content_margin_right = 32.0
content_margin_top = 28.0
content_margin_bottom = 28.0

[node name="MainMenu" type="Node2D"]
script = ExtResource("1_menu")

[node name="BgSky" type="ColorRect" parent="."]
color = Color(0.09, 0.07, 0.26, 1)
size = Vector2(1280, 720)

[node name="GlowTop" type="Polygon2D" parent="."]
color = Color(0.26, 0.16, 0.55, 0.28)
polygon = PackedVector2Array(0,0, 1280,0, 1280,360, 0,360)

[node name="Stars" type="Node2D" parent="."]

[node name="S1" type="Polygon2D" parent="Stars"]
color = Color(1,1,1,0.92)
polygon = PackedVector2Array(140,75, 142,82, 150,82, 144,87, 146,94, 140,89, 134,94, 136,87, 130,82, 138,82)

[node name="S2" type="Polygon2D" parent="Stars"]
color = Color(1,1,0.85,0.82)
polygon = PackedVector2Array(320,38, 321,42, 325,42, 322,45, 323,49, 320,46, 317,49, 318,45, 315,42, 319,42)

[node name="S3" type="Polygon2D" parent="Stars"]
color = Color(1,1,1,0.88)
polygon = PackedVector2Array(560,65, 562,72, 570,72, 564,77, 566,84, 560,79, 554,84, 556,77, 550,72, 558,72)

[node name="S4" type="Polygon2D" parent="Stars"]
color = Color(1,1,0.85,0.76)
polygon = PackedVector2Array(760,32, 761,36, 765,36, 762,39, 763,43, 760,40, 757,43, 758,39, 755,36, 759,36)

[node name="S5" type="Polygon2D" parent="Stars"]
color = Color(1,1,1,0.85)
polygon = PackedVector2Array(980,82, 982,89, 990,89, 984,94, 986,101, 980,96, 974,101, 976,94, 970,89, 978,89)

[node name="S6" type="Polygon2D" parent="Stars"]
color = Color(1,1,0.85,0.72)
polygon = PackedVector2Array(200,155, 201,158, 204,158, 202,160, 203,163, 200,161, 197,163, 198,160, 196,158, 199,158)

[node name="S7" type="Polygon2D" parent="Stars"]
color = Color(1,1,1,0.80)
polygon = PackedVector2Array(840,130, 841,133, 844,133, 842,135, 843,138, 840,136, 837,138, 838,135, 836,133, 839,133)

[node name="S8" type="Polygon2D" parent="Stars"]
color = Color(1,1,0.85,0.78)
polygon = PackedVector2Array(440,110, 441,113, 444,113, 442,115, 443,118, 440,116, 437,118, 438,115, 436,113, 439,113)

[node name="MoonGroup" type="Node2D" parent="."]
position = Vector2(940, 70)

[node name="MoonGlow" type="Polygon2D" parent="MoonGroup"]
color = Color(1.0, 0.95, 0.70, 0.14)
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

[node name="SilMasjidL" type="Node2D" parent="."]
position = Vector2(50, 0)

[node name="Minaret" type="ColorRect" parent="SilMasjidL"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(112, 440)
size = Vector2(20, 280)

[node name="MinaretTop" type="Polygon2D" parent="SilMasjidL"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(112,444, 122,418, 132,444)

[node name="Body" type="ColorRect" parent="SilMasjidL"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(0, 520)
size = Vector2(112, 200)

[node name="Dome" type="Polygon2D" parent="SilMasjidL"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(0,524, 20,488, 44,470, 56,466, 68,470, 92,488, 112,524)

[node name="SilMasjidR" type="Node2D" parent="."]
position = Vector2(1108, 0)

[node name="Minaret" type="ColorRect" parent="SilMasjidR"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(-18, 450)
size = Vector2(18, 270)

[node name="MinaretTop" type="Polygon2D" parent="SilMasjidR"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(-18,454, -9,430, 0,454)

[node name="Body" type="ColorRect" parent="SilMasjidR"]
color = Color(0.07, 0.12, 0.09, 1)
position = Vector2(0, 530)
size = Vector2(100, 190)

[node name="Dome" type="Polygon2D" parent="SilMasjidR"]
color = Color(0.06, 0.10, 0.08, 1)
polygon = PackedVector2Array(0,534, 18,500, 38,484, 50,480, 62,484, 82,500, 100,534)

[node name="UI" type="CanvasLayer" parent="."]

[node name="Center" type="CenterContainer" parent="UI"]
anchors_preset = 15
offset_right = 1280.0
offset_bottom = 720.0

[node name="Card" type="Panel" parent="UI/Center"]
custom_minimum_size = Vector2(460, 0)
theme_override_styles/panel = SubResource("SB_card")

[node name="Inner" type="VBoxContainer" parent="UI/Center/Card"]
anchors_preset = 15
theme_override_constants/separation = 14

[node name="LblTitle" type="Label" parent="UI/Center/Card/Inner"]
text = "🌙 Maryam Journey"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 32

[node name="LblBismillah" type="Label" parent="UI/Center/Card/Inner"]
text = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 16
theme_override_colors/font_color = Color(1.0, 0.90, 0.38, 1)

[node name="LblDesc" type="Label" parent="UI/Center/Card/Inner"]
text = "Jelajahi dunia bersama Maryam\nBelajar, bermain, dan tumbuh bersama Islam 🌟"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 13
theme_override_colors/font_color = Color(0.80, 0.80, 0.94, 1)

[node name="LblStars" type="Label" parent="UI/Center/Card/Inner"]
text = "Petualangan baru menantimu!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 12
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="Sep" type="HSeparator" parent="UI/Center/Card/Inner"]

[node name="BtnStart" type="Button" parent="UI/Center/Card/Inner"]
text = "✨  Mulai Petualangan Baru"
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 15

[node name="BtnContinue" type="Button" parent="UI/Center/Card/Inner"]
text = "▶  Lanjutkan Petualangan"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 15

[node name="BtnReset" type="Button" parent="UI/Center/Card/Inner"]
text = "🗑  Hapus Progress"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 12
theme_override_colors/font_color = Color(1, 0.50, 0.50, 1)
""")

# ── 2. Fix WorldMap — player tepat di atas tanah ─────────────
# Ground StaticBody2D di Y=580, collision center di Y=580+100=680
# Player harus start di Y = 580 - (collision_half_height) = 580 - 26 = 554
# Kita set player start Y=545 supaya ada sedikit ruang

# Baca file WorldMap.tscn yang ada, ganti posisi Player
wmap_path = os.path.join(BASE, "scenes", "world", "WorldMap.tscn")
if os.path.exists(wmap_path):
    with open(wmap_path, "r", encoding="utf-8") as f:
        wmap = f.read()

    # Fix player position — tepat di atas tanah (ground Y=580)
    # Player collision setengah = 26, jadi player Y = 580 - 26 = 554
    import re

    # Ganti posisi player
    wmap = re.sub(
        r'(\[node name="Player"[^\]]*\])\nposition = Vector2\([^)]+\)',
        r'\1\nposition = Vector2(200, 545)',
        wmap
    )

    # Fix camera limit agar tidak melayang
    wmap = wmap.replace(
        "limit_top = 0\nlimit_bottom = 720",
        "limit_top = 0\nlimit_bottom = 720\ndrag_horizontal_enabled = true\ndrag_horizontal_offset = 0.0"
    )

    with open(wmap_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(wmap)
    print("  ✅  scenes/world/WorldMap.tscn — player position fixed")
else:
    print("  ⚠️   WorldMap.tscn tidak ditemukan, skip")

# ── 3. Player.gd — perbaiki FLOOR_Y sesuai ground baru ───────
write(os.path.join(BASE, "scripts", "player", "Player.gd"), """\
# =============================================================
#  scripts/player/Player.gd  —  Godot 4.7
# =============================================================
extends CharacterBody2D

const SPEED       : float = 200.0
const GRAVITY     : float = 800.0
const JUMP_FORCE  : float = -420.0

# Ground StaticBody2D di Y=580
# Collision player half-height = 26
# Floor = 580 - 26 = 554
const WORLD_LEFT  : float = 40.0
const WORLD_RIGHT : float = 4760.0
const WORLD_TOP   : float = 50.0
const FLOOR_Y     : float = 554.0

@onready var _sprite : AnimatedSprite2D = $AnimatedSprite2D

var _anim_current : String = ""


func _ready() -> void:
\tassert(_sprite != null, "AnimatedSprite2D tidak ditemukan!")
\tadd_to_group("player")
\t_play_anim("idle")


func _physics_process(delta: float) -> void:
\t_apply_gravity(delta)
\t_handle_movement()
\t_handle_jump()
\tmove_and_slide()
\t_enforce_boundary()
\t_update_animation()


func _apply_gravity(delta: float) -> void:
\tif not is_on_floor():
\t\tvelocity.y += GRAVITY * delta
\t\tvelocity.y = min(velocity.y, 1400.0)


func _handle_movement() -> void:
\tvar dir := Input.get_axis("move_left", "move_right")
\tvelocity.x = dir * SPEED
\tif dir != 0.0:
\t\t_sprite.flip_h = dir < 0.0


func _handle_jump() -> void:
\tif is_on_floor() and Input.is_action_just_pressed("jump"):
\t\tvelocity.y = JUMP_FORCE


func _enforce_boundary() -> void:
\tvar pos := global_position
\tif pos.x < WORLD_LEFT:
\t\tpos.x = WORLD_LEFT
\t\tvelocity.x = 0.0
\tif pos.x > WORLD_RIGHT:
\t\tpos.x = WORLD_RIGHT
\t\tvelocity.x = 0.0
\tif pos.y < WORLD_TOP:
\t\tpos.y = WORLD_TOP
\t\tvelocity.y = 0.0
\tif pos.y > FLOOR_Y + 30.0:
\t\tpos.y = FLOOR_Y
\t\tvelocity.y = 0.0
\tglobal_position = pos


func _update_animation() -> void:
\tvar next : String
\tif not is_on_floor():
\t\tnext = "jump"
\telif abs(velocity.x) > 10.0:
\t\tnext = "walk"
\telse:
\t\tnext = "idle"
\t_play_anim(next)


func _play_anim(anim_name: String) -> void:
\tif _anim_current == anim_name:
\t\treturn
\tif _sprite.sprite_frames and _sprite.sprite_frames.has_animation(anim_name):
\t\t_anim_current = anim_name
\t\t_sprite.play(anim_name)
""")

# ── 4. Parallax script untuk WorldMap ────────────────────────
write(os.path.join(BASE, "scripts", "world", "ParallaxSky.gd"), """\
# =============================================================
#  scripts/world/ParallaxSky.gd
#  Tempelkan ke node Sky (ColorRect) di WorldMap
#  Sky bergerak 20% dari kecepatan kamera — memberi kesan depth
# =============================================================
extends Node2D

const PARALLAX_FACTOR : float = 0.15

var _start_x   : float = 0.0
var _camera    : Camera2D


func _ready() -> void:
\t_start_x = position.x
\tawait get_tree().process_frame
\t# Cari Camera2D di dalam Player
\tvar player = get_tree().get_first_node_in_group("player")
\tif player:
\t\t_camera = player.get_node_or_null("Camera2D")


func _process(_delta: float) -> void:
\tif not _camera:
\t\treturn
\tposition.x = _start_x + _camera.get_screen_center_position().x * PARALLAX_FACTOR
""")

# ── 5. Git commit ─────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "fix: player position on ground, moon fix, card centered, parallax sky"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

print("\n" + "=" * 52)
print("  SELESAI!")
print("  1. Godot → Project → Reload Current Project")
print("  2. Tekan F5")
print("  3. Main Menu: bulan fix, card center, tidak terpotong")
print("  4. World: karakter berdiri TEPAT di atas tanah")
print("  5. Boundary kiri & kanan aktif")
print("=" * 52 + "\n")
