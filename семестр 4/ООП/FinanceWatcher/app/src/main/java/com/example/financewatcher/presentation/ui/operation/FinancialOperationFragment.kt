package com.example.financewatcher.presentation.ui.operation

import android.content.DialogInterface
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.navArgs
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.financewatcher.R
import com.example.financewatcher.data.database.FirestoreService
import com.example.financewatcher.data.model.Card
import com.example.financewatcher.data.model.CategoryProvider
import com.example.financewatcher.data.model.FinancialOperation
import com.example.financewatcher.databinding.FragmentFinancialOperationBinding
import com.example.financewatcher.databinding.DialogAddOperationBinding
import com.example.financewatcher.presentation.viewmodel.FinancialOperationViewModel
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import java.text.SimpleDateFormat
import java.util.*

class FinancialOperationFragment : Fragment() {

    private lateinit var binding: FragmentFinancialOperationBinding
    private lateinit var viewModel: FinancialOperationViewModel
    private val args: FinancialOperationFragmentArgs by navArgs()
    private lateinit var adapter: FinancialOperationAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        binding = FragmentFinancialOperationBinding.inflate(inflater, container, false)
        viewModel = ViewModelProvider(this)[FinancialOperationViewModel::class.java]

        val categoryMap = CategoryProvider.categories.associateBy { it.id }
        adapter = FinancialOperationAdapter(requireContext(), categoryMap)

        binding.recyclerView.layoutManager = LinearLayoutManager(context)
        binding.recyclerView.adapter = adapter

        viewModel.operationsByCard.observe(viewLifecycleOwner) { operations ->
            adapter.submitList(operations)
        }

        viewModel.getOperationsForCard(args.cardId)

        binding.addButton.setOnClickListener {
            showAddOperationDialog()
        }

        return binding.root
    }

    private fun showAddOperationDialog() {
        val dialogBinding = DialogAddOperationBinding.inflate(LayoutInflater.from(context))
        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setTitle(R.string.add_operation)
            .setView(dialogBinding.root)
            .setPositiveButton(R.string.add_operation, null)
            .setNegativeButton(R.string.cancel, null)
            .create()

        setupCategorySpinner(dialogBinding)

        dialogBinding.operationTypeRadioGroup.setOnCheckedChangeListener { _, checkedId ->
            when (checkedId) {
                R.id.radioIncome -> dialogBinding.operationCategorySpinner.visibility = View.GONE
                R.id.radioExpense -> dialogBinding.operationCategorySpinner.visibility = View.VISIBLE
            }
        }

        dialog.setOnShowListener {
            val positiveButton = dialog.getButton(DialogInterface.BUTTON_POSITIVE)
            positiveButton.setOnClickListener {
                val amountText = dialogBinding.operationAmountEditText.text.toString().trim()
                if (amountText.isEmpty()) {
                    dialogBinding.operationAmountEditText.error = getString(R.string.error_empty_amount)
                    return@setOnClickListener
                }

                val type = if (dialogBinding.operationTypeRadioGroup.checkedRadioButtonId == R.id.radioIncome) "Income" else "Expense"
                val amount = amountText.toDouble()
                val categoryId = if (type == "Expense") {
                    val selectedCategory = dialogBinding.operationCategorySpinner.selectedItem as String
                    val category = CategoryProvider.categories.find { getString(it.name) == selectedCategory }
                    category?.id ?: ""
                } else {
                    ""
                }
                val dateTime = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(Date())
                val operationId = FirestoreService.db.collection("operations").document().id
                val operation = FinancialOperation(
                    id = operationId,
                    type = type,
                    amount = amount,
                    dateTime = dateTime,
                    cardId = args.cardId,
                    categoryId = categoryId
                )
                viewModel.addOperation(operation)
                updateCardFunds(args.cardId, amount, type)
                dialog.dismiss()
            }
        }

        dialog.show()
    }

    private fun setupCategorySpinner(dialogBinding: DialogAddOperationBinding) {
        val categoryNames = CategoryProvider.categories.map { getString(it.name) }
        val adapter = ArrayAdapter(requireContext(), android.R.layout.simple_spinner_item, categoryNames)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        dialogBinding.operationCategorySpinner.adapter = adapter
    }

    private fun updateCardFunds(cardId: String, amount: Double, type: String) {
        FirestoreService.cardsCollection.document(cardId).get().addOnSuccessListener { document ->
            val card = document.toObject(Card::class.java)
            if (card != null) {
                val newFunds = if (type == "Income") card.availableFunds + amount else card.availableFunds - amount
                FirestoreService.cardsCollection.document(cardId).update("availableFunds", newFunds)
            }
        }
    }
}
