# =============================================================
#  scripts/ui/MainMenu.gd
# =============================================================
extends Node2D

@onready var _btn_start    : Button = $UI/CenterBox/VBox/BtnStart
@onready var _btn_continue : Button = $UI/CenterBox/VBox/BtnContinue
@onready var _btn_reset    : Button = $UI/CenterBox/VBox/BtnReset
@onready var _lbl_stars    : Label  = $UI/CenterBox/VBox/LblStars

const WORLD_SCENE : String = "res://scenes/world/WorldMap.tscn"


func _ready() -> void:
	var has_save := SaveManager.has_save()
	_btn_continue.visible = has_save
	_btn_reset.visible    = has_save
	if has_save:
		SaveManager.load_save()
		_lbl_stars.text = "⭐ " + str(GameManager.total_stars) + " bintang tersimpan"
	else:
		_lbl_stars.text = "Petualangan baru menantimu!"

	_btn_start.pressed.connect(_on_start)
	_btn_continue.pressed.connect(_on_continue)
	_btn_reset.pressed.connect(_on_reset)


func _on_start() -> void:
	SaveManager.delete_save()
	GameManager.total_stars        = 0
	GameManager.unlocked_locations = ["masjid", "pondok", "taman", "kebun", "rumah"]
	TransitionManager.go_to(WORLD_SCENE)


func _on_continue() -> void:
	TransitionManager.go_to(WORLD_SCENE)


func _on_reset() -> void:
	SaveManager.delete_save()
	GameManager.total_stars        = 0
	GameManager.unlocked_locations = ["masjid", "pondok", "taman", "kebun", "rumah"]
	_btn_continue.visible = false
	_btn_reset.visible    = false
	_lbl_stars.text       = "Petualangan baru menantimu!"
