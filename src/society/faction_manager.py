from .faction import Faction

class FactionManager:
    """
    Gerencia todas as facções do jogo e a reputação do jogador com elas.
    """
    def __init__(self):
        self.factions = self._initialize_factions()
        # A reputação é um dicionário mapeando o nome da facção para um valor inteiro.
        self.reputations = {name: 0 for name in self.factions.keys()}

    def _initialize_factions(self) -> dict[str, Faction]:
        """
        Cria as facções iniciais do mundo.
        """
        factions_data = {
            "Guilda dos Mercadores": Faction(
                name="Guilda dos Mercadores",
                description="Uma organização poderosa que controla o comércio na região.",
                alignment="lawful_neutral"
            ),
            "Guardiões da Floresta": Faction(
                name="Guardiões da Floresta",
                description="Um grupo recluso de druidas e patrulheiros que protegem a natureza.",
                alignment="neutral_good"
            ),
            "Coroa do Rei": Faction(
                name="Coroa do Rei",
                description="A nobreza e os cavaleiros leais ao Rei Eldred.",
                alignment="lawful_good"
            ),
            "Os Despojados": Faction(
                name="Os Despojados",
                description="Uma guilda de ladrões e espiões que opera nas sombras da cidade.",
                alignment="chaotic_neutral"
            )
        }
        return factions_data

    def get_reputation(self, faction_name: str) -> int:
        """
        Retorna a reputação do jogador com uma facção específica.
        """
        return self.reputations.get(faction_name, 0)

    def change_reputation(self, faction_name: str, amount: int):
        """
        Altera a reputação do jogador com uma facção.
        """
        if faction_name in self.reputations:
            self.reputations[faction_name] += amount
            print(f"Sua reputação com '{faction_name}' mudou em {amount}. Novo valor: {self.reputations[faction_name]}")
        else:
            print(f"Facção desconhecida: '{faction_name}'")

    def get_all_reputations(self) -> dict:
        """
        Retorna um dicionário com todas as reputações do jogador.
        """
        return self.reputations
