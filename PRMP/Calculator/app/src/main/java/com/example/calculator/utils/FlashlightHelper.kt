//Calculator/app/src/main/java/com/example/calculator/utils/FlashlightHelper.kt
package com.example.calculator.utils

import android.content.Context
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CameraManager
import android.os.Handler
import android.os.Looper
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext

class FlashlightHelper(private val context: Context) {

    fun blinkFlashlight(duration: Long = 200) {
        val cameraManager = context.getSystemService(Context.CAMERA_SERVICE) as? CameraManager ?: return
        val cameraId = cameraManager.cameraIdList.firstOrNull { id ->
            val characteristics = cameraManager.getCameraCharacteristics(id)
            characteristics.get(CameraCharacteristics.FLASH_INFO_AVAILABLE) == true
        } ?: return
        try {
            cameraManager.setTorchMode(cameraId, true)
            Handler(Looper.getMainLooper()).postDelayed({
                cameraManager.setTorchMode(cameraId, false)
            }, duration)
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}

@Composable
fun rememberFlashlightHelper(): FlashlightHelper {
    val context = LocalContext.current
    return remember { FlashlightHelper(context) }
}
