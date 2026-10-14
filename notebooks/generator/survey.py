from nbkit import NB, link, TUTORIALS, CODEBOOK

SETUP_NOTE = "Run the setup cell. The lines printed by `library(tidyverse)` and `read_csv()` are normal."

SETUP = """
library(tidyverse)

nhis <- read_csv("NHIS_DATA_nhis2025_adult.csv")
"""

# =====================================================================  N1
nb = NB("N1", [
    "Describe what the NHIS is and why its data need special care",
    "Load the NHIS teaching file",
    "Read a codebook entry: the question, who was asked, and what each code means",
    "Spot special codes such as 7 = Refused and 9 = Don't know",
], needs="the six R Foundations notebooks, ending with " + link("F6"), minutes="30 to 40")

nb.md(f"""
## 1. The survey

The **National Health Interview Survey (NHIS)** is run every year by the National Center for Health Statistics (NCHS), part of the U.S. Centers for Disease Control and Prevention. Interviewers contact tens of thousands of households across the country and ask about health, health care, and living conditions. In each household, one adult is chosen at random to answer a long set of questions. That person is called the **sample adult**.

NCHS publishes the answers as a **public-use file**: anyone can download it, and nothing in it identifies a person. These lessons use the 2025 Sample Adult file, which has **24,215 adults**.

### The project

Over the next lessons you will answer one research question:

> **Among adults who have had cancer, how does self-rated health differ by income and education?**

### Why survey data need special care

Not every adult in the country had the same chance of ending up in the file. For example, only one adult is interviewed per household, so a person who lives alone is more likely to be chosen than one who lives with three other adults. Some groups are also less likely to respond. NCHS corrects for all of this by giving every person a **weight**: the number of U.S. adults that person stands for. Analyses that ignore the weights describe the 24,215 people in the file, not the country. Lesson N4 is all about this. For now, just know that three columns in the file (`WTFA_A`, `PSTRAT`, `PPSU`) carry this information and must never be dropped.

## 2. Load the data

{SETUP_NOTE}
""")
nb.code(SETUP)
nb.md("""
The full NCHS file has 577 columns. This teaching file keeps 16 of them, and **every one of the 24,215 adults**.

> **If you download the full file from NCHS yourself:** add `guess_max = 24215` inside `read_csv()`. By default, `read_csv()` looks at only the first 1,000 rows to decide each column's type, and for questions that few people were asked, that can go wrong. NCHS's own instructions recommend this.
""")
nb.code("dim(nhis)")
nb.code("head(nhis)")
nb.md("""
## 3. Every answer is a number

Look at the first rows again: apart from `HHX`, every column holds numbers, even for questions like "What is your sex?". Each number is a **code** that stands for an answer. To know what the codes mean, you need the **codebook**.

| Column | What it is |
|---|---|
| `HHX` | Household ID |
| `WTFA_A`, `PSTRAT`, `PPSU` | Survey design: weight, stratum, and sampling unit (lesson N4) |
| `PHSTAT_A` | Self-rated health |
| `CANEV_A` | Ever told by a doctor that you had cancer |
| `NUMCAN_A` | Number of different types of cancer reported |
| `SKNNMCAN_A` | Non-melanoma skin cancer was one of them |
| `POVRATTC_A` | Family income compared with the poverty line |
| `EDUCP_A` | Highest level of education |
| `NOTCOV_A` | Health insurance coverage |
| `AGEP_A` | Age |
| `SEX_A` | Sex |
| `HISPALLP_A` | Race and Hispanic origin |
| `REGION` | Region of the country |
| `URBRRL23` | How urban or rural the county is |

## 4. Reading the codebook

The [2025 Sample Adult codebook](CODEBOOK_) is a 577-page PDF with one page per variable. Open it in a new tab and search for a variable name (Ctrl+F, or Cmd+F on a Mac). Here is the entry for `PHSTAT_A`, shortened:

**Variable:** PHSTAT_A
**Question Text:** Would you say your health in general is excellent, very good, good, fair, or poor?
**Universe Description:** Sample adults 18+

| Code | Description | Frequency |
|---|---|---|
| 1 | Excellent | 4,789 |
| 2 | Very Good | 8,215 |
| 3 | Good | 7,389 |
| 4 | Fair | 2,970 |
| 5 | Poor | 845 |
| 7 | Refused | 4 |
| 8 | Not Ascertained | 0 |
| 9 | Don't Know | 3 |

Three parts of every entry matter:

- **Question Text**: exactly what was asked.
- **Universe**: who was asked. "Sample adults 18+" means everyone in the file.
- **Codes and frequencies**: what each number means, and how many people gave each answer.

The frequencies are your first check. Count the column yourself and compare.
""".replace("CODEBOOK_", CODEBOOK))
nb.code("nhis %>% count(PHSTAT_A)")
nb.md("""
The numbers match the codebook exactly, so the file was read correctly. Make this comparison a habit with every new variable.
""")
nb.turn("""
Count `CANEV_A` and compare your counts with its codebook entry, shown here:

| Code | Description | Frequency |
|---|---|---|
| 1 | Yes | 3,378 |
| 2 | No | 20,804 |
| 7 | Refused | 25 |
| 8 | Not Ascertained | 0 |
| 9 | Don't Know | 8 |
""", solution="nhis %>% count(CANEV_A)",
        expected="1 = 3,378, 2 = 20,804, 7 = 25, 9 = 8, matching the codebook (code 8 does not appear because nobody has it)")

