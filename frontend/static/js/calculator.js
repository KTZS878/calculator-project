let currentExpression = '';
let isServerOnline = false;

window.onload = function() {
    checkServerHealth();
    loadHistory();
    setInterval(checkServerHealth, 5000);
};

async function checkServerHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        if (data.status === 'ok') {
            isServerOnline = true;
            document.getElementById('status-indicator').className = 'status-dot online';
            document.getElementById('status-text').textContent = '服务器在线';
        }
    } catch (error) {
        isServerOnline = false;
        document.getElementById('status-indicator').className = 'status-dot offline';
        document.getElementById('status-text').textContent = '服务器离线';
    }
}

function appendNumber(num) {
    if (currentExpression === '0') {
        currentExpression = num;
    } else {
        currentExpression += num;
    }
    updateDisplay();
}

function appendOperator(op) {
    if (currentExpression === '') return;
    currentExpression += op;
    updateDisplay();
}

function appendFunction(func) {
    currentExpression += func + '(';
    updateDisplay();
}

function clearDisplay() {
    currentExpression = '';
    document.getElementById('expression').textContent = '0';
    document.getElementById('result').textContent = '准备就绪';
}

function deleteLastChar() {
    currentExpression = currentExpression.slice(0, -1);
    updateDisplay();
}

function updateDisplay() {
    document.getElementById('expression').textContent = currentExpression || '0';
}

async function calculate() {
    if (!currentExpression) return;
    
    if (!isServerOnline) {
        document.getElementById('result').textContent = '⚠️ 服务器未连接';
        return;
    }

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ expression: currentExpression })
        });

        const data = await response.json();
        
        if (data.result !== undefined) {
            document.getElementById('result').textContent = `= ${data.result}`;
            loadHistory();
        } else if (data.error) {
            document.getElementById('result').textContent = `❌ ${data.error}`;
        }
    } catch (error) {
        document.getElementById('result').textContent = '❌ 计算失败';
        console.error('Error:', error);
    }
}

async function loadHistory() {
    try {
        const response = await fetch('/history');
        const data = await response.json();
        
        const historyList = document.getElementById('historyList');
        
        if (data.history && data.history.length > 0) {
            historyList.innerHTML = data.history.map(item => `
                <div class="history-item" onclick="loadExpression('${item.expression}')">
                    <div class="history-expression">${item.expression}</div>
                    <div class="history-result">= ${item.result}</div>
                    <div class="history-time">${new Date(item.timestamp).toLocaleString('zh-CN')}</div>
                </div>
            `).join('');
        } else {
            historyList.innerHTML = '<p class="no-history">暂无历史记录</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

function loadExpression(expr) {
    currentExpression = expr;
    updateDisplay();
}

async function clearHistory() {
    if (!confirm('确定要清空所有历史记录吗？')) return;
    
    try {
        await fetch('/history', { method: 'DELETE' });
        loadHistory();
    } catch (error) {
        console.error('Error clearing history:', error);
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key >= '0' && event.key <= '9') {
        appendNumber(event.key);
    } else if (event.key === '.') {
        appendNumber('.');
    } else if (event.key === '+') {
        appendOperator('+');
    } else if (event.key === '-') {
        appendOperator('-');
    } else if (event.key === '*') {
        appendOperator('*');
    } else if (event.key === '/') {
        appendOperator('/');
    } else if (event.key === 'Enter') {
        calculate();
    } else if (event.key === 'Escape') {
        clearDisplay();
    } else if (event.key === 'Backspace') {
        deleteLastChar();
    }
});
