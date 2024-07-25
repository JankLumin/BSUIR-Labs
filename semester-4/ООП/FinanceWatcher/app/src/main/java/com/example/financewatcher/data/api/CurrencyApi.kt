package com.example.financewatcher.data.api

import android.content.Context
import android.content.SharedPreferences
import com.example.financewatcher.data.database.FirestoreService
import com.example.financewatcher.data.model.CurrencyRate
import com.google.firebase.firestore.SetOptions
import org.json.JSONArray
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.HttpURLConnection
import java.net.URL

class CurrencyApi(context: Context) {

    private val prefs: SharedPreferences = context.getSharedPreferences("currency_rates", Context.MODE_PRIVATE)
    private val firestore = FirestoreService.ratesCollection
    private val userId = "default_user"

    fun getExchangeRates(onComplete: (List<CurrencyRate>) -> Unit) {
        Thread {
            try {
                val url = URL("https://www.nbrb.by/api/exrates/rates?periodicity=0")
                val httpURLConnection = url.openConnection() as HttpURLConnection
                httpURLConnection.requestMethod = "GET"
                httpURLConnection.connect()

                val responseCode = httpURLConnection.responseCode
                if (responseCode == 200) {
                    val inputStream = httpURLConnection.inputStream
                    val bufferedReader = BufferedReader(InputStreamReader(inputStream))
                    val response = bufferedReader.use { it.readText() }
                    bufferedReader.close()
                    val rates = parseExchangeRates(response)
                    saveRatesToCache(rates)
                    saveRatesToFirestore(rates)
                    onComplete(rates)
                } else {
                    throw Exception("Error fetching exchange rates: $responseCode")
                }
            } catch (e: Exception) {
                val cachedRates = getCachedExchangeRates()
                if (cachedRates.isNotEmpty()) {
                    onComplete(cachedRates)
                } else {
                    getRatesFromFirestore(onComplete)
                }
            }
        }.start()
    }

    private fun parseExchangeRates(response: String): List<CurrencyRate> {
        val jsonArray = JSONArray(response)
        val exchangeRates = mutableListOf<CurrencyRate>()

        for (i in 0 until jsonArray.length()) {
            val currency = jsonArray.getJSONObject(i)
            val currencyId = currency.getString("Cur_ID")
            val code = currency.getString("Cur_Abbreviation")
            val name = currency.getString("Cur_Name")
            val rate = currency.getDouble("Cur_OfficialRate")
            if (code in listOf("USD", "EUR", "RUB")) {
                exchangeRates.add(CurrencyRate(id = currencyId, code = code, name = name, exchangeRate = rate))
            }
        }

        return exchangeRates
    }

    private fun saveRatesToCache(rates: List<CurrencyRate>) {
        val editor = prefs.edit()
        rates.forEach { rate ->
            editor.putString(rate.code, rate.exchangeRate.toString())
        }
        editor.apply()
    }

    private fun saveRatesToFirestore(rates: List<CurrencyRate>) {
        val ratesMap = rates.associate { it.code to it.exchangeRate }
        firestore.document(userId).set(ratesMap, SetOptions.merge())
    }

    private fun getCachedExchangeRates(): List<CurrencyRate> {
        val rates = mutableListOf<CurrencyRate>()
        val codes = listOf("USD", "EUR", "RUB")
        codes.forEach { code ->
            val rate = prefs.getString(code, null)?.toDoubleOrNull()
            if (rate != null) {
                rates.add(CurrencyRate(id = code, code = code, name = code, exchangeRate = rate))
            }
        }
        return rates
    }

    private fun getRatesFromFirestore(onComplete: (List<CurrencyRate>) -> Unit) {
        firestore.document(userId).get().addOnSuccessListener { document ->
            if (document.exists()) {
                val rates = mutableListOf<CurrencyRate>()
                val codes = listOf("USD", "EUR", "RUB")
                codes.forEach { code ->
                    val rate = document.getDouble(code)
                    if (rate != null) {
                        rates.add(CurrencyRate(id = code, code = code, name = code, exchangeRate = rate))
                    }
                }
                onComplete(rates)
            } else {
                onComplete(emptyList())
            }
        }.addOnFailureListener {
            onComplete(emptyList())
        }
    }
}