nb.md("""
## 5. Special codes

Most NHIS questions use the same codes for answers that are not real answers:

| Code | Meaning |
|---|---|
| 7 | Refused |
| 8 | Not ascertained (the answer was not recorded) |
| 9 | Don't know |

Questions with many categories use two digits instead: **97, 98, 99**. These codes are numbers like any other, so R treats them as real values unless you tell it otherwise.
""")
nb.code("nhis %>% count(SEX_A)")
nb.md("""
1 is male and 2 is female, but 25 people have 7 or 9. If you calculated "percent female" as the share of all 24,215 adults with code 2, those 25 would quietly count as "not female".

Age is a sharper example. Look at the oldest ages in the file.
""")
nb.code("nhis %>% filter(AGEP_A >= 85) %>% count(AGEP_A)")
nb.md("""
Two different things are going on:

- **85 means "85 or older".** To protect privacy, NCHS does not publish exact ages above 84. This is called **top-coding**. The 963 people coded 85 are not all 85 years old.
- **97 and 99 are not ages at all.** They are "Refused" and "Don't know". Nobody in the file is 97 or 99.

Codes are labels, not quantities. Before you calculate anything, find out which codes are real answers. Lesson N2 turns the special codes into missing values (`NA`).
""")
nb.turn("""
How many adults have an age code that is not an age? Use `sum()` and `%in%`.
""", solution="sum(nhis$AGEP_A %in% c(97, 98, 99))", expected="60 (56 refused, 4 don't know)")

nb.md("""
## 6. Who was asked: the universe

Not every question is asked of everyone. `SKNNMCAN_A` records whether non-melanoma skin cancer was one of a person's cancers. Its codebook universe is:

> Sample adults 18+ **who were ever told they had cancer**

People outside the universe were never asked, so their value is blank in the file, which R reads as `NA`.
""")
nb.code("nhis %>% count(SKNNMCAN_A)")
nb.turn("""
20,837 people have `NA` for `SKNNMCAN_A`. Show where that number comes from by counting `CANEV_A` and `SKNNMCAN_A` together: `count(CANEV_A, SKNNMCAN_A)`.
""", solution="nhis %>% count(CANEV_A, SKNNMCAN_A)",
        expected="every `NA` belongs to someone who did not answer Yes to `CANEV_A`: 20,804 No + 25 Refused + 8 Don't know = 20,837",
        note="A missing value can mean \"not asked\" as well as \"no answer\". The universe tells you which.")

nb.md("""
## 7. A number that really is a number: income

`POVRATTC_A` compares a family's income with the federal **poverty threshold** for a family of that size. A value of 1 means income exactly at the poverty line; 2 means twice the poverty line; 0.5 means half of it.
""")
nb.code("summary(nhis$POVRATTC_A)")
nb.md("""
Two things to know about this column:

- **It is top-coded at 12.** Families with income 12 or more times the poverty line all appear as 12, again to protect privacy.
- **Some values are imputed.** About one in five adults did not report an exact family income (some gave only a range, some nothing). For them, NCHS filled in a statistically estimated value based on similar families, a process called **imputation**. The result has no missing values. These lessons use the column as NCHS provides it; studies that depend heavily on income sometimes use NCHS's more advanced multiple-imputation files instead.
""")
nb.turn("""
How many adults have family income **below** the poverty line? And how many are top-coded at 12?
""", solution="sum(nhis$POVRATTC_A < 1)\nsum(nhis$POVRATTC_A == 12)", expected="2,211 below the poverty line; 1,258 top-coded at 12")

