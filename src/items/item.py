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
    Classe base para todos os itens do jogo, agora com mais detalhes.
    """
    def __init__(self, name: str, description: str, quality: str = 'comum',
                 item_level: int = 1, is_identified: bool = True,
                 lore_description: str = None, ascii_art: str = None, value: int = 0):
        self.name = name
        self.description = description
        self.quality = quality
        self.item_level = item_level
        self.is_identified = is_identified
        self.lore_description = lore_description
        self.ascii_art = ascii_art
        self.value = value

    def __str__(self) -> str:
        if not self.is_identified:
            return f"Item Não Identificado ({self.quality})"
        return f"{self.name} (Nível {self.item_level}, {self.quality})"

class Equipment(Item):
    """
    Classe para itens que podem ser equipados.
    """
    def __init__(self, name: str, description: str, slot: ItemSlot, stats_bonus: dict = None, **kwargs):
        super().__init__(name, description, **kwargs)
        self.slot = slot
        self.stats_bonus = stats_bonus if stats_bonus else {}

    def __str__(self) -> str:
        if not self.is_identified:
            return f"Equipamento Não Identificado ({self.quality})"
        return f"{self.name} ({self.slot.value}) - Bônus: {self.stats_bonus}"

class Reagent(Item):
    """
    Classe para reagentes de crafting e alquimia.
    """
    def __init__(self, name: str, description: str, value: int = 1):
        super().__init__(name, description, value)

class Herb(Reagent):
    """
    Classe específica para ervas coletadas com Herbalismo.
    """
    def __init__(self, name: str, description: str, value: int = 2):
        super().__init__(name, description, value)

class Potion(Item):
    """
    Classe para poções criadas com Alquimia.
    """
    def __init__(self, name: str, description: str, effect: dict, value: int = 10):
        super().__init__(name, description, value)
        # Exemplo de efeito: {"type": "heal", "amount": 20}
        self.effect = effect
