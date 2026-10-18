import pygame
from .clock import Clock
from .assets import AssetManager
from .scene import Scene
from .systems import RenderSystem, PhysicsSystem, CollisionSystem, ScriptSystem

class Engine:
    def __init__(self, width=800, height=600, title='PyEngine', target_fps=60):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = Clock(target_fps)
        self.assets = AssetManager()
        self.render_system = RenderSystem(self.screen)
        self.physics_system = PhysicsSystem()
        self.collision_system = CollisionSystem()
        self.script_system = ScriptSystem()
        self.scene = None
        self.running = False
        self._fixed_accumulator = 0.0
        self._fixed_dt = 1.0 / 60.0
        self._on_quit = None

    def set_scene(self, scene):
        if self.scene is not None:
            self.scene.clear()
        self.scene = scene

    def on_quit(self, fn):
        self._on_quit = fn

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                if self._on_quit:
                    self._on_quit()

    def _update(self, dt):
        if self.scene is None:
            return
        self._fixed_accumulator += dt
        while self._fixed_accumulator >= self._fixed_dt:
            self.physics_system.update(self.scene, self._fixed_dt)
            self.collision_system.update(self.scene, self._fixed_dt)
            self.scene.update(self._fixed_dt)
            self.script_system.update(self.scene, self._fixed_dt)
            self._fixed_accumulator -= self._fixed_dt

    def _render(self):
        if self.scene is None:
            self.screen.fill((0, 0, 0))
        else:
            self.screen.fill(self.scene.background_color)
            self.render_system.render(self.scene)
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick()
            self._handle_events()
            self._update(dt)
            self._render()
            self.clock.target_fps  
            pygame.time.Clock().tick(self.clock.target_fps)
        pygame.quit()

    def stop(self):
        self.running = False