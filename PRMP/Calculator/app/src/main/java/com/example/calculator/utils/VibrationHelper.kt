package com.example.calculator.utils

import android.content.Context
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext

class VibrationHelper(context: Context) {
    private val vibrator: Vibrator =
        context.getSystemService(VibratorManager::class.java).defaultVibrator

    fun vibrate(milliseconds: Long = 50) {
        if (vibrator.hasVibrator()) {
            vibrator.vibrate(
                VibrationEffect.createOneShot(
                    milliseconds,
                    VibrationEffect.DEFAULT_AMPLITUDE
                )
            )
        }
    }
}

@Composable
fun rememberVibrationHelper(): VibrationHelper {
    val context = LocalContext.current
    return remember { VibrationHelper(context) }
}
