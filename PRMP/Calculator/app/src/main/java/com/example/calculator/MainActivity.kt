package com.example.calculator

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import com.example.calculator.ui.CalculatorScreen
import com.example.calculator.ui.CalculatorViewModel
import com.example.calculator.ui.theme.CalculatorTheme
import android.util.Log

class MainActivity : ComponentActivity() {

    private val viewModel by viewModels<CalculatorViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            CalculatorTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) {
                    CalculatorScreen(viewModel)
                }
            }
        }
    }
}