nb.md("""
## 8. Your turn: education

Here are the codes for `EDUCP_A` from the codebook:

| Code | Description |
|---|---|
| 1 | Grade 0 to 11 |
| 2 | 12th grade, no diploma |
| 3 | GED or equivalent |
| 4 | High school graduate |
| 5 | Some college, no degree |
| 6 | Associate degree: occupational, technical, or vocational program |
| 7 | Associate degree: academic program |
| 8 | Bachelor's degree |
| 9 | Master's degree |
| 10 | Professional school or doctoral degree |
| 97 | Refused |
| 99 | Don't know |
""")
nb.turn("""
Count `EDUCP_A`. Then answer two questions with `sum()` and `%in%`: how many adults have a bachelor's degree or higher, and how many refused or did not know?
""", solution="nhis %>% count(EDUCP_A)\nsum(nhis$EDUCP_A %in% 8:10)\nsum(nhis$EDUCP_A %in% c(97, 98, 99))",
        expected="9,577 with a bachelor's degree or higher; 83 refused or did not know (28 + 55)",
        note="`8:10` is a shortcut for `c(8, 9, 10)`.")

nb.finish([
    ("nhis %>% count(x)", "Count each code; compare with the codebook"),
    ("nhis %>% count(x, y)", "Count combinations of two columns"),
    ("sum(x %in% c(7, 8, 9))", "How many special codes"),
    ("8:10", "The numbers 8, 9, 10"),
    ("summary(x)", "Minimum, quartiles, mean, and maximum of a number column"),
    ("read_csv(file, guess_max = 24215)", "Read a full NCHS file correctly"),
], f"Continue with {link('N2')}.")
nb.write()


# =====================================================================  N2
nb = NB("N2", [
    "Turn special codes into missing values (`NA`)",
    "Build the analysis variables: fair or poor health, cancer survivor, income, and education",
    "Check every new variable against the original codes",
    "Put categories in a sensible order with `factor()`",
], needs=link("N1"), minutes="30 to 40")

nb.md(f"""
## 1. The plan

In N1 you met the raw NHIS codes. Before any analysis, they need to become variables that answer the research question:

| New variable | Built from | Meaning |
|---|---|---|
| `fair_poor` | `PHSTAT_A` | 1 = fair or poor health, 0 = good, very good, or excellent |
| `survivor` | `CANEV_A`, `NUMCAN_A`, `SKNNMCAN_A` | 1 = has had cancer, 0 = has not |
| `poverty` | `POVRATTC_A` | Four income groups |
| `education` | `EDUCP_A` | Three education groups |
| `age_group`, `sex`, `insured` | `AGEP_A`, `SEX_A`, `NOTCOV_A` | Characteristics to describe and adjust for |

Two rules for the whole lesson:

1. **Never overwrite an original column.** Create a new one, so you can always compare old and new.
2. **Keep every row.** Even though the question is about cancer survivors, do not remove anyone. Lesson N5 explains why this matters for survey data.

{SETUP_NOTE}
""")
nb.code(SETUP)

nb.md("""
## 2. Special codes to `NA`

Start with self-rated health. Codes 7, 8, and 9 are not answers, so they should become `NA`. `if_else()` does it in one line: if the code is a special code, use `NA`; otherwise keep the code.
""")
nb.code("""
nhis <- nhis %>%
  mutate(health = if_else(PHSTAT_A %in% c(7, 8, 9), NA, PHSTAT_A))

nhis %>% count(PHSTAT_A, health)
""")
nb.md("""
Counting the old and new columns together shows exactly what happened: codes 1 to 5 kept their values, and the 7 people with codes 7 and 9 now have `NA`. Code 8 is included even though nobody has it this year, because the codebook lists it.

## 3. The outcome: fair or poor health

Researchers usually split self-rated health into two groups: **fair or poor** versus **good, very good, or excellent**. This is the outcome for the project.

Here `case_when()` uses `.default = NA` on purpose: anything that is not a real answer becomes missing.
""")
nb.turn("""
Create `fair_poor`: 1 when `PHSTAT_A` is 4 or 5, 0 when it is 1, 2, or 3, and `NA` otherwise. Store it in `nhis`, then check it with `count(PHSTAT_A, fair_poor)`.
""", solution="""
nhis <- nhis %>%
  mutate(fair_poor = case_when(
    PHSTAT_A %in% c(4, 5) ~ 1,
    PHSTAT_A %in% c(1, 2, 3) ~ 0,
    .default = NA
  ))

nhis %>% count(PHSTAT_A, fair_poor)
""", expected="3,815 people with 1 (2,970 + 845), 20,393 with 0, and 7 with `NA`")

