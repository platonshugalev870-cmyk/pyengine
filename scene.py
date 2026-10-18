from .entity import Entity

class Scene:
    def __init__(self, name='Scene'):
        self.name = name
        self.entities = []
        self.pending_add = []
        self.pending_remove = []
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.background_color = (30, 30, 40)
        self.gravity = 980.0
        self.systems = []

    def add_entity(self, entity):
        self.pending_add.append(entity)
        return entity

    def remove_entity(self, entity):
        self.pending_remove.append(entity)

    def create_entity(self, name='Entity'):
        e = Entity(name)
        self.add_entity(e)
        return e

    def find_by_tag(self, tag):
        return [e for e in self.entities if tag in e.tags]

    def find_by_name(self, name):
        return [e for e in self.entities if e.name == name]

    def _flush(self):
        if self.pending_add:
            for e in self.pending_add:
                e.scene = self
                self.entities.append(e)
                for comp in e.all_components():
                    if hasattr(comp, 'on_start') and comp.on_start:
                        comp.on_start(e)
            self.pending_add.clear()
        if self.pending_remove:
            for e in self.pending_remove:
                if e in self.entities:
                    self.entities.remove(e)
                    for comp in e.all_components():
                        if hasattr(comp, 'on_destroy') and comp.on_destroy:
                            comp.on_destroy(e)
                    e.scene = None
            self.pending_remove.clear()

    def update(self, dt):
        self._flush()
        for e in list(self.entities):
            if not e.active:
                continue
            for comp in e.all_components():
                if hasattr(comp, 'on_update') and comp.on_update and getattr(comp, 'enabled', True):
                    comp.on_update(e, dt)
        self._flush()

    def clear(self):
        for e in self.entities:
            for comp in e.all_components():
                if hasattr(comp, 'on_destroy') and comp.on_destroy:
                    comp.on_destroy(e)
            e.scene = None
        self.entities.clear()
        self.pending_add.clear()
        self.pending_remove.clear()