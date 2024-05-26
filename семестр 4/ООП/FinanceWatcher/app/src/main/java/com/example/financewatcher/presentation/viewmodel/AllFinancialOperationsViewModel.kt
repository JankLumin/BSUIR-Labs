package com.example.financewatcher.presentation.viewmodel

import android.content.Context
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.financewatcher.R
import com.example.financewatcher.data.model.FinancialOperation
import com.example.financewatcher.data.model.CategoryProvider
import com.example.financewatcher.data.repository.FinancialOperationRepository
import java.text.SimpleDateFormat
import java.util.*

class AllFinancialOperationsViewModel(private val context: Context) : ViewModel() {

    private val repository = FinancialOperationRepository()
    private val _allOperations = MutableLiveData<List<FinancialOperation>>()

    private val _filteredOperations = MutableLiveData<List<FinancialOperation>>()
    val filteredOperations: LiveData<List<FinancialOperation>> get() = _filteredOperations

    private val _totalIncome = MutableLiveData<Double>()
    val totalIncome: LiveData<Double> get() = _totalIncome

    private val _totalExpense = MutableLiveData<Double>()
    val totalExpense: LiveData<Double> get() = _totalExpense

    init {
        fetchAllOperations()
    }

    private fun fetchAllOperations() {
        repository.fetchAllOperations()
        repository.allOperations.observeForever { operations ->
            _allOperations.value = operations
            applyFilters("", context.getString(R.string.all_categories), context.getString(R.string.all_time))
        }
    }

    fun applyFilters(type: String, category: String, period: String) {
        val operations = _allOperations.value ?: emptyList()
        val filteredOperations = operations.filter { operation ->
            val isTypeMatch = type.isEmpty() || operation.type == type
            val isCategoryMatch = category == context.getString(R.string.all_categories) || getCategoryName(operation.categoryId) == category
            val isDateMatch = isWithinPeriod(operation.dateTime, period)
            isTypeMatch && isCategoryMatch && isDateMatch
        }

        _filteredOperations.value = filteredOperations
        calculateStatistics(filteredOperations)
    }

    private fun calculateStatistics(operations: List<FinancialOperation>) {
        var totalIncome = 0.0
        var totalExpense = 0.0

        for (operation in operations) {
            if (operation.type == "Income") {
                totalIncome += operation.amount
            } else if (operation.type == "Expense") {
                totalExpense += operation.amount
            }
        }

        _totalIncome.value = totalIncome
        _totalExpense.value = totalExpense
    }

    private fun getCategoryName(categoryId: String): String {
        val category = CategoryProvider.categories.find { it.id == categoryId }
        return category?.name?.let { context.getString(it) } ?: ""
    }

    private fun isWithinPeriod(dateTime: String, period: String): Boolean {
        if (period.isEmpty() || period == context.getString(R.string.all_time)) return true
        val dateFormat = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())
        val operationDate = dateFormat.parse(dateTime.substring(0, 10)) ?: return false
        val calendar = Calendar.getInstance()

        return when (period) {
            context.getString(R.string.last_day) -> {
                calendar.add(Calendar.DAY_OF_YEAR, -1)
                !operationDate.before(calendar.time)
            }
            context.getString(R.string.last_week) -> {
                calendar.add(Calendar.WEEK_OF_YEAR, -1)
                !operationDate.before(calendar.time)
            }
            context.getString(R.string.last_month) -> {
                calendar.add(Calendar.MONTH, -1)
                !operationDate.before(calendar.time)
            }
            context.getString(R.string.last_year) -> {
                calendar.add(Calendar.YEAR, -1)
                !operationDate.before(calendar.time)
            }
            else -> true
        }
    }
}

class AllFinancialOperationsViewModelFactory(private val context: Context) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(AllFinancialOperationsViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return AllFinancialOperationsViewModel(context) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
