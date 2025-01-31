package com.example.calculator.domain.usecase

import com.example.calculator.domain.model.CalculatorState
import java.util.Stack
import kotlin.math.pow

class CalculatorUseCase {

    fun onButtonClick(state: CalculatorState, button: String): CalculatorState {
        val r = when (button) {
            "C" -> CalculatorState()
            "⌫️" -> deleteLast(state)
            "=" -> equals(state)
            "+/-" -> plusMinus(state)
            "( )" -> parentheses(state)
            else -> generalInput(state, button)
        }
        return updateSubDisplay(r)
    }

    private fun deleteLast(state: CalculatorState): CalculatorState {
        if (state.isResult) return CalculatorState()
        if (state.displayValue.isEmpty()) return state
        return state.copy(displayValue = state.displayValue.dropLast(1))
    }

    private fun equals(state: CalculatorState): CalculatorState {
        if (state.isResult) return repeatLast(state)
        val v = tryEvalExpression(state.displayValue) ?: return state.copy(
            displayValue = "Error",
            subDisplayValue = "",
            isResult = true,
            lastBinaryOp = null,
            lastOperand = null
        )
        val (op, operand) = extractLastOp(state.displayValue)
        return state.copy(
            displayValue = formatResult(v),
            subDisplayValue = "",
            isResult = true,
            lastBinaryOp = op,
            lastOperand = operand
        )
    }

    private fun repeatLast(state: CalculatorState): CalculatorState {
        val op = state.lastBinaryOp ?: return state
        val operand = state.lastOperand ?: return state
        val cur = state.displayValue.toDoubleOrNull() ?: return state
        val val2 = operand.toDoubleOrNull() ?: return state
        val r = when (op) {
            "+" -> cur + val2
            "-" -> cur - val2
            "*" -> cur * val2
            "/" -> if (val2 == 0.0) null else cur / val2
            else -> null
        } ?: return state
        return state.copy(displayValue = formatResult(r), subDisplayValue = "", isResult = true)
    }

    private fun plusMinus(state: CalculatorState): CalculatorState {
        if (state.isResult) return CalculatorState(displayValue = "(-")
        if (state.displayValue.isEmpty()) return state.copy(displayValue = "(-")
        return state.copy(displayValue = state.displayValue + "(-")
    }

    private fun parentheses(state: CalculatorState): CalculatorState {
        if (state.isResult) return CalculatorState(displayValue = "(")
        val expr = state.displayValue
        val openC = expr.count { it == '(' }
        val closeC = expr.count { it == ')' }
        val last = expr.lastOrNull()
        val needOpen = (openC == closeC) || (last != null && last in listOf('+', '-', '*', '/', '%', '('))
        val s = if (needOpen) {
            if (last != null && (last.isDigit() || last == ')')) "*(" else "("
        } else ")"
        val appended = validate(expr, s) ?: return state
        return state.copy(displayValue = appended)
    }

    private fun generalInput(state: CalculatorState, button: String): CalculatorState {
        if (state.isResult) {
            val safe = if (state.displayValue == "Error") "" else state.displayValue
            val sym = mapBtnToOp(button)
            return if (button.all { it.isDigit() } || button == ",") {
                val newVal = if (button == ",") "0." else button
                CalculatorState(displayValue = newVal)
            } else {
                val a = validate(safe, sym) ?: return state
                state.copy(displayValue = a, subDisplayValue = "", isResult = false)
            }
        }
        val sym = mapBtnToOp(button)
        val a = validate(state.displayValue, sym) ?: return state
        return state.copy(displayValue = a)
    }

    private fun mapBtnToOp(btn: String): String {
        return when (btn) {
            "," -> "."
            "×", "x", "X" -> "*"
            "÷" -> "/"
            "−" -> "-"
            else -> btn
        }
    }

