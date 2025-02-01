//Calculator/app/src/main/java/com/example/calculator/domain/model/CalculatorState.kt
package com.example.calculator.domain.model

data class CalculatorState(
    val displayValue: String = "",
    val subDisplayValue: String = "",
    val isResult: Boolean = false,
    val lastBinaryOp: String? = null,
    val lastOperand: String? = null
)
