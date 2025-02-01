package com.example.calculator.domain.usecase

import com.example.calculator.domain.model.CalculatorState
import com.example.calculator.utils.FlashlightHelper
import java.util.Stack
import kotlin.math.*

class CalculatorUseCase {

    fun onButtonClick(
        state: CalculatorState,
        button: String,
        flashlightHelper: FlashlightHelper? = null
    ): CalculatorState {
        val newState = when (button) {
            "C" -> CalculatorState()
            "⌫️" -> deleteLast(state)
            "=" -> equals(state, flashlightHelper)
            "+/-" -> plusMinus(state)
            "( )" -> parentheses(state)
            else -> generalInput(state, button)
        }
        return updateSubDisplay(newState)
    }

    private fun deleteLast(state: CalculatorState): CalculatorState {
        if (state.isResult) return CalculatorState()
        val expr = state.displayValue
        if (expr.isEmpty()) return state
        val tokens = tokenize(expr)
        if (tokens.isEmpty()) return state
        val mutableTokens = tokens.toMutableList()
        val lastToken = mutableTokens.last()
        if (isFunction(lastToken)) {
            mutableTokens.removeAt(mutableTokens.size - 1)
        } else if (lastToken.all { it.isDigit() || it == '.' || it == '-' } && lastToken.length > 1) {
            mutableTokens[mutableTokens.size - 1] = lastToken.dropLast(1)
        } else {
            mutableTokens.removeAt(mutableTokens.size - 1)
        }
        val newDisplay = mutableTokens.joinToString("")
        return state.copy(displayValue = newDisplay)
    }

    private fun equals(
        state: CalculatorState,
        flashlightHelper: FlashlightHelper?
    ): CalculatorState {
        if (!state.isResult) {
            val originalExpr = state.displayValue
            val evalResult = tryEvalExpression(originalExpr)
            if (evalResult == null) {
                flashlightHelper?.blinkFlashlight(300L)
                return state.copy(
                    displayValue = "Error",
                    subDisplayValue = "",
                    isResult = true,
                    lastBinaryOp = null,
                    lastOperand = null
                )
            } else {
                val (op, operand) = extractLastOp(originalExpr)
                return state.copy(
                    displayValue = formatResult(evalResult),
                    subDisplayValue = "",
                    isResult = true,
                    lastBinaryOp = op,
                    lastOperand = operand
                )
            }
        } else {
            return repeatLast(state)
        }
    }

    private fun repeatLast(state: CalculatorState): CalculatorState {
        val op = state.lastBinaryOp ?: return state
        val operand = state.lastOperand ?: return state
        val cur = state.displayValue.replace(',', '.').toDoubleOrNull() ?: return state
        val val2 = operand.toDoubleOrNull() ?: return state
        val newVal = when (op) {
            "+" -> cur + val2
            "-" -> cur - val2
            "×", "*" -> cur * val2
            "÷", "/" -> if (val2 == 0.0) null else cur / val2
            else -> null
        } ?: return state
        return state.copy(
            displayValue = formatResult(newVal),
            subDisplayValue = "",
            isResult = true
        )
    }

    private fun plusMinus(state: CalculatorState): CalculatorState {
        val expr = state.displayValue
        if (expr.isEmpty()) return state.copy(displayValue = "(-")
        val tokens = tokenize(expr)
        if (tokens.isEmpty()) return state
        if (tokens.size == 1) {
            val onlyToken = tokens[0]
            if (onlyToken.isOperator() || isFunction(onlyToken)) return state
            val toggled = if (onlyToken.startsWith("(-")) onlyToken.removePrefix("(-") else "(-$onlyToken"
            return state.copy(displayValue = toggled)
        }
        val lastIndex = tokens.size - 1
        val penaltyIndex = tokens.size - 2
        val lastToken = tokens[lastIndex]
        val penaltyToken = tokens[penaltyIndex]
        if (lastToken.isOperator() || isFunction(lastToken)) {
            return state
        }
        if (penaltyToken == "(" && lastToken.startsWith("-") && !isFunction(lastToken)) {
            val combined = "(-" + lastToken.removePrefix("-")
            val toggled = if (combined.startsWith("(-")) combined.removePrefix("(-") else "(-$combined"
            val newTokens = tokens.dropLast(2).toMutableList()
            if (toggled.isNotEmpty()) {
                newTokens.add(toggled)
            }
            return state.copy(displayValue = newTokens.joinToString(""))
        }
        val toggled2 = if (lastToken.startsWith("(-")) {
            lastToken.removePrefix("(-")
        } else {
            "(-$lastToken"
        }
        val newTokens = tokens.dropLast(1) + toggled2
        return state.copy(displayValue = newTokens.joinToString(""))
    }