    private fun validate(expr: String, symbol: String): String? {
        if (symbol.isEmpty()) return null
        if (expr.isEmpty()) {
            return when {
                symbol.first().isDigit() -> if (symbol == "0") "0" else symbol
                symbol == "." -> "0."
                symbol == "(" -> "("
                symbol in listOf("+", "-", "*", "/", "%") -> null
                symbol == "*(" -> "("
                else -> null
            }
        }
        if (expr.endsWith("(-") && symbol in listOf("*", "/")) return null
        if (expr.endsWith("(-")) {
            if (symbol == "-") return expr
            if (symbol.isOperatorSymbol()) return expr.dropLast(2) + symbol
        }
        val last = expr.last()
        if (last == ')' && symbol.first().isDigit()) return "$expr*$symbol"
        if (symbol == "(") {
            if (last.isDigit() || last == ')') return "$expr*("
        }
        if (symbol == "*(") return "$expr*("
        if (symbol in listOf("*", "/") && (last.isOperatorChar() || last == '(')) return null
        if (symbol.isOperatorSymbol() && last.isOperatorChar()) {
            return expr.dropLast(1) + symbol
        }
        if (last == '0') {
            val ln = lastNumber(expr)
            if (ln == "0") {
                if (symbol.first().isDigit()) {
                    if (symbol == "0") return expr
                    return expr.dropLast(1) + symbol
                }
                if (symbol == ".") return "$expr."
            }
        }
        return expr + symbol
    }

    private fun lastNumber(expr: String): String {
        var i = expr.length - 1
        while (i >= 0 && !expr[i].isOperatorChar() && expr[i] !in listOf('(', ')')) i--
        return expr.substring(i + 1)
    }

    private fun updateSubDisplay(state: CalculatorState): CalculatorState {
        if (state.isResult) return state.copy(subDisplayValue = "")
        val e = state.displayValue
        if (!e.any { it in listOf('+', '-', '*', '/', '%', '(', ')') }) return state.copy(subDisplayValue = "")
        val v = tryEvalExpression(e) ?: return state.copy(subDisplayValue = "")
        return state.copy(subDisplayValue = formatResult(v))
    }

    private fun extractLastOp(e: String): Pair<String?, String?> {
        return try {
            val t = tokenize(e)
            for (i in t.size - 1 downTo 1) {
                if (t[i - 1].isOperator() && t[i].isNumber()) {
                    val o = t[i - 1]
                    if (o in listOf("+", "-", "*", "/")) return o to t[i]
                }
            }
            null to null
        } catch (_: Exception) {
            null to null
        }
    }

    private fun tryEvalExpression(expr: String): Double? {
        return try {
            val x = transformPercent(expr)
            val tok = tokenize(x)
            val pf = infixToPostfix(tok)
            evaluatePostfix(pf)
        } catch (_: Exception) {
            null
        }
    }

    private fun transformPercent(e: String): String {
        if (!e.contains('%')) return e
        val idx = e.lastIndexOf('%')
        if (idx == -1) return e
        val left = e.substring(0, idx)
        val r = e.substring(idx + 1)
        val (lop, op, rng) = findLast(left)
        if (op == null || lop == null) {
            val x = left.toDoubleOrNull() ?: return e
            val xx = formatDouble(x / 100.0)
            return xx + r
        }
        val rp = left.substring(rng)
        val rv = rp.toDoubleOrNull() ?: return e
        val lv = lop.toDoubleOrNull() ?: return e
        val nr = when (op) {
            "+", "-" -> lv * (rv / 100.0)
            "*", "/" -> lv * (rv / 100.0)
            else -> rv / 100.0
        }
        val pref = left.substring(0, rng.first)
        return pref + formatDouble(nr) + r
    }

    private fun findLast(expr: String): Triple<String?, String?, IntRange> {
        var lvl = 0
        for (i in expr.indices.reversed()) {
            val c = expr[i]
            if (c == ')') lvl++
            if (c == '(') lvl--
            if (lvl < 0) lvl = 0
            if (lvl == 0 && c in listOf('+', '-', '*', '/')) {
                if (c == '-' && (i == 0 || expr[i - 1].isOperatorChar() || expr[i - 1] == '(')) continue
                val l = expr.substring(0, i)
                val o = c.toString()
                val rng = (i + 1) until expr.length
                return Triple(l, o, rng)
            }
        }
        return Triple(null, null, 0..0)
    }

