package com.example.financewatcher.presentation.ui.budget

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.financewatcher.R
import com.example.financewatcher.data.model.CategoryProvider
import com.example.financewatcher.databinding.FragmentBudgetBinding
import com.example.financewatcher.databinding.DialogAddBudgetBinding
import com.example.financewatcher.presentation.viewmodel.BudgetViewModel
import com.google.android.material.dialog.MaterialAlertDialogBuilder

class BudgetFragment : Fragment() {

    private lateinit var binding: FragmentBudgetBinding
    private lateinit var viewModel: BudgetViewModel
    private lateinit var adapter: BudgetAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        binding = FragmentBudgetBinding.inflate(inflater, container, false)
        viewModel = ViewModelProvider(this)[BudgetViewModel::class.java]

        adapter = BudgetAdapter(viewModel)
        binding.budgetRecyclerView.layoutManager = LinearLayoutManager(context)
        binding.budgetRecyclerView.adapter = adapter

        viewModel.allBudgets.observe(viewLifecycleOwner) { budgets ->
            adapter.submitList(budgets)
        }

        viewModel.budgetProgress.observe(viewLifecycleOwner) { progressMap ->
            progressMap.forEach { (budgetId, usedAmount) ->
                val budget = viewModel.allBudgets.value?.find { it.id == budgetId }
                budget?.let {
                    val progress = (usedAmount / it.amount * 100).toInt()
                    val viewHolder = binding.budgetRecyclerView.findViewHolderForItemId(it.hashCode().toLong()) as? BudgetAdapter.BudgetViewHolder
                    viewHolder?.binding?.budgetProgressBar?.progress = progress
                    viewHolder?.binding?.usedAmount?.text = getString(R.string.used_amount, usedAmount, it.amount)
                }
            }
        }

        binding.addBudgetButton.setOnClickListener {
            showAddBudgetDialog()
        }

        return binding.root
    }

    private fun showAddBudgetDialog() {
        val dialogBinding = DialogAddBudgetBinding.inflate(LayoutInflater.from(context))
        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setTitle(getString(R.string.add_budget))
            .setView(dialogBinding.root)
            .setPositiveButton(getString(R.string.add)) { _, _ ->
                val selectedCategoryName = dialogBinding.categorySpinner.selectedItem.toString()
                val category = CategoryProvider.categories.find { context?.getString(it.name) == selectedCategoryName }?.id ?: "8"
                val amount = dialogBinding.amountEditText.text.toString().toDoubleOrNull() ?: 0.0
                val period = when (dialogBinding.periodSpinner.selectedItem.toString()) {
                    getString(R.string.day) -> "Day"
                    getString(R.string.week) -> "Week"
                    getString(R.string.month) -> "Month"
                    getString(R.string.year) -> "Year"
                    else -> "Month"
                }
                viewModel.addBudget(category, amount, period)
            }
            .setNegativeButton(getString(R.string.cancel), null)
            .create()

        setupCategorySpinner(dialogBinding)
        setupPeriodSpinner(dialogBinding)

        dialog.show()
    }

    private fun setupCategorySpinner(dialogBinding: DialogAddBudgetBinding) {
        val categoryNames = CategoryProvider.categories.map { getString(it.name) }
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, categoryNames)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        dialogBinding.categorySpinner.adapter = adapter
    }

    private fun setupPeriodSpinner(dialogBinding: DialogAddBudgetBinding) {
        val periods = listOf(getString(R.string.day), getString(R.string.week), getString(R.string.month), getString(R.string.year))
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, periods)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        dialogBinding.periodSpinner.adapter = adapter
    }
}
