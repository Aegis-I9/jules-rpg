class CraftingSystem:
    """
    Gerencia o sistema de criação de itens (crafting).
    No futuro, irá conter as receitas e a lógica para combinar
    itens e criar novos.
    """
    def __init__(self):
        self.recipes = {
            ("galho", "pedra apontada"): "lança",
            ("couro", "tiras de couro"): "armadura de couro"
        }

    def craft_item(self, materials: list):
        """
        Tenta criar um item a partir de uma lista de materiais.
        """
        # A chave da receita precisa ser ordenada para funcionar independentemente da ordem
        sorted_materials = tuple(sorted(materials))

        if sorted_materials in self.recipes:
            new_item_name = self.recipes[sorted_materials]
            print(f"Você criou: {new_item_name}!")
            # Lógica futura para criar o objeto Item e adicioná-lo ao inventário.
            return new_item_name
        else:
            print("Você não conseguiu criar nada com esses materiais.")
            return None
