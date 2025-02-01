package com.example.calculator.presentation.screens

import androidx.compose.foundation.LocalIndication
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.calculator.presentation.theme.LocalCalculatorColors

@Composable
fun additionalDisplayField(
    displayValue: String,
    modifier: Modifier = Modifier
) {
    val colors = LocalCalculatorColors.current
    Box(
        modifier = modifier,
        contentAlignment = Alignment.CenterEnd
    ) {
        Text(
            text = displayValue,
            fontSize = 30.sp,
            color = colors.digitTextColor.copy(alpha = 0.4f),
            maxLines = 1
        )
    }
}

@Composable
fun lightDivider(modifier: Modifier = Modifier) {
    HorizontalDivider(
        modifier = modifier,
        thickness = 1.dp,
        color = Color.LightGray.copy(alpha = 0.5f)
    )
}

@Composable
fun topActionBar(
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = androidx.compose.foundation.layout.Arrangement.SpaceBetween
    ) {
        Row {
            actionPlaceholderButton(label = "🕒")
        }
        actionPlaceholderButton(label = "⌫️", onClick = onDelete)
    }
}

@Composable
fun actionPlaceholderButton(
    label: String,
    onClick: () -> Unit = {}
) {
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .size(50.dp)
            .clip(CircleShape)
            .clickable(
                onClick = onClick,
                indication = LocalIndication.current,
                interactionSource = MutableInteractionSource()
            )
    ) {
        Text(
            text = label,
            fontSize = 24.sp,
            color = Color.Gray.copy(alpha = 0.6f)
        )
    }
}
