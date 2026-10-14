from nbkit import NB, link, SITE

SETUP_NOTE = "Run the setup cell. The lines printed by `library(tidyverse)` and `read_csv()` are normal."

RECODE = """
person_df <- person_df %>%
  mutate(
    race = case_when(
      race == "Black or African American" ~ "Black",
      race == "Skip" ~ "Unknown",
      race %in% c("More than one population", "None of these") ~ "Other",
      .default = race
    ),
    sex_at_birth = case_when(
      sex_at_birth %in% c("Intersex", "Prefer not to answer", "Skip") ~ "Other",
      .default = sex_at_birth
    )
  )
"""

# =====================================================================  A1
nb = NB("A1", [
    "Get to know three linked tables of health record data",
    "Tidy up messy categories with `if_else()` and `case_when()`",
    "Check your work after every change",
], needs="the six Foundations notebooks, ending with " + link("F6"))

nb.md(f"""
## 1. The project

Over the next few notebooks you will carry out a small research project from start to finish, the way you would with *All of Us* data:

> **Is taking an anticholinergic medication associated with developing dementia?**

You have three tables of **simulated** data (randomly generated, completely fake) for 100 people. The outcome is recorded as either dementia or mild cognitive impairment (MCI), an earlier stage of memory loss. In this project both count, and from here on the notebooks call them "the condition".

Before any analysis, the tables have to be cleaned and combined into one table with one row per person. This preparation is called **data wrangling**, and in real projects it takes most of the time.

{SETUP_NOTE}
""")
nb.code("""
library(tidyverse)

person_df    <- read_csv("RAW_demographic_data.csv")
condition_df <- read_csv("RAW_conditions.csv")
drug_df      <- read_csv("RAW_drug_exposures.csv")
""")
nb.md("""
| Table | One row is... | Columns |
|---|---|---|
| `person_df` | one person | ID, year of birth, race, sex at birth |
| `condition_df` | one diagnosis record | ID, a code for the condition, the date, the condition's name |
| `drug_df` | one prescription record | ID, a code for the drug, the date |

All three share the column `person_id`, which is how they will be linked.

## 2. Look before you touch

Start every project by looking at each table.
""")
nb.code("dim(person_df)")
nb.code("head(person_df)")
nb.turn("""
Look at `condition_df` in the same way: its size and its first rows. Then use `count()` on the column `condition_source_value` to see which conditions are recorded.
""", solution="""
dim(condition_df)
head(condition_df)
condition_df %>% count(condition_source_value)
""", expected="96 rows and 4 columns; two conditions, Dementia (46 records) and MCI (50 records)",
        note="Both are treated as the outcome of interest, \"the condition\".")

nb.md("""
## 3. Messy categories

Look at the categories in the `race` column.
""")
nb.code("person_df %>% count(race)")
nb.md("""
Seven categories, some of them very small. For analysis, you might decide to:

- shorten "Black or African American" to "Black",
- relabel "Skip" (people who skipped the question) as "Unknown",
- combine "More than one population" and "None of these" into "Other".

Changing the values in a column like this is called **recoding**.

## 4. Recoding one value: `if_else()`

You met `if_else()` in notebook F5: a test, the value to use if it is true, the value to use if it is false. To change just one category, the "false" value is simply the column itself, meaning "otherwise, leave it as it is".
""")
nb.code("""
person_df %>%
  mutate(race = if_else(race == "Skip", "Unknown", race)) %>%
  count(race)
""")
nb.md("""
"Skip" has become "Unknown" and everything else is untouched. Notice that this was not stored anywhere: the result went straight into `count()` so you could look at it. `person_df` itself is unchanged. Trying a change this way before you commit to it is a good habit.

## 5. Recoding several values: `case_when()`

For several changes at once, use `case_when()`. It is a list of rules. Each rule is written `test ~ new value`: the test on the left, a squiggle `~` (called a tilde), and the value to use on the right. R goes down the list and uses the first rule whose test is true.
""")
nb.code("""
person_df %>%
  mutate(
    race = case_when(
      race == "Black or African American" ~ "Black",
      race == "Skip" ~ "Unknown",
      race %in% c("More than one population", "None of these") ~ "Other",
      .default = race
    )
  ) %>%
  count(race)
""")
nb.md("""
Two new things appear here:

- **`%in%`** tests whether a value is any one of a list. `race %in% c("A", "B")` is true when race is "A" or race is "B".
- **`.default = race`** says what to do with values that match none of the rules: keep the original value.

### What if you forget `.default`?

Run this version, which leaves it out.
""")
nb.code("""
person_df %>%
  mutate(
    race = case_when(
      race == "Black or African American" ~ "Black",
      race == "Skip" ~ "Unknown",
      race %in% c("More than one population", "None of these") ~ "Other"
    )
  ) %>%
  count(race)
""")
nb.md("""
62 people now have `NA` for race. Everyone who was "Asian", "White", or already "Other" matched none of the rules, and without `.default`, R filled in `NA`. **No error, no warning.** The only way to catch it is to count the categories afterwards. That is why you check.

(Nothing was stored, so `person_df` is still unchanged. If you come back and run this cell again after the next step, the count will be different, because `person_df` will already have been recoded.)

### Make the change for real

The version with `.default` gave the right result, so now store it back into `person_df`.
""")
nb.code("""
person_df <- person_df %>%
  mutate(
    race = case_when(
      race == "Black or African American" ~ "Black",
      race == "Skip" ~ "Unknown",
      race %in% c("More than one population", "None of these") ~ "Other",
      .default = race
    )
  )
""")
nb.md("""
## 6. Check your work

After any recoding, check three things.
""")
nb.code("person_df %>% count(race)   # 1. Are the categories what you intended?")
nb.code("nrow(person_df)             # 2. Is the number of rows unchanged?")
nb.code("sum(is.na(person_df$race))  # 3. Were any missing values created?")
nb.md("Five categories, still 100 rows, no missing values. The 15 people in \"Other\" are the original 4, plus 6, plus 5.")

