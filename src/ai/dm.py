import os
import json
import google.generativeai as genai
# from dotenv import load_dotenv # Não é mais necessário

# ATENÇÃO: A chave de API está hardcoded como uma solução alternativa
# devido a problemas no ambiente de sandbox para carregar arquivos .env.
# Em um ambiente de produção, isso NUNCA deve ser feito.
API_KEY = "AIzaSyDs6lHIMsK_-ADbWq4ZDxzjgr1k9IJpx1k"

# Configura a API da IA
try:
    if not API_KEY:
        raise ValueError("A chave de API não está definida.")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    print("Módulo de IA configurado com sucesso.")
except Exception as e:
    print(f"Erro ao configurar a IA: {e}")
    model = None

def get_ai_response(game_state_dict: dict, player_action: str) -> dict:
    """
    Envia o estado do jogo e a ação do jogador para a IA e retorna a resposta.
    """
    if not model:
        return {
            "narration": "O mestre de jogo (IA) não está disponível no momento.",
            "state_changes": {}
        }

    # O prompt é a parte mais importante. Ele instrui a IA sobre seu papel e formato de saída.
    prompt = f"""
    Você é um Mestre de Jogo de RPG de texto, criativo, detalhado e justo.
    Sua tarefa é receber o estado atual do jogo e a ação de um jogador, e então determinar o resultado.

    REGRAS IMPORTANTES:
    1.  **Seja Descritivo:** Narre o que acontece de forma imersiva. Descreva o ambiente, os sons, os cheiros.
    2.  **Mantenha a Coerência:** O mundo deve ser consistente. Se uma porta for destruída, ela deve permanecer destruída. Ações devem ter consequências lógicas.
    3.  **Seja Justo:** As ações do jogador podem falhar. Se um jogador tentar algo impossível, descreva a falha de forma realista.
    4.  **Formato de Saída OBRIGATÓRIO:** Sua resposta DEVE ser um único bloco de código JSON, sem nenhum texto antes ou depois.
    5.  **Estrutura do JSON:** O JSON deve ter DUAS chaves no nível raiz:
        -   `narration`: (string) Uma descrição do que acontece como resultado da ação do jogador.
        -   `state_changes`: (objeto) Um objeto JSON contendo as alterações a serem aplicadas ao estado do jogo. Use notação de ponto para chaves aninhadas. Se nada mudar, retorne um objeto vazio {{}}.

    EXEMPLO DE RESPOSTA:
    ```json
    {{
      "narration": "Você avança para o leste, pisando em galhos secos. O som ecoa na floresta silenciosa. Você nota uma pequena caverna escura à sua direita.",
      "state_changes": {{
        "player.position.x": 3,
        "player.position.y": 2
      }}
    }}
    ```

    EXEMPLO 2 (Interação com item):
    ```json
    {{
      "narration": "Você come a maçã. Ela é surpreendentemente doce e revigorante. Você se sente um pouco melhor.",
      "state_changes": {{
        "inventory.remove": "Maçã",
        "player.hp.current": 11
      }}
    }}
    ```

    Agora, processe a seguinte situação:

    **ESTADO ATUAL DO JOGO:**
    ```json
    {json.dumps(game_state_dict, indent=2)}
    ```

    **AÇÃO DO JOGADOR:**
    "{player_action}"

    Qual o resultado? Responda APENAS com o bloco de código JSON.
    """

    try:
        response = model.generate_content(prompt)

        # Limpa a resposta da IA para garantir que seja um JSON válido
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "").strip()

        ai_data = json.loads(cleaned_response_text)

        # Validação mínima da estrutura da resposta
        if 'narration' not in ai_data or 'state_changes' not in ai_data:
            raise ValueError("A resposta da IA não contém as chaves 'narration' ou 'state_changes'.")

        return ai_data

    except Exception as e:
        print(f"Erro ao processar a resposta da IA: {e}")
        print(f"Resposta bruta da IA: {response.text if 'response' in locals() else 'N/A'}")
        return {
            "narration": "O mestre de jogo parece confuso com sua ação e o mundo permanece como está.",
            "state_changes": {}
        }
