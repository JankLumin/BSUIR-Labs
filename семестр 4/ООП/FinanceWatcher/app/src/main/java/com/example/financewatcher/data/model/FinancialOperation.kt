package com.example.financewatcher.data.model

data class FinancialOperation(
    val id: String = "",
    val categoryId: String = "",
    val type: String = "",
    val amount: Double = 0.0,
    val dateTime: String = "",
    val cardId: String = ""
)