nb.md("""
## 7. Your turn: sex at birth
""")
nb.code("person_df %>% count(sex_at_birth)")
nb.turn("""
Recode `sex_at_birth` so that "Intersex", "Prefer not to answer", and "Skip" all become "Other", and "Female" and "Male" stay as they are. Follow the same steps as above:

1. Try it first without storing, ending the pipeline with `count(sex_at_birth)`.
2. When the result is right, store it back into `person_df`.
""", solution="""
person_df <- person_df %>%
  mutate(
    sex_at_birth = case_when(
      sex_at_birth %in% c("Intersex", "Prefer not to answer", "Skip") ~ "Other",
      .default = sex_at_birth
    )
  )
person_df %>% count(sex_at_birth)
""", expected="Female 44, Male 48, Other 8")
nb.turn("Check your recoding: confirm `person_df` still has 100 rows, and use `colSums(is.na(person_df))` to confirm that no column has missing values.",
        solution="nrow(person_df)\ncolSums(is.na(person_df))", expected="100 rows; 0 missing values in every column")

nb.md(f"""
> **A note if you read other people's code:** there are several ways to recode in R. The newest versions of the tidyverse add `replace_values()`, which is used on the [workshop website]({SITE}session-3.html). The result is the same, but the function may not be available in your Colab session yet.
""")

nb.finish([
    ('if_else(x == "a", "b", x)', 'Change "a" to "b"; leave everything else'),
    ("case_when(test ~ value, ...)", "A list of rules; the first true one is used"),
    (".default = x", "Inside `case_when()`: what to use when no rule matches"),
    ('x %in% c("a", "b")', "Is x any one of these values?"),
    ("df %>% count(x)", "Check the categories before and after recoding"),
    ("colSums(is.na(df))", "Missing values in every column"),
], f"Continue with {link('A2')}.")
nb.write()

# =====================================================================  A2
nb = NB("A2", [
    "Reduce a table with many records per person to one row per person",
    "Do a calculation separately for each person with `group_by()`",
    "Merge three tables into one and check the result",
], needs=link("A1"))

nb.md(f"""
## 1. Where we are

The goal is one table with one row per person. `person_df` is already like that. But at the end of the Foundations you saw that `condition_df` and `drug_df` have several records per person, and that joining them directly multiplies the rows.

{SETUP_NOTE} It also repeats the recoding you did in notebook A1, so that you start from clean data.
""")
nb.code("""
library(tidyverse)

person_df    <- read_csv("RAW_demographic_data.csv")
condition_df <- read_csv("RAW_conditions.csv")
drug_df      <- read_csv("RAW_drug_exposures.csv")

# Catch-up: the recoding from notebook A1
""" + RECODE.strip())

nb.md("""
## 2. Look at one person

Before writing code for 100 people, look closely at one. Here are all the diagnosis records for person 8.
""")
nb.code("condition_df %>% filter(person_id == 8)")
nb.md("""
Four records, on four dates. For this study, the date that matters is when the condition **first** appeared: the earliest one.

## 3. Keeping the earliest row: `slice_min()`

`slice_min()` keeps the row with the smallest value in a column you choose. For a date column, the smallest value is the earliest date. `n = 1` asks for one row.
""")
nb.code("""
condition_df %>%
  filter(person_id == 8) %>%
  slice_min(condition_start_date, n = 1)
""")
nb.md("""
One row is left: the earliest record, dated 2025-06-09. (The data are simulated, so do not read anything into the dates.)

## 4. Doing it for every person: `group_by()`

Without the `filter()`, `slice_min()` would return the single earliest record in the **whole table**, which is not what you want. You want the earliest record **for each person**.

`group_by(person_id)` tells R: "from now on, do each step separately for each person". After it, `slice_min()` picks the earliest row within each person's records.
""")
nb.code("""
earliest_condition <- condition_df %>%
  group_by(person_id) %>%                          # for each person...
  slice_min(condition_start_date, n = 1, with_ties = FALSE) %>%   # ...keep the earliest record
  ungroup()                                        # stop working person by person
""")
nb.md("""
Two details:

- **`with_ties = FALSE`**: if a person has two records on the same earliest date, keep only one of them. Without this, both would be kept and that person would still have two rows.
- **`ungroup()`**: switches the "for each person" behavior off again. Always finish a grouped step with it, so later steps are not affected.

### Check
""")
nb.code("""
nrow(earliest_condition)                    # rows
n_distinct(earliest_condition$person_id)    # different people
""")
nb.code("earliest_condition %>% filter(person_id == 8)   # the person you looked at by hand")
nb.md("30 rows for 30 people, and person 8 has the date you found by hand. Checking a result against a case you worked out yourself is one of the most reliable tests there is.")

nb.turn("""
Do the same for the prescription records. Create `earliest_drug` from `drug_df`, keeping each person's earliest `drug_exposure_start_date`. Then check the number of rows against the number of different people.
""", solution="""
earliest_drug <- drug_df %>%
  group_by(person_id) %>%
  slice_min(drug_exposure_start_date, n = 1, with_ties = FALSE) %>%
  ungroup()

nrow(earliest_drug)
n_distinct(earliest_drug$person_id)
""", expected="35 rows, 35 different people")

