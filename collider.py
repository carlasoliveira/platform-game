class Collider:
    @staticmethod
    def check_collision(position, size, game_map):
        pos_x = position[0]
        pos_y = position[1]
        width, height = size

        # Define bounding box (simplificada)
        box = [
            [pos_x, pos_y],
            [pos_x + width, pos_y],
            [pos_x, pos_y + height],
            [pos_x + width, pos_y + height]
        ]

        for y, row in enumerate(game_map):
            for x, tile in enumerate(row):
                if tile != ' ':
                    for bx, by in box:
                        if x * 64 <= bx < (x + 1) * 64 and y * 64 <= by < (y + 1) * 64:
                            return True
        return False
