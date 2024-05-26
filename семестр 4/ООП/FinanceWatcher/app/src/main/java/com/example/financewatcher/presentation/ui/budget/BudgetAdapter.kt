package com.example.financewatcher.presentation.ui.budget

import android.content.Context
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.example.financewatcher.R
import com.example.financewatcher.data.model.Budget
import com.example.financewatcher.data.model.CategoryProvider
import com.example.financewatcher.databinding.ItemBudgetBinding
import com.example.financewatcher.presentation.viewmodel.BudgetViewModel

class BudgetAdapter(private val viewModel: BudgetViewModel) : ListAdapter<Budget, BudgetAdapter.BudgetViewHolder>(BudgetDiffCallback()) {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): BudgetViewHolder {
        val binding = ItemBudgetBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return BudgetViewHolder(binding, viewModel)
    }

    override fun onBindViewHolder(holder: BudgetViewHolder, position: Int) {
        val budget = getItem(position)
        holder.bind(budget)
    }

    class BudgetViewHolder(
        val binding: ItemBudgetBinding,
        private val viewModel: BudgetViewModel
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(budget: Budget) {
            binding.budget = budget
            binding.budgetCategory.text = getCategoryDisplayName(budget.categoryId, binding.root.context)
            binding.budgetPeriod.text = getPeriodDisplayName(budget.period, binding.root.context)

            viewModel.getUsedAmount(budget) { usedAmount ->
                val progress = (usedAmount / budget.amount * 100).toInt()
                binding.budgetProgressBar.progress = progress
                binding.usedAmount.text = binding.root.context.getString(R.string.used_amount, usedAmount, budget.amount)
            }

            binding.deleteButton.setOnClickListener {
                viewModel.deleteBudget(budget.id)
            }

            binding.executePendingBindings()
        }

        private fun getCategoryDisplayName(categoryId: String, context: Context): String {
            val categoryResource = CategoryProvider.categories.find { it.id == categoryId }?.name
            return categoryResource?.let { context.getString(it) } ?: categoryId
        }

        private fun getPeriodDisplayName(period: String, context: Context): String {
            return when (period) {
                "Day" -> context.getString(R.string.day)
                "Week" -> context.getString(R.string.week)
                "Month" -> context.getString(R.string.month)
                "Year" -> context.getString(R.string.year)
                else -> period
            }
        }
    }

    class BudgetDiffCallback : DiffUtil.ItemCallback<Budget>() {
        override fun areItemsTheSame(oldItem: Budget, newItem: Budget): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: Budget, newItem: Budget): Boolean {
            return oldItem == newItem
        }
    }
}
