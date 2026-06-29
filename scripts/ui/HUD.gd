# =============================================================
#  scripts/ui/HUD.gd
# =============================================================
extends CanvasLayer

@onready var _name_label : Label = $NameLabel
@onready var _star_label : Label = $StarPanel/StarLabel


func _ready() -> void:
	assert(_name_label != null, "HUD: NameLabel tidak ditemukan!")
	assert(_star_label != null, "HUD: StarLabel tidak ditemukan!")
	GameManager.star_collected.connect(_on_star)
	_name_label.text = "🌙 " + GameManager.player_name
	_star_label.text = "⭐  " + str(GameManager.total_stars)
	# Play BGM world saat HUD siap (WorldMap sudah terbuka)
	AudioManager.play_bgm("world")


func _on_star(total: int) -> void:
	_star_label.text = "⭐  " + str(total)
