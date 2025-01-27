package com.example.calculator.ui

import androidx.compose.animation.ExperimentalAnimationApi
import androidx.compose.animation.animateColorAsState
import androidx.compose.foundation.LocalIndication
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextRange
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.TextFieldValue
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.calculator.ui.theme.*
import androidx.compose.foundation.text.BasicTextField
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun CalculatorScreen(viewModel: CalculatorViewModel = viewModel()) {
    val uiState by viewModel.uiState.collectAsState()

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxSize()
            .background(CalcBackground)
            .padding(20.dp)
    ) {
        val screenHeight = maxHeight

        Column(
            modifier = Modifier.fillMaxSize()
        ) {
            PercentSpacer(0.01f)
            DisplayField(
                displayValue = uiState.displayValue,
                onValueChange = { newValue ->
                    viewModel.onDirectInputChange(newValue)
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(screenHeight * 0.19f)
            )
            PercentSpacer(0.05f)

            AdditionalDisplayField(
                displayValue = uiState.subDisplayValue,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(screenHeight * 0.05f)
            )

            PercentSpacer(0.03f)

            TopActionBar(
                onDelete = { viewModel.onButtonClick("⌫️") },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(screenHeight * 0.08f)
            )

            PercentSpacer(0.01f)

            LightDivider(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(1.dp)
            )

            PercentSpacer(0.03f)

            BasicCalcPad(
                onButtonClick = { text -> viewModel.onButtonClick(text) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(screenHeight * 0.7f)
            )
        }
    }
}

@Composable
fun PercentSpacer(percentage: Float) {
    BoxWithConstraints {
        val screenHeight = maxHeight
        Spacer(
            modifier = Modifier.height(screenHeight * percentage)
        )
    }
}

@Composable
fun DisplayField(
    displayValue: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var textFieldValue by remember {
        mutableStateOf(
            TextFieldValue(
                text = displayValue,
                selection = TextRange(displayValue.length)
            )
        )
    }

    LaunchedEffect(displayValue) {
        if (textFieldValue.text != displayValue) {
            textFieldValue = textFieldValue.copy(
                text = displayValue,
                selection = TextRange(displayValue.length)
            )
        }
    }

    val textSize = when {
        displayValue.length > 18 -> 30.sp
        displayValue.length > 12 -> 40.sp
        else -> 48.sp
    }

    Box(
        modifier = modifier
            .verticalScroll(rememberScrollState()),
        contentAlignment = Alignment.BottomEnd
    ) {
        BasicTextField(
            value = textFieldValue,
            onValueChange = { newValue ->
                textFieldValue = newValue
                onValueChange(newValue.text)
            },
            textStyle = TextStyle(
                fontSize = textSize,
                fontWeight = FontWeight.Normal,
                color = DigitTextColor,
                textAlign = TextAlign.End,
                lineHeight = 56.sp
            ),
            cursorBrush = androidx.compose.ui.graphics.SolidColor(Color.White),
            decorationBox = { innerTextField ->
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.BottomEnd
                ) {
                    if (textFieldValue.text.isEmpty()) {
                        Text(
                            text = "",
                            fontSize = textSize,
                            fontWeight = FontWeight.Normal,
                            color = DigitTextColor.copy(alpha = 0.4f),
                            textAlign = TextAlign.End,
                            lineHeight = 56.sp
                        )
                    }
                    innerTextField()
                }
            },
            modifier = Modifier.fillMaxSize()
        )
    }
}

@OptIn(ExperimentalAnimationApi::class)
@Composable
fun AdditionalDisplayField(displayValue: String, modifier: Modifier = Modifier) {
    Box(
        modifier = modifier,
        contentAlignment = Alignment.CenterEnd
    ) {
        Text(
            text = displayValue,
            fontSize = 30.sp,
            fontWeight = FontWeight.Normal,
            color = DigitTextColor.copy(alpha = 0.4f),
            textAlign = TextAlign.End,
            maxLines = 1
        )
    }
}

@Composable
fun TopActionBar(
    onDelete: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier,
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            ActionPlaceholderButton("🕒")
        }
        ActionPlaceholderButton("⌫️", onClick = onDelete)
    }
}

@Composable
fun ActionPlaceholderButton(label: String, onClick: () -> Unit = {}) {
    Box(
        contentAlignment = Alignment.Center,
        modifier = Modifier
            .size(50.dp)
            .clip(CircleShape)
            .clickable(
                onClick = onClick,
                indication = LocalIndication.current,
                interactionSource = remember { MutableInteractionSource() }
            )
    ) {
        Text(
            text = label,
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = Color.Gray.copy(alpha = 0.6f)
        )
    }
}

@Composable
fun BasicCalcPad(
    onButtonClick: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    val buttons = listOf(
        "C", "( )", "%", "÷",
        "7", "8", "9", "×",
        "4", "5", "6", "−",
        "1", "2", "3", "+",
        "+/-", "0", ",", "="
    )

    LazyVerticalGrid(
        columns = GridCells.Fixed(4),
        modifier = modifier,
        horizontalArrangement = Arrangement.spacedBy(20.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp)
    ) {
        items(buttons) { btnText ->
            CalculatorButton(
                text = btnText,
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(1f),
                onClick = { onButtonClick(btnText) }
            )
        }
    }
}

@Composable
fun CalculatorButton(
    text: String,
    modifier: Modifier = Modifier,
    onClick: () -> Unit
) {
    val backgroundColor: Color
    val contentColor: Color

    when (text) {
        "C" -> {
            backgroundColor = ClearButtonBackground
            contentColor = ClearButtonText
        }
        "=" -> {
            backgroundColor = EqualsButtonBackground
            contentColor = EqualsButtonText
        }
        "÷", "×", "−", "+", "%" -> {
            backgroundColor = ButtonGray
            contentColor = SymbolTextColor
        }
        "( )" -> {
            backgroundColor = ButtonGray
            contentColor = SymbolTextColor
        }
        "+/-", "," -> {
            backgroundColor = ButtonGray
            contentColor = DigitTextColor
        }
        else -> {
            if (text.all { it.isDigit() }) {
                backgroundColor = ButtonGray
                contentColor = DigitTextColor
            } else {
                backgroundColor = ButtonGray
                contentColor = Color.White
            }
        }
    }

    val fontSize = when (text) {
        "( )" -> 32.sp
        in listOf("%", "÷", "×", "−", "+", "=") -> 48.sp
        else -> 42.sp
    }

    val animatedBgColor by animateColorAsState(targetValue = backgroundColor)

    Box(
        contentAlignment = Alignment.Center,
        modifier = modifier
            .clip(CircleShape)
            .background(animatedBgColor)
            .clickable(
                onClick = onClick,
                indication = LocalIndication.current,
                interactionSource = remember { MutableInteractionSource() }
            )
            .padding(8.dp)
    ) {
        Text(
            text = text,
            fontSize = fontSize,
            fontWeight = FontWeight.Normal,
            color = contentColor
        )
    }
}

@Composable
fun LightDivider(modifier: Modifier = Modifier) {
    HorizontalDivider(
        modifier = modifier,
        thickness = 1.dp,
        color = Color.LightGray.copy(alpha = 0.5f)
    )
}