nb.md("""
## 5. Merge the three tables

Now every table has one row per person, so the joins are safe. Start from `person_df` and add the other two with `left_join()`, so that all 100 people are kept.
""")
nb.code("""
combined_df <- person_df %>%
  left_join(earliest_condition, by = "person_id") %>%
  left_join(earliest_drug, by = "person_id")
""", solution="""
earliest_drug <- drug_df %>%
  group_by(person_id) %>%
  slice_min(drug_exposure_start_date, n = 1, with_ties = FALSE) %>%
  ungroup()
combined_df <- person_df %>%
  left_join(earliest_condition, by = "person_id") %>%
  left_join(earliest_drug, by = "person_id")
""")
nb.md("(If this cell gives the error `object 'earliest_drug' not found`, finish the exercise above first.)\n\n### Check")
nb.code("""
nrow(combined_df)                    # should still be 100
n_distinct(combined_df$person_id)    # should also be 100
""")
nb.code("head(combined_df)")
nb.code("colSums(is.na(combined_df))")
nb.md("""
100 rows, 100 people. The missing values are expected and meaningful here: 70 people have no diagnosis record, and 65 have no prescription record. In this table, `NA` in a date column means "this never happened", as far as the records show.

`!` means "not". So `!is.na(x)` means "x is **not** missing".
""")
nb.code("""
combined_df %>%
  filter(!is.na(condition_start_date)) %>%   # people who do have a diagnosis date
  nrow()
""")
nb.turn("How many people have **both** a diagnosis date and a prescription date? Use `filter()` with `!is.na()` twice, joined by `&`.",
        solution="""
combined_df %>%
  filter(!is.na(condition_start_date) & !is.na(drug_exposure_start_date)) %>%
  nrow()
""", expected="21")

nb.md("""
## 6. Optional extra: survey answers, from long to wide

This section is useful if your project uses *All of Us* survey data. You can skip it and come back later.

Survey data arrives in a **long** layout: one row per person per question.
""")
nb.code("""
survey_long <- data.frame(
  person_id = c(1, 1, 1, 2, 2, 2),
  question  = c("smoked_100_cigs", "alcohol_frequency", "general_health",
                "smoked_100_cigs", "alcohol_frequency", "general_health"),
  answer    = c("Yes", "Never", "Good", "No", "Monthly", "Fair")
)
survey_long
""")
nb.md("For analysis you want a **wide** layout: one row per person, one column per question. `pivot_wider()` does this. You tell it which column holds the new column names and which holds the values.")
nb.code("""
survey_wide <- survey_long %>%
  pivot_wider(
    id_cols     = person_id,   # one row for each of these
    names_from  = question,    # new column names come from here
    values_from = answer       # the values to fill in come from here
  )
survey_wide
""")

nb.finish([
    ("slice_min(date, n = 1, with_ties = FALSE)", "Keep the one row with the earliest date"),
    ("group_by(person_id)", "Do the following steps separately for each person"),
    ("ungroup()", "Stop working group by group"),
    ("a %>% left_join(b, by = \"person_id\")", "Add columns from b, keeping every row of a"),
    ("!is.na(x)", "x is not missing"),
    ("pivot_wider(...)", "Reshape long data to one row per person"),
], f"Continue with {link('A3')}.")
nb.write()

# =====================================================================  A3
nb = NB("A3", [
    "Compare and subtract dates",
    "Work out who was exposed to a drug before their diagnosis",
    "Test your logic on a few cases where you know the answer",
    "Create the variables needed for analysis, and save your data",
], needs=link("A2"))

nb.md(f"""
## 1. Where we are

You have one table, `combined_df`, with one row per person. It contains each person's first diagnosis date and first prescription date, where they exist. Now you need to turn those dates into the variables the analysis needs.

{SETUP_NOTE} It loads a saved copy of the table you built in notebook A2.
""")
nb.code("""
library(tidyverse)

# Catch-up: the merged table from notebook A2
# (a minus sign inside select() removes a column instead of keeping it)
combined_df <- read_csv("RAW_final_dataset.csv") %>%
  select(-true_exposure_status, -SBP)

head(combined_df)
""")

nb.md("""
## 2. Arithmetic with dates

The two date columns are marked `<date>`, so R knows they are dates and not text. That means you can subtract them. Here are the people who have both dates, with the number of days from first prescription to first diagnosis.
""")
nb.code("""
combined_df %>%
  filter(!is.na(drug_exposure_start_date) & !is.na(condition_start_date)) %>%
  mutate(days_between = condition_start_date - drug_exposure_start_date) %>%
  select(person_id, drug_exposure_start_date, condition_start_date, days_between) %>%
  head()
""")
nb.md("You can also compare dates with `<` and `>`. An earlier date counts as smaller.")
nb.code('as.Date("2010-01-01") < as.Date("2015-01-01")')

