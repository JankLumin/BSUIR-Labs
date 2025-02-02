package com.example.calculator

import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import com.example.calculator.presentation.CalculatorViewModel
import com.example.calculator.presentation.pinAuthScreen
import com.example.calculator.presentation.calculatorScreen
import com.example.calculator.presentation.theme.calculatorTheme
import com.example.calculator.utils.showBiometricPrompt

class MainActivity : AppCompatActivity() {
    private val viewModel by viewModels<CalculatorViewModel>()

    override fun onCreate(savedInstanceState: Bundle?) {
        val splashScreen = installSplashScreen()
        splashScreen.setKeepOnScreenCondition { !viewModel.isThemeLoaded.value }
        super.onCreate(savedInstanceState)

        setContent {
            val activity = LocalContext.current as androidx.fragment.app.FragmentActivity

            var isAuthenticated by rememberSaveable { mutableStateOf(false) }

            var biometricPromptShown by rememberSaveable { mutableStateOf(false) }

            val useDarkTheme by viewModel.useDarkTheme.collectAsState(initial = true)

            LaunchedEffect(Unit) {
                if (!isAuthenticated && !biometricPromptShown) {
                    biometricPromptShown = true
                    showBiometricPrompt(
                        activity = activity,
                        onAuthenticated = { isAuthenticated = true },
                        onError = { error ->
                        }
                    )
                }
            }

            calculatorTheme(useDarkTheme = useDarkTheme) {
                Scaffold(modifier = Modifier.fillMaxSize()) {
                    if (isAuthenticated) {
                        calculatorScreen(viewModel)
                    } else {
                        pinAuthScreen(onAuthenticated = { isAuthenticated = true })
                    }
                }
            }
        }
    }
}
