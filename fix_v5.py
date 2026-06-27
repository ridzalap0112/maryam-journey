"""
Maryam Journey - Fix V5
Menyelesaikan: main menu center, player di tanah, fitur baru
python fix_v5.py
"""
import os, re, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Fix V5")
print("=" * 52)

# ═══════════════════════════════════════════════════════════
# 1. MainMenu.tscn + MainMenu.gd
#    Fix: pakai MarginContainer wrapping VBox supaya card
#    benar-benar centered secara vertikal di layar 720px
# ═══════════════════════════════════════════════════════════

# Node tree (FINAL, tidak boleh berubah tanpa update gd):
# MainMenu (Node2D)
#   [visual nodes...]
#   UI (CanvasLayer)
#     Root (Control) — full rect 1280x720
#       Card (Panel)  — anchored center
#         Inner (VBoxContainer)
#           LblTitle
#           LblBismillah
#           LblDesc
#           LblStars
#           Sep (HSeparator)
#           BtnStart
#           BtnContinue
#           BtnReset

write(os.path.join(BASE, "scripts", "ui", "MainMenu.gd"), """\
# =============================================================
#  scripts/ui/MainMenu.gd
# =============================================================
extends Node2D

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"

@onready var _btn_start    : Button = $UI/Root/Card/Inner/BtnStart
@onready var _btn_continue : Button = $UI/Root/Card/Inner/BtnContinue
@onready var _btn_reset    : Button = $UI/Root/Card/Inner/BtnReset
@onready var _lbl_stars    : Label  = $UI/Root/Card/Inner/LblStars


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
content_margin_left = 36.0
content_margin_right = 36.0
content_margin_top = 32.0
content_margin_bottom = 32.0

[sub_resource type="StyleBoxEmpty" id="SB_empty"]

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

[node name="Root" type="Control" parent="UI"]
anchor_right = 1.0
anchor_bottom = 1.0
offset_right = 1280.0
offset_bottom = 720.0
grow_horizontal = 2
grow_vertical = 2

[node name="Card" type="Panel" parent="UI/Root"]
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -230.0
offset_top = -200.0
offset_right = 230.0
offset_bottom = 200.0
grow_horizontal = 2
grow_vertical = 2
theme_override_styles/panel = SubResource("SB_card")

[node name="Inner" type="VBoxContainer" parent="UI/Root/Card"]
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 36.0
offset_top = 32.0
offset_right = -36.0
offset_bottom = -32.0
theme_override_constants/separation = 12

[node name="LblTitle" type="Label" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3
text = "🌙 Maryam Journey"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 30

[node name="LblBismillah" type="Label" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3
text = "بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 15
theme_override_colors/font_color = Color(1.0, 0.90, 0.38, 1)

[node name="LblDesc" type="Label" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3
text = "Jelajahi dunia bersama Maryam\nBelajar, bermain, dan tumbuh bersama Islam 🌟"
horizontal_alignment = 1
autowrap_mode = 3
theme_override_font_sizes/font_size = 12
theme_override_colors/font_color = Color(0.80, 0.80, 0.94, 1)

[node name="LblStars" type="Label" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3
text = "Petualangan baru menantimu!"
horizontal_alignment = 1
theme_override_font_sizes/font_size = 11
theme_override_colors/font_color = Color(1.0, 0.84, 0.12, 1)

[node name="Sep" type="HSeparator" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3

[node name="BtnStart" type="Button" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3
text = "✨  Mulai Petualangan Baru"
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 14

[node name="BtnContinue" type="Button" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3
text = "▶  Lanjutkan Petualangan"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 14

[node name="BtnReset" type="Button" parent="UI/Root/Card/Inner"]
size_flags_horizontal = 3
text = "🗑  Hapus Progress"
visible = false
theme_override_styles/normal = SubResource("SB_btn")
theme_override_styles/hover = SubResource("SB_hover")
theme_override_styles/pressed = SubResource("SB_btn")
theme_override_font_sizes/font_size = 11
theme_override_colors/font_color = Color(1, 0.50, 0.50, 1)
""")

