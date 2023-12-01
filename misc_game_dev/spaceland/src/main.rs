use bevy::core_pipeline::clear_color::ClearColorConfig;
use bevy::prelude::*;
use bevy::render::camera::Viewport;
use bevy::render::view::RenderLayers;
use bevy::window::{PresentMode, WindowResolution};
use bevy_prototype_lyon::prelude::*;
use bevy_prototype_lyon::shapes::Rectangle;
use bevy_rapier2d::prelude::*;
use rand::{thread_rng, Rng};
use std::f32::consts::PI;

#[derive(Component)]
struct EnemyShip(Option<Vec2>);

#[derive(Component)]
struct Player;

#[derive(Component)]
struct IType;

#[derive(Component)]
struct GameCamera;

#[derive(Component)]
struct MinimapCamera;

#[derive(Component)]
struct ShipComputerCamera;

#[derive(Component)]
struct MinimapCameraOffset(Vec3);

#[derive(Component)]
struct MinimapActual(Entity);

#[derive(Component)]
struct MinimapMarker;

#[derive(Component)]
struct ShipComputerScreen;

#[derive(Component)]
struct CameraOffset(Vec3);

#[derive(Component)]
struct Speed(f32);

#[derive(Component)]
struct WarpDrive {
    capacity: f32,
    charged: f32,
}

#[derive(Component)]
struct PointOfInterest {
    maker_color: Color,
    minimap_marker: Entity,
    map_marker: Entity,
}

#[derive(Resource, Deref, DerefMut)]
struct MinimapZoom(f32);

#[derive(Event)]
struct OpenMapEvent;

fn main() {
    App::new()
        .insert_resource(ClearColor(Color::DARK_GRAY))
        .insert_resource(MinimapZoom(20.0))
        .add_event::<OpenMapEvent>()
        .add_plugins((
            DefaultPlugins
                .set(ImagePlugin::default_nearest())
                .set(WindowPlugin {
                    primary_window: Some(Window {
                        title: "Spaceland".into(),
                        resolution: WindowResolution::new(1000., 750.)
                            .with_scale_factor_override(1.0),
                        present_mode: PresentMode::AutoVsync,
                        prevent_default_event_handling: false,
                        // fit_canvas_to_parent: true,
                        ..default()
                    }),
                    ..default()
                }),
            ShapePlugin,
            RapierPhysicsPlugin::<NoUserData>::pixels_per_meter(100.0),
            // RapierDebugRenderPlugin::default(),
            // bevy::diagnostic::LogDiagnosticsPlugin::default(),
            // bevy::diagnostic::FrameTimeDiagnosticsPlugin::default(),
            // bevy_inspector_egui::quick::WorldInspectorPlugin::new(),
        ))
        .add_systems(Startup, setup_game)
        .add_systems(
            Update,
            (
                player_input,
                spawn_enemy_ships,
                move_enemy_ships,
                update_minimap,
                handle_open_map_event,
                ship_computer_screen_tween,
                gizmos,
            ),
        )
        .add_systems(PostUpdate, follow_camera)
        .run();
}

