package com.example.financewatcher.data.model

data class Card(
    val cardId: String = "",
    val cardType: String = "",
    val cardNumber: String = "",
    var availableFunds: Double = 0.0
)
