package com.example.calculator.auth

import android.content.Context
import android.util.Base64
import java.security.MessageDigest

object PasskeyManager {
    private const val PREFS_NAME = "calculator_auth_prefs"
    private const val KEY_PASSKEY = "passkey_hash"
    private const val KEY_RECOVERY = "recovery_answer_hash"

    fun isPasskeySet(context: Context): Boolean {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        return prefs.contains(KEY_PASSKEY)
    }

    fun setPasskey(context: Context, passkey: String, recoveryAnswer: String) {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        prefs.edit()
            .putString(KEY_PASSKEY, hashString(passkey))
            .putString(KEY_RECOVERY, hashString(recoveryAnswer))
            .apply()
    }

    fun verifyPasskey(context: Context, input: String): Boolean {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val saved = prefs.getString(KEY_PASSKEY, null)
        return saved != null && saved == hashString(input)
    }

    fun verifyRecoveryAnswer(context: Context, input: String): Boolean {
        val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
        val saved = prefs.getString(KEY_RECOVERY, null)
        return saved != null && saved == hashString(input)
    }

    fun resetPasskey(context: Context, recoveryAnswer: String, newPasskey: String): Boolean {
        if (verifyRecoveryAnswer(context, recoveryAnswer)) {
            val prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)
            prefs.edit().putString(KEY_PASSKEY, hashString(newPasskey)).apply()
            return true
        }
        return false
    }

    private fun hashString(input: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
        val hashBytes = digest.digest(input.toByteArray(Charsets.UTF_8))
        return Base64.encodeToString(hashBytes, Base64.NO_WRAP)
    }
}
