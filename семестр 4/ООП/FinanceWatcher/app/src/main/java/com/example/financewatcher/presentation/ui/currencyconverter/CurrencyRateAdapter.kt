package com.example.financewatcher.presentation.ui.currencyconverter

import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.financewatcher.R
import com.example.financewatcher.data.model.CurrencyRate
import com.example.financewatcher.databinding.ItemCurrencyRateBinding

class CurrencyRateAdapter : RecyclerView.Adapter<CurrencyRateAdapter.CurrencyRateViewHolder>() {

    private var currencyRates: List<CurrencyRate> = listOf()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CurrencyRateViewHolder {
        val binding = ItemCurrencyRateBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return CurrencyRateViewHolder(binding)
    }

    override fun onBindViewHolder(holder: CurrencyRateViewHolder, position: Int) {
        holder.bind(currencyRates[position])
    }

    override fun getItemCount(): Int = currencyRates.size

    @SuppressLint("NotifyDataSetChanged")
    fun submitList(rates: List<CurrencyRate>) {
        currencyRates = rates.filter { it.code != "BYN" }
        notifyDataSetChanged()
    }

    class CurrencyRateViewHolder(private val binding: ItemCurrencyRateBinding) : RecyclerView.ViewHolder(binding.root) {
        fun bind(currencyRate: CurrencyRate) {
            binding.currencyRate = currencyRate
            binding.currencyFlag.setImageResource(getFlagResource(currencyRate.code))
            binding.executePendingBindings()
        }

        private fun getFlagResource(currencyCode: String): Int {
            return when (currencyCode) {
                "USD" -> R.drawable.usd
                "EUR" -> R.drawable.eur
                "RUB" -> R.drawable.rub
                else -> R.drawable.rub
            }
        }
    }
}