    private fun parentheses(state: CalculatorState): CalculatorState {
        if (state.isResult) {
            return CalculatorState(displayValue = "(")
        }
        val expr = state.displayValue
        val openCount = expr.count { it == '(' }
        val closeCount = expr.count { it == ')' }
        val last = expr.lastOrNull()
        val needOpen = (openCount == closeCount) || (last != null && last in listOf('+', '-', '×', '÷', '%', '('))
        val symbol = if (needOpen) {
            if (last != null && (last.isDigit() || last == ')')) "×(" else "("
        } else {
            ")"
        }
        val validated = validate(expr, symbol) ?: return state
        return state.copy(displayValue = validated)
    }

    private fun generalInput(state: CalculatorState, button: String): CalculatorState {
        val sym = mapBtnToOp(button)
        if (state.isResult) {
            val safe = if (state.displayValue == "Error") "" else state.displayValue
            return if (button.all { it.isDigit() } || button == ",") {
                val newVal = if (button == ",") "0," else button
                CalculatorState(displayValue = newVal)
            } else {
                val exprWithMul = if (safe.isNotEmpty()) autoInsertMultiplication(safe, sym) else safe
                val validated = validate(exprWithMul, sym) ?: return state
                state.copy(displayValue = validated, subDisplayValue = "", isResult = false)
            }
        }
        val autoExpr = autoInsertMultiplication(state.displayValue, sym)
        val validated = validate(autoExpr, sym) ?: return state
        return state.copy(displayValue = validated)
    }

    private fun autoInsertMultiplication(currentExpr: String, newSymbol: String): String {
        if (currentExpr.isEmpty()) return currentExpr
        if (currentExpr.last().isDigit() && newSymbol.firstOrNull()?.isDigit() == true) {
            return currentExpr
        }
        val lastChar = currentExpr.last()
        val needsMul = (
                lastChar.isDigit() ||
                        lastChar == ')' ||
                        lastChar == 'e' ||
                        lastChar == 'π' ||
                        lastChar == '!' ||
                        lastChar == '%'
                )
        val startsOperand = when {
            newSymbol.startsWith("√(") || newSymbol.startsWith("∛(") -> true
            newSymbol.firstOrNull()?.isDigit() == true -> true
            newSymbol.firstOrNull()?.isLetter() == true -> true
            newSymbol.startsWith("(") || newSymbol.startsWith("(-") -> true
            else -> false
        }
        return if (needsMul && startsOperand) {
            "$currentExpr×"
        } else {
            currentExpr
        }
    }

    private fun mapBtnToOp(btn: String): String {
        return when (btn) {
            "," -> ","
            "×" -> "×"
            "÷" -> "÷"
            "−" -> "-"
            "+" -> "+"
            "e^x" -> "e^("
            "sin" -> "sin("
            "cos" -> "cos("
            "tan" -> "tan("
            "ln" -> "ln("
            "log" -> "log("
            "√" -> "√("
            "∛" -> "∛("
            "x²" -> "^(2)"
            "x^y" -> "^("
            "1/x" -> "1÷("
            "|x|" -> "abs("
            "π" -> "π"
            "e" -> "e"
            "!" -> "!"
            else -> btn
        }
    }