fn setup_game(
    mut commands: Commands,
    mut rapier_config: ResMut<RapierConfiguration>,
    asset_server: Res<AssetServer>,
) {
    rapier_config.gravity = Vec2::ZERO;

    // 0 -- game camera
    commands.spawn((
        Camera2dBundle {
            camera: Camera {
                order: 0,
                ..default()
            },
            camera_2d: Camera2d {
                clear_color: ClearColorConfig::None,
            },
            projection: OrthographicProjection {
                scale: 1.5,
                far: 1000.,
                near: -1000.,
                ..Default::default()
            },
            ..default()
        },
        UiCameraConfig { show_ui: false },
        GameCamera,
        RenderLayers::from_layers(&[0]),
    ));

    // 1 -- minimap
    commands.spawn((
        Camera2dBundle {
            camera: Camera {
                order: 2,
                viewport: Some(Viewport {
                    physical_position: UVec2::new(1000 - 200 - 15, 750 - 200 - 15),
                    physical_size: UVec2::new(200, 200),
                    ..default()
                }),
                ..default()
            },
            camera_2d: Camera2d {
                clear_color: ClearColorConfig::None,
            },
            ..default()
        },
        UiCameraConfig { show_ui: false },
        MinimapCamera,
        RenderLayers::from_layers(&[1]),
    ));

    // 3 -- hud camera
    commands.spawn((
        Camera2dBundle {
            camera: Camera {
                order: 1,
                viewport: Some(Viewport {
                    physical_position: UVec2::new(0, 0),
                    physical_size: UVec2::new(1000, 750),
                    ..default()
                }),
                ..default()
            },
            camera_2d: Camera2d {
                clear_color: ClearColorConfig::None,
            },
            ..default()
        },
        UiCameraConfig { show_ui: true },
        RenderLayers::from_layers(&[3]),
    ));

    // 4 -- computer camera
    commands.spawn((
        Camera2dBundle {
            camera: Camera {
                order: 4,
                viewport: Some(Viewport {
                    physical_position: UVec2::new(0, 0),
                    physical_size: UVec2::new(1000, 750),
                    ..default()
                }),
                ..default()
            },
            camera_2d: Camera2d {
                clear_color: ClearColorConfig::None,
            },
            ..default()
        },
        UiCameraConfig { show_ui: true },
        ShipComputerCamera,
        RenderLayers::from_layers(&[4]),
    ));

    commands.spawn((
        ShapeBundle {
            path: GeometryBuilder::build_as(&shapes::Rectangle {
                extents: Vec2::new(200.0, 200.0),
                origin: RectangleOrigin::Center,
            }),
            transform: Transform::from_xyz(500.0 - 100.0 - 15.0, ((750. - 200.) / -2.0) + 15.0, 5.0),
            ..default()
        },
        Fill::color(Color::BLACK),
        Stroke::new(Color::GREEN, 1.25),
        RenderLayers::layer(3),
    ));

    // minimap player
    let m = commands.spawn((
        SpriteBundle {
            texture: asset_server.load("marker.png"),
            transform: Transform {
                translation: Vec3::new(0.0, 0.0, 3.0),
                ..default()
            },
            ..default()
        },
        MinimapMarker,
        RenderLayers::layer(1),
    )).id();

    // player
    commands.spawn((
        SpriteBundle {
            texture: asset_server.load("player.png"),
            transform: Transform::from_xyz(0.0, 0.0, 10.0),
            ..default()
        },
        // Animation {
        //     timer: Timer::from_seconds(0.35, TimerMode::Repeating),
        //     n_sprites: 2,
        //     one_time: false,
        // },
        Player,
        Speed(200.0),
        WarpDrive {
            capacity: 100.0,
            charged: 0.0,
        },
        RigidBody::Dynamic,
        Collider::ball(28.0),
        Ccd::enabled(),
        Sensor,
        CollisionGroups::new(
            Group::from_bits_truncate(0b00000001),
            Group::from_bits_truncate(0b11001110),
        ),
        CameraOffset(Vec3::ZERO),
        Velocity {
            linvel: Vec2::new(200.0, 0.0),
            angvel: 0.0,
        },
        ExternalImpulse { impulse: Vec2::ZERO, torque_impulse: 0.0 },
        MinimapActual(m),
        RenderLayers::layer(0),
        Sleeping {
            linear_threshold: -1.0,
            ..default()
        },
    ));

    let m = commands.spawn((
        ShapeBundle {
            path: GeometryBuilder::build_as(&shapes::Circle {
                radius: 8.0,
                ..default()
            }),
            transform: Transform::from_xyz(20.0, 20.0, 3.0),
            ..default()
        },
        Stroke::new(Color::ORANGE, 1.0),
        Fill::color(Color::BLACK),
        MinimapMarker,
        RenderLayers::layer(1),
    )).id();

    commands.spawn((
        SpriteBundle {
            texture: asset_server.load("planet.png"),
            transform: Transform::from_xyz(500.0, 500.0, 5.0),
            ..default()
        },
        RigidBody::Fixed,
        Collider::ball(28.0),
        MinimapActual(m),
        Sensor,
        RenderLayers::layer(0),
    ));

    let m = commands.spawn((
        ShapeBundle {
            path: GeometryBuilder::build_as(&shapes::Circle {
                radius: 8.0,
                ..default()
            }),
            transform: Transform::from_xyz(0.0, 0.0, 3.0),
            ..default()
        },
        Stroke::new(Color::ORANGE, 1.0),
        Fill::color(Color::BLACK),
        MinimapMarker,
        RenderLayers::layer(1),
    )).id();

    commands.spawn((
        SpriteBundle {
            texture: asset_server.load("planet.png"),
            transform: Transform::from_xyz(-550.0, -2000.0, 5.0),
            ..default()
        },
        RigidBody::Fixed,
        Collider::ball(28.0),
        MinimapActual(m),
        Sensor,        
        RenderLayers::layer(0),
    ));

    for x in (-3000..=3000).step_by(1000) {
        for y in (-3000..=3000).step_by(1000) {
            commands.spawn((SpriteBundle {
                texture: asset_server.load("background.png"),
                transform: Transform::from_xyz(x as f32, y as f32, 0.0),
                ..default()
            },));
        }
    }

    // commands.spawn((
    //     TextBundle::from_sections([
    //         TextSection::new(
    //             "Cygnus System",
    //             TextStyle {
    //                 // font: asset_server.load("fonts/boba_mono/boba-mono.otf"),
    //                 font: asset_server.load("fonts/pixelsplitter/PixelSplitter-Bold.ttf"),
    //                 font_size: 16.0,
    //                 color: Color::GREEN,
    //             },
    //         ),
    //     ])
    //     .with_style(Style {
    //         position_type: PositionType::Absolute,
    //         top: Val::Px(750.0 - 200.0 - 15.0 - 16.0 - 2.0),
    //         left: Val::Px(1000.0 - 200.0 - 15.0),
    //         ..default()
    //     }),
    //     RenderLayers::layer(3),
    //     Name::from("Text"),
    // ));

    commands.spawn((
        ShapeBundle {
            path: GeometryBuilder::build_as(&shapes::Rectangle {
                extents: Vec2::new(200.0, 10.0),
                ..default()
            }),
            transform: Transform::from_xyz(500.0 - 100.0 - 15.0, 375.0 - 5.0 - 15.0, 3.0),
            ..default()
        },
        Stroke::new(Color::GREEN, 1.0),
        RenderLayers::layer(3),
    ));

    commands.spawn((
        ShapeBundle {
            path: GeometryBuilder::build_as(&shapes::Rectangle {
                extents: Vec2::new(150.0, 10.0),
                ..default()
            }),
            transform: Transform::from_xyz(500.0 - 100.0 - 15.0, 375.0 - 5.0 - 15.0, 3.0),
            ..default()
        },
        Fill::color(Color::rgba(0.0, 1.0, 0.0, 1.0)),
        RenderLayers::layer(3),
    ));
}

