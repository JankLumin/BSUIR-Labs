package com.example.financewatcher.data.repository

import android.content.Context
import android.content.SharedPreferences
import com.example.financewatcher.data.database.FirestoreService
import com.example.financewatcher.data.model.Settings
import com.google.firebase.firestore.SetOptions

class SettingsRepository(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("settings", Context.MODE_PRIVATE)
    private val userId = "default_user"

    fun saveSettings(settings: Settings) {
        prefs.edit().apply {
            putString("theme", settings.theme)
            putString("language", settings.language)
            putBoolean("notificationsEnabled", settings.notificationsEnabled)
            apply()
        }
        FirestoreService.settingsCollection.document(userId).set(settings, SetOptions.merge())
    }

    fun getSettings(): Settings {
        val theme = prefs.getString("theme", "light") ?: "light"
        val language = prefs.getString("language", "en") ?: "en"
        val notificationsEnabled = prefs.getBoolean("notificationsEnabled", false)
        return Settings(theme, language, notificationsEnabled)
    }

    fun loadSettingsFromFirestore(onComplete: () -> Unit) {
        FirestoreService.settingsCollection.document(userId).get().addOnSuccessListener { document ->
            if (document.exists()) {
                val settings = document.toObject(Settings::class.java)
                if (settings != null) {
                    saveSettings(settings)
                }
            }
            onComplete()
        }.addOnFailureListener {
            onComplete()
        }
    }

    fun syncSettingsToFirestore() {
        val settings = getSettings()
        FirestoreService.settingsCollection.document(userId).set(settings, SetOptions.merge())
    }
}
