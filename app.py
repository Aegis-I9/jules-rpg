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

    # 1. Obter o estado atual do jogo como um dicionário
    current_state_dict = game.to_dict()

    # 2. Chamar a IA para obter o resultado da ação
    ai_result = get_ai_response(current_state_dict, player_action)

    # 3. Aplicar as mudanças de estado retornadas pela IA
    if ai_result.get("state_changes"):
        game.apply_state_changes(ai_result["state_changes"])

    # 4. Montar a resposta final com a narração da IA e o NOVO estado do jogo
    response_data = {
        "narration": ai_result.get("narration", "O mestre parece ter se perdido em pensamentos..."),
        "gameState": game.to_dict() # Pega o estado atualizado
    }

    return jsonify(response_data)


# --- PONTO DE ENTRADA ---

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
