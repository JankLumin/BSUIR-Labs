package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.financewatcher.domain.usecase.GetCurrencyRatesUseCase

class CurrencyViewModelFactory(private val getCurrencyRatesUseCase: GetCurrencyRatesUseCase) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(CurrencyViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return CurrencyViewModel(getCurrencyRatesUseCase) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
