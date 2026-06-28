# =============================================================
#  scripts/ui/HUD.gd
# =============================================================
extends CanvasLayer

@onready var _star_label : Label = $StarPanel/StarLabel
@onready var _name_label : Label = $NameLabel


func _ready() -> void:
	GameManager.star_collected.connect(_on_star)
	_name_label.text = "🌙 " + GameManager.player_name
	_star_label.text = "⭐  " + str(GameManager.total_stars)


func _on_star(total: int) -> void:
	_star_label.text = "⭐  " + str(total)
