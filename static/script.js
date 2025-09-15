document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chat-log');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');

    // --- FUNÇÕES DE ATUALIZAÇÃO DA UI ---

    /**
     * Adiciona uma mensagem ao log de chat.
     * @param {string} sender - Quem enviou a mensagem ('Mestre' ou 'Jogador').
     * @param {string} text - O conteúdo da mensagem.
     */
    function addMessageToLog(sender, text) {
        const messageDiv = document.createElement('div');
        const p = document.createElement('p');

        if (sender === 'Jogador') {
            messageDiv.className = 'message player-message';
            p.innerHTML = `<strong>Você:</strong> ${text}`;
        } else { // Mestre ou Sistema
            messageDiv.className = 'message game-message';
            p.innerHTML = `<strong>${sender}:</strong> ${text}`;
        }

        messageDiv.appendChild(p);

        // Adiciona a nova mensagem no topo do log (pois está invertido com flex-direction)
        chatLog.prepend(messageDiv);
    }

    /**
     * Atualiza o painel de personagem com novos dados.
     * @param {object} charData - Objeto com os dados do personagem.
     */
    function updateCharacterPane(charData) {
        document.getElementById('char-name').textContent = charData.name;
        document.getElementById('char-level').textContent = charData.level;

        // Atualiza Barras de HP e MP
        const hp = charData.hp;
        const hpBarFill = document.querySelector('#hp-bar .bar-fill');
        const hpBarText = document.querySelector('#hp-bar .bar-text');
        hpBarFill.style.width = `${(hp.current / hp.max) * 100}%`;
        hpBarText.textContent = `${hp.current} / ${hp.max}`;

        const mp = charData.mp;
        const mpBarFill = document.querySelector('#mp-bar .bar-fill');
        const mpBarText = document.querySelector('#mp-bar .bar-text');
        mpBarFill.style.width = `${(mp.current / mp.max) * 100}%`;
        mpBarText.textContent = `${mp.current} / ${mp.max}`;

        // Atualiza Atributos
        document.getElementById('attr-strength').textContent = charData.attributes.strength;
        document.getElementById('attr-dexterity').textContent = charData.attributes.dexterity;
        // ... adicione outros atributos conforme necessário
    }

    /**
     * Atualiza a lista de inventário.
     * @param {object[]} inventoryItems - Array de objetos de item.
     */
    function updateInventory(inventoryItems) {
        const inventoryList = document.getElementById('inventory-list');
        inventoryList.innerHTML = ''; // Limpa a lista atual
        inventoryItems.forEach(item => {
            const li = document.createElement('li');

            const itemName = document.createElement('span');
            itemName.className = 'item-name';
            itemName.textContent = item.name;

            const itemAscii = document.createElement('pre');
            itemAscii.className = 'item-ascii';
            itemAscii.textContent = item.ascii || ''; // Usa a arte ASCII ou string vazia

            li.appendChild(itemAscii);
            li.appendChild(itemName);
            inventoryList.appendChild(li);
        });
    }

    /**
     * Atualiza o mini-mapa.
     * @param {string} mapString - String ASCII do mapa.
     */
    function updateMap(mapString) {
        document.getElementById('mini-map').textContent = mapString;
    }


    // --- LÓGICA DE INTERAÇÃO COM O BACKEND ---

    /**
     * Envia a ação do jogador para o backend e processa a resposta.
     * @param {string} actionText - A ação digitada pelo jogador.
     */
    async function sendAction(actionText) {
        addMessageToLog('Jogador', actionText);
        chatInput.value = ''; // Limpa o input

        try {
            const response = await fetch('/interact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ action: actionText }),
            });

            if (!response.ok) {
                throw new Error(`Erro na comunicação com o servidor: ${response.statusText}`);
            }

            const data = await response.json();

            // Adiciona a narração do mestre ao log
            if (data.narration) {
                addMessageToLog('Mestre', data.narration);
            }

            // Atualiza os painéis da UI com os novos dados do estado do jogo
            if (data.gameState) {
                updateCharacterPane(data.gameState.character);
                updateInventory(data.gameState.inventory);
                updateMap(data.gameState.map);
            }

        } catch (error) {
            console.error('Falha ao enviar ação:', error);
            addMessageToLog('Sistema', 'Não foi possível conectar ao mundo. Tente novamente mais tarde.');
        }
    }

    /**
     * Carrega o estado inicial do jogo a partir do backend.
     */
    async function initializeGame() {
        try {
            const response = await fetch('/get_initial_state');
            if (!response.ok) {
                throw new Error('Falha ao carregar o estado inicial do jogo.');
            }
            const initialState = await response.json();
            updateCharacterPane(initialState.character);
            updateInventory(initialState.inventory);
            updateMap(initialState.map);
            addMessageToLog('Mestre', 'Bem-vindo! O mundo foi carregado. O que você faz?');
        } catch (error) {
            console.error('Erro na inicialização:', error);
            addMessageToLog('Sistema', 'Não foi possível carregar o mundo.');
        }
    }

    // --- EVENT LISTENERS ---

    chatForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const actionText = chatInput.value.trim();
        if (actionText) {
            sendAction(actionText);
        }
    });

    // Inicia o jogo ao carregar a página
    initializeGame();
});
