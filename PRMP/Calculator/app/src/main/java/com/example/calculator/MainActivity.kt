package com.example.calculator

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import com.example.calculator.presentation.CalculatorViewModel
import com.example.calculator.presentation.screens.calculatorScreen
import com.example.calculator.presentation.theme.calculatorTheme

class MainActivity : ComponentActivity() {

    private val viewModel by viewModels<CalculatorViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        installSplashScreen()

        setContent {
            calculatorTheme {
                Scaffold(
                    modifier = Modifier.fillMaxSize()
                ) {
                    calculatorScreen(viewModel)
                }
            }
        }
    }
}
