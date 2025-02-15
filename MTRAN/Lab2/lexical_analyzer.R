keywords <- c(
  "PROCEDURE", "OPTIONS", "DECLARE", "VAR", "STATIC", "INITIAL", "FILE",
  "OPEN", "UPDATE", "RECORD", "TITLE", "PUT", "SKIP", "LIST", "ADDR",
  "IF", "THEN", "GOTO", "CALL", "END", "BASED",
  "DO", "WHILE", "MOD", "CONTINUE", "REPEAT", "ELSE", "LEAVE", "TO",
  "BY", "LIKE"
)

operators_delimiters <- c(
  "(", ")", ";", ":", ",", "=", "+", "-", "*", "/",
  "{", "}", "[", "]", "<", ">", "."
)

data_types_list <- c(
  "CHAR", "FIXED", "DECIMAL", "BIT", "BINARY", "FLOAT", "COMPLEX",
  "LABEL", "ENTRY", "VARIABLE", "POINTER", "FILE", "CHARACTER"
)

identifiers_table <- list()
constants_table <- list()

lex_errors <- list()

token_id_counter <<- 1

get_data_type <- function(tok) {
  if (tok$type == "numeric_constant") {
    if (grepl("[\\.eE]", tok$value)) {
      return("Числовая константа с плавающей точкой")
    } else {
      return("Целочисленная константа")
    }
  } else if (tok$type == "string_constant") {
    if (nchar(tok$value) == 1) {
      return("Символьный литерал")
    } else {
      return("Строковый литерал")
    }
  } else if (tok$type == "bit_constant") {
    return("Битовая константа")
  } else if (tok$type == "identifier") {
    return("Идентификатор")
  } else if (tok$type == "keyword") {
    return(paste("Ключевое слово (KW_", toupper(tok$value), ")", sep = ""))
  } else if (tok$type == "operator") {
    op_map <- list(
      "="  = "OP_ASSIGN",
      "+"  = "OP_PLUS",
      "-"  = "OP_MINUS",
      "*"  = "OP_MULT",
      "/"  = "OP_DIV",
      "("  = "OP_LPAREN",
      ")"  = "OP_RPAREN",
      ":"  = "OP_COLON",
      ";"  = "OP_SEMICOLON",
      ","  = "OP_COMMA",
      "<=" = "OP_LE",
      ">=" = "OP_GE",
      "<>" = "OP_NE",
      "!=" = "OP_NE",
      "<"  = "OP_LT",
      ">"  = "OP_GT",
      "."  = "OP_DOT"
    )
    if (tok$value %in% names(op_map)) {
      return(paste("Оператор (", op_map[[tok$value]], ")", sep = ""))
    } else {
      return("Оператор/разделитель")
    }
  } else {
    return("Неизвестный тип")
  }
}

