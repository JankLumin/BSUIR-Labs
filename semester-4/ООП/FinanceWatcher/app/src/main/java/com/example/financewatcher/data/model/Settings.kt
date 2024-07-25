package com.example.financewatcher.data.model

data class Settings(
    val theme: String = "light",
    val language: String = "en",
    val notificationsEnabled: Boolean = false
)