nb.md("""
## 3. Why the order of events matters

A drug cannot have contributed to a disease if the person started taking it **after** the disease was diagnosed. So "took the drug" is not enough. For this study, a person counts as **exposed** only if they started the drug before their diagnosis, or took it and were never diagnosed.

| Situation | Status |
|---|---|
| No prescription record | Unexposed |
| Took the drug, never diagnosed | Exposed |
| Took the drug **before** diagnosis | Exposed |
| Started the drug **on or after** the diagnosis date | Unexposed (Post-Diagnosis) |

You will store this in a column called `true_exposure_status`: "true" because it takes the timing into account, and not just whether a prescription exists.

## 4. Start with a small test

Rules like these are easy to get subtly wrong. So before using them on the real table, try them on a few made-up patients for whom the right answer is obvious.
""")
nb.code("""
timing_test <- tibble(
  person_id                = 1:6,
  drug_exposure_start_date = as.Date(c(NA, "2010-01-01", "2010-01-01", "2018-01-01", NA, "2015-01-01")),
  condition_start_date     = as.Date(c(NA, NA, "2015-01-01", "2015-01-01", "2015-01-01", "2015-01-01"))
)
timing_test
""")
nb.md("""
**Before running any more code, decide the status of each of the six patients using the table of rules above.** Write your answers down. (`tibble()` is the tidyverse's version of `data.frame()`.)

### A complication: comparing with a missing date

What does R say when you compare a date with a missing date?
""")
nb.code('as.Date("2010-01-01") < NA')
nb.md("""
`NA`: R cannot know. This is why the rules have to deal with the missing dates **first**, before comparing any dates.

### Writing the rules with `case_when()`

`case_when()` checks its rules from top to bottom and uses the first one that is true.
""")
nb.code("""
timing_test %>%
  mutate(
    true_exposure_status = case_when(
      # Rule 1: no prescription record
      is.na(drug_exposure_start_date) ~ "Unexposed",
      # Rule 2: took the drug, never diagnosed
      !is.na(drug_exposure_start_date) & is.na(condition_start_date) ~ "Exposed",
      # Rule 3: took the drug BEFORE the diagnosis
      drug_exposure_start_date < condition_start_date ~ "Exposed",
      # Rule 4: started the drug ON or AFTER the diagnosis date
      drug_exposure_start_date >= condition_start_date ~ "Unexposed (Post-Diagnosis)"
    )
  )
""")
nb.md("""
Compare with your own answers. Patients 2 and 3 are exposed. Patient 4 started the drug three years after diagnosis, and patient 6 on the day of diagnosis, so neither is. Patients 1 and 5 never took it.

In notebook A1 you saw that leaving out `.default` can silently create missing values. Here it is left out on purpose: the four rules are meant to cover every possible case. If anyone ended up with `NA`, it would mean a case had been overlooked, and you would want to see that.

## 5. Apply it to the real table

The rules work on the test cases, so now use exactly the same code on `combined_df`, and store the result.
""")
nb.code("""
combined_df <- combined_df %>%
  mutate(
    true_exposure_status = case_when(
      is.na(drug_exposure_start_date) ~ "Unexposed",
      !is.na(drug_exposure_start_date) & is.na(condition_start_date) ~ "Exposed",
      drug_exposure_start_date < condition_start_date ~ "Exposed",
      drug_exposure_start_date >= condition_start_date ~ "Unexposed (Post-Diagnosis)"
    )
  )

combined_df %>% count(true_exposure_status)
""")
nb.md("""
35 exposed, 65 unexposed, and no missing values.

Notice that nobody in this dataset falls into the "Post-Diagnosis" group. That means that **if Rule 4 had been written wrongly, this count would look exactly the same**, and you would never know. The small test table is what showed that the rule works. Real data will not always contain the cases that reveal a mistake, so make your own.

## 6. Age
""")
nb.turn("Add a column `age` to `combined_df`, calculated as 2026 minus `year_of_birth`. Store the result back in `combined_df`, then find the mean age.",
        solution="""
combined_df <- combined_df %>% mutate(age = 2026 - year_of_birth)
mean(combined_df$age)
""", expected="52.91")

nb.md("""
## 7. Yes/no variables as 1 and 0

For statistical models, a yes/no variable is best stored as the numbers 1 (yes) and 0 (no).

A person has the condition if they have a diagnosis record, that is, if `condition_concept_id` is not missing.
""")
nb.code("""
combined_df <- combined_df %>%
  mutate(condition_status = if_else(is.na(condition_concept_id), 0, 1))

combined_df %>% count(condition_status)
""")
nb.md("30 people with the condition, 70 without. Because the values are 1 and 0, `sum()` counts the people with the condition and `mean()` gives the proportion.")
nb.code("""
sum(combined_df$condition_status)
mean(combined_df$condition_status)
""")
nb.turn("""
Add a column `exposure_status` that is 1 if `true_exposure_status` is "Exposed" and 0 otherwise. Store it back in `combined_df`, then count the two groups.
""", solution="""
combined_df <- combined_df %>%
  mutate(exposure_status = if_else(true_exposure_status == "Exposed", 1, 0))

combined_df %>% count(exposure_status)
""", expected="65 people with 0, 35 people with 1")

nb.md("""
## 8. A first look at the research question

`count()` with two columns gives every combination: a simple cross-tabulation of exposure against outcome.
""")
nb.code("combined_df %>% count(exposure_status, condition_status)", solution="""
combined_df <- combined_df %>% mutate(age = 2026 - year_of_birth)
combined_df <- combined_df %>% mutate(exposure_status = if_else(true_exposure_status == "Exposed", 1, 0))
combined_df %>% count(exposure_status, condition_status)
""")
nb.md("""
(If this gives an error about `exposure_status`, finish the exercise above first.)

Among the 65 unexposed people, 9 have the condition. Among the 35 exposed people, 21 do. That looks like a large difference. Whether it is statistically convincing is a question for the notebooks on statistics.

## 9. Save your work

Everything you have built exists only in R's memory, and Colab's memory is wiped when the session ends. `write_csv()` saves a dataframe as a CSV file. You give it the dataframe and a file name. (The saved table is complete only if you have done both exercises above.)
""")
nb.code('write_csv(combined_df, "cleaned_dataset.csv")')
nb.md("""
In Colab, the file appears in the **Files** panel (the folder icon in the left sidebar). It is deleted when the session ends, so download it from that panel if you want to keep it. In the *All of Us* Researcher Workbench, you save files to your workspace instead.

Good file names have no spaces and say what is inside. If you include a date, write it as year-month-day, for example `cleaned_dataset_2026-05-21.csv`.
""")

