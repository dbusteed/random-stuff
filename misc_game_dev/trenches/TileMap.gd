extends TileMap
class_name ASTAR

@onready var astar = AStar2D.new()

var id1
var id2
var path
var cells
var cell2
var half_tile
var objects

var neighbors = [
	Vector2(1, 0),
	Vector2(-1, 0),
	Vector2(0, 1),
	Vector2(0, -1)
]

#func _ready():	
#	build_nav_mesh()
#
#func build_nav_mesh():
#	astar.clear()
#	cells = get_used_cells(1)
#	half_tile = cell_size / 2
#	for cell in cells:
#		astar.add_point(id(cell), cell, 1.0)
#
#	for cell in cells:
#		id1 = id(cell)
#		for n in neighbors:
#			cell2 = cell + n
#			if cells.has(cell2):
#				id2 = id(cell2)	
##				var line = load("res://Scenes/Line2D.tscn").instantiate()
##				line.points = [(map_to_local(cell) + half_tile), (map_to_world(cell2) + half_tile)]
##				line.name = str(id(cell)) + str(randf_range(0, 100000))
##				add_child(line)
#				astar.connect_points(id1, id2, true)
#
#func _get_path(start, end):
#	path = astar.get_point_path(id(start), id(end))
#	path.remove(0)
#	var world_path = []
#	for p in path:
#		world_path.append((map_to_local(p) + half_tile))
#	return world_path
#
#func id(point):
#	var a = point.x
#	var b = point.y
#	return (a + b) * (a + b + 1) / 2 + b
