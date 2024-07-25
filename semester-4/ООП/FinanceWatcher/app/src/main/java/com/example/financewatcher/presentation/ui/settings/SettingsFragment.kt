package com.example.financewatcher.presentation.ui.settings

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.financewatcher.data.repository.SettingsRepository
import com.example.financewatcher.databinding.FragmentSettingsBinding
import com.example.financewatcher.domain.usecase.ManageSettingsUseCase
import com.example.financewatcher.presentation.viewmodel.SettingsViewModel
import com.example.financewatcher.presentation.viewmodel.SettingsViewModelFactory
import java.util.*

@Suppress("DEPRECATION")
class SettingsFragment : Fragment() {
    private var _binding: FragmentSettingsBinding? = null
    private val binding get() = _binding!!

    private lateinit var settingsViewModel: SettingsViewModel
    private lateinit var manageSettingsUseCase: ManageSettingsUseCase

    private val requestPermissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            startBalanceNotificationService()
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentSettingsBinding.inflate(inflater, container, false)

        val settingsRepository = SettingsRepository(requireContext())
        manageSettingsUseCase = ManageSettingsUseCase(settingsRepository)

        val factory = SettingsViewModelFactory(manageSettingsUseCase)
        settingsViewModel = ViewModelProvider(this, factory)[SettingsViewModel::class.java]

        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupThemeAndLanguageOptions()
        setupNotificationOption()
    }

    private fun setupThemeAndLanguageOptions() {
        settingsViewModel.currentTheme.observe(viewLifecycleOwner) { theme ->
            when (theme) {
                "light" -> binding.radioLight.isChecked = true
                "dark" -> binding.radioDark.isChecked = true
            }
        }

        settingsViewModel.currentLanguage.observe(viewLifecycleOwner) { language ->
            when (language) {
                "en" -> binding.radioEnglish.isChecked = true
                "ru" -> binding.radioRussian.isChecked = true
            }
        }

        binding.radioLight.setOnClickListener {
            settingsViewModel.changeTheme("light")
            applyTheme("light")
        }
        binding.radioDark.setOnClickListener {
            settingsViewModel.changeTheme("dark")
            applyTheme("dark")
        }

        binding.radioEnglish.setOnClickListener {
            settingsViewModel.changeLanguage("en")
            applyLanguage("en")
        }
        binding.radioRussian.setOnClickListener {
            settingsViewModel.changeLanguage("ru")
            applyLanguage("ru")
        }
    }

    private fun setupNotificationOption() {
        val settings = manageSettingsUseCase.getSettings()
        binding.checkBalance.isChecked = settings.notificationsEnabled

        binding.checkBalance.setOnCheckedChangeListener { _, isChecked ->
            val newSettings = settings.copy(notificationsEnabled = isChecked)
            manageSettingsUseCase.saveSettings(newSettings)

            if (isChecked) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    when {
                        ContextCompat.checkSelfPermission(
                            requireContext(),
                            Manifest.permission.POST_NOTIFICATIONS
                        ) == PackageManager.PERMISSION_GRANTED -> {
                            startBalanceNotificationService()
                        }
                        shouldShowRequestPermissionRationale(Manifest.permission.POST_NOTIFICATIONS) -> {}
                        else -> {
                            requestPermissionLauncher.launch(Manifest.permission.POST_NOTIFICATIONS)
                        }
                    }
                } else {
                    startBalanceNotificationService()
                }
            } else {
                stopBalanceNotificationService()
            }
        }
    }

    private fun applyTheme(theme: String) {
        val settings = manageSettingsUseCase.getSettings().copy(theme = theme)
        manageSettingsUseCase.saveSettings(settings)
        requireActivity().recreate()
    }

    private fun applyLanguage(language: String) {
        val settings = manageSettingsUseCase.getSettings().copy(language = language)
        manageSettingsUseCase.saveSettings(settings)
        setLocale(language)
        updateConfiguration()
    }

    private fun setLocale(languageCode: String) {
        val locale = Locale(languageCode)
        Locale.setDefault(locale)
        val config = resources.configuration
        config.setLocale(locale)
        resources.updateConfiguration(config, resources.displayMetrics)
    }

    private fun updateConfiguration() {
        val res = requireActivity().resources
        val config = res.configuration
        val locale = Locale(manageSettingsUseCase.getSettings().language)
        Locale.setDefault(locale)
        config.setLocale(locale)
        res.updateConfiguration(config, res.displayMetrics)
        requireActivity().recreate()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    private fun startBalanceNotificationService() {
        context?.let {
            val intent = Intent(it, BalanceNotificationService::class.java)
            it.startService(intent)
        }
    }

    private fun stopBalanceNotificationService() {
        context?.let {
            val intent = Intent(it, BalanceNotificationService::class.java)
            it.stopService(intent)
        }
    }
}
