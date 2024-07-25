package com.example.financewatcher.domain.usecase

import com.example.financewatcher.data.model.CurrencyRate
import com.example.financewatcher.data.repository.CurrencyRepository

class GetCurrencyRatesUseCase(private val currencyRepository: CurrencyRepository) {

    fun execute(onComplete: (List<CurrencyRate>) -> Unit) {
        currencyRepository.getExchangeRates(onComplete)
    }
}