    private fun validate(expr: String, symbol: String): String? {
        val disallowedStart = listOf("×", "÷", "+", "-", "!", "^(", "^(2)")
        if (expr.isEmpty() && symbol in disallowedStart) return null
        if (expr.isEmpty()) {
            return when {
                symbol.firstOrNull()?.isDigit() == true -> if (symbol == "0") "0" else symbol
                symbol == "," -> "0,"
                symbol == "(" -> "("
                symbol.firstOrNull()?.isLetter() == true -> symbol
                else -> symbol
            }
        }
        if (symbol in listOf("+", "-", "×", "÷") && expr.last() in listOf('+', '-', '×', '÷')) {
            return replaceLastOperator(expr, symbol)
        }
        return expr + symbol
    }

    private fun updateSubDisplay(state: CalculatorState): CalculatorState {
        val e = state.displayValue
        if (!e.any { it in listOf('+', '-', '×', '÷', '%', '(', ')', '!', 'π', 'e') }) {
            return state.copy(subDisplayValue = "")
        }
        val v = tryEvalExpression(e) ?: return state.copy(subDisplayValue = "")
        return state.copy(subDisplayValue = formatResult(v))
    }

    private fun extractLastOp(expr: String): Pair<String?, String?> {
        return try {
            val t = tokenize(expr.replace(',', '.'))
            for (i in t.size - 1 downTo 1) {
                if (t[i - 1] in listOf("+", "-", "×", "÷") && t[i].toDoubleOrNull() != null) {
                    return t[i - 1] to t[i]
                }
            }
            null to null
        } catch (_: Exception) {
            null to null
        }
    }

    private fun tryEvalExpression(expr: String): Double? {
        var transformed = expr
            .replace(',', '.')
            .replace("×", "*")
            .replace("÷", "/")
            .replace("-", "-")
            .replace("e^(", "exp(")
            .replace(Regex("\\be\\b"), "${Math.E}")
            .replace("π", "${Math.PI}")
        transformed = transformPercent(transformed)
        val openCount = transformed.count { it == '(' }
        val closeCount = transformed.count { it == ')' }
        if (openCount > closeCount) {
            transformed += ")".repeat(openCount - closeCount)
        }
        return try {
            val tokens = tokenize(transformed)
            val postfix = infixToPostfix(tokens)
            evaluatePostfix(postfix)
        } catch (_: Exception) {
            null
        }
    }

    private fun transformPercent(s: String): String {
        return s.replace(Regex("(\\d+(?:\\.\\d+)?)%")) { mr ->
            "(${mr.groupValues[1]}/100)"
        }
    }

    private fun formatResult(d: Double): String {
        val l = d.toLong()
        val result = if (d == l.toDouble()) l.toString() else d.toString()
        return result.replace('.', ',')
    }

