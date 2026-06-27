"""
Maryam Journey - Build V2
Jalankan: python build_v2.py
"""
import os

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Build V2")
print("=" * 52)

# ── scripts/world/ folder ────────────────────────────────────
os.makedirs(os.path.join(BASE, "scripts", "world"), exist_ok=True)

# ── 1. HUD.gd ────────────────────────────────────────────────
write(os.path.join(BASE, "scripts", "ui", "HUD.gd"), """\
# =============================================================
#  scripts/ui/HUD.gd
# =============================================================
extends CanvasLayer

@onready var _star_label : Label = $StarPanel/StarLabel
@onready var _name_label : Label = $NameLabel


func _ready() -> void:
\tGameManager.star_collected.connect(_on_star_collected)
\t_name_label.text = "🌙 " + GameManager.player_name
\t_star_label.text = "⭐ " + str(GameManager.total_stars)


func _on_star_collected(total: int) -> void:
\t_star_label.text = "⭐ " + str(total)
""")

# ── 2. LocationZone.gd (improved) ────────────────────────────
write(os.path.join(BASE, "scripts", "locations", "LocationZone.gd"), """\
# =============================================================
#  scripts/locations/LocationZone.gd
# =============================================================
extends Area2D

@export var location_name : String = "Lokasi"
@export var location_key  : String = "masjid"

@onready var _label_panel : Panel = $LabelPanel
@onready var _label       : Label = $LabelPanel/Label
@onready var _hint        : Label = $LabelPanel/Hint

var _player_inside : bool = false
var _bob_time      : float = 0.0


func _ready() -> void:
\t_label.text = location_name
\t_hint.text = "[Enter] Masuk"
\t_label_panel.visible = false
\tbody_entered.connect(_on_body_entered)
\tbody_exited.connect(_on_body_exited)


func _process(delta: float) -> void:
\tif _player_inside:
\t\t_bob_time += delta
\t\t_label_panel.position.y = -160.0 + sin(_bob_time * 3.0) * 5.0
\t\tif Input.is_action_just_pressed("interact"):
\t\t\t_enter_location()


func _on_body_entered(body: Node2D) -> void:
\tif body.is_in_group("player"):
\t\t_player_inside = true
\t\t_bob_time = 0.0
\t\t_label_panel.visible = true


func _on_body_exited(body: Node2D) -> void:
\tif body.is_in_group("player"):
\t\t_player_inside = false
\t\t_label_panel.visible = false


func _enter_location() -> void:
\tif not GameManager.is_location_unlocked(location_key):
\t\t_hint.text = "🔒 Terkunci"
\t\treturn
\tprint("[Zone] Masuk ke: ", location_name)
""")

