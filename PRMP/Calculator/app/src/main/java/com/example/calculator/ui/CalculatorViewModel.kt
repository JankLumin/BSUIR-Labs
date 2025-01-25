package com.example.calculator.ui

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.Stack
import kotlin.math.pow

data class CalculatorState(
    val displayValue: String = "",
    val subDisplayValue: String = "",
    val isResult: Boolean = false
)

class CalculatorViewModel : ViewModel() {

    private val _uiState = MutableStateFlow(CalculatorState())
    val uiState = _uiState.asStateFlow()

    private var lastBinaryOp: String? = null
    private var lastOperand: String? = null

    fun onDirectInputChange(newVal: String) {
        _uiState.value = _uiState.value.copy(
            displayValue = newVal,
            isResult = false
        )
        updateSubDisplay()
    }

    fun onButtonClick(button: String) {
        when (button) {
            "C" -> onClear()
            "⌫️" -> onDeleteLast()
            "=" -> onEquals()
            "+/-" -> onPlusMinus()
            "( )" -> onParentheses()
            else -> onGeneralInput(button)
        }
        updateSubDisplay()
    }

    private fun onClear() {
        _uiState.value = CalculatorState(
            displayValue = "",
            subDisplayValue = "",
            isResult = false
        )
        lastBinaryOp = null
        lastOperand = null
    }

    private fun onDeleteLast() {
        val st = _uiState.value
        if (st.isResult) {
            onClear()
            return
        }
        val expr = st.displayValue
        if (expr.isEmpty()) return
        val newExpr = expr.dropLast(1)
        _uiState.value = st.copy(displayValue = newExpr)
    }

    private fun onEquals() {
        val st = _uiState.value
        if (st.isResult) {
            repeatLastOperation()
            return
        }

        val expression = st.displayValue
        val result = tryEvalExpression(expression)
        if (result != null) {
            val resultStr = formatResult(result)
            extractLastOperationForRepeat(expression)

            _uiState.value = st.copy(
                displayValue = resultStr,
                subDisplayValue = "",
                isResult = true
            )
        } else {
            _uiState.value = st.copy(
                displayValue = "Error",
                subDisplayValue = "",
                isResult = true
            )
        }
    }

    private fun repeatLastOperation() {
        val st = _uiState.value
        if (lastBinaryOp == null || lastOperand == null) return
        val currentVal = st.displayValue.toDoubleOrNull() ?: return
        val operandVal = lastOperand!!.toDoubleOrNull() ?: return

        val newResult = when (lastBinaryOp) {
            "+" -> currentVal + operandVal
            "-" -> currentVal - operandVal
            "*" -> currentVal * operandVal
            "/" -> if (operandVal == 0.0) null else currentVal / operandVal
            else -> null
        }
        if (newResult != null) {
            _uiState.value = st.copy(
                displayValue = formatResult(newResult),
                subDisplayValue = "",
                isResult = true
            )
        }
    }

    private fun extractLastOperationForRepeat(expression: String) {
        try {
            val tokens = tokenize(expression)
            for (i in tokens.size - 1 downTo 1) {
                if (tokens[i - 1].isOperator() && tokens[i].isNumber()) {
                    val op = tokens[i - 1]
                    if (op in listOf("+", "-", "*", "/")) {
                        lastBinaryOp = op
                        lastOperand = tokens[i]
                        return
                    }
                }
            }
        } catch (_: Exception) {
            lastBinaryOp = null
            lastOperand = null
        }
    }

    private fun onPlusMinus() {
        val st = _uiState.value
        if (st.isResult) {
            _uiState.value = CalculatorState(displayValue = "(-", isResult = false)
            return
        }
        val expr = st.displayValue
        _uiState.value = st.copy(displayValue = expr + "(-")
    }

    private fun onParentheses() {
        val st = _uiState.value
        if (st.isResult) {
            _uiState.value = st.copy(displayValue = "(", subDisplayValue = "", isResult = false)
            return
        }
        val expr = st.displayValue
        val openCount = expr.count { it == '(' }
        val closeCount = expr.count { it == ')' }

        val lastChar = expr.lastOrNull()
        val needOpen = (openCount == closeCount) ||
                (lastChar != null && lastChar in listOf('+', '-', '*', '/', '%', '('))

        val newExpr = if (needOpen) expr + "(" else expr + ")"
        _uiState.value = st.copy(displayValue = newExpr)
    }