    private fun tokenize(e: String): List<String> {
        val r = mutableListOf<String>()
        var i = 0
        while (i < e.length) {
            val c = e[i]
            when {
                c.isWhitespace() -> {
                    i++
                }
                c == '√' || c == '∛' -> {
                    if (i + 1 < e.length && e[i + 1] == '(') {
                        r.add("$c(")
                        i += 2
                    } else {
                        r.add("$c(")
                        i++
                    }
                }
                c == '(' || c == ')' -> {
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
                c == '!' -> {
                    r.add("!")
                    i++
                }
                c.isDigit() || c == '.' -> {
                    val (num, len) = readNumber(e, i)
                    r.add(num)
                    i += len
                }
                c.isLetter() -> {
                    val start = i
                    while (i < e.length && e[i].isLetter()) {
                        i++
                    }
                    if (i < e.length && e[i] == '(') {
                        val token = e.substring(start, i + 1)
                        r.add(token)
                        i++
                    } else {
                        val token = e.substring(start, i)
                        r.add(token)
                    }
                }
                else -> {
                    r.add(c.toString())
                    i++
                }
            }
        }
        return r
    }

    private fun readNumber(e: String, s: Int): Pair<String, Int> {
        var i = s
        val sb = StringBuilder()
        if (i < e.length && (e[i] == '+' || e[i] == '-')) {
            sb.append(e[i])
            i++
        }
        var dotUsed = false
        while (i < e.length) {
            val c = e[i]
            if (c.isDigit()) {
                sb.append(c)
                i++
            } else if (c == '.' && !dotUsed) {
                sb.append('.')
                dotUsed = true
                i++
            } else {
                break
            }
        }
        return sb.toString() to (i - s)
    }

    private fun infixToPostfix(tokens: List<String>): List<String> {
        val out = mutableListOf<String>()
        val st = Stack<String>()
        for (x in tokens) {
            when {
                x.toDoubleOrNull() != null -> out.add(x)
                isFunction(x) -> st.push(x)
                x.isOperator() -> {
                    while (st.isNotEmpty() && (st.peek().isOperator() || isFunction(st.peek())) && priority(st.peek()) >= priority(x)) {
                        out.add(st.pop())
                    }
                    st.push(x)
                }
                x == "(" -> st.push(x)
                x == ")" -> {
                    while (st.isNotEmpty() && st.peek() != "(") {
                        out.add(st.pop())
                    }
                    if (st.isNotEmpty() && st.peek() == "(") st.pop()
                    if (st.isNotEmpty() && isFunction(st.peek())) {
                        out.add(st.pop())
                    }
                }
            }
        }
        while (st.isNotEmpty()) {
            out.add(st.pop())
        }
        return out
    }

    private fun evaluatePostfix(tokens: List<String>): Double? {
        val st = Stack<Double>()
        for (x in tokens) {
            val d = x.toDoubleOrNull()
            if (d != null) {
                st.push(d)
            } else if (x == "!") {
                if (st.isEmpty()) return null
                val top = st.pop()
                val ff = factorial(top) ?: return null
                st.push(ff)
            } else if (x == "π") {
                st.push(Math.PI)
            } else if (x == "e") {
                st.push(Math.E)
            } else if (isFunction(x)) {
                if (st.isEmpty()) return null
                val top = st.pop()
                val res = when {
                    x.startsWith("sin(") -> sin(top)
                    x.startsWith("cos(") -> cos(top)
                    x.startsWith("tan(") -> tan(top)
                    x.startsWith("ln(") -> if (top > 0) ln(top) else return null
                    x.startsWith("log(") -> if (top > 0) log10(top) else return null
                    x.startsWith("exp(") -> exp(top)
                    x.startsWith("√(") -> if (top >= 0) sqrt(top) else return null
                    x.startsWith("∛(") -> cbrt(top)
                    x.startsWith("abs(") -> abs(top)
                    else -> return null
                }
                if (res.isNaN() || res.isInfinite()) return null
                st.push(res)
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
                if (r.isNaN() || r.isInfinite()) return null
                st.push(r)
            } else {
                return null
            }
        }
        if (st.size != 1) return null
        return st.pop()
    }

    private fun priority(op: String): Int {
        return when {
            isFunction(op) -> 4
            op == "!" -> 4
            op == "+" || op == "-" -> 1
            op == "*" || op == "/" || op == "%" -> 2
            op == "^" -> 3
            else -> 0
        }
    }

    private fun factorial(a: Double): Double? {
        if (a < 0 || a != floor(a)) return null
        var res = 1.0
        val n = a.toLong()
        for (i in 1..n) {
            res *= i
            if (res.isInfinite()) return null
        }
        return res
    }

    private fun String.isOperator(): Boolean = this in listOf("+", "-", "*", "/", "%", "^", "!")
    private fun isFunction(token: String): Boolean {
        val regex = Regex("^(sin|cos|tan|ln|log|exp|√|∛|abs)\\($")
        return regex.matches(token)
    }
}

private fun replaceLastOperator(expr: String, newOp: String): String {
    if (expr.isEmpty()) return newOp
    return expr.dropLast(1) + newOp
}
