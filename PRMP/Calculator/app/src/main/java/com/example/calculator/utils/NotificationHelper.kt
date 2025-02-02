package com.example.calculator.utils

import android.annotation.SuppressLint
import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat

class NotificationHelper(private val context: Context) {

    companion object {
        const val CHANNEL_ID = "calculator_channel_id"
        const val CHANNEL_NAME = "Calculator Notifications"
        const val CHANNEL_DESCRIPTION = "Notifications from Calculator App"
    }

    init {
        createNotificationChannel()
    }

    private fun createNotificationChannel() {
        val importance = NotificationManager.IMPORTANCE_DEFAULT
        val channel = NotificationChannel(CHANNEL_ID, CHANNEL_NAME, importance).apply {
            description = CHANNEL_DESCRIPTION
        }
        val notificationManager =
            context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.createNotificationChannel(channel)
    }

    @SuppressLint("MissingPermission")
    fun showErrorNotification(message: String) {
        val builder = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.stat_notify_error)
            .setContentTitle("Ошибка калькулятора")
            .setContentText(message)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setOngoing(true)
            .setAutoCancel(false)
            .setOnlyAlertOnce(true)

        NotificationManagerCompat.from(context).notify(1, builder.build())
    }
}

@Composable
fun rememberNotificationHelper(): NotificationHelper {
    val context = LocalContext.current
    return remember { NotificationHelper(context) }
}
