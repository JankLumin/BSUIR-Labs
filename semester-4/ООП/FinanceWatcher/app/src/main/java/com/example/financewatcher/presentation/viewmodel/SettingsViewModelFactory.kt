package com.example.financewatcher.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.example.financewatcher.domain.usecase.ManageSettingsUseCase

class SettingsViewModelFactory(private val manageSettingsUseCase: ManageSettingsUseCase) : ViewModelProvider.Factory {

    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(SettingsViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return SettingsViewModel(manageSettingsUseCase) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