    private fun onGeneralInput(button: String) {
        val st = _uiState.value

        if (st.isResult) {
            if (button.all { it.isDigit() } || button == ",") {
                val newVal = if (button == ",") "0." else button
                _uiState.value = CalculatorState(displayValue = mapBtnToOp(newVal), isResult = false)
            } else {
                val safeVal = if (st.displayValue == "Error") "" else st.displayValue
                val appended = validateAndAppend(safeVal, mapBtnToOp(button))
                if (appended != null) {
                    _uiState.value = st.copy(
                        displayValue = appended,
                        subDisplayValue = "",
                        isResult = false
                    )
                }
            }
            return
        }

        val expr = st.displayValue
        val appended = validateAndAppend(expr, mapBtnToOp(button))
        if (appended != null) {
            _uiState.value = st.copy(displayValue = appended)
        }
    }

    private fun updateSubDisplay() {
        val st = _uiState.value
        if (st.isResult) {
            _uiState.value = st.copy(subDisplayValue = "")
            return
        }
        val hasOperator = st.displayValue.any { it in listOf('+', '-', '*', '/', '%') }
        if (!hasOperator) {
            _uiState.value = st.copy(subDisplayValue = "")
            return
        }

        val partial = tryEvalExpression(st.displayValue)
        if (partial != null) {
            _uiState.value = st.copy(subDisplayValue = formatResult(partial))
        } else {
            _uiState.value = st.copy(subDisplayValue = "")
        }
    }

    private fun mapBtnToOp(button: String): String {
        return when (button) {
            "," -> "."
            "×", "x", "X" -> "*"
            "÷" -> "/"
            "−" -> "-"
            else -> button
        }
    }

    private fun validateAndAppend(expr: String, symbol: String): String? {
        if (symbol.isEmpty()) return null

        if (expr.isEmpty()) {
            if (symbol.first().isDigit()) {
                return symbol
            } else if (symbol == "-") {
                return symbol
            } else if (symbol == ".") {
                return "0."
            }
            return null
        }

        val lastCh = expr.last()

        if (symbol.isOperatorSymbol() && lastCh.isOperatorChar()) {
            return expr.dropLast(1) + symbol
        }

        if (symbol == ".") {
            var i = expr.length - 1
            while (i >= 0 && !expr[i].isOperatorChar() && expr[i] !in listOf('(', ')')) {
                if (expr[i] == '.') {
                    return null
                }
                i--
            }
        }

        return expr + symbol
    }

    private fun tryEvalExpression(expr: String): Double? {
        return try {
            val expanded = transformClassicPercent(expr)
            val tokens = tokenize(expanded)
            val postfix = infixToPostfix(tokens)
            evaluatePostfix(postfix)
        } catch (_: Exception) {
            null
        }
    }

    private fun transformClassicPercent(expression: String): String {
        if (!expression.contains("%")) return expression

        val lastPercentIndex = expression.lastIndexOf('%')
        if (lastPercentIndex == -1) return expression

        val leftExpr = expression.substring(0, lastPercentIndex)
        val rightAfterPercent = expression.substring(lastPercentIndex + 1)

        val (leftOperand, op, rightOperandRange) = findLastOperator(leftExpr)
        if (op == null || leftOperand == null) {
            val x = leftExpr.toDoubleOrNull() ?: return expression
            val replaced = formatDoubleToExpression(x / 100.0)
            return replaced + rightAfterPercent
        }

        val rightPart = leftExpr.substring(rightOperandRange)
        val rightVal = rightPart.toDoubleOrNull() ?: return expression
        val leftVal = leftOperand.toDoubleOrNull() ?: return expression

        val newRightVal = when (op) {
            "+", "-" -> leftVal * (rightVal / 100.0)
            "*", "/" -> leftVal * (rightVal / 100.0)
            else -> {
                rightVal / 100.0
            }
        }

        val prefix = leftExpr.substring(0, rightOperandRange.first)
        val newRightStr = formatDoubleToExpression(newRightVal)
        return prefix + newRightStr + rightAfterPercent
    }

