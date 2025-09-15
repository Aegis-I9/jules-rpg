import random
from .item import Item, Equipment, Potion, Herb, ItemSlot
from .ascii_generator import generate_ascii_for_item

def create_random_item(item_level: int) -> Item:
    """
    Cria um item aleatório com base em um nível de item.
    """
    # Exemplo simples de criação de item. Isso pode ser expandido com tabelas de loot.
    item_type = random.choice(['potion', 'equipment', 'herb'])

    if item_type == 'potion':
        return create_random_potion(item_level)
    elif item_type == 'equipment':
        return create_random_equipment(item_level)
    else: # herb
        return create_random_herb(item_level)

def create_random_potion(item_level: int) -> Potion:
    potion_name = "Poção de Cura"
    quality = random.choice(['fraca', 'comum', 'forte'])

    if quality == 'fraca':
        heal_amount = 10 + item_level
    elif quality == 'comum':
        heal_amount = 20 + (item_level * 2)
    else: # forte
        heal_amount = 30 + (item_level * 3)

    potion = Potion(
        name=f"{potion_name} {quality.capitalize()}",
        description=f"Restaura {heal_amount} pontos de vida.",
        effect={"type": "heal", "amount": heal_amount},
        quality=quality,
        item_level=item_level,
        is_identified=False # Poções precisam ser identificadas
    )
    potion.ascii_art = generate_ascii_for_item(potion)
    return potion

def create_random_equipment(item_level: int) -> Equipment:
    qualities = ['quebrado', 'comum', 'bom', 'obra-prima', 'lendário']
    quality_weights = [0.2, 0.5, 0.2, 0.08, 0.02]
    quality = random.choices(qualities, quality_weights)[0]

    item_types = {
        "Espada": ItemSlot.WEAPON,
        "Elmo": ItemSlot.HEAD,
        "Peitoral": ItemSlot.CHEST
    }
    item_name_base, slot = random.choice(list(item_types.items()))

    # Bônus baseado na qualidade e nível
    stats_bonus = {}
    if quality == 'bom':
        stats_bonus = {"strength": item_level}
    elif quality == 'obra-prima':
        stats_bonus = {"strength": item_level, "dexterity": item_level}
    elif quality == 'lendário':
        stats_bonus = {"strength": item_level * 2, "dexterity": item_level * 2, "constitution": item_level}

    equipment = Equipment(
        name=f"{item_name_base} de {quality.capitalize()}",
        description=f"Um(a) {item_name_base.lower()} de qualidade {quality}.",
        slot=slot,
        stats_bonus=stats_bonus,
        quality=quality,
        item_level=item_level,
        is_identified=False # Equipamentos mágicos/de alta qualidade precisam ser identificados
    )
    equipment.ascii_art = generate_ascii_for_item(equipment)
    return equipment

def create_random_herb(item_level: int) -> Herb:
    herb_name = random.choice(["Folha da Serra", "Raiz-de-sangue", "Flor-do-gelo"])
    herb = Herb(
        name=herb_name,
        description="Uma erva com propriedades medicinais.",
        item_level=item_level
        # Ervas são geralmente identificadas na coleta
    )
    herb.ascii_art = generate_ascii_for_item(herb)
    return herb
