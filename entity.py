import itertools

class Entity:
    _id_counter = itertools.count()

    def __init__(self, name='Entity'):
        self.id = next(Entity._id_counter)
        self.name = name
        self.active = True
        self.tags = set()
        self._components = {}
        self.scene = None

    def add(self, component):
        self._components[type(component)] = component
        if self.scene is not None and hasattr(component, 'on_start'):
            if component.on_start:
                component.on_start(self)
        return self

    def remove(self, cls):
        if cls in self._components:
            comp = self._components.pop(cls)
            if self.scene is not None and hasattr(comp, 'on_destroy') and comp.on_destroy:
                comp.on_destroy(self)
            return comp
        return None

    def get(self, cls):
        return self._components.get(cls)

    def has(self, cls):
        return cls in self._components

    def all_components(self):
        return list(self._components.values())

    def __repr__(self):
        return f"<Entity {self.name} id={self.id}>"