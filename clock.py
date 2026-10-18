import time

class Clock:
    def __init__(self, target_fps=60):
        self.target_fps = target_fps
        self.fixed_dt = 1.0 / target_fps
        self.last_time = time.perf_counter()
        self.dt = 0.0
        self.fps = 0.0
        self._frames = 0
        self._acc = 0.0

    def tick(self):
        now = time.perf_counter()
        self.dt = now - self.last_time
        self.last_time = now
        if self.dt > 0.25:
            self.dt = 0.25
        self._frames += 1
        self._acc += self.dt
        if self._acc >= 1.0:
            self.fps = self._frames / self._acc
            self._frames = 0
            self._acc = 0.0
        return self.dt