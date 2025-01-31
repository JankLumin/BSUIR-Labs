package com.example.calculator.presentation

import androidx.lifecycle.ViewModel
import com.example.calculator.domain.model.CalculatorState
import com.example.calculator.domain.usecase.CalculatorUseCase
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow

class CalculatorViewModel(
    private val calculatorUseCase: CalculatorUseCase = CalculatorUseCase()
) : ViewModel() {

    private val _uiState = MutableStateFlow(CalculatorState())
    val uiState = _uiState.asStateFlow()

    fun onButtonClick(button: String) {
        val newState = calculatorUseCase.onButtonClick(_uiState.value, button)
        _uiState.value = newState
    }
}
