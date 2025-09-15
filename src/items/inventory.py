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

    def equip(self, item_to_equip: Equipment):
        """
        Equipa um item da mochila.
        """
        if not isinstance(item_to_equip, Equipment):
            print(f"'{item_to_equip.name}' não é um item equipável.")
            return

        if item_to_equip not in self.backpack:
            print(f"'{item_to_equip.name}' não está na sua mochila.")
            return

        slot = item_to_equip.slot

        # Lógica para slots duplicados (anéis e brincos)
        if slot == ItemSlot.RING:
            if self.equipped["ring_1"] is None:
                self.equipped["ring_1"] = item_to_equip
                self.backpack.remove(item_to_equip)
                print(f"'{item_to_equip.name}' equipado no anel 1.")
            elif self.equipped["ring_2"] is None:
                self.equipped["ring_2"] = item_to_equip
                self.backpack.remove(item_to_equip)
                print(f"'{item_to_equip.name}' equipado no anel 2.")
            else:
                print("Ambos os slots de anel estão ocupados.")
        elif slot == ItemSlot.EARRING:
            if self.equipped["earring_1"] is None:
                self.equipped["earring_1"] = item_to_equip
                self.backpack.remove(item_to_equip)
                print(f"'{item_to_equip.name}' equipado no brinco 1.")
            elif self.equipped["earring_2"] is None:
                self.equipped["earring_2"] = item_to_equip
                self.backpack.remove(item_to_equip)
                print(f"'{item_to_equip.name}' equipado no brinco 2.")
            else:
                print("Ambos os slots de brinco estão ocupados.")
        # Lógica para slots únicos
        elif self.equipped.get(slot) is None:
            self.equipped[slot] = item_to_equip
            self.backpack.remove(item_to_equip)
            print(f"'{item_to_equip.name}' equipado.")
        else:
            print(f"O slot '{slot.value}' já está ocupado.")

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
