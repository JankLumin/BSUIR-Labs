package com.example.financewatcher.presentation.ui.operation

import android.annotation.SuppressLint
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.financewatcher.data.model.FinancialOperation
import com.example.financewatcher.data.model.OperationCategory
import com.example.financewatcher.databinding.ItemOperationBinding
import android.content.Context
import android.util.Log
import com.example.financewatcher.R

class FinancialOperationAdapter(
    private val context: Context,
    private val categories: Map<String, OperationCategory>
) : RecyclerView.Adapter<FinancialOperationAdapter.OperationViewHolder>() {

    private var operations: List<FinancialOperation> = emptyList()

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): OperationViewHolder {
        val binding = ItemOperationBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return OperationViewHolder(binding)
    }

    override fun onBindViewHolder(holder: OperationViewHolder, position: Int) {
        val operation = operations[position]
        holder.bind(context, operation, categories)
    }

    override fun getItemCount(): Int = operations.size

    @SuppressLint("NotifyDataSetChanged")
    fun submitList(operations: List<FinancialOperation>) {
        this.operations = operations
        notifyDataSetChanged()
    }

    class OperationViewHolder(private val binding: ItemOperationBinding) : RecyclerView.ViewHolder(binding.root) {

        fun bind(context: Context, operation: FinancialOperation, categories: Map<String, OperationCategory>) {
            binding.operationAmount.text = operation.amount.toString()
            binding.operationDateTime.text = operation.dateTime

            if (operation.type == "Expense") {
                binding.operationType.text = context.getString(R.string.expense)
                binding.operationCategory.visibility = View.VISIBLE
                val categoryNameResId = categories[operation.categoryId]?.name ?: R.string.category_other
                binding.operationCategory.text = context.getString(categoryNameResId)
                Log.d("OperationViewHolder", "CategoryId: ${operation.categoryId}, CategoryNameResId: $categoryNameResId")
            } else {
                binding.operationType.text = context.getString(R.string.income)
                binding.operationCategory.visibility = View.GONE
            }
        }
    }
}