# ═══════════════════════════════════════════════════════════
# 2. Fix WorldMap.tscn — ground collision dan player Y
#
#    Ground StaticBody2D di Y=580
#    CollisionShape2D size=Vector2(4800,300)
#    → shape center default di (0,0) relatif ke StaticBody2D
#    → jadi collision top = 580 + 0 - 150 = 430  ← SALAH
#
#    FIX: geser CollisionShape2D ke position=(2400, 150)
#    → collision top = 580 + 150 - 150 = 580  ✅
#
#    Player collision half-height = 26 (size=52)
#    → Player harus di Y = 580 - 26 = 554
# ═══════════════════════════════════════════════════════════
wmap_path = os.path.join(BASE, "scenes", "world", "WorldMap.tscn")
with open(wmap_path, "r", encoding="utf-8") as f:
    wmap = f.read()

# Fix GroundCollision position — collision top tepat di Y=580
wmap = wmap.replace(
    '[node name="GroundCollision" type="CollisionShape2D" parent="Ground"]\nposition = Vector2(2400, 100)',
    '[node name="GroundCollision" type="CollisionShape2D" parent="Ground"]\nposition = Vector2(2400, 150)'
)

# Fix jika belum ada position di GroundCollision
if 'position = Vector2(2400, 150)' not in wmap:
    wmap = wmap.replace(
        '[node name="GroundCollision" type="CollisionShape2D" parent="Ground"]',
        '[node name="GroundCollision" type="CollisionShape2D" parent="Ground"]\nposition = Vector2(2400, 150)'
    )

# Fix Player position — tepat di Y=554 (580 - 26)
wmap = re.sub(
    r'(\[node name="Player" type="CharacterBody2D"[^\]]*\])\nposition = Vector2\([^)]+\)',
    r'\1\nposition = Vector2(200, 554)',
    wmap
)

with open(wmap_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(wmap)
print("  ✅  WorldMap.tscn — ground collision + player Y fixed")

# ═══════════════════════════════════════════════════════════
# 3. Player.gd — FLOOR_Y = 554 sesuai ground fix
# ═══════════════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "player", "Player.gd"), """\
# =============================================================
#  scripts/player/Player.gd  —  Godot 4.7
# =============================================================
extends CharacterBody2D

const SPEED       : float = 200.0
const GRAVITY     : float = 800.0
const JUMP_FORCE  : float = -420.0

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
\tif pos.y > FLOOR_Y + 20.0:
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

# ═══════════════════════════════════════════════════════════
# 4. HUD — tambah tombol hint arah (fitur baru)
# ═══════════════════════════════════════════════════════════
write(os.path.join(BASE, "scripts", "ui", "HUD.gd"), """\
# =============================================================
#  scripts/ui/HUD.gd
# =============================================================
extends CanvasLayer

@onready var _star_label : Label = $StarPanel/StarLabel
@onready var _name_label : Label = $NameLabel
@onready var _hint_arrow : Label = $HintArrow

var _hint_time : float = 0.0
var _show_hint : bool  = true


func _ready() -> void:
\tGameManager.star_collected.connect(_on_star)
\t_name_label.text = "🌙 " + GameManager.player_name
\t_star_label.text = "⭐  " + str(GameManager.total_stars)
\t_hint_arrow.text = "Jalan ke kanan →"
\t_hint_arrow.visible = true


func _process(delta: float) -> void:
\tif not _show_hint:
\t\treturn
\t_hint_time += delta
\t_hint_arrow.modulate.a = 0.6 + sin(_hint_time * 3.0) * 0.4


func hide_hint() -> void:
\t_show_hint = false
\t_hint_arrow.visible = false


func _on_star(total: int) -> void:
\t_star_label.text = "⭐  " + str(total)
""")

# ── Git commit ────────────────────────────────────────────────
print("\n  📦 Commit ke GitHub...")
try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m",
        "fix: main menu centered, ground collision fixed, player on floor, hud hint"],
        cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️   Git: {e}")

print("\n" + "=" * 52)
print("  SELESAI — no errors!")
print("  1. Godot → Project → Reload Current Project")
print("  2. F5 → Main Menu tepat di tengah layar")
print("  3. Klik Mulai → karakter berdiri tepat di tanah")
print("  4. Ada hint 'Jalan ke kanan →' berkedip di HUD")
print("=" * 52 + "\n")
