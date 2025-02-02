package com.example.calculator.utils

import android.content.Context
import android.content.SharedPreferences

object ThemePreferences {
    private const val PREFS_NAME = "calculator_prefs"
    private const val KEY_THEME = "user_theme"

    fun saveTheme(context: Context, theme: String) {
        val prefs: SharedPreferences = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit().putString(KEY_THEME, theme).apply()
    }
}
