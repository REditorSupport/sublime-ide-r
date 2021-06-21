detect_free_vars <- function(text) {
    f <- function() {}
    callee <- list(as.symbol("{"))
    callee <- append(callee, parse(text = text))
    body(f) <- as.call(callee)
    codetools::findGlobals(f, merge = FALSE)$variables
}

text <- paste(readLines(file("stdin")), collapse = "\n")

for (var in detect_free_vars(text)) {
    cat(var, "\n")
}
