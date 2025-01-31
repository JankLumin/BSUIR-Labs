package com.example.calculator.presentation.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowInsetsControllerCompat

data class CalculatorColorScheme(
    val calcBackground: Color,
    val digitTextColor: Color,
    val symbolTextColor: Color,
    val buttonGray: Color,
    val equalsButtonBackground: Color,
    val equalsButtonText: Color,
    val clearButtonBackground: Color,
    val clearButtonText: Color
)

private val DarkColorScheme = CalculatorColorScheme(
    calcBackground = DarkCalcBackground,
    digitTextColor = DarkDigitTextColor,
    symbolTextColor = DarkSymbolTextColor,
    buttonGray = DarkButtonGray,
    equalsButtonBackground = DarkEqualsButtonBackground,
    equalsButtonText = DarkEqualsButtonText,
    clearButtonBackground = DarkClearButtonBackground,
    clearButtonText = DarkClearButtonText
)

private val LightColorScheme = CalculatorColorScheme(
    calcBackground = LightCalcBackground,
    digitTextColor = LightDigitTextColor,
    symbolTextColor = LightSymbolTextColor,
    buttonGray = LightButtonGray,
    equalsButtonBackground = LightEqualsButtonBackground,
    equalsButtonText = LightEqualsButtonText,
    clearButtonBackground = LightClearButtonBackground,
    clearButtonText = LightClearButtonText
)

val LocalCalculatorColors = staticCompositionLocalOf { LightColorScheme }

@Composable
fun calculatorTheme(
    useDarkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colors = if (useDarkTheme) DarkColorScheme else LightColorScheme

    val view = LocalView.current
    val activity = (LocalContext.current as? Activity)

    activity?.window?.let { window ->
        window.statusBarColor = colors.calcBackground.toArgb()
        window.navigationBarColor = colors.calcBackground.toArgb()

        val controller = WindowInsetsControllerCompat(window, view)
        controller.isAppearanceLightStatusBars = !useDarkTheme
        controller.isAppearanceLightNavigationBars = !useDarkTheme
    }

    CompositionLocalProvider(LocalCalculatorColors provides colors) {
        MaterialTheme(
            colorScheme = if (useDarkTheme) darkColorScheme() else lightColorScheme(),
            typography = Typography,
            content = content
        )
    }
}
