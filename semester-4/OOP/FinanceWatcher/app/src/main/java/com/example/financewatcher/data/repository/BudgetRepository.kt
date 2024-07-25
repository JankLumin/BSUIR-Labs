package com.example.financewatcher.data.repository

import androidx.lifecycle.MutableLiveData
import com.example.financewatcher.data.database.FirestoreService
import com.example.financewatcher.data.model.Budget
import com.example.financewatcher.data.model.FinancialOperation
import com.google.firebase.firestore.Query
import java.text.SimpleDateFormat
import java.util.*

class BudgetRepository {

    val allBudgets = MutableLiveData<List<Budget>>()
    val budgetProgress = MutableLiveData<Map<String, Double>>()

    init {
        fetchBudgets()
    }

    fun fetchBudgets() {
        FirestoreService.budgetsCollection
            .addSnapshotListener { snapshot, error ->
                if (error != null || snapshot == null) {
                    allBudgets.value = emptyList()
                    return@addSnapshotListener
                }

                val budgets = snapshot.documents.mapNotNull { it.toObject(Budget::class.java) }
                allBudgets.value = budgets
            }
    }

    fun addBudget(budget: Budget) {
        FirestoreService.budgetsCollection.document(budget.id).set(budget)
            .addOnSuccessListener {}
            .addOnFailureListener {}
    }

    fun deleteBudget(budgetId: String) {
        FirestoreService.budgetsCollection.document(budgetId).delete()
            .addOnSuccessListener {
            }
            .addOnFailureListener {
            }
    }

    fun getOperationsByCategory(categoryId: String, period: String, onComplete: (List<FinancialOperation>) -> Unit) {
        val operationsQuery: Query = FirestoreService.db.collection("operations")
            .whereEqualTo("categoryId", categoryId)

        val calendar = Calendar.getInstance()

        when (period) {
            "Day" -> {
                calendar.add(Calendar.DAY_OF_YEAR, -1)
            }
            "Week" -> {
                calendar.add(Calendar.WEEK_OF_YEAR, -1)
            }
            "Month" -> {
                calendar.add(Calendar.MONTH, -1)
            }
            "Year" -> {
                calendar.add(Calendar.YEAR, -1)
            }
        }

        val dateFormatter = SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
        val startDate = dateFormatter.format(calendar.time)

        operationsQuery.whereGreaterThanOrEqualTo("dateTime", startDate)
            .get()
            .addOnSuccessListener { snapshot ->
                val operations = snapshot.documents.mapNotNull { it.toObject(FinancialOperation::class.java) }
                onComplete(operations)
            }
    }
}
