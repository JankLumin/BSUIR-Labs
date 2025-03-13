if (!require(jsonlite)) {
    install.packages("jsonlite", repos = "http://cran.us.r-project.org")
    library(jsonlite)
}

tree <- fromJSON(
    "st_tree.txt",
    flatten           = FALSE,
    simplifyDataFrame = FALSE,
    simplifyMatrix    = FALSE,
    simplifyVector    = FALSE
)

output_file <- "semantic_errors.txt"
semantic_errors <- c()

type_keywords <- c(
    "CHAR", "CHARACTER", "BIT", "FIXED", "DECIMAL", "BINARY",
    "FLOAT", "COMPLEX", "LABEL", "ENTRY", "FILE",
    "POINTER", "VAR", "STATIC", "BASED", "INITIAL", "LIKE"
)

known_labels_or_procs <- c("test", "geometric_mean", "simple_procedure")

extractTypeAndInitialValue <- function(tokens) {
    typeTokens <- c()
    initValue <- NULL

    inInitial <- FALSE
    bufInit <- c()

    for (tok in tokens) {
        if (tok$type == "keyword" && toupper(tok$value) == "INITIAL") {
            inInitial <- TRUE
            next
        }
        if (inInitial) {
            if (tok$type == "operator" && tok$value == "(") {
                next
            } else if (tok$type == "operator" && tok$value == ")") {
                inInitial <- FALSE
                rawInit <- paste0(bufInit, collapse = "")
                rawInit <- trimws(rawInit)

                if (grepl("^['\"]", rawInit) && grepl("['\"]$", rawInit)) {
                    rawInit <- substring(rawInit, 2, nchar(rawInit) - 1)
                }

                initValue <- rawInit
                bufInit <- c()
            } else {
                bufInit <- c(bufInit, tok$value)
            }
        } else {
            if (!(toupper(tok$value) %in% c(
                "DECLARE", "VAR", "STATIC", "BASED", "INITIAL",
                "LABEL", "ENTRY", "POINTER", "FILE", "LIKE", "CHARACTER"
            ))) {
                typeTokens <- c(typeTokens, tok$value)
            }
        }
    }

    rawType <- paste(typeTokens, collapse = " ")
    rawType <- gsub("\\s*\\(\\s*", "(", rawType)
    rawType <- gsub("\\s*\\)\\s*", ")", rawType)
    rawType <- gsub("\\s*,\\s*", ",", rawType)

    list(type = rawType, init = initValue)
}

checkTypeCompatibility <- function(declaredType, initVal) {
    if (is.null(initVal)) {
        return(NULL)
    }

    if (grepl("CHAR", declaredType, ignore.case = TRUE)) {
        if (!is.na(suppressWarnings(as.numeric(initVal)))) {
            return(paste("Ошибка: для CHAR/CHARACTER ожидается строка, получено числовое:", initVal))
        }
    }

    if (grepl("BIT", declaredType, ignore.case = TRUE)) {
        valNoSpace <- gsub("\\s+", "", initVal)
        if (!grepl("^[01]+B$", valNoSpace)) {
            return(paste("Ошибка: для BIT(...) нужно двоичное значение с 'B' на конце, получено:", initVal))
        }
    }

    if (grepl("FIXED BINARY", declaredType, ignore.case = TRUE)) {
        if (!grepl("^[0-9]+$", initVal)) {
            return(paste("Ошибка: для FIXED BINARY ожидается целое число, получено:", initVal))
        }
    }

    if (grepl("FIXED DECIMAL", declaredType, ignore.case = TRUE)) {
        if (!grepl("^[0-9]+(\\.[0-9]+)?$", initVal)) {
            return(paste("Ошибка: для FIXED DECIMAL ожидается числовое значение, получено:", initVal))
        }
    }

    if (grepl("\\bFLOAT\\b", declaredType, ignore.case = TRUE) &&
        !grepl("COMPLEX FLOAT", declaredType, ignore.case = TRUE)) {
        if (!grepl("^[0-9]+(\\.[0-9]+)?$", initVal)) {
            return(paste("Ошибка: для FLOAT ожидается вещественное число, получено:", initVal))
        }
    }

    if (grepl("COMPLEX FLOAT", declaredType, ignore.case = TRUE)) {
        if (!grepl("^[0-9]+\\+[0-9]+I$", initVal)) {
            return(paste("Ошибка: для COMPLEX FLOAT ожидается a+bI, получено:", initVal))
        }
    }

    if (grepl("DECIMAL FLOAT", declaredType, ignore.case = TRUE)) {
        if (!grepl("^[0-9]+(\\.[0-9]+)?$", initVal)) {
            return(paste("Ошибка: для DECIMAL FLOAT ожидается вещественное число, получено:", initVal))
        }
    }

    return(NULL)
}

