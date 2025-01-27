package com.example.calculator.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color

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
fun CalculatorTheme(
    useDarkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colors = if (useDarkTheme) DarkColorScheme else LightColorScheme

    CompositionLocalProvider(LocalCalculatorColors provides colors) {
        MaterialTheme(
            colorScheme = if (useDarkTheme) darkColorScheme() else lightColorScheme(),
            typography = Typography,
            content = content
        )
    }
}
