package com.example.financewatcher.presentation.ui.currency

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.financewatcher.databinding.FragmentCurrencyBinding
import com.example.financewatcher.presentation.viewmodel.CurrencyViewModel

class CurrencyFragment : Fragment() {

    private lateinit var binding: FragmentCurrencyBinding
    private lateinit var viewModel: CurrencyViewModel

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        binding = FragmentCurrencyBinding.inflate(inflater, container, false)

        viewModel = ViewModelProvider(requireActivity())[CurrencyViewModel::class.java]

        viewModel.exchangeRates.observe(viewLifecycleOwner) { rates ->
            val usdRate = rates.find { it.code == "USD" }?.exchangeRate ?: "N/A"
            val eurRate = rates.find { it.code == "EUR" }?.exchangeRate ?: "N/A"
            val rubRate = rates.find { it.code == "RUB" }?.exchangeRate ?: "N/A"
            binding.usdRate.text = usdRate.toString()
            binding.eurRate.text = eurRate.toString()
            binding.rubRate.text = rubRate.toString()
        }

        binding.refreshButton.setOnClickListener {
            viewModel.fetchExchangeRates()
        }

        return binding.root
    }
}
