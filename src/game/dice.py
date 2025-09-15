import random
import re

def roll(expression: str) -> int:
    """
    Rola dados com base em uma expressão no formato 'NdM+X' ou 'NdM-X'.
    Exemplos: '1d20', '2d6+3', '1d8-1'.

    Args:
        expression: A string da expressão dos dados.

    Returns:
        O resultado total da rolagem.
    """
    # Regex para capturar (N)d(M) e o modificador opcional (+/- X)
    match = re.match(r'(\d+)d(\d+)([+\-]\d+)?', expression.lower())

    if not match:
        raise ValueError(f"Expressão de dados inválida: '{expression}'")

    num_dice = int(match.group(1))
    die_type = int(match.group(2))
    modifier_str = match.group(3)

    modifier = 0
    if modifier_str:
        modifier = int(modifier_str)

    total = sum(random.randint(1, die_type) for _ in range(num_dice))

    return total + modifier

# Exemplos de uso (para teste)
if __name__ == '__main__':
    print(f"Rolando 1d20: {roll('1d20')}")
    print(f"Rolando 2d6+5: {roll('2d6+5')}")
    print(f"Rolando 1d8-2: {roll('1d8-2')}")
    try:
        roll('d20')
    except ValueError as e:
        print(e)
