package com.example.financewatcher

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.navigation.NavController
import androidx.navigation.fragment.NavHostFragment
import androidx.navigation.ui.setupActionBarWithNavController
import androidx.navigation.ui.setupWithNavController
import com.example.financewatcher.data.repository.SettingsRepository
import com.example.financewatcher.databinding.ActivityMainBinding
import com.example.financewatcher.domain.usecase.ManageSettingsUseCase
import com.google.android.material.bottomnavigation.BottomNavigationView

@Suppress("DEPRECATION")
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var navController: NavController
    private lateinit var manageSettingsUseCase: ManageSettingsUseCase

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val settingsRepository = SettingsRepository(applicationContext)
        manageSettingsUseCase = ManageSettingsUseCase(settingsRepository)

        applySavedTheme()

        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        setSupportActionBar(binding.toolbar)

        val navHostFragment = supportFragmentManager.findFragmentById(R.id.nav_host_fragment) as NavHostFragment
        navController = navHostFragment.navController
        setupActionBarWithNavController(navController)

        val bottomNavigationView: BottomNavigationView = binding.bottomNavigation
        bottomNavigationView.setupWithNavController(navController)

        bottomNavigationView.setOnNavigationItemSelectedListener { item ->
            when (item.itemId) {
                R.id.navigation_cards -> {
                    navController.navigate(R.id.cardFragment)
                    true
                }
                R.id.navigation_currency_converter -> {
                    navController.navigate(R.id.currencyConverterFragment)
                    true
                }
                R.id.navigation_all_operations -> {
                    navController.navigate(R.id.allFinancialOperationsFragment)
                    true
                }
                R.id.navigation_budget -> {
                    navController.navigate(R.id.budgetFragment)
                    true
                }
                R.id.navigation_settings -> {
                    navController.navigate(R.id.settingsFragment)
                    true
                }
                else -> false
            }
        }
    }

    private fun applySavedTheme() {
        val settings = manageSettingsUseCase.getSettings()
        val theme = settings.theme
        when (theme) {
            "dark" -> setTheme(R.style.Theme_FinanceWatcher_Dark)
            "light" -> setTheme(R.style.Theme_FinanceWatcher_Light)
            else -> setTheme(R.style.Theme_FinanceWatcher_Light)
        }
    }

    override fun onSupportNavigateUp(): Boolean {
        return navController.navigateUp() || super.onSupportNavigateUp()
    }
}