fn gizmos(mut gizmos: Gizmos) {
    gizmos.rect_2d(Vec2::ZERO, 0.0, Vec2::splat(1000.0), Color::RED);
}

fn update_minimap(
    q_actuals: Query<(&Transform, &MinimapActual), Without<MinimapMarker>>,
    mut q_markers: Query<&mut Transform, (With<MinimapMarker>, Without<MinimapActual>)>,
    mm_zoom: Res<MinimapZoom>,
) {
    for (trans, &MinimapActual(marker_id)) in q_actuals.iter() {
        let mut marker_trans = q_markers.get_mut(marker_id).expect("Can't find MinimapMarker!");
        marker_trans.translation = trans.translation / Vec3::new(**mm_zoom, **mm_zoom, 1.0);
        marker_trans.rotation = trans.rotation;
    }
}

fn handle_open_map_event(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut open_map_event: EventReader<OpenMapEvent>,
) {
    for _evt in open_map_event.iter() {
        commands.spawn((
            SpriteBundle {
                texture: asset_server.load("ship_computer_background.png"),
                transform: Transform {
                    scale: Vec3::new(0.01, 0.01, 1.0),
                    ..default()
                },
                ..default()
            },
            ShipComputerScreen,
            RenderLayers::layer(4),
        ));

        // commands.spawn((
        //     ShapeBundle {
        //         path: GeometryBuilder::build_as(&shapes::Rectangle {
        //             extents: Vec2::new(500.0, 500.0),
        //             origin: RectangleOrigin::Center,
        //         }),
        //         transform: Transform::from_xyz(0.0, 0.0, 51.0),
        //         ..default()
        //     },
        //     Fill::color(Color::BLACK),
        //     Stroke::new(Color::RED, 1.0),
        //     RenderLayers::layer(4),
        // ));
    }
}

