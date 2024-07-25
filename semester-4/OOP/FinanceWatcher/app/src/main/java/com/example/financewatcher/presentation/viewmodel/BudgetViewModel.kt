package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.financewatcher.data.model.Budget
import com.example.financewatcher.data.model.CategoryProvider
import com.example.financewatcher.data.model.OperationCategory
import com.example.financewatcher.data.repository.BudgetRepository
import java.util.*

class BudgetViewModel : ViewModel() {

    private val budgetRepository = BudgetRepository()
    val allBudgets: LiveData<List<Budget>> = budgetRepository.allBudgets
    val budgetProgress: LiveData<Map<String, Double>> = budgetRepository.budgetProgress
    private val _allCategories = MutableLiveData<List<OperationCategory>>()

    init {
        fetchCategories()
        fetchBudgets()
    }

    private fun fetchCategories() {
        _allCategories.value = CategoryProvider.categories
    }

    private fun fetchBudgets() {
        budgetRepository.fetchBudgets()
    }

    fun addBudget(categoryId: String, amount: Double, period: String) {
        val budgetId = UUID.randomUUID().toString()
        val budget = Budget(id = budgetId, categoryId = categoryId, amount = amount, period = period)
        budgetRepository.addBudget(budget)
    }

    fun deleteBudget(budgetId: String) {
        budgetRepository.deleteBudget(budgetId)
    }

    fun getUsedAmount(budget: Budget, onComplete: (Double) -> Unit) {
        budgetRepository.getOperationsByCategory(budget.categoryId, budget.period) { operations ->
            val usedAmount = operations.sumOf { it.amount }
            onComplete(usedAmount)
        }
    }
}