    private fun findLastOperator(expr: String): Triple<String?, String?, IntRange> {
        var level = 0
        for (i in expr.indices.reversed()) {
            val c = expr[i]
            if (c == ')') level++
            if (c == '(') level--
            if (level < 0) level = 0

            if (level == 0 && c in listOf('+', '-', '*', '/')) {
                // проверка на унарный минус
                if (c == '-' && (i == 0 || expr[i - 1].isOperatorChar() || expr[i - 1] == '(')) {
                    continue
                }
                val left = expr.substring(0, i)
                val op = c.toString()
                val rightRange = (i + 1) until expr.length
                return Triple(left, op, rightRange)
            }
        }
        return Triple(null, null, 0..0)
    }

    private fun formatDoubleToExpression(d: Double): String {
        val s = formatResult(d)
        return s.replace(',', '.')
    }

    private fun tokenize(expr: String): List<String> {
        val result = mutableListOf<String>()
        var i = 0
        while (i < expr.length) {
            val c = expr[i]
            when {
                c.isWhitespace() -> i++
                c in listOf('(', ')') -> {
                    result.add(c.toString())
                    i++
                }
                c in listOf('+', '-', '*', '/', '%', '^') -> {
                    if ((c == '+' || c == '-') && (i == 0 || expr[i - 1] in listOf('(', '+', '-', '*', '/', '^'))) {
                        val (num, len) = readNumber(expr, i)
                        result.add(num)
                        i += len
                    } else {
                        result.add(c.toString())
                        i++
                    }
                }
                c.isDigit() || c == '.' -> {
                    val (num, len) = readNumber(expr, i)
                    result.add(num)
                    i += len
                }
                else -> {
                    i++
                }
            }
        }
        return result
    }

    private fun readNumber(expr: String, start: Int): Pair<String, Int> {
        var i = start
        val sb = StringBuilder()
        if (i < expr.length && (expr[i] == '+' || expr[i] == '-')) {
            sb.append(expr[i])
            i++
        }
        var hasDot = false
        while (i < expr.length) {
            val c = expr[i]
            if (c.isDigit()) {
                sb.append(c)
                i++
            } else if (c == '.' && !hasDot) {
                sb.append(c)
                hasDot = true
                i++
            } else {
                break
            }
        }
        return sb.toString() to (i - start)
    }

    private fun infixToPostfix(tokens: List<String>): List<String> {
        val output = mutableListOf<String>()
        val stack = Stack<String>()

        for (token in tokens) {
            when {
                token.isNumber() -> output.add(token)
                token.isOperator() -> {
                    while (stack.isNotEmpty() && stack.peek().isOperator() &&
                        precedence(stack.peek()) >= precedence(token)
                    ) {
                        output.add(stack.pop())
                    }
                    stack.push(token)
                }
                token == "(" -> stack.push(token)
                token == ")" -> {
                    while (stack.isNotEmpty() && stack.peek() != "(") {
                        output.add(stack.pop())
                    }
                    if (stack.isNotEmpty() && stack.peek() == "(") {
                        stack.pop()
                    }
                }
            }
        }
        while (stack.isNotEmpty()) {
            output.add(stack.pop())
        }
        return output
    }

    private fun evaluatePostfix(postfix: List<String>): Double? {
        val stack = Stack<Double>()
        for (token in postfix) {
            when {
                token.isNumber() -> {
                    val d = token.toDoubleOrNull() ?: return null
                    stack.push(d)
                }
                token.isOperator() -> {
                    if (stack.size < 2) return null
                    val b = stack.pop()
                    val a = stack.pop()
                    val r = when (token) {
                        "+" -> a + b
                        "-" -> a - b
                        "*" -> a * b
                        "/" -> if (b == 0.0) null else a / b
                        "%" -> a % b
                        "^" -> a.pow(b)
                        else -> null
                    }
                    if (r == null) return null
                    stack.push(r)
                }
            }
        }
        return if (stack.size == 1) stack.pop() else null
    }

    private fun precedence(op: String): Int {
        return when (op) {
            "+", "-" -> 1
            "*", "/", "%" -> 2
            "^" -> 3
            else -> 0
        }
    }

    private fun formatResult(d: Double): String {
        val lv = d.toLong()
        return if (d == lv.toDouble()) lv.toString() else d.toString()
    }

    private fun String.isNumber(): Boolean = this.toDoubleOrNull() != null

    private fun String.isOperator(): Boolean {
        return this in listOf("+", "-", "*", "/", "%", "^")
    }

    private fun Char.isOperatorChar(): Boolean {
        return this in listOf('+', '-', '*', '/', '%', '^')
    }

    private fun String.isOperatorSymbol(): Boolean {
        return length == 1 && get(0).isOperatorChar()
    }
}
