extends Node2D

@onready var tm = get_node("/root/World/TileMap")
@onready var selection_box = $SelectionBox

var selected = []
var start_sel_pos = Vector2()
var building = false

func _process(delta):
	var m_pos = get_viewport().get_mouse_position()
	if Input.is_action_just_pressed("rightclick"):
		selection_box.start_sel_pos = m_pos
		start_sel_pos = m_pos
	if Input.is_action_pressed("rightclick"):
		selection_box.m_pos = m_pos
		selection_box.is_visible = true
	else:
		selection_box.is_visible = false
	if Input.is_action_just_released("rightclick"):
		selected = get_units_in_box(start_sel_pos, m_pos)
		print(selected)

	if Input.is_action_just_pressed("leftclick") and len(selected) > 0 and !building:
		selected.sort_custom(Callable(self,"sort_nearest_selected"))
		var i = 0
		for unit in selected:
			unit.move_delay = (i / 3.0)
			unit.nav_path = tm._get_path(
				tm.local_to_map(unit.global_position),
				tm.local_to_map(get_global_mouse_position())
			)
			i += 1
			
	if Input.is_action_just_pressed("build"):
		building = !building

	if Input.is_action_just_pressed("leftclick") and building:
		var tile = tm.local_to_map(get_global_mouse_position())
		print(tile)
		if tm.get_cellv(tile) == 1:
			tm.set_cellv(tile, 0)
			tm.update_bitmask_area(tile)
		elif tm.get_cellv(tile) == 0:
			tm.set_cellv(tile, 1)
			tm.update_bitmask_area(tile)
		tm.build_nav_mesh()
		
	if Input.is_action_just_pressed("up") and len(selected) > 0:
		for unit in selected:
			unit.rotate(0)
	
	if Input.is_action_just_pressed("down") and len(selected) > 0:
		for unit in selected:
			unit.rotate(PI)
	
	if Input.is_action_just_pressed("left") and len(selected) > 0:
		for unit in selected:
			unit.rotate((3 * PI / 2))
	
	if Input.is_action_just_pressed("right") and len(selected) > 0:
		for unit in selected:
			unit.rotate((PI / 2))
			
	if Input.is_action_just_pressed("debug"):
		for unit in selected:
			print(unit.ray.is_colliding())


func sort_nearest_selected(a, b):
	var m = get_global_mouse_position()
	var aa = a.global_position.distance_to(m)
	var bb = b.global_position.distance_to(m)
	return aa < bb

func get_units_in_box(top_left, bot_right):
	if top_left.x > bot_right.x:
		var tmp = top_left.x
		top_left.x = bot_right.x
		bot_right.x = tmp
	if top_left.y > bot_right.y:
		var tmp = top_left.y
		top_left.y = bot_right.y
		bot_right.y = tmp
	var box = Rect2(top_left, bot_right - top_left)
	var box_selected_units = []
	for unit in get_tree().get_nodes_in_group("soldier"):
		if box.has_point(unit.global_transform.origin):
			box_selected_units.append(unit)
	return box_selected_units
