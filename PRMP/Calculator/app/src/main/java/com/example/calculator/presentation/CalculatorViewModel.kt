package com.example.calculator.presentation

import android.app.Application
import com.example.calculator.domain.model.CalculatorState
import com.example.calculator.domain.model.HistoryItem
import com.example.calculator.domain.model.UserTheme
import com.example.calculator.domain.usecase.CalculatorUseCase
import com.example.calculator.utils.ThemePreferences
import com.example.calculator.utils.getDeviceId
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import androidx.lifecycle.AndroidViewModel

class CalculatorViewModel(application: Application) : AndroidViewModel(application) {

    private val calculatorUseCase = CalculatorUseCase()
    private val db = FirebaseFirestore.getInstance()

    private val historyCollection = "CalculatorHistory"
    private val themeCollection = "UserThemes"

    private val deviceId: String by lazy { getDeviceId(application) }

    private val _uiState = MutableStateFlow(CalculatorState())
    val uiState = _uiState.asStateFlow()

    private val _useDarkTheme = MutableStateFlow(true)
    val useDarkTheme = _useDarkTheme.asStateFlow()

    init {
        loadHistoryFromFirebase()
        loadThemeFromFirebase()
    }

    fun onButtonClick(button: String, flashlightHelper: com.example.calculator.utils.FlashlightHelper? = null) {
        val oldState = _uiState.value
        val newState = calculatorUseCase.onButtonClick(oldState, button, flashlightHelper)
        _uiState.value = newState

        if (button == "=" && newState.displayValue != "Error") {
            val expression = oldState.displayValue
            val result = newState.displayValue
            addHistoryItem(expression, result)
        }
    }

    fun toggleHistory() {
        val current = _uiState.value
        val newHistoryState = !current.isHistoryOpen
        if (newHistoryState) {
            loadHistoryFromFirebase()
        }
        _uiState.value = current.copy(isHistoryOpen = newHistoryState)
    }

    fun clearHistory() {
        _uiState.value.historyList.forEach { item ->
            if (item.id.isNotEmpty()) {
                db.collection(historyCollection).document(item.id).delete()
            }
        }
        _uiState.value = _uiState.value.copy(historyList = emptyList())
    }

    private fun addHistoryItem(expression: String, result: String) {
        if (expression.isBlank()) return

        val newItem = HistoryItem(
            expression = expression,
            result = result,
            timestamp = System.currentTimeMillis(),
            deviceId = deviceId
        )

        _uiState.value = _uiState.value.copy(historyList = _uiState.value.historyList + newItem)

        db.collection(historyCollection)
            .add(newItem)
            .addOnSuccessListener { docRef ->
                val itemWithId = newItem.copy(id = docRef.id)
                val updatedList = _uiState.value.historyList.map {
                    if (it.timestamp == newItem.timestamp) itemWithId else it
                }
                _uiState.value = _uiState.value.copy(historyList = updatedList)
            }
            .addOnFailureListener { exception ->
            }
    }

    private fun loadHistoryFromFirebase() {
        db.collection(historyCollection)
            .whereEqualTo("deviceId", deviceId)
            .orderBy("timestamp")
            .get()
            .addOnSuccessListener { snapshot ->
                val items = snapshot.documents.mapNotNull { doc ->
                    doc.toObject(HistoryItem::class.java)?.copy(id = doc.id)
                }
                _uiState.value = _uiState.value.copy(historyList = items)
            }
            .addOnFailureListener { exception ->
            }
    }

    private val _isThemeLoaded = MutableStateFlow(false)
    val isThemeLoaded = _isThemeLoaded.asStateFlow()

    private fun loadThemeFromFirebase() {
        db.collection(themeCollection)
            .document(deviceId)
            .get()
            .addOnSuccessListener { document ->
                if (document != null && document.exists()) {
                    val theme = document.getString("theme")
                    _useDarkTheme.value = theme == "dark"
                    ThemePreferences.saveTheme(getApplication(), theme ?: "light")
                } else {
                    _useDarkTheme.value = false
                    db.collection(themeCollection)
                        .document(deviceId)
                        .set(UserTheme(deviceId, "light"))
                    ThemePreferences.saveTheme(getApplication(), "light")
                }
                _isThemeLoaded.value = true
            }
            .addOnFailureListener { exception ->
                _useDarkTheme.value = false
                ThemePreferences.saveTheme(getApplication(), "light")
                _isThemeLoaded.value = true
            }
    }

    fun toggleTheme() {
        val newTheme = if (_useDarkTheme.value) "light" else "dark"
        _useDarkTheme.value = !_useDarkTheme.value

        db.collection(themeCollection)
            .document(deviceId)
            .set(UserTheme(deviceId, newTheme))
            .addOnSuccessListener {
                ThemePreferences.saveTheme(getApplication(), newTheme)
            }
            .addOnFailureListener { exception ->
            }
    }
}
