package com.example.financewatcher.data.repository

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.example.financewatcher.data.database.FirestoreService
import com.example.financewatcher.data.model.FinancialOperation

class FinancialOperationRepository {

    private val _allOperations = MutableLiveData<List<FinancialOperation>>()
    val allOperations: LiveData<List<FinancialOperation>> get() = _allOperations

    private val _operationsByCard = MutableLiveData<List<FinancialOperation>>()
    val operationsByCard: LiveData<List<FinancialOperation>> get() = _operationsByCard

    fun fetchAllOperations() {
        FirestoreService.operationsCollection
            .addSnapshotListener { snapshot, error ->
                if (error != null || snapshot == null) {
                    _allOperations.value = emptyList()
                    return@addSnapshotListener
                }

                val operationsList = snapshot.documents.mapNotNull { it.toObject(FinancialOperation::class.java) }
                _allOperations.value = operationsList
            }
    }

    fun getOperationsForCard(cardId: String) {
        FirestoreService.operationsCollection
            .whereEqualTo("cardId", cardId)
            .addSnapshotListener { snapshot, error ->
                if (error != null || snapshot == null) {
                    _operationsByCard.value = emptyList()
                    return@addSnapshotListener
                }
                _operationsByCard.value = snapshot.toObjects(FinancialOperation::class.java)
            }
    }

    fun addOperation(operation: FinancialOperation, onComplete: (Boolean) -> Unit) {
        FirestoreService.operationsCollection.document(operation.id).set(operation)
            .addOnSuccessListener {
                updateLocalOperations(operation)
                onComplete(true)
            }
            .addOnFailureListener { onComplete(false) }
    }

    private fun updateLocalOperations(operation: FinancialOperation) {
        val currentOperations = _operationsByCard.value?.toMutableList() ?: mutableListOf()
        currentOperations.add(operation)
        _operationsByCard.postValue(currentOperations)
    }

    fun deleteOperationsByCardId(cardId: String, onComplete: () -> Unit) {
        FirestoreService.operationsCollection
            .whereEqualTo("cardId", cardId)
            .get()
            .addOnSuccessListener { snapshot ->
                val batch = FirestoreService.db.batch()
                for (document in snapshot.documents) {
                    batch.delete(document.reference)
                }
                batch.commit().addOnCompleteListener {
                    removeLocalOperationsByCardId(cardId)
                    onComplete()
                }
            }
    }

    private fun removeLocalOperationsByCardId(cardId: String) {
        val currentOperations = _operationsByCard.value?.toMutableList() ?: mutableListOf()
        currentOperations.removeAll { it.cardId == cardId }
        _operationsByCard.postValue(currentOperations)
    }
}
