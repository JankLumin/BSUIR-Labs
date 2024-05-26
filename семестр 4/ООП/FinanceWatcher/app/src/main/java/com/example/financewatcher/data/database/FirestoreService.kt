package com.example.financewatcher.data.database

import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.FirebaseFirestoreSettings

@Suppress("DEPRECATION")
object FirestoreService {
    val db: FirebaseFirestore by lazy {
        FirebaseFirestore.getInstance().apply {
            firestoreSettings = FirebaseFirestoreSettings.Builder()
                .setPersistenceEnabled(true)
                .build()
        }
    }
    val cardsCollection = db.collection("cards")
    val settingsCollection = db.collection("settings")
    val ratesCollection = db.collection("currency_rates")
    val budgetsCollection = db.collection("budgets")
    val operationsCollection = db.collection("operations")
}
