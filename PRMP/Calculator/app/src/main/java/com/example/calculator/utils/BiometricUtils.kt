package com.example.calculator.utils

import androidx.fragment.app.FragmentActivity
import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat

fun showBiometricPrompt(
    activity: FragmentActivity,
    onAuthenticated: () -> Unit,
    onError: (String) -> Unit = {}
) {
    val biometricManager = BiometricManager.from(activity)
    if (biometricManager.canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_STRONG)
        != BiometricManager.BIOMETRIC_SUCCESS
    ) {
        onError("Биометрия недоступна")
        return
    }

    val executor = ContextCompat.getMainExecutor(activity)
    val biometricPrompt = BiometricPrompt(activity, executor, object : BiometricPrompt.AuthenticationCallback() {
        override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
            super.onAuthenticationError(errorCode, errString)
            onError(errString.toString())
        }

        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
            super.onAuthenticationSucceeded(result)
            onAuthenticated()
        }

        override fun onAuthenticationFailed() {
            super.onAuthenticationFailed()
            onError("Не удалось распознать биометрию")
        }
    })

    val promptInfo = BiometricPrompt.PromptInfo.Builder()
        .setTitle("Биометрическая аутентификация")
        .setSubtitle("Используйте отпечаток пальца для входа")
        .setNegativeButtonText("Использовать PIN")
        .build()

    biometricPrompt.authenticate(promptInfo)
}