# ── 3. WorldMap.tscn V2 ──────────────────────────────────────
write(os.path.join(BASE, "scenes", "world", "WorldMap.tscn"), """\
[gd_scene load_steps=13 format=3]

[ext_resource type="Script" path="res://scripts/player/Player.gd" id="1_player"]
[ext_resource type="Script" path="res://scripts/locations/LocationZone.gd" id="2_zone"]
[ext_resource type="Script" path="res://scripts/ui/HUD.gd" id="3_hud"]
[ext_resource type="Texture2D" path="res://icon.svg" id="4_icon"]

[sub_resource type="SpriteFrames" id="SF_player"]
animations = [{
"frames": [{"duration": 1.0, "texture": ExtResource("4_icon")}],
"loop": true, "name": &"idle", "speed": 5.0
}, {
"frames": [{"duration": 1.0, "texture": ExtResource("4_icon")}],
"loop": true, "name": &"walk", "speed": 8.0
}, {
"frames": [{"duration": 1.0, "texture": ExtResource("4_icon")}],
"loop": false, "name": &"jump", "speed": 5.0
}]

[sub_resource type="RectangleShape2D" id="Shape_ground"]
size = Vector2(4800, 40)

[sub_resource type="RectangleShape2D" id="Shape_player"]
size = Vector2(40, 56)

[sub_resource type="RectangleShape2D" id="Shape_zone"]
size = Vector2(160, 220)

[sub_resource type="StyleBoxFlat" id="StyleBox_panel"]
bg_color = Color(0.10, 0.08, 0.20, 0.88)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(1.0, 0.85, 0.20, 1.0)
corner_radius_top_left = 10
corner_radius_top_right = 10
corner_radius_bottom_right = 10
corner_radius_bottom_left = 10

[sub_resource type="StyleBoxFlat" id="StyleBox_hud"]
bg_color = Color(0.05, 0.05, 0.15, 0.80)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0.8, 0.7, 0.2, 0.9)
corner_radius_top_left = 8
corner_radius_top_right = 8
corner_radius_bottom_right = 8
corner_radius_bottom_left = 8

[sub_resource type="GDScript" id="CloudScript"]
script/source = "extends Node2D
@export var speed : float = 22.0
func _process(delta):
\tposition.x += speed * delta
\tif position.x > 5200.0:
\t\tposition.x = -300.0
"

[node name="WorldMap" type="Node2D"]

[node name="Sky" type="ColorRect" parent="."]
color = Color(0.45, 0.75, 0.95, 1)
size = Vector2(4800, 720)

[node name="Cloud1" type="Node2D" parent="."]
position = Vector2(120, 55)
script = SubResource("CloudScript")
[node name="Shape" type="Polygon2D" parent="Cloud1"]
color = Color(1, 1, 1, 0.92)
polygon = PackedVector2Array(0,26, 16,6, 42,0, 74,4, 98,0, 118,6, 128,26)

[node name="Cloud2" type="Node2D" parent="."]
position = Vector2(500, 36)
script = SubResource("CloudScript")
[node name="Shape" type="Polygon2D" parent="Cloud2"]
color = Color(1, 1, 1, 0.86)
polygon = PackedVector2Array(0,22, 14,4, 36,0, 62,3, 82,0, 96,4, 102,22)

[node name="Cloud3" type="Node2D" parent="."]
position = Vector2(950, 68)
script = SubResource("CloudScript")
[node name="Shape" type="Polygon2D" parent="Cloud3"]
color = Color(1, 1, 1, 0.89)
polygon = PackedVector2Array(0,20, 12,3, 30,0, 54,4, 72,0, 84,3, 90,20)

[node name="Cloud4" type="Node2D" parent="."]
position = Vector2(1500, 44)
script = SubResource("CloudScript")
[node name="Shape" type="Polygon2D" parent="Cloud4"]
color = Color(1, 1, 1, 0.83)
polygon = PackedVector2Array(0,18, 10,2, 28,0, 48,3, 64,0, 74,2, 80,18)

[node name="Cloud5" type="Node2D" parent="."]
position = Vector2(2100, 60)
script = SubResource("CloudScript")
[node name="Shape" type="Polygon2D" parent="Cloud5"]
color = Color(1, 1, 1, 0.88)
polygon = PackedVector2Array(0,24, 14,5, 38,0, 66,4, 88,0, 104,5, 112,24)

[node name="Cloud6" type="Node2D" parent="."]
position = Vector2(2900, 42)
script = SubResource("CloudScript")
[node name="Shape" type="Polygon2D" parent="Cloud6"]
color = Color(1, 1, 1, 0.84)
polygon = PackedVector2Array(0,20, 12,3, 32,0, 56,4, 74,0, 86,3, 92,20)

[node name="Cloud7" type="Node2D" parent="."]
position = Vector2(3700, 70)
script = SubResource("CloudScript")
[node name="Shape" type="Polygon2D" parent="Cloud7"]
color = Color(1, 1, 1, 0.87)
polygon = PackedVector2Array(0,22, 13,4, 34,0, 60,3, 80,0, 92,4, 98,22)

[node name="MountainFar" type="Polygon2D" parent="."]
color = Color(0.55, 0.72, 0.60, 0.50)
polygon = PackedVector2Array(0,570, 200,390, 500,440, 800,370, 1100,420, 1400,360, 1700,410, 2000,375, 2300,415, 2600,380, 2900,420, 3200,365, 3500,405, 3800,380, 4100,420, 4400,390, 4800,440, 4800,570)

[node name="MountainNear" type="Polygon2D" parent="."]
color = Color(0.32, 0.58, 0.30, 1)
polygon = PackedVector2Array(0,590, 150,500, 350,535, 600,470, 850,515, 1100,475, 1400,510, 1700,468, 2000,505, 2300,472, 2600,508, 2900,465, 3200,502, 3500,470, 3800,508, 4100,472, 4400,500, 4800,480, 4800,590)

[node name="Trees" type="Node2D" parent="."]

[node name="T1" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T1"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(52, 530)
size = Vector2(18, 70)
[node name="Top2" type="Polygon2D" parent="Trees/T1"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(61,458, 20,538, 102,538)
[node name="Top1" type="Polygon2D" parent="Trees/T1"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(61,480, 16,552, 106,552)

[node name="T2" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T2"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(185, 534)
size = Vector2(16, 66)
[node name="Top2" type="Polygon2D" parent="Trees/T2"]
color = Color(0.17, 0.50, 0.20, 1)
polygon = PackedVector2Array(193,462, 157,542, 229,542)
[node name="Top1" type="Polygon2D" parent="Trees/T2"]
color = Color(0.22, 0.62, 0.26, 1)
polygon = PackedVector2Array(193,484, 153,558, 233,558)

[node name="T3" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T3"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(1250, 530)
size = Vector2(18, 70)
[node name="Top2" type="Polygon2D" parent="Trees/T3"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(1259,458, 1218,538, 1300,538)
[node name="Top1" type="Polygon2D" parent="Trees/T3"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(1259,480, 1214,552, 1304,552)

[node name="T4" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T4"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(1420, 534)
size = Vector2(16, 66)
[node name="Top2" type="Polygon2D" parent="Trees/T4"]
color = Color(0.17, 0.50, 0.20, 1)
polygon = PackedVector2Array(1428,462, 1392,542, 1464,542)
[node name="Top1" type="Polygon2D" parent="Trees/T4"]
color = Color(0.22, 0.62, 0.26, 1)
polygon = PackedVector2Array(1428,484, 1388,558, 1468,558)

[node name="T5" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T5"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(2600, 530)
size = Vector2(18, 70)
[node name="Top2" type="Polygon2D" parent="Trees/T5"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(2609,458, 2568,538, 2650,538)
[node name="Top1" type="Polygon2D" parent="Trees/T5"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(2609,480, 2564,552, 2654,552)

[node name="T6" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T6"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(3380, 532)
size = Vector2(16, 68)
[node name="Top2" type="Polygon2D" parent="Trees/T6"]
color = Color(0.17, 0.50, 0.20, 1)
polygon = PackedVector2Array(3388,462, 3352,542, 3424,542)
[node name="Top1" type="Polygon2D" parent="Trees/T6"]
color = Color(0.22, 0.62, 0.26, 1)
polygon = PackedVector2Array(3388,484, 3348,558, 3428,558)

[node name="T7" type="Node2D" parent="Trees"]
[node name="Trunk" type="ColorRect" parent="Trees/T7"]
color = Color(0.40, 0.25, 0.10, 1)
position = Vector2(4250, 530)
size = Vector2(18, 70)
[node name="Top2" type="Polygon2D" parent="Trees/T7"]
color = Color(0.15, 0.48, 0.18, 1)
polygon = PackedVector2Array(4259,458, 4218,538, 4300,538)
[node name="Top1" type="Polygon2D" parent="Trees/T7"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(4259,480, 4214,552, 4304,552)

[node name="Buildings" type="Node2D" parent="."]

[node name="House1" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/House1"]
color = Color(0.82, 0.72, 0.55, 1)
position = Vector2(300, 460)
size = Vector2(120, 140)
[node name="Roof" type="Polygon2D" parent="Buildings/House1"]
color = Color(0.62, 0.30, 0.18, 1)
polygon = PackedVector2Array(288,464, 360,405, 432,464)
[node name="Door" type="ColorRect" parent="Buildings/House1"]
color = Color(0.45, 0.28, 0.12, 1)
position = Vector2(342, 520)
size = Vector2(36, 80)
[node name="Window" type="ColorRect" parent="Buildings/House1"]
color = Color(0.55, 0.78, 0.92, 1)
position = Vector2(308, 478)
size = Vector2(28, 28)

[node name="House2" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/House2"]
color = Color(0.76, 0.65, 0.50, 1)
position = Vector2(510, 472)
size = Vector2(100, 128)
[node name="Roof" type="Polygon2D" parent="Buildings/House2"]
color = Color(0.55, 0.27, 0.16, 1)
polygon = PackedVector2Array(498,476, 560,420, 622,476)
[node name="Door" type="ColorRect" parent="Buildings/House2"]
color = Color(0.42, 0.26, 0.10, 1)
position = Vector2(542, 530)
size = Vector2(32, 70)

[node name="Masjid" type="Node2D" parent="Buildings"]
[node name="Body" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.96, 0.95, 0.88, 1)
position = Vector2(700, 400)
size = Vector2(180, 200)
[node name="Dome" type="Polygon2D" parent="Buildings/Masjid"]
color = Color(0.18, 0.62, 0.32, 1)
polygon = PackedVector2Array(700,404, 724,362, 760,342, 790,336, 820,342, 856,362, 880,404)
[node name="DomeLine" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.14, 0.50, 0.26, 1)
position = Vector2(784, 308)
size = Vector2(12, 32)
[node name="DomeStar" type="Polygon2D" parent="Buildings/Masjid"]
color = Color(1.0, 0.88, 0.10, 1)
polygon = PackedVector2Array(790,308, 793,318, 803,318, 795,325, 798,335, 790,329, 782,335, 785,325, 777,318, 787,318)
[node name="Door" type="Polygon2D" parent="Buildings/Masjid"]
color = Color(0.32, 0.20, 0.06, 1)
polygon = PackedVector2Array(762,600, 762,490, 772,468, 790,462, 808,468, 818,490, 818,600)
[node name="WindowL" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(712, 430)
size = Vector2(32, 52)
[node name="WindowR" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(836, 430)
size = Vector2(32, 52)
[node name="Minaret" type="ColorRect" parent="Buildings/Masjid"]
color = Color(0.94, 0.93, 0.86, 1)
position = Vector2(888, 390)
size = Vector2(32, 210)
[node name="MinaretTop" type="Polygon2D" parent="Buildings/Masjid"]
color = Color(0.18, 0.62, 0.32, 1)
polygon = PackedVector2Array(888,394, 904,362, 920,394)

[node name="PondokBaca" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.90, 0.78, 0.58, 1)
position = Vector2(1580, 448)
size = Vector2(170, 152)
[node name="Roof" type="Polygon2D" parent="Buildings/PondokBaca"]
color = Color(0.48, 0.22, 0.10, 1)
polygon = PackedVector2Array(1566,452, 1665,385, 1764,452)
[node name="SignBg" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.30, 0.18, 0.06, 1)
position = Vector2(1612, 456)
size = Vector2(82, 22)
[node name="Door" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.38, 0.22, 0.08, 1)
position = Vector2(1646, 520)
size = Vector2(40, 80)
[node name="WindowL" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(1590, 466)
size = Vector2(36, 36)
[node name="WindowR" type="ColorRect" parent="Buildings/PondokBaca"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(1698, 466)
size = Vector2(36, 36)

[node name="TamanLogika" type="Node2D" parent="Buildings"]
[node name="GateL" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.28, 0.55, 0.25, 1)
polygon = PackedVector2Array(2380,600, 2380,490, 2392,468, 2412,458, 2432,468, 2444,490, 2444,600)
[node name="GateR" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.28, 0.55, 0.25, 1)
polygon = PackedVector2Array(2556,600, 2556,490, 2544,468, 2524,458, 2504,468, 2492,490, 2492,600)
[node name="GateTop" type="ColorRect" parent="Buildings/TamanLogika"]
color = Color(0.22, 0.46, 0.20, 1)
position = Vector2(2380, 432)
size = Vector2(176, 32)
[node name="GateStar" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(1.0, 0.88, 0.10, 1)
polygon = PackedVector2Array(2468,432, 2471,442, 2481,442, 2473,449, 2476,459, 2468,453, 2460,459, 2463,449, 2455,442, 2465,442)
[node name="Bush1" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.20, 0.58, 0.22, 1)
polygon = PackedVector2Array(2310,600, 2310,550, 2348,524, 2386,550, 2386,600)
[node name="Bush2" type="Polygon2D" parent="Buildings/TamanLogika"]
color = Color(0.16, 0.50, 0.18, 1)
polygon = PackedVector2Array(2556,600, 2556,550, 2594,524, 2632,550, 2632,600)

[node name="KebunKarakter" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/KebunKarakter"]
color = Color(0.74, 0.88, 0.64, 1)
position = Vector2(3180, 452)
size = Vector2(180, 148)
[node name="Roof" type="Polygon2D" parent="Buildings/KebunKarakter"]
color = Color(0.26, 0.52, 0.20, 1)
polygon = PackedVector2Array(3166,456, 3270,390, 3374,456)
[node name="Door" type="ColorRect" parent="Buildings/KebunKarakter"]
color = Color(0.36, 0.20, 0.07, 1)
position = Vector2(3248, 520)
size = Vector2(44, 80)
[node name="WindowL" type="ColorRect" parent="Buildings/KebunKarakter"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(3192, 466)
size = Vector2(36, 36)
[node name="WindowR" type="ColorRect" parent="Buildings/KebunKarakter"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(3308, 466)
size = Vector2(36, 36)
[node name="Flower1" type="Polygon2D" parent="Buildings/KebunKarakter"]
color = Color(0.95, 0.38, 0.38, 1)
polygon = PackedVector2Array(3162,600, 3162,555, 3180,534, 3198,555, 3198,600)
[node name="Flower2" type="Polygon2D" parent="Buildings/KebunKarakter"]
color = Color(0.95, 0.80, 0.18, 1)
polygon = PackedVector2Array(3360,600, 3360,555, 3378,534, 3396,555, 3396,600)

[node name="RumahMaryam" type="Node2D" parent="Buildings"]
[node name="Wall" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.99, 0.94, 0.82, 1)
position = Vector2(3980, 420)
size = Vector2(210, 180)
[node name="Roof" type="Polygon2D" parent="Buildings/RumahMaryam"]
color = Color(0.72, 0.32, 0.18, 1)
polygon = PackedVector2Array(3966,424, 4085,350, 4204,424)
[node name="Door" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.40, 0.24, 0.08, 1)
position = Vector2(4058, 500)
size = Vector2(48, 100)
[node name="WindowL" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(3992, 440)
size = Vector2(42, 42)
[node name="WindowR" type="ColorRect" parent="Buildings/RumahMaryam"]
color = Color(0.55, 0.80, 0.95, 1)
position = Vector2(4130, 440)
size = Vector2(42, 42)
[node name="Star" type="Polygon2D" parent="Buildings/RumahMaryam"]
color = Color(1.0, 0.88, 0.10, 1)
polygon = PackedVector2Array(4085,348, 4090,364, 4106,364, 4093,374, 4098,390, 4085,380, 4072,390, 4077,374, 4064,364, 4080,364)

[node name="Ground" type="StaticBody2D" parent="."]
position = Vector2(0, 600)

[node name="GroundShape" type="CollisionShape2D" parent="Ground"]
shape = SubResource("Shape_ground")

[node name="GroundTop" type="ColorRect" parent="Ground"]
color = Color(0.24, 0.60, 0.16, 1)
size = Vector2(4800, 18)

[node name="GroundBody" type="ColorRect" parent="Ground"]
color = Color(0.18, 0.46, 0.12, 1)
position = Vector2(0, 18)
size = Vector2(4800, 22)

[node name="Locations" type="Node2D" parent="."]

[node name="ZoneMasjid" type="Area2D" parent="Locations"]
position = Vector2(790, 500)
script = ExtResource("2_zone")
location_name = "Masjid An-Nur"
location_key = "masjid"
[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneMasjid"]
shape = SubResource("Shape_zone")
[node name="LabelPanel" type="Panel" parent="Locations/ZoneMasjid"]
position = Vector2(-100, -160)
size = Vector2(200, 56)
visible = false
theme_override_styles/panel = SubResource("StyleBox_panel")
[node name="Label" type="Label" parent="Locations/ZoneMasjid/LabelPanel"]
position = Vector2(0, 4)
size = Vector2(200, 28)
text = "Masjid An-Nur"
horizontal_alignment = 1
[node name="Hint" type="Label" parent="Locations/ZoneMasjid/LabelPanel"]
position = Vector2(0, 30)
size = Vector2(200, 22)
text = "[Enter] Masuk"
horizontal_alignment = 1

[node name="ZonePondok" type="Area2D" parent="Locations"]
position = Vector2(1665, 500)
script = ExtResource("2_zone")
location_name = "Pondok Baca"
location_key = "pondok"
[node name="Shape" type="CollisionShape2D" parent="Locations/ZonePondok"]
shape = SubResource("Shape_zone")
[node name="LabelPanel" type="Panel" parent="Locations/ZonePondok"]
position = Vector2(-100, -160)
size = Vector2(200, 56)
visible = false
theme_override_styles/panel = SubResource("StyleBox_panel")
[node name="Label" type="Label" parent="Locations/ZonePondok/LabelPanel"]
position = Vector2(0, 4)
size = Vector2(200, 28)
text = "Pondok Baca"
horizontal_alignment = 1
[node name="Hint" type="Label" parent="Locations/ZonePondok/LabelPanel"]
position = Vector2(0, 30)
size = Vector2(200, 22)
text = "[Enter] Masuk"
horizontal_alignment = 1

[node name="ZoneTaman" type="Area2D" parent="Locations"]
position = Vector2(2468, 500)
script = ExtResource("2_zone")
location_name = "Taman Logika"
location_key = "taman"
[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneTaman"]
shape = SubResource("Shape_zone")
[node name="LabelPanel" type="Panel" parent="Locations/ZoneTaman"]
position = Vector2(-100, -160)
size = Vector2(200, 56)
visible = false
theme_override_styles/panel = SubResource("StyleBox_panel")
[node name="Label" type="Label" parent="Locations/ZoneTaman/LabelPanel"]
position = Vector2(0, 4)
size = Vector2(200, 28)
text = "Taman Logika"
horizontal_alignment = 1
[node name="Hint" type="Label" parent="Locations/ZoneTaman/LabelPanel"]
position = Vector2(0, 30)
size = Vector2(200, 22)
text = "[Enter] Masuk"
horizontal_alignment = 1

[node name="ZoneKebun" type="Area2D" parent="Locations"]
position = Vector2(3270, 500)
script = ExtResource("2_zone")
location_name = "Kebun Karakter"
location_key = "kebun"
[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneKebun"]
shape = SubResource("Shape_zone")
[node name="LabelPanel" type="Panel" parent="Locations/ZoneKebun"]
position = Vector2(-100, -160)
size = Vector2(200, 56)
visible = false
theme_override_styles/panel = SubResource("StyleBox_panel")
[node name="Label" type="Label" parent="Locations/ZoneKebun/LabelPanel"]
position = Vector2(0, 4)
size = Vector2(200, 28)
text = "Kebun Karakter"
horizontal_alignment = 1
[node name="Hint" type="Label" parent="Locations/ZoneKebun/LabelPanel"]
position = Vector2(0, 30)
size = Vector2(200, 22)
text = "[Enter] Masuk"
horizontal_alignment = 1

[node name="ZoneRumah" type="Area2D" parent="Locations"]
position = Vector2(4085, 500)
script = ExtResource("2_zone")
location_name = "Rumah Maryam"
location_key = "rumah"
[node name="Shape" type="CollisionShape2D" parent="Locations/ZoneRumah"]
shape = SubResource("Shape_zone")
[node name="LabelPanel" type="Panel" parent="Locations/ZoneRumah"]
position = Vector2(-100, -160)
size = Vector2(200, 56)
visible = false
theme_override_styles/panel = SubResource("StyleBox_panel")
[node name="Label" type="Label" parent="Locations/ZoneRumah/LabelPanel"]
position = Vector2(0, 4)
size = Vector2(200, 28)
text = "Rumah Maryam"
horizontal_alignment = 1
[node name="Hint" type="Label" parent="Locations/ZoneRumah/LabelPanel"]
position = Vector2(0, 30)
size = Vector2(200, 22)
text = "[Enter] Masuk"
horizontal_alignment = 1

[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(200, 510)
script = ExtResource("1_player")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Player"]
scale = Vector2(0.18, 0.18)
sprite_frames = SubResource("SF_player")
animation = &"idle"
autoplay = "idle"

[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("Shape_player")

[node name="Camera2D" type="Camera2D" parent="Player"]
position_smoothing_enabled = true
position_smoothing_speed = 5.0
zoom = Vector2(1.0, 1.0)
limit_left = 0
limit_right = 4800
limit_top = 0
limit_bottom = 720

[node name="HUD" type="CanvasLayer" parent="."]
script = ExtResource("3_hud")

[node name="NameLabel" type="Label" parent="HUD"]
position = Vector2(16, 12)
size = Vector2(200, 32)
text = "🌙 Maryam"

[node name="StarPanel" type="Panel" parent="HUD"]
position = Vector2(16, 48)
size = Vector2(120, 36)
theme_override_styles/panel = SubResource("StyleBox_hud")

[node name="StarLabel" type="Label" parent="HUD/StarPanel"]
position = Vector2(8, 6)
size = Vector2(104, 24)
text = "⭐ 0"
""")

print("\n" + "=" * 52)
print("  SELESAI! Sekarang:")
print("  1. Godot → Project → Reload Current Project")
print("  2. Tekan F5")
print("  3. Jalan ke kanan — temukan 5 lokasi!")
print("  4. Dekati bangunan → panel nama muncul + bobbing")
print("  5. Tekan Enter untuk masuk")
print("=" * 52 + "\n")
