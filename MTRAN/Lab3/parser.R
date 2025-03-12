library(jsonlite)
library(DiagrammeR)
library(DiagrammeRsvg)
library(rsvg)

tokens <- fromJSON("tokens_output.json", simplifyDataFrame = FALSE)
pos <- 1

currentToken <- function() {
    if (pos <= length(tokens)) {
        return(tokens[[pos]])
    } else {
        return(NULL)
    }
}

peekToken <- function() {
    if (pos + 1 <= length(tokens)) {
        return(tokens[[pos + 1]])
    } else {
        return(NULL)
    }
}

nextToken <- function() {
    pos <<- pos + 1
    return(currentToken())
}

createTokenNode <- function(expectedType = NULL) {
    token <- currentToken()
    if (is.null(token)) {
        stop("Неожиданный конец токенов")
    }
    cat(sprintf(
        "Parsed token: id=%s, type=%s, value=%s\n",
        token$tokenID, token$type, token$value
    ))
    node <- list(type = token$type, value = token$value)
    pos <<- pos + 1
    return(node)
}

parseProcedureHeader <- function() {
    header <- list(type = "ProcedureHeader")
    header$identifier <- createTokenNode("identifier")
    header$separator <- createTokenNode("operator")
    header$procedureKeyword <- createTokenNode("keyword")
    header$optionsKeyword <- createTokenNode("keyword")
    header$openParen <- createTokenNode("operator")
    header$options <- createTokenNode("identifier")
    header$closeParen <- createTokenNode("operator")
    header$endHeader <- createTokenNode("operator")
    return(header)
}

parseDeclaration <- function() {
    decl <- list(type = "Declaration")
    decl$declareKeyword <- createTokenNode("keyword")
    decl$tokens <- list()
    while (!is.null(currentToken())) {
        token <- currentToken()
        if (token$type == "operator" && token$value == ";") {
            decl$endDeclaration <- createTokenNode("operator")
            break
        }
        decl$tokens <- c(decl$tokens, list(createTokenNode()))
    }
    return(decl)
}

parseDeclarations <- function() {
    decls <- list()
    while (!is.null(currentToken()) &&
        currentToken()$type == "keyword" &&
        currentToken()$value == "DECLARE") {
        decls <- c(decls, list(parseDeclaration()))
    }
    return(decls)
}

parseStatementBlock <- function() {
    block <- list(type = "StatementBlock", tokens = list())
    token <- currentToken()
    if (!is.null(token) && token$type == "keyword" && token$value == "END") {
        block$tokens <- c(block$tokens, list(createTokenNode()))
        return(block)
    }
    while (!is.null(currentToken())) {
        token <- currentToken()
        if (token$type == "operator" && token$value == ";") {
            block$tokens <- c(block$tokens, list(createTokenNode()))
            break
        }
        block$tokens <- c(block$tokens, list(createTokenNode()))
    }
    return(block)
}

parseStatements <- function(procName) {
    stmts <- list()
    while (!is.null(currentToken())) {
        token <- currentToken()
        if (token$type == "keyword" && token$value == "END") {
            nextTok <- peekToken()
            if (!is.null(nextTok) &&
                nextTok$type == "identifier" &&
                trimws(nextTok$value) == procName) {
                break
            }
        }
        stmts <- c(stmts, list(parseStatementBlock()))
    }
    return(stmts)
}

parseProcedureEnd <- function(expectedName) {
    procEnd <- list(type = "ProcedureEnd")
    procEnd$endKeyword <- createTokenNode("keyword")
    procEnd$identifier <- createTokenNode("identifier")
    if (procEnd$identifier$value != expectedName) {
        stop("Идентификатор завершения процедуры не совпадает с именем процедуры")
    }
    procEnd$endSymbol <- createTokenNode("operator")
    return(procEnd)
}

parseProcedure <- function() {
    ast <- list(type = "Procedure")
    ast$header <- parseProcedureHeader()
    ast$declarations <- parseDeclarations()
    procName <- ast$header$identifier$value
    ast$statements <- parseStatements(procName)
    ast$procedureEnd <- parseProcedureEnd(procName)
    return(ast)
}

ast_tree <- parseProcedure()

ast_text <- toJSON(ast_tree, pretty = TRUE, auto_unbox = TRUE)
write(ast_text, file = "ast_tree.txt")

dotNodes <- c()
dotEdges <- c()
nodeIdCounter <- 0

newNodeId <- function() {
    nodeIdCounter <<- nodeIdCounter + 1
    return(paste0("node", nodeIdCounter))
}

traverseAst <- function(ast, parent = NULL, edgeLabel = NULL) {
    currentId <- newNodeId()
    label <- ""
    if (is.list(ast)) {
        if (length(ast) == 2 && all(c("type", "value") %in% names(ast))) {
            label <- paste0(ast$type, ": ", ast$value)
        } else if (!is.null(ast$type)) {
            label <- ast$type
        } else {
            label <- "Object"
        }
    } else {
        label <- as.character(ast)
    }
    label <- gsub('"', '\\"', label)
    dotNodes <<- c(dotNodes, sprintf('  %s [label="%s"];', currentId, label))

    if (!is.null(parent)) {
        if (!is.null(edgeLabel)) {
            dotEdges <<- c(dotEdges, sprintf('  %s -> %s [label="%s"];', parent, currentId, edgeLabel))
        } else {
            dotEdges <<- c(dotEdges, sprintf("  %s -> %s;", parent, currentId))
        }
    }

    if (is.list(ast) && !(length(ast) == 2 && all(c("type", "value") %in% names(ast)))) {
        if (!is.null(names(ast))) {
            for (name in names(ast)) {
                if (name == "pointer") next
                child <- ast[[name]]
                if (!is.null(child)) {
                    if (is.list(child)) {
                        traverseAst(child, currentId, name)
                    } else {
                        childId <- newNodeId()
                        dotNodes <<- c(dotNodes, sprintf('  %s [label="%s"];', childId, as.character(child)))
                        dotEdges <<- c(dotEdges, sprintf('  %s -> %s [label="%s"];', currentId, childId, name))
                    }
                }
            }
        } else {
            for (child in ast) {
                if (!is.null(child)) {
                    if (is.list(child)) {
                        traverseAst(child, currentId)
                    } else {
                        childId <- newNodeId()
                        dotNodes <<- c(dotNodes, sprintf('  %s [label="%s"];', childId, as.character(child)))
                        dotEdges <<- c(dotEdges, sprintf("  %s -> %s;", currentId, childId))
                    }
                }
            }
        }
    }
    return(currentId)
}

dotNodes <<- c()
dotEdges <<- c()
nodeIdCounter <<- 0
rootId <- traverseAst(ast_tree)
dotGraphString <- paste("digraph AST {",
    paste(dotNodes, collapse = "\n"),
    paste(dotEdges, collapse = "\n"),
    "}",
    sep = "\n"
)

svg_code <- export_svg(grViz(dotGraphString))
write(svg_code, file = "ast_tree.svg")

cat("AST дерево сохранено в 'ast_tree.txt'\n")
cat("Визуальное представление AST сохранено в 'ast_tree.svg'\n")