nb.md("""
## 4. Who counts as a cancer survivor?

`CANEV_A` asks whether a doctor ever said you had cancer. One adjustment is standard in cancer survivorship research: people whose **only** cancer was **non-melanoma skin cancer** are not counted as survivors. These skin cancers are very common and rarely life-threatening, and including them would mix many people with a very different experience into the survivor group.

So a survivor is someone who answered Yes to `CANEV_A`, unless their only cancer type was non-melanoma skin cancer: `NUMCAN_A` is 1 and `SKNNMCAN_A` is 1.

### A trap with `==` and `NA`

`SKNNMCAN_A` is `NA` for everyone who was never asked. Watch what `==` does with `NA`.
""")
nb.code("""
x <- c(1, 2, NA)
x == 1
x %in% 1
""")
nb.md("""
`NA == 1` gives `NA` ("unknown"), but `NA %in% 1` gives `FALSE`. For "is this value exactly 1?", `%in%` is the safer choice when a column has missing values.
""")
nb.code("""
nhis <- nhis %>%
  mutate(
    skin_only = NUMCAN_A == 1 & SKNNMCAN_A %in% 1,
    survivor = case_when(
      CANEV_A == 1 & !skin_only ~ 1,
      CANEV_A == 2 | skin_only ~ 0,
      .default = NA
    )
  )

nhis %>% count(CANEV_A, skin_only, survivor)
""")
nb.md("""
Read the rules: `!` means "not" and `|` means "or". A survivor said Yes and is **not** skin-only. A non-survivor said No **or** is skin-only. Refused and don't know (7 and 9) become `NA`.

The check shows 545 people whose only cancer was non-melanoma skin cancer moved from Yes to 0.
""")
nb.turn("How many survivors are there, how many non-survivors, and how many `NA`? Use `count(survivor)`.",
        solution="nhis %>% count(survivor)", expected="2,833 survivors, 21,349 non-survivors, 33 `NA`")

nb.md("""
## 5. Income groups

`POVRATTC_A` is a number, but for comparing groups it helps to cut it into categories. A common choice uses multiples of the poverty line: below 100%, 100 to 199%, 200 to 399%, and 400% or more.

`case_when()` checks its rules **in order** and uses the first one that is true. So the second rule, `POVRATTC_A < 2`, only ever sees people who failed the first rule, meaning people at 1 or above.
""")
nb.turn("""
Create `poverty` with these four groups, as text: "Below 100%", "100-199%", "200-399%", "400% or more". Store it in `nhis` and count it.
""", solution="""
nhis <- nhis %>%
  mutate(poverty = case_when(
    POVRATTC_A < 1 ~ "Below 100%",
    POVRATTC_A < 2 ~ "100-199%",
    POVRATTC_A < 4 ~ "200-399%",
    POVRATTC_A >= 4 ~ "400% or more"
  ))

nhis %>% count(poverty)
""", expected="Below 100%: 2,211; 100-199%: 4,181; 200-399%: 7,300; 400% or more: 10,523; no `NA`",
        note="`POVRATTC_A` has no missing values (they were imputed), so no `NA` appears.")

nb.md("""
## 6. Your turn: education groups

Combine the ten education codes into three groups, using the code table from N1:

| Codes | Group |
|---|---|
| 1 to 4 | High school or less |
| 5 to 7 | Some college (including associate degrees) |
| 8 to 10 | Bachelor or higher |
| 97, 98, 99 | `NA` |
""")
nb.turn("""
Create `education` with the groups "High school or less", "Some college", and "Bachelor or higher". Check it with `count(EDUCP_A, education)` and then `count(education)`.
""", solution="""
nhis <- nhis %>%
  mutate(education = case_when(
    EDUCP_A %in% 1:4 ~ "High school or less",
    EDUCP_A %in% 5:7 ~ "Some college",
    EDUCP_A %in% 8:10 ~ "Bachelor or higher",
    .default = NA
  ))

nhis %>% count(EDUCP_A, education)
nhis %>% count(education)
""", expected="Bachelor or higher 9,577; High school or less 7,900; Some college 6,655; `NA` 83")

