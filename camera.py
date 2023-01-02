class Camera:
    SPEED_COEFF = 0.1

    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.x = width // 2
        self.y = height // 2
        self.observers = []

    def add(self, observer):
        self.observers.append(observer)

    def add_group(self, group):
        for sprite in group:
            self.add(sprite)

    # сдвинуть объект obj на смещение камеры
    def _apply(self):
        for observer in self.observers:
            observer.rect.x += int(self.dx * self.SPEED_COEFF)
            observer.rect.y += int(self.dy * self.SPEED_COEFF)

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.x)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.y)
        self._apply()
