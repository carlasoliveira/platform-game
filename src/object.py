from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, position, size):
        self._position = position  
        self._size = size         

    def get_position(self):
        return self._position

    def set_position(self, pos):
        self._position = pos

    def get_size(self):
        return self._size

    @abstractmethod
    def render(self, surface):
        pass


class ObjectDynamic(Object):
    def __init__(self, position, size, velocity):
        super().__init__(position, size)
        self._velocity = velocity

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, velocity):
        self._velocity = velocity

    @abstractmethod
    def update(self, delta_time, game_map):
        pass