nb.finish([
    ("date2 - date1", "Number of days between two dates"),
    ("date1 < date2", "Is date1 earlier?"),
    ("case_when(rule1, rule2, ...)", "Rules are checked top to bottom; deal with missing values first"),
    ("tibble(a = ..., b = ...)", "Make a small table by hand, for testing"),
    ("if_else(is.na(x), 0, 1)", "0 if missing, 1 if present"),
    ("count(a, b)", "Count every combination of two columns"),
    ('write_csv(df, "file.csv")', "Save a dataframe to a file"),
], f"Continue with {link('A4')}.")
nb.write()

# =====================================================================  A4
nb = NB("A4", [
    "Summarize a dataset overall and by group",
    "Draw a histogram, a box plot, and a scatter plot with `ggplot()`",
    "Add titles and axis labels",
], needs=link("A3"))

nb.md(f"""
## 1. Where we are

The dataset is ready. Before running any statistical test, get to know the data: how the values are distributed, how the groups compare, and whether anything looks odd. This is called **exploratory data analysis**.

{SETUP_NOTE} It loads the finished dataset from notebook A3 under a new name, `study_df`, with one extra column: `SBP`, systolic blood pressure.
""")
nb.code("""
library(tidyverse)

study_df <- read_csv("RAW_final_dataset2.csv")
""")
nb.code("dim(study_df)")
nb.code("names(study_df)")

nb.md("""
## 2. Summaries of one column

`summary()` on a numeric column gives the minimum, the quartiles (the values a quarter and three quarters of the way up), the median, the mean, the maximum, and the number of missing values if there are any.
""")
nb.code("summary(study_df$age)")
nb.code("summary(study_df$SBP)")
nb.md("Blood pressure is missing for 5 people (`NA's`). Keep that in mind: anything you calculate from `SBP` is based on 95 people, not 100.")

nb.md("""
## 3. Summaries by group

Often the interesting question is how groups compare. You met `group_by()` in notebook A2: it means "do the next step separately for each group". Followed by `summarise()`, it produces one row of summary per group.

Inside `summarise()`, you name each summary and say how to calculate it. `n()` counts the rows in the group.
""")
nb.code("""
study_df %>%
  group_by(sex_at_birth) %>%
  summarise(
    n        = n(),
    mean_SBP = mean(SBP, na.rm = TRUE),
    sd_SBP   = sd(SBP, na.rm = TRUE)
  )
""")
nb.md("Mean blood pressure is similar in the three groups. Note `na.rm = TRUE`: without it, each mean would be `NA`.")
nb.turn("""
Compare people with and without the condition. Group by `condition_status` and calculate the number of people and the mean `age` in each group.
""", solution="""
study_df %>%
  group_by(condition_status) %>%
  summarise(
    n        = n(),
    mean_age = mean(age)
  )
""", expected="70 people without the condition, mean age 51.4; 30 people with it, mean age 56.4")

nb.md("""
## 4. Your first plot

Plots are made with `ggplot()`, which is part of the tidyverse. A plot is built from three ingredients:

1. **The data**: which dataframe.
2. **The mapping**, written inside `aes()`: which column goes on which axis.
3. **The shape**, called a geom: bars, boxes, points.

The ingredients are joined with a **plus sign**. Here is a histogram, which shows how the values of one numeric column are distributed.
""")
nb.code("""
ggplot(study_df, aes(x = age)) +
  geom_histogram(binwidth = 5)
""")
nb.md("""
Read the code as: make a plot from `study_df`, put `age` on the x axis, and draw a histogram with bars 5 years wide. Each bar's height is the number of people in that 5-year age range.

Try changing `binwidth = 5` to `binwidth = 10`, and then to `2`, and run the cell again each time.

> **A very common mistake:** layers of a plot are joined with `+`, not with the pipe `%>%`. If you get an error in a plot, check this first.

### Labels and appearance

Add more layers with more plus signs. `labs()` sets the title and axis labels. `fill` and `color` set the color of the bars' insides and outlines. `theme_minimal()` gives a cleaner background.
""")
nb.code("""
ggplot(study_df, aes(x = age)) +
  geom_histogram(binwidth = 5, fill = "steelblue", color = "black") +
  labs(
    title = "Age Distribution",
    x = "Age (years)",
    y = "Number of people"
  ) +
  theme_minimal()
""")
nb.turn("""
Draw a histogram of `SBP` with bars 5 units wide. Give it a title and label the x axis "Systolic blood pressure (mmHg)".

R will print a **warning** that 5 rows were removed. Those are the 5 people with missing blood pressure. The plot is fine; the warning is reminding you that they are not in it. You will see the same warning on every plot of `SBP`.
""", solution="""
ggplot(study_df, aes(x = SBP)) +
  geom_histogram(binwidth = 5, fill = "steelblue", color = "black") +
  labs(
    title = "Systolic Blood Pressure",
    x = "Systolic blood pressure (mmHg)",
    y = "Number of people"
  ) +
  theme_minimal()
""", note="If you ever see the \"rows removed\" warning when you were not expecting missing values, investigate.")

nb.md("""
## 5. Box plot: a numeric column across groups

A box plot compares the distribution of a numeric column between groups. Now there are two mappings: the group on the x axis and the numeric column on the y axis.
""")
nb.code("""
ggplot(study_df, aes(x = sex_at_birth, y = SBP)) +
  geom_boxplot() +
  labs(
    title = "Systolic Blood Pressure by Sex",
    x = "Sex at birth",
    y = "SBP (mmHg)"
  ) +
  theme_minimal()
""")
nb.md("""
How to read a box plot: the thick line in the middle of each box is the **median**. The box covers the middle half of the values. The lines above and below reach to the lowest and highest typical values, and any dots beyond them are unusually far from the rest.
""")
nb.turn("""
Draw a box plot of `age` for each `true_exposure_status` group. Does one group look older?
""", solution="""
ggplot(study_df, aes(x = true_exposure_status, y = age)) +
  geom_boxplot() +
  labs(
    title = "Age by Exposure Status",
    x = "Exposure status",
    y = "Age (years)"
  ) +
  theme_minimal()
""", note="The exposed group is somewhat older: its median age (the thick line) is 61, compared with 52 in the unexposed group, though the two boxes overlap a great deal.")

