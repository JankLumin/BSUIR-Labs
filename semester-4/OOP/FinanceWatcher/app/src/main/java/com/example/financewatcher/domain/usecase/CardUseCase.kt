package com.example.financewatcher.domain.usecase

import androidx.lifecycle.LiveData
import com.example.financewatcher.data.model.Card
import com.example.financewatcher.data.repository.CardRepository

class CardUseCase(private val repository: CardRepository) {

    val allCards: LiveData<List<Card>> get() = repository.allCards

    fun fetchAllCards() {
        repository.fetchAllCards()
    }

    fun addCard(card: Card, onComplete: (Boolean) -> Unit) {
        repository.addCard(card, onComplete)
    }

    fun updateCardFunds(cardId: String, newFunds: Double, onComplete: (Boolean) -> Unit) {
        repository.updateCardFunds(cardId, newFunds, onComplete)
    }

    fun checkCardExists(cardNumber: String, onComplete: (Boolean) -> Unit) {
        repository.checkCardExists(cardNumber, onComplete)
    }

    fun deleteCard(cardId: String, onComplete: (Boolean) -> Unit) {
        repository.deleteCard(cardId, onComplete)
    }

    fun generateCardId(): String {
        return repository.generateCardId()
    }
}
