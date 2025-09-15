from .item import Item, Equipment, ItemSlot

class Inventory:
    """
    Gerencia o inventário do personagem, incluindo itens na mochila e equipamentos.
    """
    def __init__(self):
        # Itens não equipados na mochila
        self.backpack = []

        # Dicionário para os itens equipados
        self.equipped = {
            ItemSlot.HEAD: None,
            ItemSlot.CHEST: None,
            ItemSlot.LEGS: None,
            ItemSlot.BOOTS: None,
            ItemSlot.GLOVES: None,

            # Slots duplicados
            "ring_1": None,
            "ring_2": None,
            "earring_1": None,
            "earring_2": None,

            ItemSlot.BELT: None,
            ItemSlot.FACE: None,
            ItemSlot.WEAPON: None,
        }

    def add_item(self, item: Item):
        """
        Adiciona um item à mochila.
        """
        self.backpack.append(item)
        print(f"'{item.name}' foi adicionado à sua mochila.")

    def equip(self, character, item_to_equip: Equipment):
        """
        Equipa um item da mochila, aplicando seus bônus ao personagem.
        """
        if not isinstance(item_to_equip, Equipment):
            print(f"'{item_to_equip.name}' não é um item equipável.")
            return
        if item_to_equip not in self.backpack:
            print(f"'{item_to_equip.name}' não está na sua mochila.")
            return

        # Unequip item if slot is occupied
        slot_to_fill = self._get_slot_to_fill(item_to_equip.slot)
        if not slot_to_fill:
            print(f"Todos os slots para '{item_to_equip.slot.value}' estão ocupados.")
            return

        if self.equipped[slot_to_fill]:
            self.unequip(character, slot_to_fill)

        # Equip new item
        self.equipped[slot_to_fill] = item_to_equip
        self.backpack.remove(item_to_equip)
        self._apply_item_bonus(character, item_to_equip)
        print(f"'{item_to_equip.name}' equipado.")

    def unequip(self, character, slot_to_unequip):
        """
        Desequipa um item, removendo seus bônus e movendo-o para a mochila.
        """
        item = self.equipped.get(slot_to_unequip)
        if not item:
            print(f"Nenhum item equipado no slot '{slot_to_unequip}'.")
            return

        self._remove_item_bonus(character, item)
        self.add_item(item)
        self.equipped[slot_to_unequip] = None
        print(f"'{item.name}' desequipado.")

    def _get_slot_to_fill(self, slot: ItemSlot):
        """Helper para encontrar um slot vago, especialmente para anéis e brincos."""
        if slot == ItemSlot.RING:
            if self.equipped["ring_1"] is None: return "ring_1"
            if self.equipped["ring_2"] is None: return "ring_2"
        elif slot == ItemSlot.EARRING:
            if self.equipped["earring_1"] is None: return "earring_1"
            if self.equipped["earring_2"] is None: return "earring_2"
        elif slot in self.equipped:
            return slot
        return None

    def _apply_item_bonus(self, character, item: Equipment):
        """Aplica os bônus de um item ao personagem."""
        if not item.stats_bonus: return
        for stat, value in item.stats_bonus.items():
            if hasattr(character, stat):
                setattr(character, stat, getattr(character, stat) + value)
            elif stat in character.attributes:
                character.attributes[stat] += value
            print(f"Aplicando bônus: +{value} {stat}")

    def _remove_item_bonus(self, character, item: Equipment):
        """Remove os bônus de um item do personagem."""
        if not item.stats_bonus: return
        for stat, value in item.stats_bonus.items():
            if hasattr(character, stat):
                setattr(character, stat, getattr(character, stat) - value)
            elif stat in character.attributes:
                character.attributes[stat] -= value
            print(f"Removendo bônus: -{value} {stat}")

    def __str__(self) -> str:
        """
        Retorna uma representação do inventário em string.
        """
        # Exibe itens equipados
        equipped_str = "--- Equipamento ---\n"
        for slot, item in self.equipped.items():
            slot_name = slot.value if isinstance(slot, ItemSlot) else slot
            item_name = item.name if item else "Vazio"
            equipped_str += f"{slot_name.capitalize()}: {item_name}\n"

        # Exibe itens na mochila
        backpack_str = "\n--- Mochila ---\n"
        if not self.backpack:
            backpack_str += "Sua mochila está vazia.\n"
        else:
            for item in self.backpack:
                backpack_str += f"- {item.name}\n"

        return equipped_str + backpack_str