nb.md("""
## 7. The other variables

Age, sex, and insurance follow the same pattern. Run this cell, then read it line by line: every piece is something you have already used.
""")
nb.code("""
nhis <- nhis %>%
  mutate(
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
""")
nb.md("""
Remember that `age` is still top-coded: 85 means 85 or older. That does not matter for `age_group`, since everyone 85 and over belongs in "65+" anyway.
""")
nb.turn("Check the three new variables with `count()`: `age_group`, `sex`, and `insured`.",
        solution="nhis %>% count(age_group)\nnhis %>% count(sex)\nnhis %>% count(insured)",
        expected="age_group: 18-44 8,485; 45-64 7,202; 65+ 8,468; `NA` 60. sex: Female 12,975; Male 11,215; `NA` 25. insured: Yes 22,520; No 1,626; `NA` 69")

nb.md("""
## 8. Putting categories in order

`count()` lists text categories alphabetically, which is why "100-199%" came before "Below 100%". Tables and plots read much better in a natural order. `factor()` with `levels` sets the order.
""")
nb.code("""
nhis <- nhis %>%
  mutate(
    poverty = factor(poverty, levels = c("Below 100%", "100-199%", "200-399%", "400% or more")),
    education = factor(education, levels = c("High school or less", "Some college", "Bachelor or higher"))
  )

nhis %>% count(poverty)
""")
nb.md("""
Same counts, now in order from lowest to highest income.

## 9. The analysis file

Now keep just the columns you need, **including the three survey design columns**. Without `WTFA_A`, `PSTRAT`, and `PPSU`, the analyses in N4 to N6 are impossible.
""")
nb.code("""
analysis <- nhis %>%
  select(HHX, WTFA_A, PSTRAT, PPSU,
         fair_poor, survivor, poverty, education, age, age_group, sex, insured)

dim(analysis)
""")
nb.md("""
24,215 rows: everyone is still here. 12 columns.

## 10. A first look, and a warning

Here is the share of survivors and non-survivors in fair or poor health. `mean()` of a 0/1 column is the proportion of 1s.
""")
nb.code("""
analysis %>%
  filter(!is.na(survivor), !is.na(fair_poor)) %>%
  group_by(survivor) %>%
  summarize(people = n(), pct_fair_poor = 100 * mean(fair_poor))
""")
nb.md("""
About 27% of survivors report fair or poor health, compared with about 14% of everyone else.
""")
nb.turn("""
Among **survivors only**, calculate the percent in fair or poor health for each education group. Leave out people with missing education or missing `fair_poor`.
""", solution="""
analysis %>%
  filter(survivor == 1, !is.na(fair_poor), !is.na(education)) %>%
  group_by(education) %>%
  summarize(people = n(), pct_fair_poor = 100 * mean(fair_poor))
""", expected="High school or less 39.7% (867 people); Some college 28.4% (846); Bachelor or higher 15.9% (1,109)")

nb.md("""
A striking gradient. But **these numbers are not yet results.** They describe the people who happened to be interviewed, without the weights. Not everyone had the same chance of being interviewed, so unweighted percentages can differ from the true U.S. figures. Lesson N4 shows how much, and how to fix it.

## 11. Save your work

Colab's memory is wiped when your session ends. `write_csv()` saves the analysis file, and Colab's **Files** panel (the folder icon on the left) lets you download it.
""")
nb.code('write_csv(analysis, "nhis_analysis.csv")')
nb.md("""
In the next lesson you move to RStudio on your own computer, where files stay put, and you will run the code from this lesson as a script.
""")

nb.finish([
    ("if_else(x %in% c(7, 8, 9), NA, x)", "Turn special codes into `NA`"),
    ("case_when(..., .default = NA)", "Anything that matches no rule becomes `NA`"),
    ("x %in% 1", "Like `x == 1`, but `FALSE` instead of `NA` when x is missing"),
    ("!a, a | b", "Not a; a or b"),
    ("count(old, new)", "Check a recode against the original codes"),
    ("factor(x, levels = c(...))", "Put categories in a set order"),
    ("100 * mean(x)", "Percent of 1s in a 0/1 column"),
], f"""
Continue with [N3: Moving to RStudio]({TUTORIALS}survey/n3-rstudio.html), a lesson on the tutorials website.
""")
nb.write()
