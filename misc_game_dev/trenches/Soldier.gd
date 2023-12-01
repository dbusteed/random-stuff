extends CharacterBody2D

@onready var sprite = $Sprite2D
@onready var timer = $Timer
@onready var sights = $Area2D2
@onready var ray = $RayCast2D

@export var speed: int = 20
@export var team: String = 'red'

var dist
var nav_path = []
var nav_path_tmp = []
var nav_thresh = 1
var velocity = Vector2.ZERO
var moving = true
var move_delay = 0

func _physics_process(delta):
	if move_delay > 0 and !moving:
		nav_path_tmp = nav_path
		nav_path = []
		timer.start(move_delay)
		move_delay = 0
	if nav_path.size() > 0:
		moving = true
		sprite.modulate =  Color(0,1,0)
		move_along_path(delta)

func move_along_path(delta):
	if nav_path.size() > 0:
		dist = global_position.distance_to(nav_path[0])
		if dist < nav_thresh:
			nav_path.remove(0)
			if nav_path.size() != 0:
				velocity = global_position.direction_to(nav_path[0]) * speed
				set_velocity(velocity)
				move_and_slide()
				velocity = velocity
			else:
				moving = false
				sprite.modulate =  Color(1,0,0)
		else:
			velocity = global_position.direction_to(nav_path[0]) * speed
			set_velocity(velocity)
			move_and_slide()
			velocity = velocity
	rotate(velocity.angle() + (PI / 2))

# if at final position, set to not_moving,
# if collide with not_moving friend, then
# become not moving too (chain reaction)
#
# when target found, find the closest and make
# them the leader, then route thru their position first
# to get a following effect

func rotate(rot):
	sprite.global_rotation = rot
	sights.global_rotation = rot

func _on_Area2D_body_entered(body):
	if body.is_in_group('soldier'):
		if !body.moving:
			nav_path = []
			moving = false
			sprite.modulate =  Color(1,0,0)
			


#func _on_Area2D_area_entered(area):
#	print('ya')


func _on_Timer_timeout():
	nav_path = nav_path_tmp
	timer.stop()


func _on_Area2D2_body_entered(body):
	if body.is_in_group('soldier'):
		if body.team != team:
			ray.target_position = body.global_position - global_position
	else:
		print(body)