    private fun formatDouble(d: Double): String {
        val l = d.toLong()
        return if (d == l.toDouble()) l.toString() else d.toString()
    }

    private fun tokenize(e: String): List<String> {
        val r = mutableListOf<String>()
        var i = 0
        while (i < e.length) {
            val c = e[i]
            when {
                c.isWhitespace() -> i++
                c in listOf('(', ')') -> {
                    r.add(c.toString())
                    i++
                }
                c in listOf('+', '-', '*', '/', '%', '^') -> {
                    if ((c == '+' || c == '-') && (i == 0 || e[i - 1] in listOf('(', '+', '-', '*', '/', '^'))) {
                        val (num, len) = readNumber(e, i)
                        r.add(num)
                        i += len
                    } else {
                        r.add(c.toString())
                        i++
                    }
                }
                c.isDigit() || c == '.' -> {
                    val (num, len) = readNumber(e, i)
                    r.add(num)
                    i += len
                }
                else -> i++
            }
        }
        return r
    }

    private fun readNumber(e: String, s: Int): Pair<String, Int> {
        var i = s
        val b = StringBuilder()
        if (i < e.length && (e[i] == '+' || e[i] == '-')) {
            b.append(e[i])
            i++
        }
        var dot = false
        while (i < e.length) {
            val c = e[i]
            if (c.isDigit()) {
                b.append(c)
                i++
            } else if (c == '.' && !dot) {
                b.append(c)
                dot = true
                i++
            } else break
        }
        return b.toString() to (i - s)
    }

    private fun infixToPostfix(t: List<String>): List<String> {
        val o = mutableListOf<String>()
        val st = Stack<String>()
        for (x in t) {
            when {
                x.isNumber() -> o.add(x)
                x.isOperator() -> {
                    while (st.isNotEmpty() && st.peek().isOperator() && priority(st.peek()) >= priority(x)) {
                        o.add(st.pop())
                    }
                    st.push(x)
                }
                x == "(" -> st.push(x)
                x == ")" -> {
                    while (st.isNotEmpty() && st.peek() != "(") o.add(st.pop())
                    if (st.isNotEmpty() && st.peek() == "(") st.pop()
                }
            }
        }
        while (st.isNotEmpty()) o.add(st.pop())
        return o
    }

    private fun evaluatePostfix(p: List<String>): Double? {
        val st = Stack<Double>()
        for (x in p) {
            if (x.isNumber()) {
                val d = x.toDoubleOrNull() ?: return null
                st.push(d)
            } else if (x.isOperator()) {
                if (st.size < 2) return null
                val b = st.pop()
                val a = st.pop()
                val r = when (x) {
                    "+" -> a + b
                    "-" -> a - b
                    "*" -> a * b
                    "/" -> if (b == 0.0) null else a / b
                    "%" -> a % b
                    "^" -> a.pow(b)
                    else -> null
                } ?: return null
                st.push(r)
            }
        }
        return if (st.size == 1) st.pop() else null
    }

    private fun priority(op: String): Int {
        return when (op) {
            "+", "-" -> 1
            "*", "/", "%" -> 2
            "^" -> 3
            else -> 0
        }
    }

    private fun formatResult(d: Double): String {
        val l = d.toLong()
        return if (d == l.toDouble()) l.toString() else d.toString()
    }

    private fun String.isNumber(): Boolean = toDoubleOrNull() != null
    private fun String.isOperator(): Boolean = this in listOf("+", "-", "*", "/", "%", "^")
    private fun Char.isOperatorChar(): Boolean = this in listOf('+', '-', '*', '/', '%', '^')
    private fun String.isOperatorSymbol(): Boolean = length == 1 && get(0).isOperatorChar()
}
