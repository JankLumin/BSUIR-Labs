package com.example.financewatcher

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.view.animation.AnimationUtils
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.lifecycle.ViewModelProvider
import com.example.financewatcher.data.api.CurrencyApi
import com.example.financewatcher.data.repository.CurrencyRepository
import com.example.financewatcher.data.repository.SettingsRepository
import com.example.financewatcher.domain.usecase.GetCurrencyRatesUseCase
import com.example.financewatcher.domain.usecase.ManageSettingsUseCase
import com.example.financewatcher.presentation.viewmodel.CurrencyViewModel
import com.example.financewatcher.presentation.viewmodel.CurrencyViewModelFactory
import java.util.*

@Suppress("DEPRECATION")
@SuppressLint("CustomSplashScreen")
class SplashActivity : AppCompatActivity() {
    private lateinit var manageSettingsUseCase: ManageSettingsUseCase
    private lateinit var currencyViewModel: CurrencyViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val settingsRepository = SettingsRepository(applicationContext)
        manageSettingsUseCase = ManageSettingsUseCase(settingsRepository)

        applyThemeAndLanguage()

        setContentView(R.layout.activity_splash)

        val fadeIn = AnimationUtils.loadAnimation(this, R.anim.fade_in)
        findViewById<View>(R.id.splashScreen).startAnimation(fadeIn)

        val factory = CurrencyViewModelFactory(GetCurrencyRatesUseCase(CurrencyRepository(CurrencyApi(applicationContext))))
        currencyViewModel = ViewModelProvider(this, factory)[CurrencyViewModel::class.java]

        currencyViewModel.exchangeRates.observe(this) {
            Handler(Looper.getMainLooper()).postDelayed({
                startMainActivity()
            }, 1500)
        }

        currencyViewModel.error.observe(this) {
            Handler(Looper.getMainLooper()).postDelayed({
                startMainActivity()
            }, 1500)
        }
    }

    private fun applyThemeAndLanguage() {
        val settings = manageSettingsUseCase.getSettings()
        val theme = settings.theme
        val mode = when (theme) {
            "dark" -> AppCompatDelegate.MODE_NIGHT_YES
            "light" -> AppCompatDelegate.MODE_NIGHT_NO
            else -> AppCompatDelegate.MODE_NIGHT_FOLLOW_SYSTEM
        }
        AppCompatDelegate.setDefaultNightMode(mode)

        val language = settings.language
        setLocale(language)
    }

    private fun setLocale(languageCode: String) {
        val locale = Locale(languageCode)
        Locale.setDefault(locale)
        val config = resources.configuration
        config.setLocale(locale)
        resources.updateConfiguration(config, resources.displayMetrics)
    }

    private fun startMainActivity() {
        val intent = Intent(this, MainActivity::class.java)
        startActivity(intent)
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out)
        finish()
    }
}
