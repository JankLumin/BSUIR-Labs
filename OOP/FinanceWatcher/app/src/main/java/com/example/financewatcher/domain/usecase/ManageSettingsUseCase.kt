package com.example.financewatcher.domain.usecase

import com.example.financewatcher.data.model.Settings
import com.example.financewatcher.data.repository.SettingsRepository

class ManageSettingsUseCase(private val repository: SettingsRepository) {

    fun saveSettings(settings: Settings) {
        repository.saveSettings(settings)
    }

    fun getSettings(): Settings {
        return repository.getSettings()
    }

    fun loadSettingsFromFirestore(onComplete: () -> Unit) {
        repository.loadSettingsFromFirestore(onComplete)
    }

    fun syncSettingsToFirestore() {
        repository.syncSettingsToFirestore()
    }
}
