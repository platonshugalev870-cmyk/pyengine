import pygame
from pyengine import Engine, Scene, Vec2
from pyengine import Transform, Sprite, RigidBody, BoxCollider, Script

def make_player_script():
    def on_update(entity, dt):
        keys = pygame.key.get_pressed()
        rb = entity.get(RigidBody)
        speed = 400
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            rb.velocity.x = -speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            rb.velocity.x = speed
        else:
            rb.velocity.x = 0
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and entity.get(Script).data.get('on_ground'):
            rb.velocity.y = -600
            entity.get(Script).data['on_ground'] = False
    return Script(on_update=on_update)

def main():
    engine = Engine(960, 540, 'PyEngine Demo')
    scene = Scene('Demo')
    scene.background_color = (20, 20, 35)
    scene.gravity = 1400
    ground = scene.create_entity('Ground')
    ground.add(Transform(480, 500))
    ground.add(Sprite(color=(60, 80, 60), size=(2000, 40)))
    ground.add(BoxCollider(2000, 40))
    ground.tags.add('ground')
    player = scene.create_entity('Player')
    player.add(Transform(200, 300))
    player.add(Sprite(color=(80, 180, 255), size=(40, 60)))
    player.add(RigidBody(use_gravity=True))
    player.add(BoxCollider(40, 60))
    player.add(make_player_script())
    player.tags.add('player')
    box = scene.create_entity('Box')
    box.add(Transform(600, 440))
    box.add(Sprite(color=(220, 120, 60), size=(50, 50)))
    box.add(RigidBody())
    box.add(BoxCollider(50, 50))

    def on_collision(e1, e2, normal):
        if e1.has(Script) and 'player' in e1.tags and 'ground' in e2.tags:
            e1.get(Script).data['on_ground'] = True
        if e2.has(Script) and 'player' in e2.tags and 'ground' in e1.tags:
            e2.get(Script).data['on_ground'] = True
    engine.collision_system.add_listener(on_collision)
    engine.set_scene(scene)
    engine.run()

if __name__ == '__main__':
    main()