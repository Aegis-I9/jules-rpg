from src.items.item import Item

class Recipe:
    """
    Define uma receita para crafting ou alquimia.
    """
    def __init__(self, name: str, required_reagents: dict[str, int], output_item: Item):
        """
        Args:
            name: Nome da receita (ex: "Criar Poção de Cura Menor").
            required_reagents: Dicionário onde a chave é o nome do reagente e o valor é a quantidade.
            output_item: O objeto Item que é criado.
        """
        self.name = name
        self.required_reagents = required_reagents
        self.output_item = output_item

class Profession:
    """
    Classe base para todas as profissões.
    """
    def __init__(self, name: str, description: str, level: int = 1):
        self.name = name
        self.description = description
        self.level = level
        self.recipes = []

    def add_recipe(self, recipe: Recipe):
        """
        Adiciona uma nova receita à lista de receitas conhecidas da profissão.
        """
        self.recipes.append(recipe)

class Herbalism(Profession):
    """
    Profissão de Herbalismo, focada em coletar ervas.
    """
    def __init__(self):
        super().__init__("Herbalismo", "A arte de identificar e coletar ervas raras.")
        # Herbalismo pode não ter "receitas", mas sim a habilidade de encontrar reagentes.
        # A lógica de coleta seria um teste de perícia.

class Alchemy(Profession):
    """
    Profissão de Alquimia, focada em criar poções.
    """
    def __init__(self):
        super().__init__("Alquimia", "A ciência de misturar reagentes para criar poções e elixires.")
        self._initialize_recipes()

    def _initialize_recipes(self):
        from src.items.item import Potion, Herb

        # Receita de exemplo
        pocao_cura_menor = Potion("Poção de Cura Menor", "Restaura 10 pontos de vida.", {"type": "heal", "amount": 10})
        receita_cura = Recipe(
            name="Poção de Cura Menor",
            required_reagents={"Folha da Serra": 2, "Água Purificada": 1},
            output_item=pocao_cura_menor
        )
        self.add_recipe(receita_cura)
