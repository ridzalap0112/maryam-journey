"""
Maryam Journey - Fix Sprite Player
Jalankan di PowerShell di folder maryam-journey:
  python fix_sprite.py
"""
import os

BASE = os.getcwd()

def path(*parts):
    return os.path.join(BASE, *parts)

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Maryam Journey — Fix Sprite Player")
print("=" * 48)

# Cek icon.svg ada
icon_path = path("icon.svg")
if not os.path.exists(icon_path):
    print("  ❌  icon.svg tidak ditemukan!")
    exit(1)

# Tulis ulang WorldMap.tscn dengan sprite icon.svg yang benar-benar ter-embed
worldmap = '''[gd_scene load_steps=7 format=3]

[ext_resource type="Script" path="res://scripts/player/Player.gd" id="1_player"]
[ext_resource type="Texture2D" uid="uid://icon" path="res://icon.svg" id="2_icon"]

[sub_resource type="SpriteFrames" id="SpriteFrames_1"]
animations = [{
"frames": [{
"duration": 1.0,
"texture": ExtResource("2_icon")
}],
"loop": true,
"name": &"idle",
"speed": 5.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("2_icon")
}],
"loop": true,
"name": &"walk",
"speed": 8.0
}, {
"frames": [{
"duration": 1.0,
"texture": ExtResource("2_icon")
}],
"loop": false,
"name": &"jump",
"speed": 5.0
}]

[sub_resource type="RectangleShape2D" id="RectangleShape2D_ground"]
size = Vector2(1280, 40)

[sub_resource type="RectangleShape2D" id="RectangleShape2D_player"]
size = Vector2(40, 40)

[node name="WorldMap" type="Node2D"]

[node name="Background" type="ColorRect" parent="."]
color = Color(0.529, 0.808, 0.922, 1)
size = Vector2(1280, 720)

[node name="Ground" type="StaticBody2D" parent="."]
position = Vector2(0, 680)

[node name="GroundShape" type="CollisionShape2D" parent="Ground"]
shape = SubResource("RectangleShape2D_ground")

[node name="GroundVisual" type="ColorRect" parent="Ground"]
color = Color(0.29, 0.647, 0.208, 1)
size = Vector2(1280, 40)

[node name="Player" type="CharacterBody2D" parent="."]
position = Vector2(300, 600)
script = ExtResource("1_player")

[node name="AnimatedSprite2D" type="AnimatedSprite2D" parent="Player"]
scale = Vector2(0.15, 0.15)
sprite_frames = SubResource("SpriteFrames_1")
animation = &"idle"
autoplay = "idle"

[node name="CollisionShape2D" type="CollisionShape2D" parent="Player"]
shape = SubResource("RectangleShape2D_player")

[node name="Camera2D" type="Camera2D" parent="Player"]
zoom = Vector2(1, 1)
'''

write(path("scenes", "world", "WorldMap.tscn"), worldmap)

print("\n" + "=" * 48)
print("  SELESAI! Sekarang:")
print("  1. Kembali ke Godot")
print("  2. Klik Project > Reload Current Project")
print("  3. Tekan F5")
print("  4. Karakter Godot icon akan muncul dan bisa jalan!")
print("=" * 48 + "\n")
