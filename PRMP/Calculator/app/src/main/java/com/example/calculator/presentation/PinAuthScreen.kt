package com.example.calculator.presentation

import android.content.res.Configuration
import android.widget.Toast
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentHeight
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.runtime.saveable.rememberSaveable
import com.example.calculator.auth.PasskeyManager
import com.example.calculator.presentation.theme.LocalCalculatorColors

private const val PIN_LENGTH = 4

@Composable
fun pinAuthScreen(
    onAuthenticated: () -> Unit
) {
    val context = LocalContext.current
    val configuration = LocalConfiguration.current
    val isPortrait = configuration.orientation == Configuration.ORIENTATION_PORTRAIT

    var mode by rememberSaveable { mutableStateOf(if (PasskeyManager.isPasskeySet(context)) "verify" else "set") }
    var pinInput by rememberSaveable { mutableStateOf("") }
    var firstPin by rememberSaveable { mutableStateOf<String?>(null) }
    var recoveryPhrase by rememberSaveable { mutableStateOf("") }
    var newPinInput by rememberSaveable { mutableStateOf("") }
    var firstNewPin by rememberSaveable { mutableStateOf<String?>(null) }
    var errorMessage by rememberSaveable { mutableStateOf("") }


    fun resetPinInput() { pinInput = "" }
    fun resetNewPinInput() { newPinInput = "" }

    @Composable
    fun pinIndicator(current: String) {
        val dotSize = if (isPortrait) 20.dp else 16.dp
        Row(
            horizontalArrangement = Arrangement.spacedBy(if (isPortrait) 12.dp else 8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            repeat(PIN_LENGTH) { index ->
                val filled = index < current.length
                Box(
                    modifier = Modifier
                        .size(dotSize)
                        .clip(CircleShape)
                        .background(
                            color = if (filled) LocalCalculatorColors.current.digitTextColor
                            else Color.LightGray
                        )
                )
            }
        }
    }

    fun onDigitClick(digit: String) {
        when (mode) {
            "verify" -> {
                if (pinInput.length < PIN_LENGTH) {
                    pinInput += digit
                    if (pinInput.length == PIN_LENGTH) {
                        if (PasskeyManager.verifyPasskey(context, pinInput)) {
                            onAuthenticated()
                        } else {
                            errorMessage = "Неверный PIN"
                            resetPinInput()
                        }
                    }
                }
            }
            "set" -> {
                if (firstPin == null) {
                    if (pinInput.length < PIN_LENGTH) {
                        pinInput += digit
                        if (pinInput.length == PIN_LENGTH) {
                            firstPin = pinInput
                            resetPinInput()
                        }
                    }
                } else {
                    if (pinInput.length < PIN_LENGTH) {
                        pinInput += digit
                        if (pinInput.length == PIN_LENGTH) {
                            if (pinInput == firstPin) {
                                if (recoveryPhrase.isBlank()) {
                                    errorMessage = "Введите контрольную фразу для восстановления"
                                    resetPinInput()
                                    return
                                }
                                PasskeyManager.setPasskey(context, pinInput, recoveryPhrase)
                                Toast.makeText(context, "PIN успешно установлен", Toast.LENGTH_SHORT).show()
                                onAuthenticated()
                            } else {
                                errorMessage = "Введённые PIN не совпадают. Попробуйте ещё раз."
                                firstPin = null
                                resetPinInput()
                            }
                        }
                    }
                }
            }
            "recover" -> {
                if (firstNewPin == null) {
                    if (newPinInput.length < PIN_LENGTH) {
                        newPinInput += digit
                        if (newPinInput.length == PIN_LENGTH) {
                            firstNewPin = newPinInput
                            resetNewPinInput()
                        }
                    }
                } else {
                    if (newPinInput.length < PIN_LENGTH) {
                        newPinInput += digit
                        if (newPinInput.length == PIN_LENGTH) {
                            if (newPinInput == firstNewPin) {
                                if (PasskeyManager.resetPasskey(context, recoveryPhrase, newPinInput)) {
                                    Toast.makeText(context, "PIN сброшен", Toast.LENGTH_SHORT).show()
                                    onAuthenticated()
                                } else {
                                    errorMessage = "Неверная контрольная фраза"
                                    firstNewPin = null
                                    resetNewPinInput()
                                }
                            } else {
                                errorMessage = "Введённые PIN не совпадают. Попробуйте ещё раз."
                                firstNewPin = null
                                resetNewPinInput()
                            }
                        }
                    }
                }
            }
        }
    }

    fun onDelete() {
        when (mode) {
            "verify", "set" -> {
                if (pinInput.isNotEmpty()) {
                    pinInput = pinInput.dropLast(1)
                }
            }
            "recover" -> {
                if (newPinInput.isNotEmpty()) {
                    newPinInput = newPinInput.dropLast(1)
                }
            }
        }
    }

    @Composable
    fun numberKeypad(
        onDigitClick: (String) -> Unit,
        onDelete: () -> Unit
    ) {
        val colors = LocalCalculatorColors.current
        val (columns, buttons, spacing) = if (isPortrait) {
            Triple(3, listOf("1", "2", "3",
                "4", "5", "6",
                "7", "8", "9",
                "←", "0", "OK"), 12.dp)
        } else {
            Triple(4, listOf("1", "2", "3", "←",
                "4", "5", "6", "0",
                "7", "8", "9", "OK"), 4.dp)
        }
        BoxWithConstraints {
            val gridWidth: Dp = if (isPortrait) maxWidth else maxWidth * 0.25f
            val totalSpacing = spacing * (columns + 1)
            val buttonSize: Dp = (gridWidth - totalSpacing) / columns
            LazyVerticalGrid(
                columns = GridCells.Fixed(columns),
                modifier = Modifier
                    .width(gridWidth)
                    .wrapContentHeight(),
                horizontalArrangement = Arrangement.spacedBy(spacing),
                verticalArrangement = Arrangement.spacedBy(spacing)
            ) {
                items(buttons.size) { index ->
                    val label = buttons[index]
                    val interactionSource = remember { MutableInteractionSource() }
                    val isPressed by interactionSource.collectIsPressedAsState()
                    val scale by animateFloatAsState(if (isPressed) 0.9f else 1f)
                    Surface(
                        modifier = Modifier
                            .size(buttonSize)
                            .scale(scale)
                            .clip(CircleShape)
                            .clickable(
                                interactionSource = interactionSource,
                                indication = null
                            ) {
                                when (label) {
                                    "←" -> onDelete()
                                    "OK" -> {  }
                                    else -> onDigitClick(label)
                                }
                            },
                        color = colors.buttonGray,
                        shadowElevation = 4.dp,
                        shape = CircleShape
                    ) {
                        Box(
                            contentAlignment = Alignment.Center,
                            modifier = Modifier.fillMaxSize()
                        ) {
                            Text(
                                text = label,
                                fontSize = if (isPortrait) 28.sp else 20.sp,
                                fontWeight = FontWeight.Bold,
                                textAlign = TextAlign.Center,
                                color = colors.digitTextColor
                            )
                        }
                    }
                }
            }
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(if (isPortrait) 16.dp else 8.dp),
        verticalArrangement = Arrangement.SpaceEvenly,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        when (mode) {
            "verify" -> {
                Text("Введите PIN", style = MaterialTheme.typography.headlineMedium)
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                pinIndicator(pinInput)
                if (errorMessage.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(errorMessage, color = MaterialTheme.colorScheme.error)
                }
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                numberKeypad(onDigitClick = { onDigitClick(it) }, onDelete = { onDelete() })
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                TextButton(onClick = {
                    mode = "recover"
                    errorMessage = ""
                    recoveryPhrase = ""
                    newPinInput = ""
                    firstNewPin = null
                }) {
                    Text("Забыли PIN?")
                }
            }
            "set" -> {
                if (firstPin == null) {
                    Text("Установите PIN", style = MaterialTheme.typography.headlineMedium)
                } else {
                    Text("Подтвердите PIN", style = MaterialTheme.typography.headlineMedium)
                }
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                pinIndicator(pinInput)
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                OutlinedTextField(
                    value = recoveryPhrase,
                    onValueChange = { recoveryPhrase = it },
                    label = { Text("Контрольная фраза для восстановления") },
                    modifier = Modifier.fillMaxWidth()
                )
                if (errorMessage.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(errorMessage, color = MaterialTheme.colorScheme.error)
                }
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                numberKeypad(onDigitClick = { onDigitClick(it) }, onDelete = { onDelete() })
            }
            "recover" -> {
                Text("Восстановление PIN", style = MaterialTheme.typography.headlineMedium)
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                OutlinedTextField(
                    value = recoveryPhrase,
                    onValueChange = { recoveryPhrase = it },
                    label = { Text("Введите контрольную фразу") },
                    modifier = Modifier.fillMaxWidth()
                )
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                if (firstNewPin == null) {
                    Text("Введите новый PIN", style = MaterialTheme.typography.headlineMedium)
                } else {
                    Text("Подтвердите новый PIN", style = MaterialTheme.typography.headlineMedium)
                }
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                pinIndicator(newPinInput)
                if (errorMessage.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(errorMessage, color = MaterialTheme.colorScheme.error)
                }
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                numberKeypad(onDigitClick = { onDigitClick(it) }, onDelete = { onDelete() })
                Spacer(modifier = Modifier.height(if (isPortrait) 16.dp else 8.dp))
                TextButton(onClick = {
                    mode = "verify"
                    resetPinInput()
                    resetNewPinInput()
                    firstNewPin = null
                    errorMessage = ""
                }) {
                    Text("Назад")
                }
            }
        }
    }
}
