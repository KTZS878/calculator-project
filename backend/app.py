from flask import Flask, render_template, request, jsonify
import subprocess
import sqlite3
import logging
from datetime import datetime
import os

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# C程序路径
CALCULATOR_PATH = "/root/calculator/calculator"

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  expression TEXT NOT NULL,
                  result TEXT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()
    logger.info("✅ 数据库初始化完成")

# 启动时初始化数据库
init_db()

@app.route('/')
def index():
    """首页"""
    logger.info("访问首页")
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """计算接口"""
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()

        if not expression:
            return jsonify({'error': '表达式不能为空'}), 400

        logger.info(f"📥 计算表达式: {expression}")

        # 调用C程序
        process = subprocess.Popen(
            [CALCULATOR_PATH, expression],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate(timeout=5)
        stdout = stdout.decode('utf-8').strip()
        stderr = stderr.decode('utf-8').strip()

        if process.returncode == 0:
            logger.info(f"✅ 计算结果: {stdout}")
            
            # 💾 保存到数据库
            try:
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                c.execute('INSERT INTO history (expression, result) VALUES (?, ?)',
                          (expression, stdout))
                conn.commit()
                row_id = c.lastrowid
                conn.close()
                logger.info(f"💾 已保存到数据库 (ID: {row_id})")
            except Exception as db_error:
                logger.error(f"❌ 数据库保存失败: {db_error}")
            
            return jsonify({'result': stdout, 'expression': expression})
        else:
            error_msg = stderr or '计算错误'
            logger.error(f"❌ 计算错误: {error_msg}")
            return jsonify({'error': error_msg}), 400

    except subprocess.TimeoutExpired:
        process.kill()
        logger.error("⏱️ 计算超时")
        return jsonify({'error': '计算超时'}), 408
    except Exception as e:
        logger.error(f"💥 异常: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """获取历史记录"""
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT expression, result, timestamp FROM history ORDER BY id DESC LIMIT 20')
        rows = c.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'expression': row[0],
                'result': row[1],
                'timestamp': row[2]
            })
        
        logger.info(f"📜 返回 {len(history)} 条历史记录")
        
        return jsonify({'history': history})
    
    except Exception as e:
        logger.error(f"❌ 获取历史失败: {str(e)}")
        return jsonify({'error': str(e), 'history': []}), 500

@app.route('/history', methods=['DELETE'])
def clear_history():
    """清空历史记录"""
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DELETE FROM history')
        deleted = c.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"🗑️ 已清空 {deleted} 条历史记录")
        
        return jsonify({'message': f'已清空 {deleted} 条历史记录'})
    
    except Exception as e:
        logger.error(f"❌ 清空历史失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'service': 'calculator'})

if __name__ == '__main__':
    # 检查C程序是否存在
    if not os.path.exists(CALCULATOR_PATH):
        logger.error(f"C程序不存在: {CALCULATOR_PATH}")
        exit(1)

    logger.info("=" * 50)
    logger.info("🚀 计算器服务启动")
    logger.info(f"📂 C程序路径: {CALCULATOR_PATH}")
    logger.info(f"🌐 监听地址: 0.0.0.0:5000")
    logger.info("=" * 50)

    app.run(host='0.0.0.0', port=5000, debug=False)