nb.md("""
## 6. Scatter plot: two numeric columns

A scatter plot shows the relationship between two numeric columns. Each point is one person.
""")
nb.code("""
ggplot(study_df, aes(x = age, y = SBP)) +
  geom_point()
""")
nb.md("Blood pressure tends to be higher in older people: the cloud of points rises from left to right.")
nb.turn("""
Improve the scatter plot: add a title, label both axes, and make the points dark blue by writing `color = "darkblue"` inside `geom_point()`.
""", solution="""
ggplot(study_df, aes(x = age, y = SBP)) +
  geom_point(color = "darkblue") +
  labs(
    title = "Systolic Blood Pressure vs. Age",
    x = "Age (years)",
    y = "SBP (mmHg)"
  ) +
  theme_minimal()
""")

nb.md("""
## 7. Which plot when?

| You want to see... | Plot | Geom |
|---|---|---|
| The distribution of one numeric column | Histogram | `geom_histogram()` |
| A numeric column compared across groups | Box plot | `geom_boxplot()` |
| The relationship between two numeric columns | Scatter plot | `geom_point()` |
""")

nb.finish([
    ("summary(df$x)", "Min, quartiles, median, mean, max, and missing count"),
    ("group_by(g) %>% summarise(m = mean(x))", "One summary row per group"),
    ("n()", "Inside `summarise()`: number of rows in the group"),
    ("ggplot(df, aes(x = a, y = b)) + geom_...()", "The pattern for every plot"),
    ("geom_histogram(binwidth = 5)", "Histogram"),
    ("geom_boxplot()", "Box plot"),
    ("geom_point()", "Scatter plot"),
    ('labs(title = "...", x = "...", y = "...")', "Title and axis labels"),
], f"Continue with {link('A5')}.")
nb.write()

# =====================================================================  A5
nb = NB("A5", [
    "Choose between a t-test, ANOVA, and a chi-square test",
    "Run each one in R",
    "Find the important numbers in the output",
], needs=link("A4") + ". This notebook assumes you have met these tests in a statistics course; it shows how to run them, not the theory behind them")

nb.md(f"""
## 1. Setup

{SETUP_NOTE}
""")
nb.code("""
library(tidyverse)

study_df <- read_csv("RAW_final_dataset2.csv")
""")
nb.md("""
## 2. Which test?

The choice depends on what kind of variables you are comparing.

| Outcome | Compared across | Test | R function |
|---|---|---|---|
| A number (e.g. blood pressure) | 2 groups | Two-sample t-test | `t.test()` |
| A number | 3 or more groups | One-way ANOVA | `aov()` |
| A category (e.g. disease yes/no) | Groups | Chi-square test | `chisq.test()` |

## 3. Two-sample t-test

**Question:** is mean systolic blood pressure different in people with and without the condition?

Always look at the numbers before testing.
""")
nb.code("""
study_df %>%
  group_by(condition_status) %>%
  summarise(n = n(), mean_SBP = mean(SBP, na.rm = TRUE))
""")
nb.md("""
The two means are almost the same. (`n` counts everyone in each group, including the few people with missing blood pressure, who are left out of the mean and of the test.) Now the test. Inside `t.test()` is a **formula**: the outcome, a tilde `~`, and the grouping variable. Read `SBP ~ condition_status` as "SBP by condition status". `data =` says which dataframe the columns come from.
""")
nb.code("t.test(SBP ~ condition_status, data = study_df)")
nb.md("""
How to read the output:

- **`p-value`**: 0.84. There is no evidence of a difference in mean blood pressure between the groups.
- **`95 percent confidence interval`**: the range of values for the true difference between the two means (group 0 minus group 1) that are compatible with the data. It runs from about -5 to 6, and includes 0.
- **`sample estimates`**: the two group means.
- **`Welch Two Sample t-test`**: by default R uses the Welch version, which does not assume the two groups have equal variance. It is generally the safer choice for clinical data.
""")
nb.turn("""
Is mean `age` different in people with and without the condition? Look at the group means, then run the t-test.
""", solution="""
study_df %>%
  group_by(condition_status) %>%
  summarise(n = n(), mean_age = mean(age))

t.test(age ~ condition_status, data = study_df)
""", expected="means 51.4 and 56.4; p-value 0.24")

nb.md("""
## 4. One-way ANOVA

**Question:** is mean blood pressure different across the three `sex_at_birth` groups? With more than two groups, use ANOVA.

It takes two steps: `aov()` fits the model, and `summary()` shows the table.
""")
nb.code("""
anova_model <- aov(SBP ~ sex_at_birth, data = study_df)
summary(anova_model)
""")
nb.md("""
The p-value is in the column `Pr(>F)`: 0.661. There is no evidence that mean blood pressure differs between the groups. The last line notes that 5 people were left out because their blood pressure is missing.
""")
nb.turn("Is mean `age` different across the `race` groups? Run a one-way ANOVA.",
        solution="""
age_model <- aov(age ~ race, data = study_df)
summary(age_model)
""", expected="p-value 0.814")

