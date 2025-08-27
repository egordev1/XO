```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Крестики-нолики</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f0f2f5;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .game-info {
            margin: 20px 0;
            font-size: 18px;
            text-align: center;
        }
        .status {
            font-size: 24px;
            font-weight: bold;
            margin: 15px 0;
            padding: 10px 20px;
            border-radius: 8px;
            background-color: #fff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .player-x { background-color: #e3f2fd; color: #1976d2; }
        .player-o { background-color: #fce4ec; color: #c62828; }
        .winner { background-color: #e8f5e8; color: #2e7d32; }
        .board {
            display: grid;
            grid-template-columns: repeat(3, 100px);
            grid-template-rows: repeat(3, 100px);
            gap: 8px;
            margin: 20px 0;
            padding: 20px;
            background-color: #333;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        .cell {
            width: 100px;
            height: 100px;
            background-color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 60px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 8px;
            transition: all 0.2s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .cell:hover {
            background-color: #f0f0f0;
            transform: scale(1.02);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .cell.x {
            color: #1976d2;
        }
        .cell.o {
            color: #c62828;
        }
        .controls {
            margin: 20px 0;
            display: flex;
            gap: 15px;
        }
        button {
            padding: 12px 24px;
            font-size: 16px;
            font-weight: bold;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        button:hover {
            background-color: #45a049;
        }
        button:active {
            transform: translateY(1px);
        }
        .score-board {
            display: flex;
            gap: 30px;
            margin: 15px 0;
            padding: 15px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .score-item {
            text-align: center;
            font-size: 18px;
        }
        .score-label {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .score-value {
            font-size: 24px;
            font-weight: bold;
        }
        .score-x { color: #1976d2; }
        .score-o { color: #c62828; }
        .score-draws { color: #666; }
        .win-animation {
            animation: pulse 0.5s ease infinite alternate;
        }
        @keyframes pulse {
            from { transform: scale(1); }
            to { transform: scale(1.05); }
        }
        .game-mode {
            margin: 15px 0;
            padding: 10px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        select {
            padding: 8px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>Крестики-нолики</h1>
    
    <div class="game-mode">
        <label for="game-mode">Режим игры: </label>
        <select id="game-mode">
            <option value="human">Человек против человека</option>
            <option value="ai-easy">Человек против ИИ (легкий)</option>
            <option value="ai-medium">Человек против ИИ (средний)</option>
            <option value="ai-hard">Человек против ИИ (сложный)</option>
        </select>
    </div>
    
    <div class="game-info">
        <div class="status" id="status">Ходит: X</div>
    </div>
    
    <div class="score-board">
        <div class="score-item">
            <div class="score-label">Игрок X</div>
            <div class="score-value score-x" id="score-x">0</div>
        </div>
        <div class="score-item">
            <div class="score-label">Ничьи</div>
            <div class="score-value score-draws" id="score-draws">0</div>
        </div>
        <div class="score-item">
            <div class="score-label">Игрок O</div>
            <div class="score-value score-o" id="score-o">0</div>
        </div>
    </div>
    
    <div class="board" id="board">
        <div class="cell" data-cell-index="0"></div>
        <div class="cell" data-cell-index="1"></div>
        <div class="cell" data-cell-index="2"></div>
        <div class="cell" data-cell-index="3"></div>
        <div class="cell" data-cell-index="4"></div>
        <div class="cell" data-cell-index="5"></div>
        <div class="cell" data-cell-index="6"></div>
        <div class="cell" data-cell-index="7"></div>
        <div class="cell" data-cell-index="8"></div>
    </div>
    
    <div class="controls">
        <button id="restart-button">Новая игра</button>
        <button id="reset-scores-button">Сбросить счет</button>
    </div>

    <script>
        class TicTacToe {
            constructor() {
                this.board = Array(9).fill('');
                this.playerX = 'X';
                this.playerO = 'O';
                this.currentPlayer = this.playerX;
                this.gameOver = false;
                this.scores = {
                    x: 0,
                    o: 0,
                    draws: 0
                };
                this.gameMode = 'human';
                
                this.winningCombinations = [
                    [0, 1, 2], [3, 4, 5], [6, 7, 8], // горизонтали
                    [0, 3, 6], [1, 4, 7], [2, 5, 8], // вертикали
                    [0, 4, 8], [2, 4, 6]             // диагонали
                ];
                
                this.initializeEventListeners();
                this.updateStatus();
                this.updateScores();
            }
            
            initializeEventListeners() {
                const cells = document.querySelectorAll('.cell');
                cells.forEach(cell => {
                    cell.addEventListener('click', (e) => {
                        const index = cell.dataset.cellIndex;
                        this.makeMove(index);
                    });
                });
                
                document.getElementById('restart-button').addEventListener('click', () => {
                    this.restartGame();
                });
                
                document.getElementById('reset-scores-button').addEventListener('click', () => {
                    this.resetScores();
                });
                
                document.getElementById('game-mode').addEventListener('change', (e) => {
                    this.gameMode = e.target.value;
                    this.restartGame();
                });
            }
            
            makeMove(index) {
                // Проверяем, можно ли сделать ход
                if (this.board[index] !== '' || this.gameOver) {
                    return;
                }
                
                // Делаем ход
                this.board[index] = this.currentPlayer;
                this.render();
                
                // Проверяем результат
                if (this.checkWin()) {
                    this.scores[this.currentPlayer.toLowerCase()]++;
                    this.gameOver = true;
                    this.updateStatus(`Победил: ${this.currentPlayer}!`);
                    this.updateScores();
                    this.highlightWinningCombination();
                    return;
                }
                
                if (this.checkDraw()) {
                    this.scores.draws++;
                    this.gameOver = true;
                    this.updateStatus('Ничья!');
                    this.updateScores();
                    return;
                }
                
                // Меняем игрока
                this.currentPlayer = this.currentPlayer === this.playerX ? this.playerO : this.playerX;
                this.updateStatus(`Ходит: ${this.currentPlayer}`);
                
                // Если играем с ИИ, делаем ход за компьютер
                if (this.gameMode !== 'human' && !this.gameOver && this.currentPlayer === this.playerO) {
                    setTimeout(() => {
                        this.makeAIMove();
                    }, 500);
                }
            }
            
            makeAIMove() {
                if (this.gameOver) return;
                
                let index;
                const difficulty = this.gameMode.split('-')[1];
                
                switch (difficulty) {
                    case 'easy':
                        index = this.getRandomMove();
                        break;
                    case 'medium':
                        // 70% шанс сделать правильный ход, 30% - случайный
                        if (Math.random() < 0.7) {
                            index = this.getSmartMove();
                        } else {
                            index = this.getRandomMove();
                        }
                        break;
                    case 'hard':
                        index = this.getBestMove();
                        break;
                    default:
                        index = this.getRandomMove();
                }
                
                this.makeMove(index);
            }
            
            getRandomMove() {
                const emptyCells = this.board.reduce((acc, cell, index) => {
                    if (cell === '') acc.push(index);
                    return acc;
                }, []);
                
                return emptyCells[Math.floor(Math.random() * emptyCells.length)];
            }
            
            getSmartMove() {
                // Проверяем, можем ли мы победить
                for (let i = 0; i < this.board.length; i++) {
                    if (this.board[i] === '') {
                        this.board[i] = this.playerO;
                        if (this.checkWinForPlayer(this.playerO)) {
                            this.board[i] = '';
                            return i;
                        }
                        this.board[i] = '';
                    }
                }
                
                // Проверяем, может ли соперник победить, и блокируем
                for (let i = 0; i < this.board.length; i++) {
                    if (this.board[i] === '') {
                        this.board[i] = this.playerX;
                        if (this.checkWinForPlayer(this.playerX)) {
                            this.board[i] = '';
                            return i;
                        }
                        this.board[i] = '';
                    }
                }
                
                // Если центр свободен, занимаем его
                if (this.board[4] === '') return 4;
                
                // Если угол свободен, занимаем его
                const corners = [0, 2, 6, 8];
                const availableCorners = corners.filter(corner => this.board[corner] === '');
                if (availableCorners.length > 0) {
                    return availableCorners[Math.floor(Math.random() * availableCorners.length)];
                }
                
                // Возвращаем случайный ход
                return this.getRandomMove();
            }
            
            getBestMove() {
                // Используем минимакс алгоритм для нахождения лучшего хода
                let bestScore = -Infinity;
                let bestMove;
                
                for (let i = 0; i < this.board.length; i++) {
                    if (this.board[i] === '') {
                        this.board[i] = this.playerO;
                        let score = this.minimax(0, false);
                        this.board[i] = '';
                        
                        if (score > bestScore) {
                            bestScore = score;
                            bestMove = i;
                        }
                    }
                }
                
                return bestMove;
            }
            
            minimax(depth, isMaximizing) {
                // Проверяем конец игры
                if (this.checkWinForPlayer(this.playerO)) return 10 - depth;
                if (this.checkWinForPlayer(this.playerX)) return depth - 10;
                if (this.board.every(cell => cell !== '')) return 0;
                
                if (isMaximizing) {
                    let bestScore = -Infinity;
                    for (let i = 0; i < this.board.length; i++) {
                        if (this.board[i] === '') {
                            this.board[i] = this.playerO;
                            let score = this.minimax(depth + 1, false);
                            this.board[i] = '';
                            bestScore = Math.max(score, bestScore);
                        }
                    }
                    return bestScore;
                } else {
                    let bestScore = Infinity;
                    for (let i = 0; i < this.board.length; i++) {
                        if (this.board[i] === '') {
                            this.board[i] = this.playerX;
                            let score = this.minimax(depth + 1, true);
                            this.board[i] = '';
                            bestScore = Math.min(score, bestScore);
                        }
                    }
                    return bestScore;
                }
            }
            
            checkWin() {
                return this.checkWinForPlayer(this.currentPlayer);
            }
            
            checkWinForPlayer(player) {
                return this.winningCombinations.some(combination => {
                    return combination.every(index => {
                        return this.board[index] === player;
                    });
                });
            }
            
            checkDraw() {
                return this.board.every(cell => cell !== '') && !this.checkWin();
            }
            
            highlightWinningCombination() {
                const winningCombo = this.winningCombinations.find(combination => {
                    return combination.every(index => {
                        return this.board[index] === this.currentPlayer;
                    });
                });
                
                if (winningCombo) {
                    winningCombo.forEach(index => {
                        const cell = document.querySelector(`[data-cell-index="${index}"]`);
                        cell.classList.add('win-animation');
                    });
                }
            }
            
            updateStatus(message) {
                const statusElement = document.getElementById('status');
                statusElement.textContent = message;
                
                // Обновляем классы для стилизации
                statusElement.className = 'status';
                if (message.includes('X')) {
                    statusElement.classList.add('player-x');
                } else if (message.includes('O')) {
                    statusElement.classList.add('player-o');
                } else if (message.includes('Победил')) {
                    statusElement.classList.add('winner');
                }
            }
            
            updateScores() {
                document.getElementById('score-x').textContent = this.scores.x;
                document.getElementById('score-o').textContent = this.scores.o;
                document.getElementById('score-draws').textContent = this.scores.draws;
            }
            
            render() {
                const cells = document.querySelectorAll('.cell');
                cells.forEach((cell, index) => {
                    cell.textContent = this.board[index];
                    cell.className = 'cell';
                    if (this.board[index] === this.playerX) {
                        cell.classList.add('x');
                    } else if (this.board[index] === this.playerO) {
                        cell.classList.add('o');
                    }
                });
            }
            
            restartGame() {
                this.board = Array(9).fill('');
                this.currentPlayer = this.playerX;
                this.gameOver = false;
                
                this.render();
                this.updateStatus(`Ходит: ${this.currentPlayer}`);
                
                // Если ИИ должен ходить первым в режиме игры с компьютером
                if (this.gameMode !== 'human' && this.currentPlayer === this.playerO) {
                    setTimeout(() => {
                        this.makeAIMove();
                    }, 500);
                }
            }
            
            resetScores() {
                this.scores = { x: 0, o: 0, draws: 0 };
                this.updateScores();
                this.restartGame();
            }
        }
        
        // Инициализация игры
        document.addEventListener('DOMContentLoaded', () => {
            new TicTacToe();
        });
    </script>
</body>
</html>
```
