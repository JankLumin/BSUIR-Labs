package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.financewatcher.domain.usecase.ManageSettingsUseCase

class SettingsViewModel(private val manageSettingsUseCase: ManageSettingsUseCase) : ViewModel() {

    private val _currentTheme = MutableLiveData<String>()
    val currentTheme: LiveData<String> get() = _currentTheme

    private val _currentLanguage = MutableLiveData<String>()
    val currentLanguage: LiveData<String> get() = _currentLanguage

    init {
        _currentTheme.value = manageSettingsUseCase.getSettings().theme
        _currentLanguage.value = manageSettingsUseCase.getSettings().language
    }

    fun changeTheme(theme: String) {
        _currentTheme.value = theme
        val settings = manageSettingsUseCase.getSettings().copy(theme = theme)
        manageSettingsUseCase.saveSettings(settings)
    }

    fun changeLanguage(language: String) {
        _currentLanguage.value = language
        val settings = manageSettingsUseCase.getSettings().copy(language = language)
        manageSettingsUseCase.saveSettings(settings)
    }
}
