from flask import Flask, render_template, request, jsonify
from src.game.game_state import GameState

# Inicialização do Flask App
app = Flask(__name__)

# --- Instância Global do Jogo ---
# Cria uma única instância do estado do jogo que persistirá enquanto
# o servidor estiver rodando.
game = GameState()
print("Instância do Jogo criada com sucesso.")


# --- ROTAS DA APLICAÇÃO ---

@app.route('/')
def index():
    """
    Serve a página principal da aplicação (index.html).
    """
    return render_template('index.html')

@app.route('/get_initial_state')
def get_initial_state():
    """
    Endpoint para fornecer o estado inicial do jogo quando a página carrega.
    """
    return jsonify(game.to_dict())

from src.ai.dm import get_ai_response

@app.route('/interact', methods=['POST'])
def interact():
    """
    Endpoint da API para receber a ação do jogador, processá-la com a IA,
    e retornar o novo estado do jogo.
    """
    data = request.get_json()
    player_action = data.get('action', '')

    if not player_action:
        return jsonify({"narration": "Você precisa dizer o que quer fazer.", "gameState": game.to_dict()}), 400

    print(f"Ação recebida do jogador: {player_action}")

    # --- Processamento de Comandos Mecânicos Especiais ---
    # Certos comandos são melhor tratados aqui do que pela IA.
    action_parts = player_action.lower().split()
    command = action_parts[0]

    if command == "identificar":
        item_name = " ".join(action_parts[1:])
        narration = "Você precisa especificar o que quer identificar." if not item_name else game.identify_item(item_name)
        return jsonify({"narration": narration, "gameState": game.to_dict()})

    elif command == "equipar":
        item_name = " ".join(action_parts[1:])
        if not item_name:
            narration = "Especifique o item que você quer equipar."
        else:
            item_to_equip = next((item for item in game.player.inventory.backpack if item.name.lower() == item_name.lower()), None)
            if item_to_equip:
                game.player.inventory.equip(game.player, item_to_equip)
                narration = f"Você equipou {item_name}."
            else:
                narration = f"Você não tem um '{item_name}' na sua mochila."
        return jsonify({"narration": narration, "gameState": game.to_dict()})

    elif command == "desequipar":
        # Mapeia nomes em português para os slots internos
        slot_map = {s.value: s for s in ItemSlot}
        slot_map.update({"anel 1": "ring_1", "anel 2": "ring_2", "brinco 1": "earring_1", "brinco 2": "earring_2"})

        slot_input = " ".join(action_parts[1:])
        if not slot_input:
            narration = "Especifique o slot que você quer desequipar (ex: cabeça, anel 1)."
        else:
            slot_to_unequip = slot_map.get(slot_input)
            if slot_to_unequip:
                game.player.inventory.unequip(game.player, slot_to_unequip)
                narration = f"Você desequipou o item do slot '{slot_input}'."
            else:
                narration = f"Slot desconhecido: '{slot_input}'."
        return jsonify({"narration": narration, "gameState": game.to_dict()})

    # 1. Obter o estado atual do jogo
    current_state_dict = game.to_dict()

    # 2. Chamar a IA para obter a resposta inicial
    ai_result = get_ai_response(current_state_dict, player_action)

    # 3. Verificar se a IA solicitou um teste de perícia
    skill_check_request = ai_result.get("skill_check")
    if skill_check_request:
        print(f"IA solicitou um teste de perícia: {skill_check_request}")
        attribute = skill_check_request.get("attribute")
        dc = skill_check_request.get("dc")

        # Realiza o teste
        success, total_roll = game.player.perform_check(attribute, dc)

        # Constrói uma nova "ação" para a IA informando o resultado do teste
        follow_up_action = (
            f"Ação original: '{player_action}'.\n"
            f"Resultado do teste de {attribute.capitalize()} (DC {dc}): {'Sucesso' if success else 'Falha'} com uma rolagem total de {total_roll}."
        )
        print(f"Enviando para a IA o resultado do teste: {follow_up_action}")

        # Chama a IA novamente com o resultado do teste
        ai_result = get_ai_response(current_state_dict, follow_up_action)

    # 4. Aplicar as mudanças de estado retornadas pela IA (da primeira ou segunda chamada)
    combat_narration = None
    if ai_result.get("state_changes"):
        combat_narration = game.apply_state_changes(ai_result["state_changes"])

    # 5. Montar a resposta final para o frontend
    final_narration = ai_result.get("narration", "O mestre parece ter se perdido em pensamentos...")
    if combat_narration:
        final_narration += f"\n\n[COMBATE] {combat_narration}"

    response_data = {
        "narration": final_narration,
        "gameState": game.to_dict() # Pega o estado sempre atualizado
    }

    return jsonify(response_data)


# --- PONTO DE ENTRADA ---

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
