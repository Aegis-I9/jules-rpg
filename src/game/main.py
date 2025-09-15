# Adicionando o path para imports funcionarem
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from character.character import Character
from items.inventory import Inventory
from world.map import GameMap
from items.item import Item, Equipment, ItemSlot

def main():
    """
    Função principal que executa o loop do jogo.
    """
    # --- Setup Inicial ---
    player_name = input("Digite o nome do seu personagem: ")
    player = Character(name=player_name, profession="Aventureiro")
    player.inventory = Inventory()

    # Adiciona alguns itens para teste
    espada_longa = Equipment("Espada Longa", "Uma espada de ferro.", ItemSlot.WEAPON, stats_bonus={"strength": 2})
    escudo_madeira = Equipment("Escudo de Madeira", "Um escudo simples.", ItemSlot.WEAPON, stats_bonus={"constitution": 1}) # Sim, pode ser arma também
    pocao_cura = Item("Poção de Cura", "Restaura um pouco de vida.", value=10)

    player.inventory.add_item(espada_longa)
    player.inventory.add_item(escudo_madeira)
    player.inventory.add_item(pocao_cura)

    # Cria e gera o mapa
    game_map = GameMap(width=20, height=15)
    game_map.generate_map(max_rooms=0, min_room_size=0, max_room_size=0) # Args não são usados ainda

    # Coloca o jogador em uma posição inicial válida
    player.position = (2, 2)
    if not game_map.is_walkable(player.position[0], player.position[1]):
        player.position = (1,1) # Posição segura

    print(f"\nBem-vindo ao nosso RPG, {player.name}!")
    print("Você se encontra em uma área desconhecida. Use comandos para interagir com o mundo.")
    print("Comandos disponíveis: 'mover [norte/sul/leste/oeste]', 'mapa', 'inventario', 'equipar [nome do item]', 'sair'.")

    # --- Loop Principal do Jogo ---
    while True:
        try:
            command = input("\n> ").lower().strip()
            parts = command.split()
            keyword = parts[0]

            if keyword == "sair":
                print("Obrigado por jogar!")
                break

            elif keyword == "mapa":
                game_map.display_map(player.position)

            elif keyword == "inventario":
                print(player.inventory)

            elif keyword == "equipar":
                if len(parts) < 2:
                    print("Uso: equipar [nome do item]")
                    continue
                item_name = " ".join(parts[1:])
                item_to_equip = next((item for item in player.inventory.backpack if item.name.lower() == item_name), None)
                if item_to_equip:
                    player.inventory.equip(item_to_equip)
                else:
                    print(f"Item '{item_name}' não encontrado na mochila.")

            elif keyword == "mover":
                if len(parts) < 2:
                    print("Uso: mover [norte/sul/leste/oeste]")
                    continue

                direction = parts[1]
                dx, dy = 0, 0
                if direction == "norte":
                    dy = -1
                elif direction == "sul":
                    dy = 1
                elif direction == "leste":
                    dx = 1
                elif direction == "oeste":
                    dx = -1
                else:
                    print(f"Direção '{direction}' desconhecida.")
                    continue

                new_x, new_y = player.position[0] + dx, player.position[1] + dy
                if game_map.is_walkable(new_x, new_y):
                    player.move(dx, dy)
                    print(f"Você se moveu para o {direction}.")
                    # game_map.display_map(player.position) # Opcional: mostrar mapa após mover
                else:
                    print("Você não pode ir por aí, há um obstáculo.")

            else:
                print("Comando desconhecido.")

        except (KeyboardInterrupt, EOFError):
            print("\nObrigado por jogar!")
            break

if __name__ == "__main__":
    main()