symbol_table <- list()

processDeclarationTokens <- function(tokens) {
    idx_identifier <- NULL
    for (i in seq_along(tokens)) {
        if (tokens[[i]]$type == "identifier" &&
            !(toupper(tokens[[i]]$value) %in% toupper(type_keywords))) {
            idx_identifier <- i
            break
        }
    }
    if (is.null(idx_identifier)) {
        semantic_errors <<- c(semantic_errors, "Ошибка: DECLARE не содержит нормального идентификатора!")
        return()
    }

    varName <- tokens[[idx_identifier]]$value
    leftover <- tokens[-(1:idx_identifier)]

    info <- extractTypeAndInitialValue(leftover)
    err <- checkTypeCompatibility(info$type, info$init)
    if (!is.null(err)) {
        semantic_errors <<- c(
            semantic_errors,
            paste0("Переменная ", varName, ": ", err)
        )
    }

    symbol_table[[varName]] <<- list(type = info$type, init = info$init)
}

if (!is.null(tree$declarations)) {
    for (decl in tree$declarations) {
        tokens <- decl$tokens
        processDeclarationTokens(tokens)
    }
}

if (!is.null(tree$statements)) {
    for (stmt in tree$statements) {
        tokens <- stmt$tokens
        if (length(tokens) == 0) next

        if (tokens[[1]]$type == "keyword" && toupper(tokens[[1]]$value) == "DECLARE") {
            processDeclarationTokens(tokens)
        } else {
            i <- 1
            while (i <= length(tokens)) {
                if (tokens[[i]]$type == "identifier") {
                    ident <- tokens[[i]]$value

                    if (toupper(ident) %in% toupper(type_keywords)) {
                        i <- i + 1
                        next
                    }
                    if (ident %in% known_labels_or_procs) {
                        i <- i + 1
                        next
                    }

                    if (!(ident %in% names(symbol_table))) {
                        semantic_errors <- c(
                            semantic_errors,
                            paste(
                                "Предупреждение: идентификатор", ident,
                                "использован, но не объявлен (как переменная/метка/процедура)."
                            )
                        )
                    }

                    j <- i + 1
                    while (j <= length(tokens)) {
                        if (tokens[[j]]$type == "operator" &&
                            tokens[[j]]$value %in% c(".", "(", ")", ":", ",")) {
                            j <- j + 1
                        } else if (tokens[[j]]$type %in% c("numeric_constant", "identifier")) {
                            j <- j + 1
                        } else {
                            break
                        }
                    }

                    i <- j
                    next
                }

                i <- i + 1
            }
        }
    }
}

if (length(semantic_errors) == 0) {
    cat("Семантических ошибок не обнаружено.\n", file = output_file)
    message("Семантических ошибок не обнаружено.")
} else {
    cat("Найдены семантические ошибки:\n\n", file = output_file)
    for (err in semantic_errors) {
        cat("- ", err, "\n", file = output_file, append = TRUE)
    }
    message("Семантические ошибки записаны в файл 'semantic_errors.txt'.")
}