tokenize <- function(input) {
  tokens <- list()
  parenthesis_counter <- 0

  last_token_was_declare <- FALSE

  remove_leading_spaces <- function(s) {
    sub("^[[:space:]]+", "", s)
  }

  multi_operators <- c("<=", ">=", "<>", "!=")

  while (nchar(input) > 0) {
    input <- remove_leading_spaces(input)
    if (nchar(input) == 0) break

    if (last_token_was_declare) {
      m_decl <- regexpr("^[0-9]+[A-Za-z_]", input, perl = TRUE)
      if (m_decl[1] != -1) {
        m_full <- regexpr("^[0-9]+[A-Za-z0-9_]*", input, perl = TRUE)
        bad_name <- substring(input, 1, attr(m_full, "match.length"))

        err_msg <- sprintf(
          "Лексическая ошибка (token_id %d): После DECLARE встретилась слитная лексема '%s' (уровень и идентификатор без пробела).",
          token_id_counter,
          bad_name
        )
        lex_errors[[length(lex_errors) + 1]] <<- err_msg

        input <- substring(input, attr(m_full, "match.length") + 1)

        last_token_was_declare <- FALSE

        next
      }
    }

    token <- NULL

    m <- regexpr("^[0-9]+(\\.[0-9]+)?([eE][+-]?[0-9]+)?", input, perl = TRUE)
    if (m[1] != -1 && attr(m, "match.length") > 0) {
      val <- substring(input, 1, attr(m, "match.length"))
      token <- list(
        tokenID = token_id_counter,
        type = "numeric_constant",
        value = val
      )
      if (!(val %in% names(constants_table))) {
        constants_table[[val]] <<- token_id_counter
      }
      token$pointer <- constants_table[[val]]
      token_id_counter <<- token_id_counter + 1
      tokens[[length(tokens) + 1]] <- token

      input <- substring(input, attr(m, "match.length") + 1)
      last_token_was_declare <- FALSE
      next
    }

    if (substr(input, 1, 1) %in% c("'", "\"")) {
      quote_char <- substr(input, 1, 1)
      remaining <- substring(input, 2)
      pos_quote <- regexpr(quote_char, remaining, fixed = TRUE)
      pos_newline <- regexpr("\n", remaining, fixed = TRUE)

      if (pos_quote == -1 || (pos_newline != -1 && pos_newline < pos_quote)) {
        err_msg <- sprintf(
          "Лексическая ошибка (token_id %d): Незакрытая строковая константа, начинается с %s",
          token_id_counter, quote_char
        )
        lex_errors[[length(lex_errors) + 1]] <<- err_msg
        return(tokens)
      } else {
        match_length <- pos_quote + 1
        raw_val <- substring(input, 1, match_length)
        m_str <- regexpr("^('([^']*)'|\"([^\"]*)\")", raw_val, perl = TRUE)
        if (m_str[1] == -1 || attr(m_str, "match.length") == 0) {
          err_msg <- sprintf(
            "Лексическая ошибка (token_id %d): Ошибка в определении строковой константы.",
            token_id_counter
          )
          lex_errors[[length(lex_errors) + 1]] <<- err_msg
          return(tokens)
        }
        val <- sub("^['\"](.*)['\"]$", "\\1", raw_val)
        token <- list(
          tokenID = token_id_counter,
          type = "string_constant",
          value = val
        )
        if (!(val %in% names(constants_table))) {
          constants_table[[val]] <<- token_id_counter
        }
        token$pointer <- constants_table[[val]]
        token_id_counter <<- token_id_counter + 1
        tokens[[length(tokens) + 1]] <- token

        input <- substring(input, match_length + 1)
        last_token_was_declare <- FALSE
        next
      }
    }

    m <- regexpr("^[A-Za-z][A-Za-z0-9_]*", input, perl = TRUE)
    if (m[1] != -1 && attr(m, "match.length") > 0) {
      val <- substring(input, 1, attr(m, "match.length"))
      if (val %in% data_types_list) {
        token <- list(
          tokenID = token_id_counter,
          type = "identifier",
          value = val
        )
        if (!(val %in% names(identifiers_table))) {
          identifiers_table[[val]] <<- token_id_counter
        }
        token$pointer <- identifiers_table[[val]]

        last_token_was_declare <- FALSE
      } else if (val %in% keywords) {
        token <- list(
          tokenID = token_id_counter,
          type = "keyword",
          value = val
        )

        if (val == "DECLARE") {
          last_token_was_declare <- TRUE
        } else {
          last_token_was_declare <- FALSE
        }
      } else {
        token <- list(
          tokenID = token_id_counter,
          type = "identifier",
          value = val
        )
        if (!(val %in% names(identifiers_table))) {
          identifiers_table[[val]] <<- token_id_counter
        }
        token$pointer <- identifiers_table[[val]]

        last_token_was_declare <- FALSE
      }
      token_id_counter <<- token_id_counter + 1
      tokens[[length(tokens) + 1]] <- token
      input <- substring(input, attr(m, "match.length") + 1)
      next
    }

    if (nchar(input) >= 2) {
      potential_op <- substr(input, 1, 2)
      if (potential_op %in% multi_operators) {
        token <- list(
          tokenID = token_id_counter,
          type = "operator",
          value = potential_op
        )
        token$pointer <- token_id_counter
        token_id_counter <<- token_id_counter + 1
        tokens[[length(tokens) + 1]] <- token

        if (potential_op == "(") {
          parenthesis_counter <- parenthesis_counter + 1
        } else if (potential_op == ")") {
          if (parenthesis_counter == 0) {
            err_msg <- sprintf(
              "Лексическая ошибка (token_id %d): Избыточная закрывающая скобка.",
              token_id_counter
            )
            lex_errors[[length(lex_errors) + 1]] <<- err_msg
            return(tokens)
          } else {
            parenthesis_counter <- parenthesis_counter - 1
          }
        }
        input <- substring(input, 3)
        last_token_was_declare <- FALSE
        next
      }
    }

    op <- substr(input, 1, 1)
    if (op %in% operators_delimiters) {
      token <- list(
        tokenID = token_id_counter,
        type = "operator",
        value = op
      )
      token$pointer <- token_id_counter
      token_id_counter <<- token_id_counter + 1
      tokens[[length(tokens) + 1]] <- token

      if (op == "(") {
        parenthesis_counter <- parenthesis_counter + 1
      } else if (op == ")") {
        if (parenthesis_counter == 0) {
          err_msg <- sprintf(
            "Лексическая ошибка (token_id %d): Избыточная закрывающая скобка.",
            token_id_counter
          )
          lex_errors[[length(lex_errors) + 1]] <<- err_msg
          return(tokens)
        } else {
          parenthesis_counter <- parenthesis_counter - 1
        }
      }
      input <- substring(input, 2)
      last_token_was_declare <- FALSE
      next
    }

    err_char <- substr(input, 1, 1)
    err_msg <- sprintf(
      "Лексическая ошибка (token_id %d): Неопознанный символ: '%s'",
      token_id_counter, err_char
    )
    lex_errors[[length(lex_errors) + 1]] <<- err_msg
    return(tokens)
  }

  if (parenthesis_counter > 0) {
    err_msg <- sprintf(
      "Лексическая ошибка: Незакрытых открывающих скобок: %d",
      parenthesis_counter
    )
    lex_errors[[length(lex_errors) + 1]] <<- err_msg
    return(tokens)
  }

  return(tokens)
}

