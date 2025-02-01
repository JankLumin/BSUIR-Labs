//Calculator/app/src/main/java/com/example/calculator/presentation/CalculatorScreen.kt
package com.example.calculator.presentation

import android.content.res.Configuration
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalConfiguration
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.calculator.presentation.screens.horizontalCalculatorScreen
import com.example.calculator.presentation.screens.verticalCalculatorScreen

@Composable
fun calculatorScreen(viewModel: CalculatorViewModel = viewModel()) {
    val configuration = LocalConfiguration.current
    if (configuration.orientation == Configuration.ORIENTATION_PORTRAIT) {
        verticalCalculatorScreen(viewModel)
    } else {
        horizontalCalculatorScreen(viewModel)
    }
}
