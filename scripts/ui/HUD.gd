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
	GameManager.star_collected.connect(_on_star)
	_name_label.text = "🌙 " + GameManager.player_name
	_star_label.text = "⭐  " + str(GameManager.total_stars)
	_hint_arrow.text = "Jalan ke kanan →"
	_hint_arrow.visible = true


func _process(delta: float) -> void:
	if not _show_hint:
		return
	_hint_time += delta
	_hint_arrow.modulate.a = 0.6 + sin(_hint_time * 3.0) * 0.4


func hide_hint() -> void:
	_show_hint = false
	_hint_arrow.visible = false


func _on_star(total: int) -> void:
	_star_label.text = "⭐  " + str(total)