nb.md("""
## 5. Chi-square test

**Question:** is drug exposure associated with the condition? Both variables are categories (yes/no), so use a chi-square test.

Start with the table of counts. `table()` with two columns makes a cross-tabulation: the first column gives the rows, the second gives the columns.
""")
nb.code("""
exposure_table <- table(study_df$exposure_status, study_df$condition_status)
exposure_table
""")
nb.md("Rows are exposure (0 = unexposed, 1 = exposed); columns are the condition (0 = no, 1 = yes). Of the 65 unexposed, 9 have the condition. Of the 35 exposed, 21 do. `chisq.test()` takes this table.")
nb.code("chisq.test(exposure_table)")
nb.md("""
The p-value is written `4.76e-06`. This is scientific notation: `e-06` means "move the decimal point 6 places to the left", so the value is 0.00000476. That is very small: strong evidence that exposure and the condition are associated in this (simulated) data.

The heading of the output mentions "Yates' continuity correction". For a table with two rows and two columns, R applies this small adjustment by default, so the p-value is slightly different from one calculated by hand without it.

### When counts are small

The chi-square test is unreliable when the **expected** count in some cell of the table is small (a common rule of thumb is below 5). That happens when a group has very few people. R warns you when it does.
""")
nb.turn("""
Is `sex_at_birth` associated with the condition? Make the table and run `chisq.test()` on it. Read the warning. Then run `fisher.test()` on the same table: Fisher's exact test is the alternative to use when counts are small.
""", solution="""
sex_table <- table(study_df$sex_at_birth, study_df$condition_status)
sex_table
chisq.test(sex_table)
fisher.test(sex_table)
""", expected="chi-square p-value 0.33, with a warning; Fisher's exact test p-value 0.30",
        note='The warning "Chi-squared approximation may be incorrect" appears because the "Other" group has only 8 people, so the expected number of them with the condition is only 2.4. Neither test shows evidence of an association.')

nb.md("""
## 6. Keeping a result

A test result can be stored in a variable, and individual numbers pulled out of it with `$`, just like columns of a dataframe.
""")
nb.code("""
t_result <- t.test(SBP ~ condition_status, data = study_df)
t_result$p.value
""")

nb.md("""
> **Remember:** R will run any test you ask for, on any data, without checking that the test is appropriate. Choosing the right test, checking its assumptions, and interpreting the result are your job.
""")

nb.finish([
    ("t.test(y ~ group, data = df)", "Two-sample t-test (Welch by default)"),
    ("summary(aov(y ~ group, data = df))", "One-way ANOVA"),
    ("table(df$a, df$b)", "Cross-tabulation of two columns"),
    ("chisq.test(tbl)", "Chi-square test on a table"),
    ("fisher.test(tbl)", "Fisher's exact test, for small counts"),
    ("result$p.value", "Pull the p-value out of a stored test result"),
], f"Continue with {link('A6')}.")
nb.write()

# =====================================================================  A6
nb = NB("A6", [
    "Fit a linear regression and read its output",
    "Adjust for other variables",
    "Fit a logistic regression for a yes/no outcome",
    "Turn logistic regression results into odds ratios",
], needs=link("A5"), minutes="30 to 40")

nb.md(f"""
## 1. Setup

{SETUP_NOTE} This notebook also loads `broom`, a package that turns model results into tidy tables.
""")
nb.code("""
library(tidyverse)
library(broom)

study_df <- read_csv("RAW_final_dataset2.csv")
""")

nb.md("""
## 2. Simple linear regression

**Question:** how does systolic blood pressure change with age?

In notebook A4 you saw in a scatter plot that blood pressure rises with age. Linear regression puts a number on that: it finds the straight line that best fits the points.

The function is `lm()`, for "linear model". It uses the same formula style as the t-test: outcome, tilde, predictor.
""")
nb.code("""
lm_model <- lm(SBP ~ age, data = study_df)
summary(lm_model)
""")
nb.md("""
The output is long. Look at the **Coefficients** table.

- The row **`age`**, column **`Estimate`**: 0.506. This is the slope. For each additional year of age, blood pressure is higher by about 0.5 mmHg on average.
- The same row, column **`Pr(>|t|)`**: the p-value for the slope. `4.75e-16` is scientific notation, as in notebook A5: a decimal point, 15 zeros, and then 475. Extremely small.
- **`(Intercept)`**: where the line crosses the vertical axis, at age 0. Rarely interesting in itself.
- Near the bottom, **`Multiple R-squared`**: 0.51. Age accounts for about half of the variation in blood pressure in this data.

### A tidier table

`tidy()` from the broom package shows the coefficients as a dataframe, which is easier to read and to use in later steps.
""")
nb.code("tidy(lm_model)")
nb.md("""
### Seeing the line

Add `geom_smooth(method = "lm")` to a scatter plot to draw the fitted line. The shaded band shows the uncertainty around it.
""")
nb.code("""
ggplot(study_df, aes(x = age, y = SBP)) +
  geom_point(color = "darkblue", alpha = 0.5) +
  geom_smooth(method = "lm", color = "red") +
  labs(
    title = "Systolic Blood Pressure by Age",
    x = "Age (years)",
    y = "SBP (mmHg)"
  ) +
  theme_minimal()
""")
nb.md("(`alpha = 0.5` makes the points half transparent. The message about `formula = 'y ~ x'` is normal, and the warnings about 5 removed rows are the 5 people with missing blood pressure.)")