fn ship_computer_screen_tween(mut commands: Commands, mut q_comp_screen: Query<&mut Transform, With<ShipComputerScreen>>) {
    for mut trans in q_comp_screen.iter_mut() {
        trans.scale = Vec3::lerp(trans.scale, Vec3::ONE, 0.15);
    }
}

fn player_input(
    mut commands: Commands,
    keys: Res<Input<KeyCode>>,
    mut player: Query<
        (
            &mut Transform,
            &mut Velocity,
            &mut CameraOffset,
            &mut Speed,
            &mut WarpDrive,
            &mut ExternalImpulse,
        ),
        With<Player>,
    >,
    mut mm_zoom: ResMut<MinimapZoom>,
    mut open_map_event: EventWriter<OpenMapEvent>,
    // mut minimap: Query<&mut Camera, With<MinimapCamera>>,
    // game_assets: Res<GameAssets>,
) {
    if let Ok((mut trans, mut vel, mut offset, mut speed, mut warp_drive, mut impulse)) = player.get_single_mut()
    {
        if keys.pressed(KeyCode::A) {
            trans.rotate_z(0.025);
        }
        if keys.pressed(KeyCode::D) {
            trans.rotate_z(-0.025);
        }
        if keys.just_pressed(KeyCode::W) {
            speed.0 += 10.0;
        }
        if keys.just_pressed(KeyCode::S) {
            speed.0 -= 10.0;
        }
        if keys.just_pressed(KeyCode::Return) {
            println!("pew\n");
        }
        if keys.pressed(KeyCode::Minus) {
            **mm_zoom += 0.1;
        }
        if keys.pressed(KeyCode::Equals) {
            **mm_zoom -= 0.1;
        }
        if keys.pressed(KeyCode::P) {
            warp_drive.charged += 1.0;
        }
        if keys.just_pressed(KeyCode::M) {
            open_map_event.send(OpenMapEvent {});
        }
        if keys.just_released(KeyCode::P) {
            impulse.impulse = vel.linvel * warp_drive.charged;
            warp_drive.capacity -= warp_drive.charged;
            warp_drive.charged = 0.0;
            println!("{:?}", warp_drive.capacity);
        }

        let (axis, mut rot) = trans.rotation.to_axis_angle();
        rot = (axis * rot).z;
        vel.linvel = Vec2::from_angle(rot) * speed.0;

        offset.0 = trans.translation;
    }
}

fn follow_camera(
    mut q_game_cam: Query<&mut Transform, (With<GameCamera>, Without<MinimapCamera>)>,
    mut q_minimap_cam: Query<&mut Transform, (Without<GameCamera>, With<MinimapCamera>)>,
    q_player: Query<&CameraOffset>,
    mm_zoom: Res<MinimapZoom>,
) {
    for offset in q_player.iter() {
        for mut cam_trans in q_game_cam.iter_mut() {
            cam_trans.translation = Vec3::lerp(cam_trans.translation, Vec3::new(offset.0.x, offset.0.y, cam_trans.translation.z), 0.90);
        }

        for mut cam_trans in q_minimap_cam.iter_mut() {
            cam_trans.translation = Vec3::new(offset.0.x, offset.0.y, cam_trans.translation.z) / Vec3::new(**mm_zoom, **mm_zoom, 1.0);
        }
    }
}

