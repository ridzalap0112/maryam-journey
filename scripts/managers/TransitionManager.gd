extends CanvasLayer

var _overlay : ColorRect
var _tween   : Tween
var _busy    : bool = false

signal transition_done


func _ready() -> void:
	_overlay              = ColorRect.new()
	_overlay.color        = Color(0, 0, 0, 0)
	_overlay.anchors_preset = Control.PRESET_FULL_RECT
	_overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_overlay)


func go_to(scene_path: String) -> void:
	if _busy:
		return
	_busy = true
	await _fade(1.0)
	get_tree().change_scene_to_file(scene_path)
	await get_tree().process_frame
	await _fade(0.0)
	_busy = false
	transition_done.emit()


func _fade(target: float) -> void:
	if _tween and _tween.is_valid():
		_tween.kill()
	_tween = create_tween()
	_tween.tween_property(_overlay, "color:a", target, 0.4)
	await _tween.finished