nb.md("""
## 3. Multiple linear regression

In medical research you usually need to account for other variables: is the relationship still there after **adjusting** for sex, for example? To adjust for a variable, add it to the formula with a plus sign.
""")
nb.code("""
lm_adjusted <- lm(SBP ~ age + sex_at_birth, data = study_df)
tidy(lm_adjusted)
""")
nb.md("""
- **`age`**: 0.504. After adjusting for sex, the slope for age has barely changed.
- **`sex_at_birthMale`** and **`sex_at_birthOther`**: for a category, R compares each group with a **reference group**, which is the first one alphabetically. Here that is Female. So males average about 1.3 mmHg higher than females of the same age, and that difference is not statistically significant (p = 0.55).
""")
nb.turn("""
Fit a linear regression of `SBP` on `age` and `exposure_status`, and show the tidy table. After adjusting for age, is drug exposure associated with blood pressure?
""", solution="""
lm_exposure <- lm(SBP ~ age + exposure_status, data = study_df)
tidy(lm_exposure)
""", expected="the estimate for exposure_status is about -2.03 with p-value 0.36",
        note="No evidence of an association: exposed people average about 2 mmHg lower at the same age, a difference that could easily be due to chance.")

nb.md("""
## 4. Logistic regression

**Question:** is drug exposure associated with the condition, after adjusting for age and sex?

The outcome here, `condition_status`, is yes or no (1 or 0). A straight line is the wrong tool for a yes/no outcome: it can predict values below 0 or above 1, which make no sense as probabilities.

**Logistic regression** is the standard method for a yes/no outcome. The key ideas:

- The **odds** of an outcome are the probability that it happens divided by the probability that it does not. A probability of 0.2 is odds of 0.2 / 0.8 = 0.25.
- Instead of modeling the outcome directly, logistic regression models the **logarithm of the odds**.
- So the coefficient it reports for each predictor is a **log odds ratio**.
- To get an **odds ratio**, you reverse the logarithm with the exponential function, `exp()`.

An odds ratio of 1 means no association. Above 1 means higher odds of the outcome; below 1 means lower odds.

The function is `glm()`, for "generalized linear model". `family = "binomial"` is what makes it a logistic regression.
""")
nb.code("""
logistic_model <- glm(
  condition_status ~ exposure_status + age + sex_at_birth,
  data = study_df,
  family = "binomial"
)
tidy(logistic_model)
""")
nb.md("""
The estimate for `exposure_status` is about 2.16. **This is a log odds ratio, not an odds ratio.** Reporting it as "the odds ratio is 2.16" is a common and serious mistake. Convert it:
""")
nb.code("exp(2.157)")
nb.md("""
The odds ratio is about 8.6. `tidy()` can do the conversion for every coefficient, without rounding, and add confidence intervals:
""")
nb.code("""
tidy(logistic_model, exponentiate = TRUE, conf.int = TRUE)
""")
nb.md("""
Now the `estimate` column holds odds ratios, and `conf.low` and `conf.high` give the 95% confidence interval. (Two details: the `(Intercept)` row is not an odds ratio and is rarely of interest, and the `std.error` column is not converted.)

**How to say it:** after adjusting for age and sex, people exposed to the drug had 8.6 times the odds of the condition compared with unexposed people (95% confidence interval 3.3 to 24.3). The interval does not include 1, which agrees with the very small p-value.

**How not to say it:** "8.6 times as likely". An odds ratio is not a ratio of probabilities. When the outcome is common, as it is here (60% of exposed people and 14% of unexposed people have the condition), the odds ratio is much larger than the ratio of the two probabilities, which is about 4.

Remember that these data are simulated. The result illustrates the method; it says nothing about real medications.
""")
nb.turn("""
Fit an **unadjusted** logistic regression, with `exposure_status` as the only predictor of `condition_status`. Show the odds ratio and its confidence interval. How does it compare with the adjusted odds ratio of 8.64?
""", solution="""
unadjusted_model <- glm(
  condition_status ~ exposure_status,
  data = study_df,
  family = "binomial"
)
tidy(unadjusted_model, exponentiate = TRUE, conf.int = TRUE)
""", expected="odds ratio 9.33 (95% confidence interval 3.63 to 25.9)",
        note="Adjusting for age and sex changed the odds ratio only slightly, from 9.33 to 8.64.")

nb.md(f"""
## 5. Before you trust a model

Regression models rest on assumptions about the data. Before drawing conclusions from one, check those assumptions with **model diagnostics**. That is beyond this notebook; see your statistics text or the [Additional Resources]({SITE}resources.html) page.

## 6. Good to know for your own project

- **Objects live in memory, files live on disk.** `study_df` exists only while your session is running. If the session restarts, run your notebook again from the top. Use `ls()` to list the objects currently in memory.
- **Where am I?** `getwd()` shows the folder R is working in, which matters when you read or save files by name.
- **Dates read as text.** In *All of Us* data, dates sometimes arrive as text such as "2020-03-15 00:00:00 UTC". Convert them with `as.Date()`, which you met in notebook F2.
- **Write code that runs top to bottom.** Anyone, including you in six months, should be able to run your notebook from the first cell to the last and get the same result.
""")
nb.code("""
ls()      # objects in memory
getwd()   # current working folder
""")

nb.finish([
    ("lm(y ~ x, data = df)", "Linear regression"),
    ("lm(y ~ x + z, data = df)", "Linear regression adjusting for z"),
    ('glm(y ~ x, data = df, family = "binomial")', "Logistic regression (y is 0 or 1)"),
    ("summary(model)", "Full model output"),
    ("tidy(model)", "Coefficients as a tidy table"),
    ("tidy(model, exponentiate = TRUE, conf.int = TRUE)", "Odds ratios with confidence intervals"),
    ("exp(x)", "Exponential: converts a log odds ratio to an odds ratio"),
    ('geom_smooth(method = "lm")', "Add a fitted line to a scatter plot"),
], f"""
You have finished Path A. You can now clean, combine, explore, and analyze a dataset in R.

The next step is to do the same with real data in the *All of Us* Researcher Workbench. See the [workshop website]({SITE}) for how to get started there.
""")
nb.write()
