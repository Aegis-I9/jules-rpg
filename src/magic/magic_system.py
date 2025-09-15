class MagicSystem:
    """
    Gerencia o sistema de magias do jogo.
    No futuro, irá lidar com a construção de magias por palavras,
    verificação de mana, e execução dos efeitos.
    """
    def __init__(self):
        self.known_words = {
            "exura": "cura",
            "vita": "vida",
            "flam": "fogo",
            "vis": "projétil"
        }

    def cast_spell(self, spell_words: str):
        """
        Tenta conjurar uma magia a partir das palavras fornecidas.
        """
        words = spell_words.lower().split()
        print(f"Tentando conjurar uma magia com as palavras: {words}")
        # Lógica futura para combinar palavras e criar efeitos.
        pass
