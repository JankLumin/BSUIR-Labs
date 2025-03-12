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
  original_input <- input
  current_index <- 1
  input_length <- nchar(original_input)
  parenthesis_counter <- 0
  last_token_was_declare <- FALSE
  multi_operators <- c("<=", ">=", "<>", "!=")

  skip_whitespace <- function() {
    rest <- substring(original_input, current_index, input_length)
    ws_match <- regexpr("^[[:space:]]+", rest, perl = TRUE)
    if (ws_match[1] != -1) {
      ws_length <- attr(ws_match, "match.length")
      current_index <<- current_index + ws_length
    }
  }

  while (current_index <= input_length) {
    skip_whitespace()
    if (current_index > input_length) break
    rest <- substring(original_input, current_index, input_length)

    if (last_token_was_declare) {
      m_decl <- regexpr("^[0-9]+[A-Za-z_]", rest, perl = TRUE)
      if (m_decl[1] != -1) {
        m_full <- regexpr("^[0-9]+[A-Za-z0-9_]*", rest, perl = TRUE)
        bad_name <- substring(rest, 1, attr(m_full, "match.length"))
        err_msg <- sprintf(
          "Лексическая ошибка (token_id %d): После DECLARE обнаружена слитная лексема '%s' (уровень и идентификатор без пробела).",
          token_id_counter,
          bad_name
        )
        lex_errors[[length(lex_errors) + 1]] <<- err_msg
        current_index <- current_index + attr(m_full, "match.length")
        last_token_was_declare <- FALSE
        next
      }
    }

    token <- NULL
    token_start <- current_index

    m <- regexpr("^[0-9]+(\\.[0-9]+)?([eE][+-]?[0-9]+)?", rest, perl = TRUE)
    if (m[1] != -1 && attr(m, "match.length") > 0) {
      match_length <- attr(m, "match.length")
      val <- substring(rest, 1, match_length)
      token <- list(
        tokenID = token_id_counter,
        type = "numeric_constant",
        value = val,
        pos = token_start,
        end = token_start + match_length - 1
      )
      if (!(val %in% names(constants_table))) {
        constants_table[[val]] <<- token_id_counter
      }
      token$pointer <- constants_table[[val]]
      token_id_counter <<- token_id_counter + 1
      tokens[[length(tokens) + 1]] <- token
      current_index <- current_index + match_length
      last_token_was_declare <- FALSE
      next
    }

    if (substr(rest, 1, 1) %in% c("'", "\"")) {
      quote_char <- substr(rest, 1, 1)
      remaining <- substring(rest, 2)
      pos_quote <- regexpr(quote_char, remaining, fixed = TRUE)
      pos_newline <- regexpr("\n", remaining, fixed = TRUE)

      if (pos_quote == -1 || (pos_newline != -1 && pos_newline < pos_quote)) {
        err_msg <- sprintf(
          "Лексическая ошибка (token_id %d): Незакрытая строковая константа, начинается с %s",
          token_id_counter, quote_char
        )
        lex_errors[[length(lex_errors) + 1]] <<- err_msg
        break
      } else {
        match_length <- pos_quote + 1
        raw_val <- substring(rest, 1, match_length + 1)
        m_str <- regexpr("^('([^']*)'|\"([^\"]*)\")", raw_val, perl = TRUE)
        if (m_str[1] == -1 || attr(m_str, "match.length") == 0) {
          err_msg <- sprintf(
            "Лексическая ошибка (token_id %d): Ошибка при определении строковой константы.",
            token_id_counter
          )
          lex_errors[[length(lex_errors) + 1]] <<- err_msg
          break
        }
        match_length <- attr(m_str, "match.length")
        val <- sub("^['\"](.*)['\"]$", "\\1", substring(raw_val, 1, match_length))
        token <- list(
          tokenID = token_id_counter,
          type = "string_constant",
          value = val,
          pos = token_start,
          end = token_start + match_length - 1
        )
        if (!(val %in% names(constants_table))) {
          constants_table[[val]] <<- token_id_counter
        }
        token$pointer <- constants_table[[val]]
        token_id_counter <<- token_id_counter + 1
        tokens[[length(tokens) + 1]] <- token
        current_index <- current_index + match_length
        last_token_was_declare <- FALSE
        next
      }
    }

    m <- regexpr("^[A-Za-z][A-Za-z0-9_]*", rest, perl = TRUE)
    if (m[1] != -1 && attr(m, "match.length") > 0) {
      match_length <- attr(m, "match.length")
      val <- substring(rest, 1, match_length)
      if (val %in% data_types_list) {
        token <- list(
          tokenID = token_id_counter,
          type = "identifier",
          value = val,
          pos = token_start,
          end = token_start + match_length - 1
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
          value = val,
          pos = token_start,
          end = token_start + match_length - 1
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
          value = val,
          pos = token_start,
          end = token_start + match_length - 1
        )
        if (!(val %in% names(identifiers_table))) {
          identifiers_table[[val]] <<- token_id_counter
        }
        token$pointer <- identifiers_table[[val]]
        last_token_was_declare <- FALSE
      }
      token_id_counter <<- token_id_counter + 1
      tokens[[length(tokens) + 1]] <- token
      current_index <- current_index + match_length
      next
    }

    if (nchar(rest) >= 2) {
      potential_op <- substr(rest, 1, 2)
      if (potential_op %in% multi_operators) {
        token <- list(
          tokenID = token_id_counter,
          type = "operator",
          value = potential_op,
          pos = token_start,
          end = token_start + 2 - 1
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
            break
          } else {
            parenthesis_counter <- parenthesis_counter - 1
          }
        }
        current_index <- current_index + 2
        last_token_was_declare <- FALSE
        next
      }
    }

    op <- substr(rest, 1, 1)
    if (op %in% operators_delimiters) {
      token <- list(
        tokenID = token_id_counter,
        type = "operator",
        value = op,
        pos = token_start,
        end = token_start
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
          break
        } else {
          parenthesis_counter <- parenthesis_counter - 1
        }
      }
      current_index <- current_index + 1
      last_token_was_declare <- FALSE
      next
    }

    err_char <- substr(rest, 1, 1)
    err_msg <- sprintf(
      "Лексическая ошибка (token_id %d): Неопознанный символ: '%s'",
      token_id_counter, err_char
    )
    lex_errors[[length(lex_errors) + 1]] <<- err_msg
    break
  }

  if (parenthesis_counter > 0) {
    err_msg <- sprintf(
      "Лексическая ошибка: Незакрытых открывающих скобок: %d",
      parenthesis_counter
    )
    lex_errors[[length(lex_errors) + 1]] <<- err_msg
  }

  return(tokens)
}

if (file.exists("INPUT.TXT")) {
  input_text <- paste(readLines("INPUT.TXT", warn = FALSE), collapse = "\n")
  token_list <- tokenize(input_text)

  for (tok in token_list) {
    cat(sprintf(
      "ID:%d  Тип:%s  Значение:'%s'  Позиция:%d-%d\n",
      tok$tokenID, tok$type, tok$value, tok$pos, tok$end
    ))
  }

  if (!require(jsonlite, quietly = TRUE)) {
    install.packages("jsonlite")
    library(jsonlite)
  }

  json_tokens <- toJSON(token_list, pretty = TRUE, auto_unbox = TRUE)
  write(json_tokens, file = "tokens_output.json")

  cat("Список токенов сохранён в файл tokens_output.json\n")
}
