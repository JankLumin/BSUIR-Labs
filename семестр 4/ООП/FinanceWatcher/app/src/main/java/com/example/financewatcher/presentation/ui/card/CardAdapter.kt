package com.example.financewatcher.presentation.ui.card

import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.financewatcher.data.model.Card
import com.example.financewatcher.databinding.ItemCardBinding

class CardAdapter(
    private val onCardClick: (Card) -> Unit,
    private val onDeleteClick: (String) -> Unit
) : RecyclerView.Adapter<CardAdapter.CardViewHolder>() {

    private var cards: List<Card> = emptyList()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CardViewHolder {
        val binding = ItemCardBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return CardViewHolder(binding, onCardClick, onDeleteClick)
    }

    override fun onBindViewHolder(holder: CardViewHolder, position: Int) {
        val card = cards[position]
        holder.bind(card)
    }

    override fun getItemCount(): Int = cards.size

    @SuppressLint("NotifyDataSetChanged")
    fun submitList(cards: List<Card>) {
        this.cards = cards
        notifyDataSetChanged()
    }

    class CardViewHolder(
        private val binding: ItemCardBinding,
        private val onCardClick: (Card) -> Unit,
        private val onDeleteClick: (String) -> Unit
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(card: Card) {
            binding.cardType.text = card.cardType
            binding.cardNumber.text = card.cardNumber
            binding.availableFunds.text = card.availableFunds.toString()

            binding.root.setOnClickListener {
                onCardClick(card)
            }

            binding.deleteButton.setOnClickListener {
                onDeleteClick(card.cardId)
            }
        }
    }
}
