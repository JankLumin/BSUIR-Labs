package com.example.financewatcher.data.repository

import com.example.financewatcher.data.api.CurrencyApi
import com.example.financewatcher.data.model.CurrencyRate

class CurrencyRepository(private val api: CurrencyApi) {

    fun getExchangeRates(onComplete: (List<CurrencyRate>) -> Unit) {
        api.getExchangeRates(onComplete)
    }
}
