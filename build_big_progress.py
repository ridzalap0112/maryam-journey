"""
Maryam Journey - Big Progress Build
Jalankan: python build_big_progress.py
"""
import os

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Big Progress Build")
print("=" * 52)

# ── 1. LocationZone.gd ───────────────────────────────────────
write(os.path.join(BASE, "scripts", "locations", "LocationZone.gd"), """\
# =============================================================
#  scripts/locations/LocationZone.gd
#  Zona lokasi yang bisa dimasuki pemain
# =============================================================
extends Area2D

@export var location_name : String = "Lokasi"
@export var location_key  : String = "masjid"
@export var hint_color    : Color  = Color(1.0, 0.85, 0.2, 1.0)

@onready var _label     : Label        = $Label
@onready var _indicator : AnimatedSprite2D = $Indicator

var _player_inside : bool = false


func _ready() -> void:
\t_label.text = location_name
\t_label.visible = false
\t_indicator.visible = false
\tbody_entered.connect(_on_body_entered)
\tbody_exited.connect(_on_body_exited)


func _process(_delta: float) -> void:
\tif _player_inside and Input.is_action_just_pressed("interact"):
\t\t_enter_location()


func _on_body_entered(body: Node2D) -> void:
\tif body.is_in_group("player"):
\t\t_player_inside = true
\t\t_label.visible = true
\t\t_indicator.visible = true
\t\t_indicator.play("bounce")


func _on_body_exited(body: Node2D) -> void:
\tif body.is_in_group("player"):
\t\t_player_inside = false
\t\t_label.visible = false
\t\t_indicator.visible = false


func _enter_location() -> void:
\tif not GameManager.is_location_unlocked(location_key):
\t\tprint("[Zone] Lokasi terkunci: ", location_key)
\t\treturn
\tprint("[Zone] Masuk ke: ", location_name)
""")

