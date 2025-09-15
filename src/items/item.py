from enum import Enum

class ItemSlot(Enum):
    """
    Enum para os slots de equipamento disponíveis.
    """
    HEAD = "cabeça"
    CHEST = "peito"
    LEGS = "calça"
    BOOTS = "bota"
    GLOVES = "luva"
    RING = "anel"
    EARRING = "brinco"
    BELT = "cinto"
    FACE = "rosto"
    WEAPON = "arma" # Adicionando um slot para arma

class Item:
    """
    Classe base para todos os itens do jogo.
    """
    def __init__(self, name: str, description: str, value: int = 0):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

class Equipment(Item):
    """
    Classe para itens que podem ser equipados.
    """
    def __init__(self, name: str, description: str, slot: ItemSlot, stats_bonus: dict = None, value: int = 0):
        super().__init__(name, description, value)
        self.slot = slot
        self.stats_bonus = stats_bonus if stats_bonus else {}

    def __str__(self) -> str:
        return f"{self.name} ({self.slot.value}) - Bônus: {self.stats_bonus}"
