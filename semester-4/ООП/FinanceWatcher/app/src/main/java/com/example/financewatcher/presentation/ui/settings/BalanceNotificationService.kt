package com.example.financewatcher.presentation.ui.settings

import android.Manifest
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.IBinder
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import com.example.financewatcher.R
import com.example.financewatcher.data.database.FirestoreService
import com.google.firebase.firestore.ListenerRegistration
import java.util.*

class BalanceNotificationService : Service() {

    private val channelId = "balance_notification_channel"
    private val notificationId = 1
    private var registration: ListenerRegistration? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
        startListeningForChanges()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        startListeningForChanges()
        return START_STICKY
    }

    override fun onDestroy() {
        super.onDestroy()
        stopListeningForChanges()
        NotificationManagerCompat.from(this).cancel(notificationId)
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }

    private fun startListeningForChanges() {
        registration = FirestoreService.cardsCollection.addSnapshotListener { snapshot, _ ->
            if (snapshot != null) {
                updateBalanceNotification(snapshot.documents.sumOf { it.getDouble("availableFunds") ?: 0.0 })
            }
        }
    }

    private fun stopListeningForChanges() {
        registration?.remove()
    }

    private fun updateBalanceNotification(totalBalance: Double) {

        val prefs = getSharedPreferences("settings", Context.MODE_PRIVATE)
        val notificationsEnabled = prefs.getBoolean("notificationsEnabled", false)

        if (notificationsEnabled) {
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED) {
                val locale = Locale(prefs.getString("language", "en") ?: "en")
                val configuration = resources.configuration
                configuration.setLocale(locale)
                val localizedContext = createConfigurationContext(configuration)

                val notification = NotificationCompat.Builder(this, channelId)
                    .setContentTitle(localizedContext.getString(R.string.current_balance))
                    .setContentText(localizedContext.getString(R.string.balance_amount, totalBalance))
                    .setSmallIcon(R.drawable.ic_balance)
                    .setPriority(NotificationCompat.PRIORITY_HIGH)
                    .build()

                with(NotificationManagerCompat.from(this)) {
                    cancel(notificationId)
                    notify(notificationId, notification)
                }
            }
        }
    }

    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = getString(R.string.balance_notification_channel_name)
            val descriptionText = getString(R.string.balance_notification_channel_description)
            val importance = NotificationManager.IMPORTANCE_HIGH
            val channel = NotificationChannel(channelId, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }
}
