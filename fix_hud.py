"""
Maryam Journey - Fix HUD.gd
python fix_hud.py
"""
import os, subprocess

BASE = os.getcwd()

def write(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"  ✅  {os.path.relpath(filepath, BASE)}")

print("\n🌙 Fix HUD.gd")
print("=" * 40)

# Root cause: HUD.gd punya @onready _hint_arrow = $HintArrow
# tapi node HintArrow tidak ada di WorldMap.tscn
# Fix: hapus _hint_arrow dari HUD.gd, buat HUD yang bersih

write(os.path.join(BASE, "scripts", "ui", "HUD.gd"), """\
# =============================================================
#  scripts/ui/HUD.gd
# =============================================================
extends CanvasLayer

@onready var _star_label : Label = $StarPanel/StarLabel
@onready var _name_label : Label = $NameLabel


func _ready() -> void:
\tGameManager.star_collected.connect(_on_star)
\t_name_label.text = "🌙 " + GameManager.player_name
\t_star_label.text = "⭐  " + str(GameManager.total_stars)


func _on_star(total: int) -> void:
\t_star_label.text = "⭐  " + str(total)
""")

try:
    subprocess.run(["git", "add", "."], cwd=BASE, check=True)
    subprocess.run(["git", "commit", "-m", "fix: remove _hint_arrow from HUD - node not in scene"], cwd=BASE, check=True)
    subprocess.run(["git", "push"], cwd=BASE, check=True)
    print("  ✅  GitHub updated!")
except Exception as e:
    print(f"  ⚠️  Git: {e}")

print("\n  Godot → Reload → F5 → Game berjalan! 🌙\n")
