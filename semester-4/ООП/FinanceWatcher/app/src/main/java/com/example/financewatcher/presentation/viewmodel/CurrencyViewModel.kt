package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.financewatcher.data.model.CurrencyRate
import com.example.financewatcher.domain.usecase.GetCurrencyRatesUseCase
import kotlinx.coroutines.launch

class CurrencyViewModel(private val getCurrencyRatesUseCase: GetCurrencyRatesUseCase) : ViewModel() {

    private val _exchangeRates = MutableLiveData<List<CurrencyRate>>()
    val exchangeRates: LiveData<List<CurrencyRate>> get() = _exchangeRates

    private val _error = MutableLiveData<String>()
    val error: LiveData<String> get() = _error

    init {
        fetchExchangeRates()
    }

    fun fetchExchangeRates() {
        viewModelScope.launch {
            try {
                getCurrencyRatesUseCase.execute(
                    onComplete = {
                        _exchangeRates.postValue(it)
                    }
                )
            } catch (e: Exception) {
                _error.postValue(e.message)
            }
        }
    }
}
