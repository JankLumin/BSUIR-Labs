package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.financewatcher.data.model.Card
import com.example.financewatcher.domain.usecase.CardUseCase

class CardViewModel(private val cardUseCase: CardUseCase) : ViewModel() {

    val allCards: LiveData<List<Card>> get() = cardUseCase.allCards

    init {
        fetchAllCards()
    }

    private fun fetchAllCards() {
        cardUseCase.fetchAllCards()
    }

    fun addCard(card: Card) {
        cardUseCase.addCard(card) { success ->
            if (success) {
                fetchAllCards()
            }
        }
    }

    fun checkCardExists(cardNumber: String, onComplete: (Boolean) -> Unit) {
        cardUseCase.checkCardExists(cardNumber, onComplete)
    }

    fun deleteCard(cardId: String) {
        val cards = allCards.value?.toMutableList()
        if (cards != null) {
            cards.removeAll { it.cardId == cardId }
            (allCards as MutableLiveData).postValue(cards)
        }

        cardUseCase.deleteCard(cardId) { success ->
            if (!success) {
                fetchAllCards()
            }
        }
    }

    fun generateCardId(): String {
        return cardUseCase.generateCardId()
    }
}
