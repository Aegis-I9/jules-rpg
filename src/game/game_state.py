import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.character.character import Character
from src.items.inventory import Inventory
from src.world.map import GameMap
from src.items.item import Item, Equipment, ItemSlot

class GameState:
    """
    Centraliza e gerencia todo o estado do jogo, incluindo o jogador,
    mapa, e outros elementos do mundo. Garante a persistência dos dados.
    """
    def __init__(self):
        # Inicializa os componentes do jogo
        self.player = Character(name="Jules", profession="Aventureiro")
        self.player.inventory = Inventory()

        # Adiciona itens de teste
        self.player.inventory.add_item(Equipment("Adaga de Aço", "Uma adaga simples.", ItemSlot.WEAPON))
        self.player.inventory.add_item(Item("Maçã", "Uma maçã vermelha e suculenta."))

        # Inicializa o mapa
        self.game_map = GameMap(width=20, height=10)
        self.game_map.generate_map(max_rooms=0, min_room_size=0, max_room_size=0)

        # Define uma posição inicial segura para o jogador
        self.player.position = (2, 2)
        if not self.game_map.is_walkable(self.player.position[0], self.player.position[1]):
            self.player.position = (1, 1)

    def process_action(self, action_text: str) -> str:
        """
        Processa a ação do jogador e atualiza o estado do jogo.
        Retorna uma narração do resultado da ação.

        Esta é uma implementação simples. A IA irá substituir isso.
        """
        narration = f"Você tentou: '{action_text}'. O mundo observa."

        parts = action_text.lower().split()
        command = parts[0]

        if command == "mover":
            if len(parts) > 1:
                direction = parts[1]
                dx, dy = 0, 0
                if direction == "norte": dy = -1
                elif direction == "sul": dy = 1
                elif direction == "leste": dx = 1
                elif direction == "oeste": dx = -1

                new_x = self.player.position[0] + dx
                new_y = self.player.position[1] + dy

                if self.game_map.is_walkable(new_x, new_y):
                    self.player.move(dx, dy)
                    narration = f"Você se move para o {direction}."
                else:
                    narration = "Você não pode ir por esse caminho."
            else:
                narration = "Para onde você quer se mover?"

        return narration

    def apply_state_changes(self, changes: dict):
        """
        Aplica as mudanças de estado retornadas pela IA.
        A implementação é simples e pode ser expandida.
        """
        print(f"Aplicando mudanças de estado: {changes}")
        for key, value in changes.items():
            try:
                # Exemplo simples para mover jogador
                if key == "player.position.x":
                    self.player.position = (value, self.player.position[1])
                elif key == "player.position.y":
                    self.player.position = (self.player.position[0], value)
                # Exemplo para remover item do inventário
                elif key == "inventory.remove":
                    item_to_remove = next((item for item in self.player.inventory.backpack if item.name == value), None)
                    if item_to_remove:
                        self.player.inventory.backpack.remove(item_to_remove)
                        print(f"Item '{value}' removido do inventário.")
                # Adicione mais lógicas de mudança de estado aqui
            except Exception as e:
                print(f"Erro ao aplicar a mudança de estado '{key}': {e}")


    def to_dict(self) -> dict:
        """
        Serializa o estado atual do jogo em um dicionário para ser enviado como JSON.
        """
        # Gera uma representação em string do mapa com o jogador
        map_lines = []
        for y in range(self.game_map.height):
            row = ""
            for x in range(self.game_map.width):
                if (x, y) == self.player.position:
                    row += '@'
                else:
                    row += self.game_map.grid[y][x]
            map_lines.append(row)
        map_string = "\n".join(map_lines)

        return {
            "character": {
                "name": self.player.name,
                "level": self.player.level,
                "attributes": self.player.attributes
            },
            "inventory": [item.name for item in self.player.inventory.backpack],
            "map": map_string
        }