# ── 2. Player.gd (tambah group) ──────────────────────────────
write(os.path.join(BASE, "scripts", "player", "Player.gd"), """\
# =============================================================
#  scripts/player/Player.gd
#  Karakter Maryam — Godot 4.7
# =============================================================
extends CharacterBody2D

const SPEED      : float = 180.0
const GRAVITY    : float = 700.0
const JUMP_FORCE : float = -380.0

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
\t_update_animation()
\tmove_and_slide()


func _apply_gravity(delta: float) -> void:
\tif not is_on_floor():
\t\tvelocity.y += GRAVITY * delta


func _handle_movement() -> void:
\tvar dir := Input.get_axis("move_left", "move_right")
\tvelocity.x = dir * SPEED
\tif dir != 0.0:
\t\t_sprite.flip_h = dir < 0.0


func _handle_jump() -> void:
\tif is_on_floor() and Input.is_action_just_pressed("jump"):
\t\tvelocity.y = JUMP_FORCE


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

# ── 3. GameManager.gd ────────────────────────────────────────
write(os.path.join(BASE, "scripts", "managers", "GameManager.gd"), """\
# =============================================================
#  scripts/managers/GameManager.gd
#  Autoload global
# =============================================================
extends Node

var player_name        : String = "Maryam"
var total_stars        : int    = 0
var unlocked_locations : Array  = ["masjid", "pondok", "taman", "kebun", "rumah"]

signal star_collected(total: int)
signal location_unlocked(location_name: String)


func _ready() -> void:
\tprint("[MaryamJourney] Assalamu'alaikum!")


func add_star(amount: int = 1) -> void:
\ttotal_stars += amount
\tstar_collected.emit(total_stars)


func unlock_location(location_name: String) -> void:
\tif location_name not in unlocked_locations:
\t\tunlocked_locations.append(location_name)
\t\tlocation_unlocked.emit(location_name)


func is_location_unlocked(location_name: String) -> bool:
\treturn location_name in unlocked_locations
""")

# ── 4. WorldMap.tscn — World luas + 5 zona lokasi ────────────
write(os.path.join(BASE, "scenes", "world", "WorldMap.tscn"), """\
[gd_scene load_steps=12 format=3]

[ext_resource type="Script" path="res://scripts/player/Player.gd" id="1_player"]
[ext_resource type="Script" path="res://scripts/locations/LocationZone.gd" id="2_zone"]
[ext_resource type="Texture2D" path="res://icon.svg" id="3_icon"]

[sub_resource type="SpriteFrames" id="SF_player"]
animations = [{
"frames": [{"duration": 1.0, "texture": ExtResource("3_icon")}],
"loop": true, "name": &"idle", "speed": 5.0
}, {
"frames": [{"duration": 1.0, "texture": ExtResource("3_icon")}],
"loop": true, "name": &"walk", "speed": 8.0
}, {
"frames": [{"duration": 1.0, "texture": ExtResource("3_icon")}],
"loop": false, "name": &"jump", "speed": 5.0
}]

[sub_resource type="SpriteFrames" id="SF_indicator"]
animations = [{
"frames": [{"duration": 1.0, "texture": ExtResource("3_icon")}],
"loop": true, "name": &"bounce", "speed": 3.0
}]

[sub_resource type="RectangleShape2D" id="Shape_ground"]
size = Vector2(4800, 40)

[sub_resource type="RectangleShape2D" id="Shape_player"]
size = Vector2(36, 36)

[sub_resource type="RectangleShape2D" id="Shape_zone"]
size = Vector2(140, 200)

[sub_resource type="GDScript" id="CloudScript"]
script/source = "extends Node2D
@export var speed : float = 22.0
func _process(delta):
\tposition.x += speed * delta
\tif position.x > 5000.0:
\t\tposition.x = -300.0
"

[sub_resource type="GDScript" id="SignScript"]
script/source = "extends Node2D
var _time : float = 0.0
func _process(delta):
\t_time += delta
\tposition.y = sin(_time * 2.5) * 6.0
"

[node name="WorldMap" type="Node2D"]

[node name="Sky" type="ColorRect" parent="."]
color = Color(0.45, 0.75, 0.95, 1)
size = Vector2(4800, 720)

[node name="SkyGlow" type="ColorRect" parent="."]
color = Color(0.62, 0.87, 0.98, 0.45)
position = Vector2(0, 420)
size = Vector2(4800, 300)

[node name="Cloud1" type="Node2D" parent="."]
position = Vector2(120, 55)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud1"]
color = Color(1, 1, 1, 0.92)
polygon = PackedVector2Array(0,26, 16,6, 42,0, 74,4, 98,0, 118,6, 128,26)

[node name="Cloud2" type="Node2D" parent="."]
position = Vector2(480, 36)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud2"]
color = Color(1, 1, 1, 0.86)
polygon = PackedVector2Array(0,22, 14,4, 36,0, 62,3, 82,0, 96,4, 102,22)

[node name="Cloud3" type="Node2D" parent="."]
position = Vector2(900, 68)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud3"]
color = Color(1, 1, 1, 0.89)
polygon = PackedVector2Array(0,20, 12,3, 30,0, 54,4, 72,0, 84,3, 90,20)

[node name="Cloud4" type="Node2D" parent="."]
position = Vector2(1400, 44)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud4"]
color = Color(1, 1, 1, 0.83)
polygon = PackedVector2Array(0,18, 10,2, 28,0, 48,3, 64,0, 74,2, 80,18)

[node name="Cloud5" type="Node2D" parent="."]
position = Vector2(2000, 60)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud5"]
color = Color(1, 1, 1, 0.88)
polygon = PackedVector2Array(0,24, 14,5, 38,0, 66,4, 88,0, 104,5, 112,24)

[node name="Cloud6" type="Node2D" parent="."]
position = Vector2(2800, 42)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud6"]
color = Color(1, 1, 1, 0.84)
polygon = PackedVector2Array(0,20, 12,3, 32,0, 56,4, 74,0, 86,3, 92,20)

[node name="Cloud7" type="Node2D" parent="."]
position = Vector2(3600, 70)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud7"]
color = Color(1, 1, 1, 0.87)
polygon = PackedVector2Array(0,22, 13,4, 34,0, 60,3, 80,0, 92,4, 98,22)

[node name="MountainFar" type="Polygon2D" parent="."]
color = Color(0.55, 0.72, 0.60, 0.50)
polygon = PackedVector2Array(0,570, 200,390, 500,440, 800,370, 1100,420, 1400,360, 1700,410, 2000,375, 2300,415, 2600,380, 2900,420, 3200,365, 3500,405, 3800,380, 4100,420, 4400,390, 4800,430, 4800,570)

[node name="MountainNear" type="Polygon2D" parent="."]
color = Color(0.32, 0.58, 0.30, 1)
polygon = PackedVector2Array(0,590, 150,500, 350,535, 600,470, 850,515, 1100,475, 1400,510, 1700,468, 2000,505, 2300,472, 2600,508, 2900,465, 3200,502, 3500,470, 3800,508, 4100,472, 4400,500, 4800,480, 4800,590)

[node name="Trees" type="Node2D" parent="."]

[node name="T1" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T1"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(60, 555)
size = Vector2(16, 90)
[node name="Top2" type="Polygon2D" parent="Trees/T1"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(68,478, 30,572, 106,572)
[node name="Top1" type="Polygon2D" parent="Trees/T1"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(68,500, 26,588, 110,588)

[node name="T2" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T2"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(185, 560)
size = Vector2(14, 85)
[node name="Top2" type="Polygon2D" parent="Trees/T2"]
color = Color(0.17, 0.50, 0.20, 1)
polygon = PackedVector2Array(192,484, 156,572, 228,572)
[node name="Top1" type="Polygon2D" parent="Trees/T2"]
color = Color(0.22, 0.62, 0.26, 1)
polygon = PackedVector2Array(192,506, 152,588, 232,588)

[node name="T3" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T3"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(1250, 558)
size = Vector2(16, 87)
[node name="Top2" type="Polygon2D" parent="Trees/T3"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(1258,480, 1220,572, 1296,572)
[node name="Top1" type="Polygon2D" parent="Trees/T3"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(1258,502, 1216,588, 1300,588)

[node name="T4" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T4"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(1850, 555)
size = Vector2(16, 90)
[node name="Top2" type="Polygon2D" parent="Trees/T4"]
color = Color(0.17, 0.50, 0.20, 1)
polygon = PackedVector2Array(1858,476, 1820,572, 1896,572)
[node name="Top1" type="Polygon2D" parent="Trees/T4"]
color = Color(0.22, 0.62, 0.26, 1)
polygon = PackedVector2Array(1858,498, 1816,588, 1900,588)

[node name="T5" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T5"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(2600, 558)
size = Vector2(16, 87)
[node name="Top2" type="Polygon2D" parent="Trees/T5"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(2608,480, 2570,572, 2646,572)
[node name="Top1" type="Polygon2D" parent="Trees/T5"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(2608,502, 2566,588, 2650,588)

[node name="T6" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T6"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(3400, 556)
size = Vector2(16, 89)
[node name="Top2" type="Polygon2D" parent="Trees/T6"]
color = Color(0.17, 0.50, 0.20, 1)
polygon = PackedVector2Array(3408,478, 3370,572, 3446,572)
[node name="Top1" type="Polygon2D" parent="Trees/T6"]
color = Color(0.22, 0.62, 0.26, 1)
polygon = PackedVector2Array(3408,500, 3366,588, 3450,588)

[node name="T7" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T7"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(4200, 558)
size = Vector2(16, 87)
[node name="Top2" type="Polygon2D" parent="Trees/T7"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(4208,480, 4170,572, 4246,572)
[node name="Top1" type="Polygon2D" parent="Trees/T7"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(4208,502, 4166,588, 4250,588)

[node name="Buildings" type="Node2D" parent="."]

[node name="House1" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/House1"]
color = Color(0.82, 0.72, 0.55, 1)
position = Vector2(320, 490)
size = Vector2(110, 150)
[node name="Roof" type="Polygon2D" parent="Buildings/House1"]
color = Color(0.62, 0.30, 0.18, 1)
polygon = PackedVector2Array(310,494, 375,435, 440,494)
[node name="Door" type="ColorRect" parent="Buildings/House1"]
color = Color(0.45, 0.28, 0.12, 1)
position = Vector2(358, 550)
size = Vector2(34, 90)
[node name="Window" type="ColorRect" parent="Buildings/House1"]
color = Color(0.55, 0.78, 0.92, 1)
position = Vector2(392, 510)
size = Vector2(28, 28)

[node name="House2" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/House2"]
color = Color(0.76, 0.65, 0.50, 1)
position = Vector2(530, 500)
size = Vector2(95, 140)
[node name="Roof" type="Polygon2D" parent="Buildings/House2"]
color = Color(0.55, 0.27, 0.16, 1)
polygon = PackedVector2Array(520,504, 577,450, 635,504)
[node name="Door" type="ColorRect" parent="Buildings/House2"]
color = Color(0.42, 0.26, 0.10, 1)
position = Vector2(560, 558)
size = Vector2(30, 82)

[node name="Masjid" type="Node2D" parent="Buildings"]
[node name="Body" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.95, 0.95, 0.88, 1)
position = Vector2(700, 430)
size = Vector2(160, 210)
[node name="Dome" type="Polygon2D" parent="Buildings/Masjid"]
color = Color(0.20, 0.65, 0.35, 1)
polygon = PackedVector2Array(700,434, 720,395, 750,375, 780,368, 810,375, 840,395, 860,434)
[node name="DomeTop" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.18, 0.58, 0.30, 1)
position = Vector2(776, 340)
size = Vector2(8, 32)
[node name="Door" type="Polygon2D" parent="Buildings/Masjid"]
color = Color(0.35, 0.22, 0.08, 1)
polygon = PackedVector2Array(756,640, 756,530, 764,510, 780,505, 796,510, 804,530, 804,640)
[node name="WindowL" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(714, 480)
size = Vector2(30, 50)
[node name="WindowR" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(816, 480)
size = Vector2(30, 50)
[node name="Minaret" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.92, 0.92, 0.84, 1)
position = Vector2(870, 420)
size = Vector2(28, 220)
[node name="MinaretTop" type="Polygon2D" parent="Buildings/Masjid"]
color = Color(0.20, 0.65, 0.35, 1)
polygon = PackedVector2Array(870,424, 884,395, 898,424)

[node name="PondokBaca" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.88, 0.76, 0.55, 1)
position = Vector2(1600, 480)
size = Vector2(150, 160)
[node name="Roof" type="Polygon2D" parent="Buildings/PondokBaca"]
color = Color(0.50, 0.24, 0.12, 1)
polygon = PackedVector2Array(1588,484, 1675,418, 1762,484)
[node name="Sign" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.35, 0.20, 0.08, 1)
position = Vector2(1628, 490)
size = Vector2(70, 20)
[node name="Door" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.40, 0.24, 0.09, 1)
position = Vector2(1656, 548)
size = Vector2(38, 92)
[node name="WindowL" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(1610, 500)
size = Vector2(34, 34)
[node name="WindowR" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(1710, 500)
size = Vector2(34, 34)

[node name="TamanLogika" type="Node2D" parent="Buildings"]
[node name="Gate" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.30, 0.58, 0.28, 1)
polygon = PackedVector2Array(2400,640, 2400,510, 2410,490, 2430,480, 2450,490, 2460,510, 2460,640)
[node name="Gate2" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.30, 0.58, 0.28, 1)
polygon = PackedVector2Array(2540,640, 2540,510, 2530,490, 2510,480, 2490,490, 2480,510, 2480,640)
[node name="GateTop" type="ColorRect" parent="Buildings/TamanLogika"]
color = Color(0.22, 0.48, 0.20, 1)
position = Vector2(2400, 454)
size = Vector2(140, 34)
[node name="Bush1" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.22, 0.60, 0.25, 1)
polygon = PackedVector2Array(2330,640, 2330,590, 2360,565, 2390,590, 2390,640)
[node name="Bush2" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.18, 0.52, 0.22, 1)
polygon = PackedVector2Array(2550,640, 2550,590, 2580,565, 2610,590, 2610,640)

[node name="KebunKarakter" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/KebunKarakter"]
color = Color(0.72, 0.85, 0.62, 1)
position = Vector2(3200, 490)
size = Vector2(160, 150)
[node name="Roof" type="Polygon2D" parent="Buildings/KebunKarakter"]
color = Color(0.28, 0.55, 0.22, 1)
polygon = PackedVector2Array(3188,494, 3280,430, 3372,494)
[node name="Door" type="ColorRect" parent="Buildings/KebunKarakter"]
color = Color(0.38, 0.22, 0.08, 1)
position = Vector2(3258, 555)
size = Vector2(44, 85)
[node name="Flower1" type="Polygon2D" parent="Buildings/KebunKarakter"]
color = Color(0.95, 0.40, 0.40, 1)
polygon = PackedVector2Array(3180,640, 3180,600, 3196,580, 3212,600, 3212,640)
[node name="Flower2" type="Polygon2D" parent="Buildings/KebunKarakter"]
color = Color(0.95, 0.80, 0.20, 1)
polygon = PackedVector2Array(3360,640, 3360,600, 3376,580, 3392,600, 3392,640)

[node name="RumahMaryam" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.98, 0.92, 0.80, 1)
position = Vector2(4000, 460)
size = Vector2(180, 180)
[node name="Roof" type="Polygon2D" parent="Buildings/RumahMaryam"]
color = Color(0.75, 0.35, 0.20, 1)
polygon = PackedVector2Array(3988,464, 4090,395, 4192,464)
[node name="Door" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.42, 0.26, 0.10, 1)
position = Vector2(4068, 538)
size = Vector2(44, 102)
[node name="WindowL" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(4012, 484)
size = Vector2(38, 38)
[node name="WindowR" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(4130, 484)
size = Vector2(38, 38)
[node name="Star" type="Polygon2D" parent="Buildings/RumahMaryam"]
color = Color(1.0, 0.85, 0.10, 1)
polygon = PackedVector2Array(4090,400, 4094,412, 4106,412, 4097,420, 4100,432, 4090,424, 4080,432, 4083,420, 4074,412, 4086,412)

[node name="Ground" type="StaticBody2D" parent="."]
position = Vector2(0, 600)

[node name="GroundShape" type="CollisionShape2D" parent="Ground"]
shape = SubResource("Shape_ground")

[node name="GroundDark" type="ColorRect" parent="Ground"]
color = Color(0.18, 0.46, 0.12, 1)
size = Vector2(4800, 40)

[node name="GroundLight" type="ColorRect" parent="Ground"]
color = Color(0.24, 0.58, 0.16, 1)
size = Vector2(4800, 14)

[node name="Locations" type="Node2D" parent="."]

[node name="ZoneMasjid" type="Area2D" parent="Locations"]
position = Vector2(780, 450)
script = ExtResource("2_zone")
location_name = "Masjid An-Nur"
location_key = "masjid"

[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneMasjid"]
shape = SubResource("Shape_zone")

[node name="Label" type="Label" parent="Locations/ZoneMasjid"]
position = Vector2(-80, -90)
size = Vector2(200, 40)
text = "Masjid An-Nur"
horizontal_alignment = 1

[node name="Indicator" type="AnimatedSprite2D" parent="Locations/ZoneMasjid"]
position = Vector2(0, -100)
scale = Vector2(0.08, 0.08)
sprite_frames = SubResource("SF_indicator")

[node name="ZonePondok" type="Area2D" parent="Locations"]
position = Vector2(1675, 490)
script = ExtResource("2_zone")
location_name = "Pondok Baca"
location_key = "pondok"

[node name="Shape" type="CollisionShape2D" parent="Locations/ZonePondok"]
shape = SubResource("Shape_zone")

[node name="Label" type="Label" parent="Locations/ZonePondok"]
position = Vector2(-80, -90)
size = Vector2(200, 40)
text = "Pondok Baca"
horizontal_alignment = 1

[node name="Indicator" type="AnimatedSprite2D" parent="Locations/ZonePondok"]
position = Vector2(0, -100)
scale = Vector2(0.08, 0.08)
sprite_frames = SubResource("SF_indicator")

[node name="ZoneTaman" type="Area2D" parent="Locations"]
position = Vector2(2480, 490)
script = ExtResource("2_zone")
location_name = "Taman Logika"
location_key = "taman"

[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneTaman"]
shape = SubResource("Shape_zone")

[node name="Label" type="Label" parent="Locations/ZoneTaman"]
position = Vector2(-80, -90)
size = Vector2(200, 40)
text = "Taman Logika"
horizontal_alignment = 1

[node name="Indicator" type="AnimatedSprite2D" parent="Locations/ZoneTaman"]
position = Vector2(0, -100)
scale = Vector2(0.08, 0.08)
sprite_frames = SubResource("SF_indicator")

[node name="ZoneKebun" type="Area2D" parent="Locations"]
position = Vector2(3280, 490)
script = ExtResource("2_zone")
location_name = "Kebun Karakter"
location_key = "kebun"

[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneKebun"]
shape = SubResource("Shape_zone")

[node name="Label" type="Label" parent="Locations/ZoneKebun"]
position = Vector2(-80, -90)
size = Vector2(200, 40)
text = "Kebun Karakter"
horizontal_alignment = 1

[node name="Indicator" type="AnimatedSprite2D" parent="Locations/ZoneKebun"]
position = Vector2(0, -100)
scale = Vector2(0.08, 0.08)
sprite_frames = SubResource("SF_indicator")

[node name="ZoneRumah" type="Area2D" parent="Locations"]
position = Vector2(4090, 490)
script = ExtResource("2_zone")
location_name = "Rumah Maryam"
location_key = "rumah"

[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneRumah"]
shape = SubResource("Shape_zone")

[node name="Label" type="Label" parent="Locations/ZoneRumah"]
position = Vector2(-80, -90)
size = Vector2(200, 40)
text = "Rumah Maryam"
horizontal_alignment = 1

[node name="Indicator" type="AnimatedSprite2D" parent="Locations/ZoneRumah"]
position = Vector2(0, -100)
scale = Vector2(0.08, 0.08)
sprite_frames = SubResource("SF_indicator")

[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(200, 520)
script = ExtResource("1_player")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Player"]
scale = Vector2(0.10, 0.10)
sprite_frames = SubResource("SF_player")
animation = &"idle"
autoplay = "idle"

[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("Shape_player")

[node name="Camera2D" type="Camera2D" parent="Player"]
position_smoothing_enabled = true
position_smoothing_speed = 6.0
zoom = Vector2(1.0, 1.0)
limit_left = 0
limit_right = 4800
limit_top = 0
limit_bottom = 720
""")

# ── Patch project.godot: tambah interact input ────────────────
proj_path = os.path.join(BASE, "project.godot")
with open(proj_path, "r", encoding="utf-8") as f:
    proj = f.read()

interact_block = """interact={
"deadzone": 0.2,
"events": [Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":4194309,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
]
}"""

if "interact" not in proj:
    proj = proj.replace("jump={", interact_block + "\njump={")
    with open(proj_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(proj)
    print("  ✅  Input 'interact' (Enter) ditambahkan")
else:
    print("  ⏭️   Input interact sudah ada")

print("\n" + "=" * 52)
print("  SELESAI! Sekarang:")
print("  1. Godot → Project → Reload Current Project")
print("  2. Tekan F5")
print("  3. Jalan ke kanan — temukan 5 lokasi!")
print("  4. Mendekati bangunan → nama muncul")
print("  5. Tekan Enter untuk masuk lokasi")
print("=" * 52 + "\n")