group_tokens <- function(tokens) {
  tokens <- lapply(tokens, function(tok) {
    if (tok$type == "identifier" && (tok$value %in% keywords) &&
      !(tok$value %in% data_types_list)) {
      tok$type <- "keyword"
    }
    return(tok)
  })

  groups <- list(
    identifiers = Filter(function(tok) tok$type == "identifier", tokens),
    constants = Filter(function(tok) {
      tok$type %in% c("numeric_constant", "string_constant")
    }, tokens),
    keywords = Filter(function(tok) tok$type == "keyword", tokens),
    operators = Filter(function(tok) tok$type == "operator", tokens)
  )

  groups$types <- Filter(
    function(tok) tok$value %in% data_types_list,
    groups$identifiers
  )
  groups$variables <- Filter(function(tok) {
    !(tok$value %in% data_types_list)
  }, groups$identifiers)

  return(groups)
}

unique_tokens <- function(token_group) {
  keys <- sapply(token_group, function(tok) {
    paste(tok$type, tok$value, sep = "|")
  })
  unique_indices <- which(!duplicated(keys))
  return(token_group[unique_indices])
}

print_token_group <- function(group_name, token_group, con) {
  unique_group <- unique_tokens(token_group)

  id_col_width <- 5
  value_col_width <- 40
  type_col_width <- 40

  writeLines(sprintf("=== %s ===", group_name), con)
  header <- paste(
    pad_string("ID", id_col_width),
    pad_string("Значение", value_col_width),
    pad_string("Тип данных", type_col_width)
  )
  writeLines(header, con)
  writeLines(strrep("-", id_col_width + value_col_width +
    type_col_width + 2), con)

  for (tok in unique_group) {
    value <- tok$value
    dtype <- get_data_type(tok)

    line <- paste(
      pad_string(as.character(tok$tokenID), id_col_width),
      pad_string(value, value_col_width),
      pad_string(dtype, type_col_width)
    )
    writeLines(line, con)
  }
  writeLines("", con)
}

pad_string <- function(text, width) {
  w <- nchar(text, type = "width")
  if (w >= width) {
    return(paste0(substr(text, 1, width - 3), "..."))
  } else {
    spaces <- strrep(" ", width - w)
    return(paste0(text, spaces))
  }
}

output_results <- function(tokens,
                           output_filename = "LEXICAL_OUTPUT.txt") {
  con <- file(output_filename, open = "w", encoding = "UTF-8")
  groups <- group_tokens(tokens)

  print_token_group("Типы данных", groups$types, con)
  print_token_group("Переменные", groups$variables, con)
  print_token_group("Константы", groups$constants, con)
  print_token_group("Ключевые слова", groups$keywords, con)
  print_token_group("Операторы и разделители", groups$operators, con)

  writeLines("=== Лексические ошибки ===", con)
  if (length(lex_errors) > 0) {
    for (err in lex_errors) {
      writeLines(err, con)
    }
  } else {
    writeLines("Ошибок не обнаружено.", con)
  }
  close(con)
}

if (file.exists("INPUT.TXT")) {
  input_text <- paste(readLines("INPUT.TXT", warn = FALSE), collapse = "\n")
}

tokens <- tokenize(input_text)
output_results(tokens, "output.txt")
