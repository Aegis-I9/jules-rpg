class Character:
    """
    Representa o personagem do jogador no RPG.
    """
    def __init__(self, name: str, profession: str):
        self.name = name
        self.profession = profession
        self.level = 1

        # Estatísticas de Combate
        self.hp = 10
        self.max_hp = 10
        self.mp = 5
        self.max_mp = 5
        self.armor = 0
        self.resistances = {
            "physical": 0.0, # Redução de 0%
            "fire": 0.0,     # Redução de 0%
            "ice": 0.0,      # Redução de 0%
            "magic": 0.0     # Redução de 0%
        }

        # Atributos base do personagem
        self.attributes = {
            "strength": 10,
            "dexterity": 10,
            "agility": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
            "constitution": 10
        }

        # Perícias do personagem (pode ser expandido)
        self.skills = {}
        self.professions = {}

        # Inventário será adicionado depois
        self.inventory = None

        # Posição no mapa
        self.position = (0, 0)

    def __str__(self) -> str:
        return (
            f"--- Personagem: {self.name} ---\n"
            f"Nível: {self.level}\n"
            f"Profissão: {self.profession}\n\n"
            f"Atributos:\n"
            f"  Força: {self.attributes['strength']}\n"
            f"  Destreza: {self.attributes['dexterity']}\n"
            f"  Agilidade: {self.attributes['agility']}\n"
            f"  Inteligência: {self.attributes['intelligence']}\n"
        )

    def level_up(self):
        """
        Aumenta o nível do personagem.
        """
        self.level += 1
        print(f"{self.name} subiu para o nível {self.level}!")
        # No futuro, podemos adicionar lógica para aumentar atributos/perícias.

    def move(self, dx: int, dy: int):
        """
        Move o personagem no mapa.
        """
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def get_attribute_modifier(self, attribute_name: str) -> int:
        """
        Calcula o modificador de um atributo. (Ex: 14 -> +2)
        """
        if attribute_name not in self.attributes:
            return 0
        return (self.attributes[attribute_name] - 10) // 2

    def perform_check(self, attribute_to_check: str, dc: int) -> tuple[bool, int]:
        """
        Realiza um teste de atributo contra uma classe de dificuldade (DC).
        Retorna (sucesso, resultado_total_da_rolagem).
        """
        from src.game.dice import roll

        modifier = self.get_attribute_modifier(attribute_to_check)
        dice_roll = roll('1d20')
        total_roll = dice_roll + modifier

        success = total_roll >= dc

        print(f"Teste de {attribute_to_check.capitalize()}: Rolagem(1d20) = {dice_roll}, Modificador = {modifier}, Total = {total_roll} vs DC {dc}. {'Sucesso' if success else 'Falha'}.")

        return success, total_roll

    def get_total_attribute(self, attribute_name: str) -> int:
        """
        Calcula o valor total de um atributo, incluindo bônus de equipamento.
        """
        # A importação é feita aqui para evitar importação circular
        from src.items.item import Equipment

        base_value = self.attributes.get(attribute_name, 0)
        bonus = 0
        if self.inventory:
            for item in self.inventory.equipped.values():
                if item and isinstance(item, Equipment) and item.stats_bonus:
                    bonus += item.stats_bonus.get(attribute_name, 0)
        return base_value + bonus

    def take_damage(self, amount: int, damage_type: str = "physical"):
        """
        Aplica dano ao personagem, considerando armadura e resistências.
        """
        resistance_multiplier = 1.0 - self.resistances.get(damage_type, 0.0)
        damage_after_resistance = amount * resistance_multiplier

        final_damage = max(0, damage_after_resistance - self.armor)
        self.hp -= final_damage
        self.hp = max(0, self.hp) # Não deixa o HP ficar negativo
        print(f"{self.name} sofreu {final_damage:.1f} de dano! HP restante: {self.hp}/{self.max_hp}")

    def heal(self, amount: int):
        """
        Cura o personagem.
        """
        self.hp += amount
        self.hp = min(self.max_hp, self.hp) # Não deixa o HP passar do máximo
        print(f"{self.name} foi curado em {amount}! HP atual: {self.hp}/{self.max_hp}")

    def is_alive(self) -> bool:
        """
        Verifica se o personagem está vivo.
        """
        return self.hp > 0
