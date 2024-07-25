package com.example.financewatcher

import android.app.Application
import androidx.appcompat.app.AppCompatDelegate
import com.example.financewatcher.data.repository.SettingsRepository
import com.example.financewatcher.domain.usecase.ManageSettingsUseCase

class App : Application() {

    override fun onCreate() {
        super.onCreate()
        val manageSettingsUseCase = ManageSettingsUseCase(SettingsRepository(this))
        manageSettingsUseCase.loadSettingsFromFirestore {
            applyTheme(manageSettingsUseCase.getSettings().theme)
            manageSettingsUseCase.syncSettingsToFirestore()
        }
    }

    private fun applyTheme(theme: String) {
        val mode = when (theme) {
            "dark" -> AppCompatDelegate.MODE_NIGHT_YES
            "light" -> AppCompatDelegate.MODE_NIGHT_NO
            else -> AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM
        }
        AppCompatDelegate.setDefaultNightMode(mode)
    }
}
