# nchs_reliability.R: check estimated proportions against the
# NCHS Data Presentation Standards for Proportions
# (Parker JD et al. Vital Health Stat 2(175), 2017; https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf)
#
# Load it with source("nchs_reliability.R"), then:
#   check_proportion(design, fair_poor)            one estimate
#   check_proportion(design, fair_poor, poverty)   one estimate per group
# `design` is a srvyr design (already filtered to your subgroup); the variable must be 0/1.

library(survey)
library(srvyr)
library(dplyr)

nchs_one <- function(design, var_name) {
  values <- design$variables[[var_name]]
  ok <- !is.na(values)
  n <- sum(ok)                      # denominator sample size
  events <- sum(values[ok] == 1)    # numerator events
  f <- reformulate(var_name)
  est <- svymean(f, design, na.rm = TRUE, deff = TRUE)
  p <- unname(coef(est))
  n_eff <- min(n / unname(deff(est)), n)   # effective sample size, never above n
  if (p == 0 || p == 1) n_eff <- n
  # Korn-Graubard (Clopper-Pearson adapted for complex surveys) 95% CI
  ci <- suppressWarnings(svyciprop(f, design, method = "beta", na.rm = TRUE))
  lims <- unname(confint(ci))
  width <- lims[2] - lims[1]
  rel_width <- if (p > 0) 100 * width / p else NA
  df <- degf(design)

  verdict <- case_when(
    n < 30 | n_eff < 30 ~ "Suppress: sample size below 30",
    width >= 0.30 ~ "Suppress: CI width 0.30 or more",
    width > 0.05 & rel_width > 130 ~ "Suppress: relative CI width above 130%",
    events == 0 | events == n ~ "Flag for review: estimate is 0% or 100%",
    df < 8 ~ "Flag for review: fewer than 8 degrees of freedom",
    .default = "Present"
  )

  # Percents and CI width in percentage points; NCHS's 0.05 and 0.30 widths are 5 and 30 points
  tibble(n = n, n_eff = round(n_eff, 1), percent = round(100 * p, 1),
         ci_low = round(100 * lims[1], 1), ci_high = round(100 * lims[2], 1),
         ci_width = round(100 * width, 1), rel_width = round(rel_width), df = df, verdict = verdict)
}

check_proportion <- function(design, var, group = NULL) {
  var_name <- rlang::as_name(rlang::enquo(var))
  group_quo <- rlang::enquo(group)
  if (rlang::quo_is_null(group_quo)) return(nchs_one(design, var_name))
  group_name <- rlang::as_name(group_quo)
  levels <- design$variables[[group_name]]
  levels <- if (is.factor(levels)) levels(droplevels(levels)) else sort(unique(na.omit(levels)))
  bind_rows(lapply(levels, function(lv) {
    sub <- design %>% filter(.data[[group_name]] == lv)
    bind_cols(tibble(!!group_name := lv), nchs_one(sub, var_name))
  }))
}
