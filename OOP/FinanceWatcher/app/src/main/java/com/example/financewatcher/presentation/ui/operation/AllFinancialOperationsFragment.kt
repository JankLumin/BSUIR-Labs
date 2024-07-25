package com.example.financewatcher.presentation.ui.operation

import android.annotation.SuppressLint
import android.content.DialogInterface
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
import com.example.financewatcher.databinding.DialogFilterOperationsBinding
import com.example.financewatcher.databinding.FragmentAllFinancialOperationsBinding
import com.example.financewatcher.presentation.viewmodel.AllFinancialOperationsViewModel
import com.example.financewatcher.presentation.viewmodel.AllFinancialOperationsViewModelFactory
import com.google.android.material.dialog.MaterialAlertDialogBuilder

class AllFinancialOperationsFragment : Fragment() {

    private lateinit var binding: FragmentAllFinancialOperationsBinding
    private lateinit var viewModel: AllFinancialOperationsViewModel
    private lateinit var adapter: FinancialOperationAdapter

    @SuppressLint("StringFormatInvalid")
    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        binding = FragmentAllFinancialOperationsBinding.inflate(inflater, container, false)
        viewModel = ViewModelProvider(this, AllFinancialOperationsViewModelFactory(requireContext()))[AllFinancialOperationsViewModel::class.java]

        val categoryMap = CategoryProvider.categories.associateBy { it.id }
        adapter = FinancialOperationAdapter(requireContext(), categoryMap)

        binding.recyclerView.layoutManager = LinearLayoutManager(context)
        binding.recyclerView.adapter = adapter

        viewModel.filteredOperations.observe(viewLifecycleOwner) { operations ->
            adapter.submitList(operations)
        }

        viewModel.totalIncome.observe(viewLifecycleOwner) { income ->
            binding.totalIncome.text = getString(R.string.total_income_amount, income)
        }

        viewModel.totalExpense.observe(viewLifecycleOwner) { expense ->
            binding.totalExpense.text = getString(R.string.total_expense_amount, expense)
        }

        binding.filterIcon.setOnClickListener {
            showFilterDialog()
        }

        return binding.root
    }

    private fun showFilterDialog() {
        val dialogBinding = DialogFilterOperationsBinding.inflate(LayoutInflater.from(context))
        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setTitle(R.string.filter_operations)
            .setView(dialogBinding.root)
            .setPositiveButton(R.string.apply, null)
            .setNegativeButton(R.string.cancel, null)
            .create()

        setupCategorySpinner(dialogBinding)
        setupPeriodSpinner(dialogBinding)

        dialogBinding.typeRadioGroup.setOnCheckedChangeListener { _, checkedId ->
            when (checkedId) {
                R.id.radioAll, R.id.radioIncome -> dialogBinding.categorySpinner.visibility = View.GONE
                R.id.radioExpense -> dialogBinding.categorySpinner.visibility = View.VISIBLE
            }
        }

        dialog.setOnShowListener {
            val positiveButton = dialog.getButton(DialogInterface.BUTTON_POSITIVE)
            positiveButton.setOnClickListener {
                val type = when (dialogBinding.typeRadioGroup.checkedRadioButtonId) {
                    R.id.radioIncome -> "Income"
                    R.id.radioExpense -> "Expense"
                    else -> ""
                }

                val category = if (type == "Expense") {
                    dialogBinding.categorySpinner.selectedItem as? String ?: ""
                } else {
                    getString(R.string.all_categories)
                }

                val period = dialogBinding.periodSpinner.selectedItem as? String ?: ""

                viewModel.applyFilters(type, category, period)
                dialog.dismiss()
            }
        }

        dialog.show()
    }

    private fun setupCategorySpinner(dialogBinding: DialogFilterOperationsBinding) {
        val categoryNames = listOf(getString(R.string.all_categories)) + CategoryProvider.categories.map { getString(it.name) }
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, categoryNames)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        dialogBinding.categorySpinner.adapter = adapter
        dialogBinding.categorySpinner.visibility = View.GONE
    }

    private fun setupPeriodSpinner(dialogBinding: DialogFilterOperationsBinding) {
        val periods = listOf(getString(R.string.all_time), getString(R.string.last_day), getString(R.string.last_week), getString(R.string.last_month), getString(R.string.last_year))
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, periods)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        dialogBinding.periodSpinner.adapter = adapter
    }
}
