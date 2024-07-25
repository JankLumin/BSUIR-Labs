package com.example.financewatcher.presentation.ui.card

import android.os.Bundle
import android.text.InputType
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.financewatcher.R
import com.example.financewatcher.data.model.Card
import com.example.financewatcher.databinding.FragmentCardBinding
import com.example.financewatcher.databinding.DialogAddCardBinding
import com.example.financewatcher.presentation.viewmodel.CardViewModel
import com.example.financewatcher.presentation.viewmodel.CardViewModelFactory
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.snackbar.Snackbar

class CardFragment : Fragment() {

    private lateinit var binding: FragmentCardBinding
    private lateinit var viewModel: CardViewModel
    private lateinit var adapter: CardAdapter

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        binding = FragmentCardBinding.inflate(inflater, container, false)
        val factory = CardViewModelFactory()
        viewModel = ViewModelProvider(this, factory)[CardViewModel::class.java]

        adapter = CardAdapter(
            onCardClick = { card -> navigateToOperations(card.cardId) },
            onDeleteClick = { cardId -> showDeleteConfirmationDialog(cardId) }
        )
        binding.recyclerView.adapter = adapter
        binding.recyclerView.layoutManager = LinearLayoutManager(context)

        viewModel.allCards.observe(viewLifecycleOwner) { cards ->
            cards?.let {
                adapter.submitList(it)
            }
        }

        binding.addButton.setOnClickListener {
            showAddCardDialog()
        }

        return binding.root
    }

    private fun showAddCardDialog() {
        val dialogBinding = DialogAddCardBinding.inflate(LayoutInflater.from(context))
        val dialog = MaterialAlertDialogBuilder(requireContext())
            .setTitle(R.string.add_card)
            .setView(dialogBinding.root)
            .setPositiveButton(R.string.add_card, null)
            .setNegativeButton(R.string.cancel, null)
            .create()

        dialog.setOnShowListener {
            val positiveButton = dialog.getButton(androidx.appcompat.app.AlertDialog.BUTTON_POSITIVE)
            positiveButton.setOnClickListener {
                val cardNumber = dialogBinding.cardNumberEditText.text.toString()
                val cardType = getCardType(cardNumber)
                val availableFunds = dialogBinding.availableFundsEditText.text.toString().toDoubleOrNull()

                if (cardNumber.length != 16) {
                    Snackbar.make(binding.root, R.string.invalid_card_number, Snackbar.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                if (availableFunds == null) {
                    Snackbar.make(binding.root, R.string.invalid_funds, Snackbar.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                val cardId = viewModel.generateCardId()
                val card = Card(cardId = cardId, cardType = cardType, cardNumber = cardNumber, availableFunds = availableFunds)

                viewModel.checkCardExists(cardNumber) { exists ->
                    if (exists) {
                        Snackbar.make(binding.root, R.string.card_exists, Snackbar.LENGTH_SHORT).show()
                    } else {
                        viewModel.addCard(card)
                        dialog.dismiss()
                    }
                }
            }
        }

        dialogBinding.availableFundsEditText.inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL

        dialog.show()
    }

    private fun getCardType(cardNumber: String): String {
        return when {
            cardNumber.startsWith("4") -> "Visa"
            cardNumber.startsWith("5") -> "MasterCard"
            cardNumber.startsWith("34") || cardNumber.startsWith("37") -> "American Express"
            cardNumber.startsWith("62") -> "China UnionPay"
            cardNumber.startsWith("60") || cardNumber.startsWith("65") -> "Discover"
            cardNumber.startsWith("35") -> "JCB"
            cardNumber.startsWith("30") || cardNumber.startsWith("36") || cardNumber.startsWith("38") -> "Diners Club"
            cardNumber.startsWith("2") -> "MIR"
            cardNumber.startsWith("50") || cardNumber.startsWith("56") || cardNumber.startsWith("57") || cardNumber.startsWith("58") -> "Белкарт"
            else -> "Unknown"
        }
    }

    private fun navigateToOperations(cardId: String) {
        val action = CardFragmentDirections.actionCardFragmentToFinancialOperationFragment(cardId)
        findNavController().navigate(action)
    }

    private fun showDeleteConfirmationDialog(cardId: String) {
        MaterialAlertDialogBuilder(requireContext())
            .setTitle(R.string.delete_card)
            .setMessage(R.string.confirm_delete_card)
            .setPositiveButton(R.string.delete) { _, _ ->
                viewModel.deleteCard(cardId)
            }
            .setNegativeButton(R.string.cancel, null)
            .show()
    }
}
