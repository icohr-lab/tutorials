# Check that a lesson page's code runs inside the student starter project.
# Turns the lesson's code chunks into a script, removes the website-only setup chunk,
# and adds the setup lines every lesson script starts with.
#
# Usage, from inside an unzipped and prepared starter project (prepare.R already run):
#   Rscript path/to/test_lesson.R path/to/survey/n4-weights.qmd n4_test.R
#   Rscript n4_test.R
args <- commandArgs(TRUE)
knitr::purl(args[1], output = args[2], quiet = TRUE, documentation = 0)
code <- readLines(args[2])
start <- grep("^prep <- readLines", code)
end <- grep("^suppressMessages\\(eval", code)
if (length(start) && length(end)) code <- code[-(start:end)]
code <- code[!grepl("^options\\(pillar", code)]
code <- code[!grepl("starter/nhis-project", code, fixed = TRUE)]   # website-only paths
writeLines(code, args[2])
# Prepend the setup every lesson script starts with
writeLines(c("library(tidyverse)", "library(srvyr)", 'analysis <- readRDS("data/nhis_analysis.rds")',
             'if (file.exists("nchs_reliability.R")) source("nchs_reliability.R")', readLines(args[2])), args[2])
