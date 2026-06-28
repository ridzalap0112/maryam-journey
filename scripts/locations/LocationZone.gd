extends Area2D

@export var location_name : String = "Lokasi"
@export var location_key  : String = "masjid"
@export var scene_path    : String = ""

@onready var _panel : Panel = $LabelPanel
@onready var _label : Label = $LabelPanel/Label
@onready var _hint  : Label = $LabelPanel/Hint

var _inside   : bool  = false
var _bob_time : float = 0.0


func _ready() -> void:
	_label.text    = location_name
	_hint.text     = "▼ Tekan Enter"
	_panel.visible = false
	body_entered.connect(_on_entered)
	body_exited.connect(_on_exited)


func _process(delta: float) -> void:
	if not _inside:
		return
	_bob_time       += delta
	_panel.position.y = -140.0 + sin(_bob_time * 2.8) * 6.0
	if Input.is_action_just_pressed("interact"):
		_enter()


func _on_entered(body: Node2D) -> void:
	if not body.is_in_group("player"):
		return
	_inside           = true
	_bob_time         = 0.0
	_panel.position.y = -140.0
	_panel.visible    = true
	if not GameManager.is_location_unlocked(location_key):
		_hint.text = "🔒 Terkunci"
	else:
		_hint.text = "▼ Tekan Enter"


func _on_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		_inside        = false
		_panel.visible = false


func _enter() -> void:
	if not GameManager.is_location_unlocked(location_key):
		return
	if scene_path == "" or not ResourceLoader.exists(scene_path):
		print("[Zone] Scene belum ada: ", location_name)
		return
	TransitionManager.go_to(scene_path)
