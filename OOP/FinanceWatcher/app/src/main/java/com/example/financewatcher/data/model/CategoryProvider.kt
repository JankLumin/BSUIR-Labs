package com.example.financewatcher.data.model

import com.example.financewatcher.R

object CategoryProvider {
    val categories = listOf(
        OperationCategory(id = "1", name = R.string.category_food),
        OperationCategory(id = "2", name = R.string.category_transport),
        OperationCategory(id = "3", name = R.string.category_health),
        OperationCategory(id = "4", name = R.string.category_entertainment),
        OperationCategory(id = "5", name = R.string.category_bills),
        OperationCategory(id = "6", name = R.string.category_shopping),
        OperationCategory(id = "7", name = R.string.category_education),
        OperationCategory(id = "8", name = R.string.category_other)
    )
}
