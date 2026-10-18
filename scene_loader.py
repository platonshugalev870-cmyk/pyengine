import json
from .scene import Scene
from .components import Transform, Sprite, RigidBody, BoxCollider, CircleCollider

class SceneLoader:
    def __init__(self, asset_manager=None):
        self.assets = asset_manager

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        scene = Scene(data.get('name', 'Scene'))
        scene.gravity = data.get('gravity', 980.0)
        scene.background_color = tuple(data.get('background_color', [30, 30, 40]))
        for ed in data.get('entities', []):
            e = scene.create_entity(ed.get('name', 'Entity'))
            e.tags.update(ed.get('tags', []))
            if 'transform' in ed:
                t = ed['transform']
                e.add(Transform(t.get('x', 0), t.get('y', 0)))
            else:
                e.add(Transform())
            if 'sprite' in ed:
                s = ed['sprite']
                surf = None
                if self.assets and s.get('image'):
                    surf = self.assets.get_image(s['image'])
                e.add(Sprite(surface=surf,
                             layer=s.get('layer', 0),
                             size=tuple(s['size']) if s.get('size') else None,
                             color=tuple(s['color']) if s.get('color') else None))
            if 'rigidbody' in ed:
                r = ed['rigidbody']
                rb = RigidBody(mass=r.get('mass', 1.0),
                               gravity=r.get('gravity', 980.0),
                               static=r.get('static', False),
                               use_gravity=r.get('use_gravity', True))
                if 'velocity' in r:
                    rb.velocity.x = r['velocity'][0]
                    rb.velocity.y = r['velocity'][1]
                e.add(rb)
            if 'box_collider' in ed:
                b = ed['box_collider']
                e.add(BoxCollider(b['width'], b['height'],
                                  b.get('offset_x', 0), b.get('offset_y', 0),
                                  b.get('is_trigger', False), b.get('tag', '')))
            if 'circle_collider' in ed:
                c = ed['circle_collider']
                e.add(CircleCollider(c['radius'],
                                     c.get('offset_x', 0), c.get('offset_y', 0),
                                     c.get('is_trigger', False), c.get('tag', '')))
        return scene