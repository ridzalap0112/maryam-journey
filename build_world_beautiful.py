"""
Maryam Journey - Beautiful World
Jalankan di PowerShell di folder maryam-journey:
  python build_world_beautiful.py
"""
import os

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Beautiful World")
print("=" * 48)

# ── WorldBackground.gd ───────────────────────────────────────
write(os.path.join(BASE, "scripts", "world", "WorldBackground.gd"), """\
# =============================================================
#  scripts/world/WorldBackground.gd
#  Menggerakkan awan secara otomatis
# =============================================================
extends Node2D

const CLOUD_SPEED : float = 18.0
const WORLD_WIDTH : float = 1280.0

@onready var _clouds : Array = []


func _ready() -> void:
\tfor child in get_children():
\t\tif child.name.begins_with("Cloud"):
\t\t\t_clouds.append(child)


func _process(delta: float) -> void:
\tfor cloud in _clouds:
\t\tcloud.position.x += CLOUD_SPEED * delta
\t\tif cloud.position.x > WORLD_WIDTH + 200.0:
\t\t\tcloud.position.x = -200.0
""")

# ── WorldMap.tscn (beautiful version) ────────────────────────
write(os.path.join(BASE, "scenes", "world", "WorldMap.tscn"), """\
[gd_scene load_steps=8 format=3]

[ext_resource type="Script" path="res://scripts/player/Player.gd" id="1_player"]
[ext_resource type="Script" path="res://scripts/world/WorldBackground.gd" id="2_bg"]
[ext_resource type="Texture2D" path="res://icon.svg" id="3_icon"]

[sub_resource type="SpriteFrames" id="SpriteFrames_1"]
animations = [{
"frames": [{
"duration": 1.0,
"texture": ExtResource("3_icon")
}],
"loop": true,
"name": &"idle",
"speed": 5.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("3_icon")
}],
"loop": true,
"name": &"walk",
"speed": 8.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("3_icon")
}],
"loop": false,
"name": &"jump",
"speed": 5.0
}]

[sub_resource type="RectangleShape2D" id="Shape_ground"]
size = Vector2(1280, 40)

[sub_resource type="RectangleShape2D" id="Shape_player"]
size = Vector2(40, 40)

[sub_resource type="GDScript" id="CloudMover"]
script/source = "extends Node2D
const SPEED = 18.0
const RESET_X = -220.0
const MAX_X = 1500.0
func _process(delta):
\tposition.x += SPEED * delta
\tif position.x > MAX_X:
\t\tposition.x = RESET_X
"

[node name="WorldMap" type="Node2D"]

[node name="Sky" type="ColorRect" parent="."]
color = Color(0.45, 0.75, 0.95, 1)
size = Vector2(1280, 720)

[node name="SkyBottom" type="ColorRect" parent="."]
color = Color(0.62, 0.87, 0.98, 1)
position = Vector2(0, 480)
size = Vector2(1280, 240)

[node name="MountainFar" type="Polygon2D" parent="."]
color = Color(0.55, 0.72, 0.60, 0.6)
polygon = PackedVector2Array(0,520, 160,380, 320,430, 480,360, 640,410, 800,350, 960,400, 1120,370, 1280,430, 1280,540, 0,540)

[node name="MountainNear" type="Polygon2D" parent="."]
color = Color(0.38, 0.60, 0.35, 1)
polygon = PackedVector2Array(0,560, 120,460, 260,500, 400,440, 560,490, 720,450, 880,480, 1040,445, 1200,470, 1280,455, 1280,580, 0,580)

[node name="Clouds" type="Node2D" parent="."]

[node name="Cloud1" type="Node2D" parent="Clouds"]
position = Vector2(100, 80)
script = SubResource("CloudMover")

[node name="CloudBody1" type="Polygon2D" parent="Clouds/Cloud1"]
color = Color(1, 1, 1, 0.92)
polygon = PackedVector2Array(0,20, 10,5, 30,0, 55,3, 75,0, 95,5, 100,20, 0,20)

[node name="Cloud2" type="Node2D" parent="Clouds"]
position = Vector2(400, 50)
script = SubResource("CloudMover")

[node name="CloudBody2" type="Polygon2D" parent="Clouds/Cloud2"]
color = Color(1, 1, 1, 0.85)
polygon = PackedVector2Array(0,16, 8,4, 25,0, 45,2, 62,0, 72,4, 76,16, 0,16)

[node name="Cloud3" type="Node2D" parent="Clouds"]
position = Vector2(750, 100)
script = SubResource("CloudMover")

[node name="CloudBody3" type="Polygon2D" parent="Clouds/Cloud3"]
color = Color(1, 1, 1, 0.88)
polygon = PackedVector2Array(0,18, 12,3, 35,0, 58,4, 80,0, 92,3, 96,18, 0,18)

[node name="Cloud4" type="Node2D" parent="Clouds"]
position = Vector2(-150, 130)
script = SubResource("CloudMover")

[node name="CloudBody4" type="Polygon2D" parent="Clouds/Cloud4"]
color = Color(1, 1, 1, 0.80)
polygon = PackedVector2Array(0,14, 8,2, 24,0, 40,3, 52,0, 60,2, 64,14, 0,14)

[node name="Trees" type="Node2D" parent="."]

[node name="TreeTrunk1" type="ColorRect" parent="Trees"]
color = Color(0.45, 0.30, 0.15, 1)
position = Vector2(80, 560)
size = Vector2(14, 80)

[node name="TreeTop1" type="Polygon2D" parent="Trees"]
color = Color(0.18, 0.55, 0.22, 1)
polygon = PackedVector2Array(87,480, 60,560, 114,560)

[node name="TreeTop1b" type="Polygon2D" parent="Trees"]
color = Color(0.22, 0.62, 0.26, 1)
polygon = PackedVector2Array(87,500, 55,575, 119,575)

[node name="TreeTrunk2" type="ColorRect" parent="Trees"]
color = Color(0.45, 0.30, 0.15, 1)
position = Vector2(200, 555)
size = Vector2(14, 85)

[node name="TreeTop2" type="Polygon2D" parent="Trees"]
color = Color(0.20, 0.58, 0.24, 1)
polygon = PackedVector2Array(207,470, 178,558, 236,558)

[node name="TreeTop2b" type="Polygon2D" parent="Trees"]
color = Color(0.15, 0.50, 0.20, 1)
polygon = PackedVector2Array(207,495, 172,572, 242,572)

[node name="TreeTrunk3" type="ColorRect" parent="Trees"]
color = Color(0.45, 0.30, 0.15, 1)
position = Vector2(900, 558)
size = Vector2(14, 82)

[node name="TreeTop3" type="Polygon2D" parent="Trees"]
color = Color(0.18, 0.56, 0.22, 1)
polygon = PackedVector2Array(907,476, 878,560, 936,560)

[node name="TreeTop3b" type="Polygon2D" parent="Trees"]
color = Color(0.22, 0.63, 0.28, 1)
polygon = PackedVector2Array(907,498, 874,574, 940,574)

[node name="TreeTrunk4" type="ColorRect" parent="Trees"]
color = Color(0.45, 0.30, 0.15, 1)
position = Vector2(1050, 553)
size = Vector2(14, 87)

[node name="TreeTop4" type="Polygon2D" parent="Trees"]
color = Color(0.17, 0.54, 0.21, 1)
polygon = PackedVector2Array(1057,466, 1026,555, 1088,555)

[node name="TreeTop4b" type="Polygon2D" parent="Trees"]
color = Color(0.21, 0.61, 0.26, 1)
polygon = PackedVector2Array(1057,490, 1022,570, 1092,570)

[node name="HouseBack" type="Polygon2D" parent="."]
color = Color(0.75, 0.65, 0.50, 0.7)
polygon = PackedVector2Array(550,580, 550,510, 600,475, 650,510, 650,580)

[node name="HouseRoof" type="Polygon2D" parent="."]
color = Color(0.60, 0.30, 0.20, 0.75)
polygon = PackedVector2Array(540,515, 600,468, 660,515)

[node name="HouseBack2" type="Polygon2D" parent="."]
color = Color(0.78, 0.68, 0.52, 0.65)
polygon = PackedVector2Array(680,580, 680,520, 724,488, 768,520, 768,580)

[node name="HouseRoof2" type="Polygon2D" parent="."]
color = Color(0.55, 0.28, 0.18, 0.7)
polygon = PackedVector2Array(672,524, 724,482, 776,524)

[node name="Ground" type="StaticBody2D" parent="."]
position = Vector2(0, 640)

[node name="GroundShape" type="CollisionShape2D" parent="Ground"]
shape = SubResource("Shape_ground")

[node name="GroundVisual" type="ColorRect" parent="Ground"]
color = Color(0.25, 0.58, 0.18, 1)
size = Vector2(1280, 40)

[node name="GroundStripe" type="ColorRect" parent="Ground"]
color = Color(0.20, 0.50, 0.14, 1)
size = Vector2(1280, 8)

[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(300, 560)
script = ExtResource("1_player")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Player"]
scale = Vector2(0.12, 0.12)
sprite_frames = SubResource("SpriteFrames_1")
animation = &"idle"
autoplay = "idle"

[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("Shape_player")

[node name="Camera2D" type="Camera2D" parent="Player"]
zoom = Vector2(1.1, 1.1)
limit_left = 0
limit_right = 1280
limit_top = 0
limit_bottom = 720
""")

print("\n" + "=" * 48)
print("  SELESAI! Sekarang:")
print("  1. Kembali ke Godot")
print("  2. Project > Reload Current Project")
print("  3. Tekan F5")
print("  Dunia kampung yang indah akan muncul!")
print("=" * 48 + "\n")
