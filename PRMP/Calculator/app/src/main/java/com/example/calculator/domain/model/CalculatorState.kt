package com.example.calculator.domain.model

data class CalculatorState(
    val displayValue: String = "",
    val subDisplayValue: String = "",
    val isResult: Boolean = false,
    val lastBinaryOp: String? = null,
    val lastOperand: String? = null,
    val isHistoryOpen: Boolean = false,
    val historyList: List<HistoryItem> = emptyList()
)
