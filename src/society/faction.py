class Faction:
    """
    Representa uma facção, guilda ou grupo social no mundo do jogo.
    """
    def __init__(self, name: str, description: str, alignment: str = "neutral"):
        """
        Inicializa uma nova facção.

        Args:
            name: O nome da facção (ex: "Guilda dos Ladrões").
            description: Uma breve descrição da facção.
            alignment: O alinhamento geral da facção (ex: "chaotic_neutral").
        """
        self.name = name
        self.description = description
        self.alignment = alignment
        self.members = []  # Lista de NPCs membros importantes
        self.titles = {}   # Dicionário de títulos que a facção pode conceder

    def __str__(self) -> str:
        return f"{self.name} ({self.alignment})"
