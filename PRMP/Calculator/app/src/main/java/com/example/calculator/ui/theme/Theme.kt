package com.example.calculator.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = DigitTextColor,
    secondary = SymbolTextColor,
    tertiary = EqualsButtonBackground,

    background = CalcBackground,
    surface = CalcBackground,
    onBackground = Color.White,
    onSurface = Color.White
)

@Composable
fun CalculatorTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = DarkColorScheme,
        typography = Typography,
        content = content
    )
}
