# 🧮 Calculator Project

一个基于 Python Flask + C 的高性能计算器 Web 应用。

## 📊 架构

用户浏览器 → Gunicorn → Flask → C 计算引擎 → SQLite 数据库

## 🚀 技术栈

- 前端: HTML5 + CSS3 + JavaScript
- 后端: Python Flask
- 计算引擎: C
- Web 服务器: Gunicorn
- 数据库: SQLite

## 📦 项目结构

calculator-project/
├── README.md
├── LICENSE
├── .gitignore
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── calculator.service
├── calculator/
│   ├── calculator.c
│   └── Makefile
└── frontend/
    ├── templates/
    │   └── index.html
    └── static/
        ├── css/style.css
        └── js/calculator.js

## 🛠️ 快速开始

1. 克隆项目
git clone git@github.com:你的用户名/calculator-project.git
cd calculator-project

2. 编译 C 程序
cd calculator
make
cd ..

3. 安装依赖
cd backend
pip3 install -r requirements.txt

4. 运行
python3 app.py

## ✨ 功能特性

- 基本四则运算
- 高级运算（幂、开方、三角函数）
- 计算历史记录
- 响应式设计

## 📝 License

MIT License
