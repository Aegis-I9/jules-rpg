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
    3.  **Use os Sistemas de Jogo:**
        *   **Testes de Perícia:** Para ações incertas (escalar um muro, persuadir um guarda), solicite um teste de perícia. Para fazer isso, inclua a chave `"skill_check": {"attribute": "nome_do_atributo", "dc": valor_da_dificuldade}` em sua resposta. O sistema irá rolar o dado e lhe informar o resultado no próximo turno. NÃO invente o resultado do dado.
        *   **Reputação:** As reações dos NPCs devem ser influenciadas pela reputação do jogador com a facção deles. Ações contra uma facção devem diminuir a reputação. Ajuda deve aumentar. Use `"state_changes": {"reputation.Nome da Facção": -5}` para alterar a reputação.
        *   **Profissões:** Ofereça oportunidades para o jogador usar suas profissões. Se houver ervas, um jogador com Herbalismo pode tentar coletá-las. Se ele tiver reagentes, pode tentar fazer uma poção com Alquimia.
    4.  **Formato de Saída OBRIGATÓRIO:** Sua resposta DEVE ser um único bloco de código JSON, sem nenhum texto antes ou depois.
    5.  **Estrutura do JSON:** O JSON deve ter as seguintes chaves no nível raiz:
        -   `narration`: (string) Uma descrição do que acontece.
        -   `state_changes`: (objeto) Um objeto JSON com as alterações a serem aplicadas ao estado do jogo. Se nada mudar, retorne um objeto vazio `{{}}`.
        -   `skill_check`: (objeto ou null) Se um teste de perícia for necessário, preencha este campo. Caso contrário, deixe-o como `null`.

    EXEMPLO DE RESPOSTA (Movimento):
    ```json
    {
      "narration": "Você avança para o leste, pisando em galhos secos. O som ecoa na floresta silenciosa. Você nota uma pequena caverna escura à sua direita.",
      "state_changes": { "player.position.x": 3 },
      "skill_check": null
    }
    ```

    EXEMPLO 2 (Pedido de Teste de Perícia):
    ```json
    {
      "narration": "Você tenta escalar o muro de pedra lisa. É uma tarefa difícil.",
      "state_changes": {{}},
      "skill_check": { "attribute": "strength", "dc": 15 }
    }
    ```

    EXEMPLO 3 (Consequência de Ação):
    ```json
    {
      "narration": "Você ataca o guarda da cidade sem provocação. Ele saca a espada, e sua reputação com a Coroa do Rei despenca.",
      "state_changes": { "reputation.Coroa do Rei": -20 },
      "skill_check": null
    }
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