fn spawn_enemy_ships(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    q_itype: Query<Entity, With<IType>>,
    q_cam_offest: Query<&CameraOffset>,
) {
    let mut count = 0;
    for _ in q_itype.iter() {
        count += 1;
    }

    if count < 5 {
        if let Ok(offset) = q_cam_offest.get_single() {
            let mut rng = rand::thread_rng();
            let angle: f32 = rng.gen_range(-PI..PI);
            let trans = Vec3::new(angle.cos(), angle.sin(), 10.0)
                * Vec3::new(650.0 * 1.25, 650.0 * 1.25, 1.0)
                + offset.0;
            let angle: f32 = rng.gen_range(-PI..PI);

            let m = commands.spawn((
                ShapeBundle {
                    path: GeometryBuilder::build_as(&shapes::RegularPolygon {
                        sides: 4,
                        feature: shapes::RegularPolygonFeature::SideLength(7.5),
                        ..default()
                    }),
                    transform: Transform {
                        translation: Vec3::new(0.0, 0.0, 3.0),
                        ..default()
                    },
                    ..default()
                },
                Fill::color(Color::BLACK),
                Stroke::new(Color::PINK, 1.0),
                MinimapMarker,
                RenderLayers::layer(1),
            )).id();

            commands.spawn((
                SpriteBundle {
                    texture: asset_server.load("i_type.png"),
                    transform: Transform {
                        translation: trans,
                        rotation: Quat::from_rotation_z(angle),
                        ..default()
                    },
                    ..default()
                },
                EnemyShip(None),
                Velocity::default(),
                RigidBody::Dynamic,
                Collider::ball(26.0),
                Sensor,
                IType,
                MinimapActual(m),
                CollisionGroups::new(
                    Group::from_bits_truncate(0b0000100),
                    Group::from_bits_truncate(0b1100111),
                ),
            ));
        }
    }
}

fn move_enemy_ships(
    mut query: Query<(&mut Velocity, &mut Transform, &mut EnemyShip)>,
    q_player: Query<&CameraOffset>,
) {
    if let Ok(player_pos) = q_player.get_single() {
        // TODO can they avoid rocks to some degree?
        for (mut vel, mut trans, mut ship) in query.iter_mut() {
            if let Some(target) = ship.0 {
                let angle = f32::atan2(
                    target.y - trans.translation.y,
                    target.x - trans.translation.x,
                );

                let (axis, mut rot) = trans.rotation.to_axis_angle();
                rot = (axis * rot).z;

                // does it need to rotate?
                if (angle - rot).abs() > 0.05 {
                    let a = (angle + 2.0 * PI) % (2.0 * PI);
                    let r = (rot + 2.0 * PI) % (2.0 * PI);

                    let mut diff = a - r;
                    if diff.abs() > PI {
                        diff += 2.0 * PI;
                    }

                    // which way to rotate?
                    if diff.is_sign_positive() {
                        trans.rotate_z(0.02);
                    } else {
                        trans.rotate_z(-0.02);
                    }
                }

                // println!("dist {:?}", trans.translation.truncate().distance(target));
                if trans.translation.truncate().distance(target) < 10.0 {
                    // vel.linvel = Vec2::ZERO;
                    ship.0 = None;
                } else {
                    vel.linvel = Vec2::from_angle(rot) * 300.0;
                }
            } else {
                let mut rng = rand::thread_rng();
                let offset = Vec2::new(rng.gen_range(-100.0..100.0), rng.gen_range(-100.0..100.0));
                ship.0 = Some(player_pos.0.truncate() + offset);
            }
        }
    }
}
