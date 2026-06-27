"""
Maryam Journey - Fix World Layout
python fix_world.py
"""
import os

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Fix World Layout")
print("=" * 48)

write(os.path.join(BASE, "scenes", "world", "WorldMap.tscn"), """\
[gd_scene load_steps=7 format=3]

[ext_resource type="Script" path="res://scripts/player/Player.gd" id="1_player"]
[ext_resource type="Texture2D" path="res://icon.svg" id="2_icon"]

[sub_resource type="SpriteFrames" id="SpriteFrames_1"]
animations = [{
"frames": [{"duration": 1.0, "texture": ExtResource("2_icon")}],
"loop": true,
"name": &"idle",
"speed": 5.0
}, {
"frames": [{"duration": 1.0, "texture": ExtResource("2_icon")}],
"loop": true,
"name": &"walk",
"speed": 8.0
}, {
"frames": [{"duration": 1.0, "texture": ExtResource("2_icon")}],
"loop": false,
"name": &"jump",
"speed": 5.0
}]

[sub_resource type="RectangleShape2D" id="Shape_ground"]
size = Vector2(1280, 40)

[sub_resource type="RectangleShape2D" id="Shape_player"]
size = Vector2(36, 36)

[sub_resource type="GDScript" id="CloudScript"]
script/source = "extends Node2D
func _process(delta):
\tposition.x += 20.0 * delta
\tif position.x > 1500.0:
\t\tposition.x = -200.0
"

[node name="WorldMap" type="Node2D"]

[node name="Sky" type="ColorRect" parent="."]
color = Color(0.45, 0.75, 0.95, 1)
size = Vector2(1280, 720)

[node name="SkyGlow" type="ColorRect" parent="."]
color = Color(0.62, 0.87, 0.98, 0.5)
position = Vector2(0, 400)
size = Vector2(1280, 260)

[node name="Cloud1" type="Node2D" parent="."]
position = Vector2(80, 60)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud1"]
color = Color(1, 1, 1, 0.90)
polygon = PackedVector2Array(0,24, 14,6, 38,0, 68,4, 90,0, 110,6, 120,24)

[node name="Cloud2" type="Node2D" parent="."]
position = Vector2(380, 38)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud2"]
color = Color(1, 1, 1, 0.85)
polygon = PackedVector2Array(0,20, 12,4, 32,0, 56,3, 74,0, 86,4, 92,20)

[node name="Cloud3" type="Node2D" parent="."]
position = Vector2(700, 75)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud3"]
color = Color(1, 1, 1, 0.88)
polygon = PackedVector2Array(0,18, 10,3, 28,0, 50,4, 68,0, 80,3, 86,18)

[node name="Cloud4" type="Node2D" parent="."]
position = Vector2(1000, 50)
script = SubResource("CloudScript")

[node name="Shape" type="Polygon2D" parent="Cloud4"]
color = Color(1, 1, 1, 0.82)
polygon = PackedVector2Array(0,16, 9,2, 26,0, 44,3, 60,0, 70,2, 76,16)

[node name="MountainFar" type="Polygon2D" parent="."]
color = Color(0.55, 0.72, 0.60, 0.55)
polygon = PackedVector2Array(0,560, 140,400, 300,450, 460,380, 620,420, 780,370, 940,415, 1100,385, 1280,440, 1280,560)

[node name="MountainNear" type="Polygon2D" parent="."]
color = Color(0.32, 0.58, 0.30, 1)
polygon = PackedVector2Array(0,580, 100,490, 240,530, 400,465, 560,510, 720,470, 880,500, 1040,460, 1180,490, 1280,470, 1280,580)

[node name="House1" type="Node2D" parent="."]
position = Vector2(420, 0)

[node name="Wall" type="ColorRect" parent="House1"]
color = Color(0.82, 0.72, 0.55, 1)
position = Vector2(0, 490)
size = Vector2(110, 110)

[node name="Roof" type="Polygon2D" parent="House1"]
color = Color(0.62, 0.30, 0.18, 1)
polygon = PackedVector2Array(-10,494, 55,438, 120,494)

[node name="Door" type="ColorRect" parent="House1"]
color = Color(0.45, 0.28, 0.12, 1)
position = Vector2(38, 540)
size = Vector2(34, 60)

[node name="Window" type="ColorRect" parent="House1"]
color = Color(0.55, 0.78, 0.92, 1)
position = Vector2(72, 505)
size = Vector2(28, 28)

[node name="House2" type="Node2D" parent="."]
position = Vector2(620, 0)

[node name="Wall" type="ColorRect" parent="House2"]
color = Color(0.78, 0.68, 0.52, 1)
position = Vector2(0, 500)
size = Vector2(95, 100)

[node name="Roof" type="Polygon2D" parent="House2"]
color = Color(0.55, 0.27, 0.16, 1)
polygon = PackedVector2Array(-8,504, 47,452, 103,504)

[node name="Door" type="ColorRect" parent="House2"]
color = Color(0.42, 0.26, 0.10, 1)
position = Vector2(30, 548)
size = Vector2(30, 52)

[node name="Tree1" type="Node2D" parent="."]

[node name="Trunk" type="ColorRect" parent="Tree1"]
color = Color(0.42, 0.27, 0.12, 1)
position = Vector2(84, 560)
size = Vector2(16, 80)

[node name="Top2" type="Polygon2D" parent="Tree1"]
color = Color(0.16, 0.50, 0.20, 1)
polygon = PackedVector2Array(92,490, 58,575, 126,575)

[node name="Top1" type="Polygon2D" parent="Tree1"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(92,510, 54,590, 130,590)

[node name="Tree2" type="Node2D" parent="."]

[node name="Trunk" type="ColorRect" parent="Tree2"]
color = Color(0.42, 0.27, 0.12, 1)
position = Vector2(210, 555)
size = Vector2(16, 85)

[node name="Top2" type="Polygon2D" parent="Tree2"]
color = Color(0.18, 0.52, 0.22, 1)
polygon = PackedVector2Array(218,482, 182,570, 254,570)

[node name="Top1" type="Polygon2D" parent="Tree2"]
color = Color(0.22, 0.62, 0.27, 1)
polygon = PackedVector2Array(218,504, 178,585, 258,585)

[node name="Tree3" type="Node2D" parent="."]

[node name="Trunk" type="ColorRect" parent="Tree3"]
color = Color(0.42, 0.27, 0.12, 1)
position = Vector2(890, 558)
size = Vector2(16, 82)

[node name="Top2" type="Polygon2D" parent="Tree3"]
color = Color(0.16, 0.50, 0.20, 1)
polygon = PackedVector2Array(898,486, 862,573, 934,573)

[node name="Top1" type="Polygon2D" parent="Tree3"]
color = Color(0.20, 0.60, 0.24, 1)
polygon = PackedVector2Array(898,508, 858,588, 938,588)

[node name="Tree4" type="Node2D" parent="."]

[node name="Trunk" type="ColorRect" parent="Tree4"]
color = Color(0.42, 0.27, 0.12, 1)
position = Vector2(1060, 553)
size = Vector2(16, 87)

[node name="Top2" type="Polygon2D" parent="Tree4"]
color = Color(0.18, 0.52, 0.22, 1)
polygon = PackedVector2Array(1068,480, 1030,568, 1106,568)

[node name="Top1" type="Polygon2D" parent="Tree4"]
color = Color(0.22, 0.62, 0.27, 1)
polygon = PackedVector2Array(1068,502, 1026,584, 1110,584)

[node name="Ground" type="StaticBody2D" parent="."]
position = Vector2(0, 600)

[node name="GroundShape" type="CollisionShape2D" parent="Ground"]
shape = SubResource("Shape_ground")

[node name="GroundDark" type="ColorRect" parent="Ground"]
color = Color(0.18, 0.46, 0.12, 1)
size = Vector2(1280, 40)

[node name="GroundLight" type="ColorRect" parent="Ground"]
color = Color(0.24, 0.58, 0.16, 1)
size = Vector2(1280, 14)

[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(300, 520)
script = ExtResource("1_player")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Player"]
scale = Vector2(0.10, 0.10)
sprite_frames = SubResource("SpriteFrames_1")
animation = &"idle"
autoplay = "idle"

[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("Shape_player")

[node name="Camera2D" type="Camera2D" parent="Player"]
zoom = Vector2(1.0, 1.0)
limit_left = 0
limit_right = 1280
limit_top = 0
limit_bottom = 720
""")

print("\n" + "=" * 48)
print("  SELESAI!")
print("  1. Godot → Project → Reload Current Project")
print("  2. Tekan F5")
print("=" * 48 + "\n")
