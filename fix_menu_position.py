"""
Maryam Journey - Fix Menu Position Only
python fix_menu_position.py
"""
import os, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Fix Menu Position")
print("=" * 40)

# Masalah: Margin offset_bottom = 720 tapi offset_right = 1280
# tapi tidak ada anchor set ke full rect
# Solusi: set anchor_right=1.0 anchor_bottom=1.0 pada MarginContainer
# sehingga ia benar-benar memenuhi seluruh layar 1280x720

tscn_path = os.path.join(BASE, "scenes", "ui", "MainMenu.tscn")
with open(tscn_path, "r", encoding="utf-8") as f:
    content = f.read()

# Ganti node Margin agar full rect dengan anchor
old = '[node name="Margin" type="MarginContainer" parent="UI"]\noffset_right = 1280.0\noffset_bottom = 720.0'
new = '[node name="Margin" type="MarginContainer" parent="UI"]\nanchor_right = 1.0\nanchor_bottom = 1.0\ngrow_horizontal = 2\ngrow_vertical = 2'

if old in content:
    content = content.replace(old, new)
    with open(tscn_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  ✅  MainMenu.tscn — Margin anchor fixed")
else:
    print("  ⚠️  Pattern tidak ditemukan, tulis ulang node Margin...")
    # Fallback: replace apapun yang ada di Margin node
    import re
    content = re.sub(
        r'\[node name="Margin" type="MarginContainer" parent="UI"\][^\[]*',
        '[node name="Margin" type="MarginContainer" parent="UI"]\nanchor_right = 1.0\nanchor_bottom = 1.0\ngrow_horizontal = 2\ngrow_vertical = 2\n\n',
        content
    )
    with open(tscn_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print("  ✅  MainMenu.tscn — Margin node rewritten")

try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m", "fix: menu margin full anchor rect"], cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️  Git: {e}")

print("\n  Godot → Reload → F5 → Card tepat di tengah! 🌙\n")
