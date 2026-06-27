# =============================================================
#  scripts/managers/TransitionManager.gd
#  Autoload — fade in/out saat pindah scene
#  Daftarkan di: Project > Autoload > TransitionManager
# =============================================================
extends CanvasLayer

var _overlay  : ColorRect
var _tween    : Tween
var _is_busy  : bool = false

signal transition_done


func _ready() -> void:
	_overlay = ColorRect.new()
	_overlay.color = Color(0, 0, 0, 0)
	_overlay.anchors_preset = Control.PRESET_FULL_RECT
	_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_overlay)


func go_to(scene_path: String) -> void:
	if _is_busy:
		return
	_is_busy = true
	await _fade(1.0)
	SaveManager.save()
	get_tree().change_scene_to_file(scene_path)
	await get_tree().process_frame
	await _fade(0.0)
	_is_busy = false
	transition_done.emit()


func _fade(target_alpha: float) -> void:
	if _tween and _tween.is_valid():
		_tween.kill()
	_tween = create_tween()
	_tween.tween_property(_overlay, "color:a", target_alpha, 0.45)		.set_ease(Tween.EASE_IN_OUT).set_trans(Tween.TRANS_SINE)
	await _tween.finished
