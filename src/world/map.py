import random

class GameMap:
    """
    Representa o mapa do jogo, com sua grade e tiles.
    """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = self._initialize_grid()

    def _initialize_grid(self) -> list:
        """
        Cria a grade inicial do mapa, preenchida com chão.
        """
        return [['.' for _ in range(self.width)] for _ in range(self.height)]

    def generate_map(self, max_rooms: int, min_room_size: int, max_room_size: int):
        """
        Gera um mapa mais interessante com salas e corredores (simplificado).
        Por enquanto, vamos adicionar apenas algumas paredes aleatórias para teste.
        """
        for y in range(self.height):
            for x in range(self.width):
                # Coloca paredes nas bordas
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    self.grid[y][x] = '#'
                # Adiciona alguns obstáculos aleatórios
                elif random.random() < 0.1:
                    self.grid[y][x] = '#'

    def is_walkable(self, x: int, y: int) -> bool:
        """
        Verifica se um tile no mapa é caminhável.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x] == '.'
        return False

    def display_map(self, player_position: tuple = None):
        """
        Exibe o mapa no console, opcionalmente mostrando a posição do jogador.
        """
        map_str = ""
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if player_position and (x, y) == player_position:
                    row += '@'
                else:
                    row += self.grid[y][x]
            map_str += row + '\n'

        print(map_str)
