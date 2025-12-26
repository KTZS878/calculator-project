#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define MAX 100

typedef struct {
    int data[MAX];
    int top;
} Stack;

void init(Stack *s) {
    s->top = -1;
}

int isEmpty(Stack *s) {
    return s->top == -1;
}

void push(Stack *s, int value) {
    if (s->top < MAX - 1) {
        s->data[++(s->top)] = value;
    }
}

int pop(Stack *s) {
    if (!isEmpty(s)) {
        return s->data[(s->top)--];
    }
    return 0;
}

int peek(Stack *s) {
    if (!isEmpty(s)) {
        return s->data[s->top];
    }
    return 0;
}

int precedence(char op) {
    if (op == '+' || op == '-') return 1;
    if (op == '*' || op == '/') return 2;
    return 0;
}

int applyOp(int a, int b, char op) {
    switch(op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return b != 0 ? a / b : 0;
    }
    return 0;
}

int evaluate(char* expr) {
    Stack values, ops;
    init(&values);
    init(&ops);
    
    int i = 0;
    while (expr[i] != '\0') {
        if (expr[i] == ' ') {
            i++;
            continue;
        }
        
        if (isdigit(expr[i])) {
            int val = 0;
            while (i < strlen(expr) && isdigit(expr[i])) {
                val = val * 10 + (expr[i] - '0');
                i++;
            }
            push(&values, val);
            continue;
        }
        
        if (expr[i] == '(') {
            push(&ops, expr[i]);
        }
        else if (expr[i] == ')') {
            while (!isEmpty(&ops) && peek(&ops) != '(') {
                int val2 = pop(&values);
                int val1 = pop(&values);
                char op = pop(&ops);
                push(&values, applyOp(val1, val2, op));
            }
            if (!isEmpty(&ops)) pop(&ops);
        }
        else if (expr[i] == '+' || expr[i] == '-' || 
                 expr[i] == '*' || expr[i] == '/') {
            while (!isEmpty(&ops) && precedence(peek(&ops)) >= precedence(expr[i])) {
                int val2 = pop(&values);
                int val1 = pop(&values);
                char op = pop(&ops);
                push(&values, applyOp(val1, val2, op));
            }
            push(&ops, expr[i]);
        }
        i++;
    }
    
    while (!isEmpty(&ops)) {
        int val2 = pop(&values);
        int val1 = pop(&values);
        char op = pop(&ops);
        push(&values, applyOp(val1, val2, op));
    }
    
    return pop(&values);
}

int main(int argc, char *argv[]) {
    // 支持两种模式：
    // 1. 命令行参数模式：./calculator "1+2*3"
    // 2. 交互模式：./calculator
    
    if (argc > 1) {
        // 命令行模式（用于 Web 调用）
        int result = evaluate(argv[1]);
        printf("%d", result);  // 只输出数字，方便解析
        return 0;
    }
    
    // 交互模式
    char expr[MAX];
    printf("简单计算器 (支持 +, -, *, /, 括号)\n");
    printf("输入 'quit' 退出\n\n");
    
    while (1) {
        printf("请输入表达式: ");
        if (fgets(expr, MAX, stdin) == NULL) break;
        
        expr[strcspn(expr, "\n")] = 0;
        
        if (strcmp(expr, "quit") == 0) {
            printf("再见!\n");
            break;
        }
        
        int result = evaluate(expr);
        printf("结果: %d\n\n", result);
    }
    
    return 0;
}
