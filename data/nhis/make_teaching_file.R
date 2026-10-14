# Build the NHIS 2025 teaching file from the NCHS public-use Sample Adult file.
#
# Source: National Center for Health Statistics. National Health Interview Survey, 2025.
#   Public-use data file and documentation: https://www.cdc.gov/nchs/nhis/
#   Data: https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHIS/2025/adult25csv.zip
#
# Usage (from the project root): Rscript data/nhis/make_teaching_file.R path/to/adult25.csv
# Keeps every adult and the original NCHS codes; recoding is taught in the lessons.

suppressMessages(library(readr))
suppressMessages(library(dplyr))

args <- commandArgs(trailingOnly = TRUE)
raw <- read_csv(args[1], guess_max = 24215, show_col_types = FALSE)

keep <- c(
  "HHX",                                  # household ID
  "WTFA_A", "PSTRAT", "PPSU",             # survey design: weight, stratum, PSU
  "PHSTAT_A",                             # self-rated health
  "CANEV_A", "NUMCAN_A", "SKNNMCAN_A",    # cancer history
  "POVRATTC_A", "EDUCP_A", "NOTCOV_A",    # socioeconomic position, insurance
  "AGEP_A", "SEX_A", "HISPALLP_A", "REGION", "URBRRL23"  # demographics
)

teach <- raw %>% select(all_of(keep))
stopifnot(nrow(teach) == 24215)
write_csv(teach, "data/nhis/nhis2025_adult.csv", na = "")
cat("Wrote data/nhis/nhis2025_adult.csv:", nrow(teach), "rows,", ncol(teach), "columns\n")
