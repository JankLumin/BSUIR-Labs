package com.example.financewatcher.presentation.ui.currencyconverter

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.financewatcher.R
import com.example.financewatcher.data.api.CurrencyApi
import com.example.financewatcher.data.model.CurrencyRate
import com.example.financewatcher.data.repository.CurrencyRepository
import com.example.financewatcher.databinding.FragmentCurrencyConverterBinding
import com.example.financewatcher.domain.usecase.GetCurrencyRatesUseCase
import com.example.financewatcher.presentation.viewmodel.CurrencyViewModel
import com.example.financewatcher.presentation.viewmodel.CurrencyViewModelFactory

class CurrencyConverterFragment : Fragment() {

    private lateinit var binding: FragmentCurrencyConverterBinding
    private lateinit var currencyViewModel: CurrencyViewModel

    private lateinit var currencyCodes: List<String>
    private lateinit var adapter: CurrencyRateAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        binding = FragmentCurrencyConverterBinding.inflate(inflater, container, false)
        val factory = CurrencyViewModelFactory(GetCurrencyRatesUseCase(CurrencyRepository(CurrencyApi(requireContext()))))
        currencyViewModel = ViewModelProvider(this, factory)[CurrencyViewModel::class.java]

        setupRecyclerView()

        currencyViewModel.exchangeRates.observe(viewLifecycleOwner) { rates ->
            val rateMap = rates.associateBy { it.code }.toMutableMap()
            rateMap["BYN"] = CurrencyRate("BYN", "BYN", "Belarusian Ruble", 1.0)

            val rubleName = getString(R.string.russian_ruble)
            val euroName = getString(R.string.euro)
            val dollarName = getString(R.string.us_dollar)

            rateMap["RUB"]?.let { rubRate ->
                rateMap["RUB"] = CurrencyRate(rubRate.id, rubRate.code, rubleName, rubRate.exchangeRate / 100)
            }

            rateMap["EUR"]?.let { euroRate ->
                rateMap["EUR"] = CurrencyRate(euroRate.id, euroRate.code, euroName, euroRate.exchangeRate)
            }

            rateMap["USD"]?.let { dollarRate ->
                rateMap["USD"] = CurrencyRate(dollarRate.id, dollarRate.code, dollarName, dollarRate.exchangeRate)
            }

            currencyCodes = rateMap.keys.toList()
            adapter.submitList(rateMap.values.toList())
            setupSpinners()

            binding.convertButton.setOnClickListener {
                val amount = binding.amountEditText.text.toString().toDoubleOrNull() ?: 0.0
                val fromCurrency = binding.fromCurrencySpinner.selectedItem.toString()
                val toCurrency = binding.toCurrencySpinner.selectedItem.toString()
                val convertedAmount = convertCurrency(amount, fromCurrency, toCurrency, rateMap)
                binding.resultTextView.text = String.format("%.2f", convertedAmount)
            }
        }

        currencyViewModel.error.observe(viewLifecycleOwner) { error ->
            Toast.makeText(context, error, Toast.LENGTH_LONG).show()
        }

        return binding.root
    }

    private fun setupRecyclerView() {
        adapter = CurrencyRateAdapter()
        binding.currencyRatesRecyclerView.layoutManager = LinearLayoutManager(context)
        binding.currencyRatesRecyclerView.adapter = adapter
    }

    private fun setupSpinners() {
        if (::currencyCodes.isInitialized && currencyCodes.isNotEmpty()) {
            val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, currencyCodes)
            adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
            binding.fromCurrencySpinner.adapter = adapter
            binding.toCurrencySpinner.adapter = adapter
        }
    }

    private fun convertCurrency(amount: Double, from: String, to: String, rates: Map<String, CurrencyRate>): Double {
        val fromRate = rates[from]?.exchangeRate ?: return 0.0
        val toRate = rates[to]?.exchangeRate ?: return 0.0
        return if (from == "BYN") {
            amount / toRate
        } else if (to == "BYN") {
            amount * fromRate
        } else {
            (amount * fromRate) / toRate
        }
    }
}
