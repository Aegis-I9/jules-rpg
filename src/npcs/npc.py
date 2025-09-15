# Adicionando o path para imports funcionarem
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from character.character import Character

class NPC(Character):
    """
    Representa um Personagem Não-Jogador (NPC) no jogo.
    Herda da classe Character e pode ter comportamentos adicionais,
    como diálogos, quests ou padrões de combate.
    """
    def __init__(self, name: str, profession: str, dialog: str = None):
        super().__init__(name, profession)
        self.dialog = dialog if dialog else "..."

    def talk(self) -> str:
        """
        Retorna a fala do NPC.
        """
        return f"{self.name} diz: '{self.dialog}'"
