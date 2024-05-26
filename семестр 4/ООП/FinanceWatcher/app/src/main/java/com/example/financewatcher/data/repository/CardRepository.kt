@file:Suppress("DEPRECATION")

package com.example.financewatcher.data.repository

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.financewatcher.data.database.FirestoreService
import com.example.financewatcher.data.model.Card
import com.google.firebase.firestore.QuerySnapshot
import com.google.firebase.firestore.ktx.toObjects

class CardRepository(private val financialOperationRepository: FinancialOperationRepository) {

    private val _allCards = MutableLiveData<List<Card>>()
    val allCards: LiveData<List<Card>> get() = _allCards

    init {
        fetchAllCards()
    }

    fun fetchAllCards() {
        FirestoreService.cardsCollection.addSnapshotListener { snapshot, error ->
            if (error != null || snapshot == null) {
                _allCards.value = emptyList()
                return@addSnapshotListener
            }
            _allCards.value = snapshot.toObjects()
        }
    }

    fun addCard(card: Card, onComplete: (Boolean) -> Unit) {
        FirestoreService.cardsCollection.document(card.cardId).set(card)
            .addOnSuccessListener {
                updateLocalCards(card)
                onComplete(true)
            }
            .addOnFailureListener { onComplete(false) }
    }

    private fun updateLocalCards(card: Card) {
        val currentCards = _allCards.value?.toMutableList() ?: mutableListOf()
        currentCards.add(card)
        _allCards.postValue(currentCards)
    }

    fun updateCardFunds(cardId: String, newFunds: Double, onComplete: (Boolean) -> Unit) {
        updateLocalCardFunds(cardId, newFunds)

        FirestoreService.cardsCollection.document(cardId).update("availableFunds", newFunds)
            .addOnSuccessListener {
                onComplete(true)
            }
            .addOnFailureListener { onComplete(false) }
    }

    private fun updateLocalCardFunds(cardId: String, newFunds: Double) {
        val currentCards = _allCards.value?.toMutableList() ?: mutableListOf()
        val card = currentCards.find { it.cardId == cardId }
        if (card != null) {
            val updatedCard = card.copy(availableFunds = newFunds)
            currentCards[currentCards.indexOf(card)] = updatedCard
            _allCards.postValue(currentCards)
        }
    }

    fun checkCardExists(cardNumber: String, onComplete: (Boolean) -> Unit) {
        FirestoreService.cardsCollection.whereEqualTo("cardNumber", cardNumber)
            .get()
            .addOnSuccessListener { result: QuerySnapshot ->
                onComplete(!result.isEmpty)
            }
            .addOnFailureListener {
                onComplete(false)
            }
    }

    fun deleteCard(cardId: String, onComplete: (Boolean) -> Unit) {
        removeLocalCard(cardId)

        financialOperationRepository.deleteOperationsByCardId(cardId) {
            FirestoreService.cardsCollection.document(cardId).delete()
                .addOnSuccessListener {
                    onComplete(true)
                }
                .addOnFailureListener { onComplete(false) }
        }
    }

    private fun removeLocalCard(cardId: String) {
        val currentCards = _allCards.value?.toMutableList() ?: mutableListOf()
        currentCards.removeAll { it.cardId == cardId }
        _allCards.postValue(currentCards)
    }

    fun generateCardId(): String {
        return FirestoreService.cardsCollection.document().id
    }
}
