# prepare.R: build the analysis file from the NHIS 2025 teaching file
# This is the code from lesson N2, as a script. Run it once at the start of
# each lesson (Source button, or Ctrl+Shift+S / Cmd+Shift+S).

library(tidyverse)

nhis <- read_csv("data/nhis2025_adult.csv")

nhis <- nhis %>%
  mutate(
    # Outcome: fair or poor self-rated health (7, 8, 9 = not an answer)
    fair_poor = case_when(
      PHSTAT_A %in% c(4, 5) ~ 1,
      PHSTAT_A %in% c(1, 2, 3) ~ 0,
      .default = NA
    ),

    # Cancer survivor, excluding people whose only cancer was non-melanoma skin cancer
    skin_only = NUMCAN_A == 1 & SKNNMCAN_A %in% 1,
    survivor = case_when(
      CANEV_A == 1 & !skin_only ~ 1,
      CANEV_A == 2 | skin_only ~ 0,
      .default = NA
    ),

    # Family income as a multiple of the poverty line
    poverty = case_when(
      POVRATTC_A < 1 ~ "Below 100%",
      POVRATTC_A < 2 ~ "100-199%",
      POVRATTC_A < 4 ~ "200-399%",
      POVRATTC_A >= 4 ~ "400% or more"
    ),
    poverty = factor(poverty, levels = c("Below 100%", "100-199%", "200-399%", "400% or more")),

    # Education
    education = case_when(
      EDUCP_A %in% 1:4 ~ "High school or less",
      EDUCP_A %in% 5:7 ~ "Some college",
      EDUCP_A %in% 8:10 ~ "Bachelor or higher",
      .default = NA
    ),
    education = factor(education, levels = c("High school or less", "Some college", "Bachelor or higher")),

    # Age (85 means 85 or older; 97, 98, 99 are not ages), sex, insurance
    age = if_else(AGEP_A %in% c(97, 98, 99), NA, AGEP_A),
    age_group = case_when(
      age < 45 ~ "18-44",
      age < 65 ~ "45-64",
      age >= 65 ~ "65+",
      .default = NA
    ),
    sex = case_when(SEX_A == 1 ~ "Male", SEX_A == 2 ~ "Female", .default = NA),
    insured = case_when(NOTCOV_A == 2 ~ "Yes", NOTCOV_A == 1 ~ "No", .default = NA)
  )

# Keep every adult, and keep the survey design columns
analysis <- nhis %>%
  select(HHX, WTFA_A, PSTRAT, PPSU,
         fair_poor, survivor, poverty, education, age, age_group, sex, insured)

# .rds keeps R details such as the order of factor categories; a CSV would lose them
saveRDS(analysis, "data/nhis_analysis.rds")
