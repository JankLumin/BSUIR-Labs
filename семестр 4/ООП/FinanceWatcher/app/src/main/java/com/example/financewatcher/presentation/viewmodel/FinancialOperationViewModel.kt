package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.ViewModel
import com.example.financewatcher.data.model.FinancialOperation
import com.example.financewatcher.data.repository.FinancialOperationRepository

class FinancialOperationViewModel : ViewModel() {

    private val repository = FinancialOperationRepository()

    val operationsByCard: LiveData<List<FinancialOperation>> get() = repository.operationsByCard

    fun getOperationsForCard(cardId: String) {
        repository.getOperationsForCard(cardId)
    }

    fun addOperation(operation: FinancialOperation) {
        repository.addOperation(operation) { success ->
            if (success) {
                repository.getOperationsForCard(operation.cardId)
            }
        }
    }

}
