package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.financewatcher.data.repository.CardRepository
import com.example.financewatcher.data.repository.FinancialOperationRepository
import com.example.financewatcher.domain.usecase.CardUseCase

class CardViewModelFactory : ViewModelProvider.Factory {

    private val financialOperationRepository = FinancialOperationRepository()
    private val cardRepository = CardRepository(financialOperationRepository)
    private val cardUseCase = CardUseCase(cardRepository)

    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(CardViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return CardViewModel(cardUseCase) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
