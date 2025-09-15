class Character:
    """
    Representa o personagem do jogador no RPG.
    """
    def __init__(self, name: str, profession: str):
        self.name = name
        self.profession = profession
        self.level = 1

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
