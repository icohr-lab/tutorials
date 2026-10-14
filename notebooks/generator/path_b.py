from nbkit import NB, link, SITE, POLICY

DESCRIBE = '''
# ---- Helper code. You do not need to read this part; just run the cell. ----
describe_columns <- function(data) {
  tibble(column = names(data), type = map_chr(data, ~ class(.x)[1]))
}
'''.strip()

HELPERS = '''
# ---- Helper code. You do not need to read this part; just run the cell. ----
describe_columns <- function(data) {
  tibble(column = names(data), type = map_chr(data, ~ class(.x)[1]))
}
check <- function(ok, label) {
  ok <- tryCatch(suppressWarnings(isTRUE(ok)), error = function(e) FALSE)
  cat(if (ok) "PASS    " else "NOT YET ", label, "\\n")
}
'''.strip()

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
""".strip()

PROMPT_CELL = "**My prompt:** *(double-click this cell and paste the prompt you used)*"
PASTE = "# Paste the AI's code here, read it, then run it\n"
OWN = "# Your own check\n"
SETUP_NOTE = "Run the setup cell. The lines printed by `library(tidyverse)` and `read_csv()` are normal."

RULES = f"""
1. **Never give an AI tool participant-level data.** Under [*All of Us* policy]({POLICY}), uploading to a public AI tool counts as disseminating the data, and moving individual-level data out of the Researcher Workbench violates the Data User Code of Conduct. The working rule in this course follows from that: you share code and descriptions of your data, never the data. Section 4 spells out what that means. *The data in these notebooks are simulated, so nothing here is restricted. Practice the habit anyway.*
2. **You are responsible for every line.** If you cannot explain what a line does, do not use it in your research. Ask the AI to explain it until you can.
3. **Check before you trust.** Code that runs without an error is not necessarily correct.
"""

# =====================================================================  B1
nb = NB("B1", [
    "Work in a loop: describe, generate, read, run, check",
    "Describe your data to an AI assistant without sharing the data itself",
    "Write a prompt that gets you usable code",
    "Check that the code did what you wanted",
], needs="the six Foundations notebooks, ending with " + link("F6"), minutes="30 to 40")

nb.md(f"""
## 1. A different way of working

In the Foundations notebooks you wrote every line yourself. From here on, an AI assistant writes most of the code. Your job changes: you **describe** what you want, **read** what comes back, and **check** that it is right.

That does not make the Foundations wasted effort. They are exactly what lets you do this well. You know what a dataframe is, what `filter()` and `left_join()` do, and why missing values matter. Without that, you could not tell good code from bad.

### Three rules
{RULES}

### Which AI assistant?

Use the AI chat tool your instructor specifies, and keep it open in a **separate window or tab** while you work.

Do not use an assistant that is built into the notebook itself (Colab has one, called Gemini). A built-in assistant may be able to read your cells and their output, which with real data would mean it sees the data without your pasting anything. With the simulated data here that would do no harm, but a separate chat window makes you practice describing your data, and that is the skill you will need.

## 2. The project

Over the next few notebooks you will carry out a small research project the way you would with *All of Us* data:

> **Is taking an anticholinergic medication associated with developing dementia?**

You have three tables of **simulated** data for 100 people. The outcome is recorded as either dementia or mild cognitive impairment (MCI), an earlier stage of memory loss. In this project both count, and the notebooks call them "the condition".

Before any analysis, the tables have to be cleaned and combined into one table with one row per person.

{SETUP_NOTE}
""")
nb.code("""
library(tidyverse)

person_df    <- read_csv("RAW_demographic_data.csv")
condition_df <- read_csv("RAW_conditions.csv")
drug_df      <- read_csv("RAW_drug_exposures.csv")

""" + HELPERS)

nb.md("""
## 3. The loop

Every task follows the same five steps.

| Step | What you do |
|---|---|
| 1. **Describe** | Tell the AI about your data and what you want |
| 2. **Generate** | The AI writes code |
| 3. **Read** | Go through the code. Can you say what each part does? |
| 4. **Run** | Paste it into the notebook and run it |
| 5. **Check** | Compare the result with something you know |

If step 3 or step 5 fails, go back to step 1 with a better description, or ask the AI to explain.

## 4. Describing data without sharing it

A chat assistant in a separate window cannot see your notebook, so it knows nothing about your data unless you tell it. The more precisely you describe the data, the better the code.

You might think of pasting the output of `head()`. With real data, **do not**: `head()` prints actual rows, and rows are participant-level data. The setup cell gave you a safer tool, `describe_columns()`, which prints only the column names and types.
""")
nb.code("describe_columns(person_df)")
nb.md("""
This is safe to paste into any AI tool. (`numeric` is a number; `character` is text.)

For a column of categories, the AI also needs to know which categories exist. The names of the categories, with no counts and no rows, are fine to share.
""")
nb.code("unique(person_df$race)")
nb.md("""
Use `unique()` this way **only on a column you know holds a short list of categories**, such as race or sex. On a column of IDs, dates, or free text, `unique()` prints values that belong to individual people.

### What may be shared

| Safe to give an AI tool | Never give an AI tool |
|---|---|
| Your code | Rows of data, even one |
| Column names and types (`describe_columns()`) | The output of `head()`, `str()`, or a printed dataframe |
| The names of the categories in a column | `person_id` values, dates, or anything else about one person |
| Error messages, once you have read them and removed any data values they quote | Screenshots or plots that show individual participants |
| Your research question and analysis plan | Tables or counts in which any cell is below 20 |
| Summary statistics with no participant count below 20 | |

Two consequences that are easy to miss:

- When a result looks wrong, **describe the problem to the AI in words**. Do not paste the output table.
- The assistant does not need to see your data to write good code. It needs to know how the data are laid out.
""")

nb.md("""
## 5. A worked example: recoding race

Follow this example through once. In the next section you will do one yourself.

**The task.** The `race` column has seven categories. For analysis, you want to shorten "Black or African American" to "Black", relabel "Skip" as "Unknown", and combine "More than one population" and "None of these" into "Other".

First, look at what you have, so that you can compare afterwards.
""")
nb.code("person_df %>% count(race)")
nb.md("""
### Step 1: Describe

Here is a prompt for this task.

> In R using tidyverse, I have a dataframe called `person_df` with one row per person. It has a column `race` (character) with these values: "Asian", "Black or African American", "More than one population", "None of these", "Other", "Skip", "White".
>
> Change "Black or African American" to "Black". Change "Skip" to "Unknown". Change both "More than one population" and "None of these" to "Other". Leave all other values unchanged. Save the result back to `person_df`.

Notice what it contains:

| Part of the prompt | Why it is there |
|---|---|
| "In R using tidyverse" | So you get code in the language and style you know |
| "a dataframe called `person_df`" | So the code uses your real names and runs without editing |
| "one row per person" | So the AI understands the table's layout |
| "a column `race` (character) with these values..." | The AI cannot guess your categories or their exact spelling |
| The changes, one by one | No room for interpretation |
| "Leave all other values unchanged" | Says what should *not* happen |
| "Save the result back to `person_df`" | Says where the result should go |

### Step 2: Generate

An AI assistant returned the code in the cell below. **Do not run it yet.** (If you try the prompt yourself, your AI may write it differently. That is fine: there is more than one correct way.)
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
### Step 3: Read

Read the code before running it. You know `mutate()` from the Foundations. You have not seen `case_when()` before, and that is normal: AI assistants often use functions that are new to you. Here is how to read this one.

- `case_when()` is a list of rules. Each rule is `test ~ new value`. R uses the first rule whose test is true.
- `race %in% c("A", "B")` is true when race is "A" or race is "B".
- `.default = race` says what to do when no rule matches: keep the original value.

When you meet an unfamiliar function, **ask the AI**: *"Explain this code line by line for a beginner."* That is always a reasonable request.

### Step 4: Run

Now go back and run the cell.

### Step 5: Check

The code ran without an error. That tells you only that R understood it, not that it did what you wanted. Three checks for any recoding:
""")
nb.code("person_df %>% count(race)   # 1. Are the categories what you intended?")
nb.code("nrow(person_df)             # 2. Is the number of rows unchanged?")
nb.code("sum(is.na(person_df$race))  # 3. Were any missing values created?")
nb.md("""
Five categories, 100 rows, no missing values. And the numbers add up: "Other" was 4 and is now 15, which is 4 + 6 + 5. The recoding worked.

## 6. Your turn, with help: recoding sex at birth

**The task.** Change every `sex_at_birth` value other than "Female" and "Male" to "Other". Save the result back to `person_df`.

Start by gathering what the AI will need to know.
""")
nb.code("unique(person_df$sex_at_birth)")
nb.md("""
### Step 1: Describe

Here is a prompt with gaps. Copy it into your AI assistant and fill in the gaps.

> In R using tidyverse, I have a dataframe called `______` with one row per person. It has a column `______` (character) with these values: ______.
>
> Change ______ to "Other". Leave "Female" and "Male" unchanged. Save the result back to `______`.
""")
nb.md(PROMPT_CELL)
nb.md("### Steps 2 to 4: Generate, read, run\n\nRead the code the AI gives you. If any part is unclear, ask the AI to explain it. Then paste it below and run it.\n\nYour data are already loaded. If the AI's answer includes lines that create example data, read a file, or install a package, leave those lines out.")
nb.code(PASTE, solution="""
person_df <- person_df %>%
  mutate(
    sex_at_birth = case_when(
      sex_at_birth %in% c("Intersex", "Prefer not to answer", "Skip") ~ "Other",
      .default = sex_at_birth
    )
  )
""")
nb.answer("Section 6: recoding sex at birth", note='A completed prompt: *In R using tidyverse, I have a dataframe called `person_df` with one row per person. It has a column `sex_at_birth` (character) with these values: "Female", "Male", "Intersex", "Prefer not to answer", "Skip". Change "Intersex", "Prefer not to answer", and "Skip" to "Other". Leave "Female" and "Male" unchanged. Save the result back to `person_df`.* One correct answer:', solution="""
person_df <- person_df %>%
  mutate(
    sex_at_birth = case_when(
      sex_at_birth %in% c("Intersex", "Prefer not to answer", "Skip") ~ "Other",
      .default = sex_at_birth
    )
  )
""")
nb.md("### Step 5: Check\n\nFirst do your own check, using the three checks from the worked example.")
nb.code(OWN, solution="person_df %>% count(sex_at_birth)\nnrow(person_df)\nsum(is.na(person_df$sex_at_birth))")
nb.md("Then run the provided check. Each line prints `PASS` or `NOT YET`.")
nb.code("""
check(nrow(person_df) == 100, "person_df still has 100 rows")
check(!anyNA(person_df$sex_at_birth), "no missing values were created")
check(setequal(unique(person_df$sex_at_birth), c("Female", "Male", "Other")), "there are exactly three categories")
check(sum(person_df$sex_at_birth == "Other") == 8, "8 people are coded Other")
""")
nb.md("""
If a line says `NOT YET`, something is off. Look at `person_df %>% count(sex_at_birth)`, work out what went wrong, and tell the AI in words what needs to change. If you have changed `person_df` in a way you did not intend, run the setup cell and the race recoding again to start fresh.

## 7. Weak prompts and strong prompts

Compare these two prompts for the task you just did.

**Weak:** "Clean up the sex variable."

**Strong:** the prompt you completed above.

The weak prompt forces the AI to guess the name of your dataframe, the name of the column, which values exist, and what "clean up" means. It will guess, and it will not tell you that it guessed. The code may run and still do something you did not intend.

## 8. The AI as a tutor

The same assistant that writes code can explain it. Useful questions:

- "Explain this code line by line for a beginner."
- "What does `.default` do here? What would happen if I left it out?"
- "Is there a simpler way to write this?"
- "What could go wrong with this code?"

Try the second question now, with the code you were given. The answer describes a real and common mistake that you will meet again in notebook B4.
""")

nb.finish([
    ("R and tidyverse", "You get code you can read"),
    ("The dataframe's name", "The code runs without editing"),
    ("Column names and types (`describe_columns()`)", "The AI cannot see your data"),
    ("What one row represents", "One row per person, or per record?"),
    ("The exact category values", "Spelling and capital letters must match"),
    ("The goal, step by step", "Leaves nothing to guess"),
    ("What should stay unchanged", "Prevents side effects"),
    ("The name for the result", "You know where to find it"),
    ("That the data are already loaded", "Stops the AI inventing example data that would overwrite yours"),
], f"Continue with {link('B2')}.", head=("Put this in your prompt", "Why"), raw=True)
nb.write()

# =====================================================================  B2
nb = NB("B2", [
    "Prompt for code that reduces records to one row per person",
    "Merge tables with AI help and check the result",
    "Test logic on cases where you already know the answer",
    "Build the variables needed for analysis",
], needs=link("B1"), minutes="30 to 40")

nb.md(f"""
## 1. Where we are

The demographics table is clean. Now you need one table with one row per person, containing each person's first diagnosis date and first prescription date. (A diagnosis here means dementia or mild cognitive impairment: "the condition".) In this notebook the prompts are yours to write; each task gives you a checklist instead of a template.

{SETUP_NOTE} It repeats the recoding from notebook B1, so that you start from clean data.

> **If you get stuck on a task,** the Solutions section at the end of the notebook has working code for each one. Paste it in and carry on; later tasks depend on earlier ones.

> **Your data are already loaded.** If the AI's answer includes lines that create example data, read a file, or install a package, leave those lines out. Otherwise they may overwrite your tables.
""")
nb.code("""
library(tidyverse)

person_df    <- read_csv("RAW_demographic_data.csv")
condition_df <- read_csv("RAW_conditions.csv")
drug_df      <- read_csv("RAW_drug_exposures.csv")

# Catch-up: the recoding from notebook B1
""" + RECODE + """

# Shuffle the records. Real data do not arrive sorted by date.
set.seed(2026)
condition_df <- condition_df %>% slice_sample(prop = 1)
drug_df      <- drug_df %>% slice_sample(prop = 1)

""" + HELPERS)

nb.md("""
## 2. Task 1: one row per person

At the end of the Foundations you saw that `condition_df` has several records for some people, and that joining it directly to `person_df` multiplies the rows. The fix is to keep only each person's **earliest** record.

### Know the answer for one person first

Before asking for code, look at one person by hand. Then you will have a case to check the code against.
""")
nb.code("condition_df %>% filter(person_id == 8)")
nb.md("""
Person 8 has four records, not in date order. The earliest is dated 2025-06-09. (The data are simulated, so the dates mean nothing.) Whatever code you get, **it must keep that row for person 8.**

Use this case to check the code yourself. **Do not put it in your prompt**: with real data, one person's ID and dates are participant-level data.

### The goal

Create `earliest_condition`, containing only the row with each person's earliest `condition_start_date`, and `earliest_drug`, containing only the row with each person's earliest `drug_exposure_start_date`. Each must have exactly one row per person.

### Write your prompt

Get the column descriptions to paste into your prompt:
""")
nb.code("""
describe_columns(condition_df)
describe_columns(drug_df)
""")
nb.md("""
Prompt checklist:

- R and tidyverse
- The names of both dataframes
- Their columns and types
- What one row represents, and that a person can have several rows
- The goal: for each person, keep the whole row that has the earliest date, with the original column names
- What to do if a person has two records on the same earliest date (keep only one)
- The names for the two results
- That the dataframes already exist, so no example data is needed
""")
nb.md(PROMPT_CELL)
S_EARLIEST = """
earliest_condition <- condition_df %>%
  group_by(person_id) %>%
  slice_min(condition_start_date, n = 1, with_ties = FALSE) %>%
  ungroup()

earliest_drug <- drug_df %>%
  group_by(person_id) %>%
  slice_min(drug_exposure_start_date, n = 1, with_ties = FALSE) %>%
  ungroup()
"""
nb.code(PASTE, solution=S_EARLIEST)
nb.answer("Task 1: one row per person", note="`group_by(person_id)` means \"do the next step separately for each person\". `slice_min()` keeps the row with the smallest (earliest) date. `with_ties = FALSE` keeps one row if two share that date. Your AI may instead sort the rows and keep the first one per person; that is also correct.", solution=S_EARLIEST)
nb.md("""
### Read it

The code almost certainly uses a function you have not met, such as `group_by()`, `slice_min()`, `arrange()`, or `summarise()`. Ask the AI: *"Explain this code line by line for a beginner."* Do not go on until you could explain it to a classmate.

### Check it yourself

Two checks. Is person 8's row the one you found by hand? Does each result have as many rows as it has different people?
""")
nb.code(OWN, solution="earliest_condition %>% filter(person_id == 8)\nnrow(earliest_condition)\nn_distinct(earliest_condition$person_id)")
nb.code("""
# Provided check (you do not need to read this code)
check(all(c("person_id", "condition_concept_id", "condition_start_date") %in% names(earliest_condition)),
      "earliest_condition still has its original columns")
check(all(c("person_id", "drug_concept_id", "drug_exposure_start_date") %in% names(earliest_drug)),
      "earliest_drug still has its original columns")
check(nrow(earliest_condition) == 30 && n_distinct(earliest_condition$person_id) == 30,
      "earliest_condition has one row for each of the 30 people with a diagnosis")
check(nrow(earliest_drug) == 35 && n_distinct(earliest_drug$person_id) == 35,
      "earliest_drug has one row for each of the 35 people with a prescription")
check(earliest_condition$condition_start_date[earliest_condition$person_id == 8] == as.Date("2025-06-09"),
      "person 8 has the earliest date, 2025-06-09")
check(nrow(earliest_condition) == 30 && all(earliest_condition$condition_start_date ==
            tapply(condition_df$condition_start_date, condition_df$person_id, min)[as.character(earliest_condition$person_id)]),
      "every person's diagnosis date is their earliest")
check(nrow(earliest_drug) == 35 && all(earliest_drug$drug_exposure_start_date ==
            tapply(drug_df$drug_exposure_start_date, drug_df$person_id, min)[as.character(earliest_drug$person_id)]),
      "every person's prescription date is their earliest")
""")

nb.md("""
## 3. Task 2: merge the three tables

### The goal

Create `combined_df` by adding the columns of `earliest_condition` and `earliest_drug` to `person_df`, matching on `person_id`. **All 100 people must be kept**, including those with no diagnosis and no prescription.

From notebook F6, you know which kind of join keeps every row of the first table. Name it in your prompt. If you leave the choice to the AI, it may pick a different join, and people will silently disappear.
""")
nb.md(PROMPT_CELL)
S_MERGE = """
combined_df <- person_df %>%
  left_join(earliest_condition, by = "person_id") %>%
  left_join(earliest_drug, by = "person_id")
"""
nb.code(PASTE, solution=S_MERGE)
nb.answer("Task 2: merge the three tables", note="A left join keeps every row of the first table.", solution=S_MERGE)
nb.md("### Check it yourself\n\nA join can drop people or duplicate them. Which two numbers would show that neither happened?")
nb.code(OWN, solution="nrow(combined_df)\nn_distinct(combined_df$person_id)")
nb.code("""
# Provided check (you do not need to read this code)
check(nrow(combined_df) == 100, "combined_df has 100 rows")
check(n_distinct(combined_df$person_id) == 100, "each person appears exactly once")
check(sum(!is.na(combined_df$condition_start_date)) == 30, "30 people have a diagnosis date")
check(sum(!is.na(combined_df$drug_exposure_start_date)) == 35, "35 people have a prescription date")
""")
nb.md("""
The other people have `NA` in those date columns. Here, `NA` means "no record": the person was never diagnosed, or never prescribed the drug.

## 4. Task 3: who was exposed before diagnosis?

A drug cannot have contributed to a disease if the person started taking it **after** the disease was diagnosed. So a person counts as **exposed** only if they started the drug before their diagnosis, or took it and were never diagnosed.

| Situation | Status |
|---|---|
| No prescription record | "Unexposed" |
| Took the drug, never diagnosed | "Exposed" |
| Started the drug **before** the diagnosis date | "Exposed" |
| Started the drug **on or after** the diagnosis date | "Unexposed (Post-Diagnosis)" |

### Make a test first

Logic like this is easy to get subtly wrong, and the AI can get it wrong too. Before using any code on the real table, try it on a few made-up patients for whom the answer is obvious.
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
(`tibble()` is the tidyverse's version of `data.frame()`.)

**Using the table of rules, decide the status of each of these six patients now, before you have any code.** Write your answers here.

**My predictions:** *(double-click to edit)* 1: ... 2: ... 3: ... 4: ... 5: ... 6: ...

### The goal

Add a column `true_exposure_status` to **both** `timing_test` and `combined_df`, following the four rules in the table.

Prompt checklist: the dataframe names, the two date columns and their type (Date), the fact that either date can be missing, the four rules with the exact labels, and the name of the new column. You can paste the table of rules. Say that both dataframes already exist; otherwise the AI may write code that rebuilds `timing_test`.
""")
nb.md(PROMPT_CELL)
S_TIMING = """
add_exposure <- function(data) {
  data %>%
    mutate(
      true_exposure_status = case_when(
        is.na(drug_exposure_start_date) ~ "Unexposed",
        !is.na(drug_exposure_start_date) & is.na(condition_start_date) ~ "Exposed",
        drug_exposure_start_date < condition_start_date ~ "Exposed",
        drug_exposure_start_date >= condition_start_date ~ "Unexposed (Post-Diagnosis)"
      )
    )
}
timing_test <- add_exposure(timing_test)
combined_df <- add_exposure(combined_df)
"""
S_TIMING_SHOWN = """
timing_test <- timing_test %>%
  mutate(
    true_exposure_status = case_when(
      is.na(drug_exposure_start_date) ~ "Unexposed",
      !is.na(drug_exposure_start_date) & is.na(condition_start_date) ~ "Exposed",
      drug_exposure_start_date < condition_start_date ~ "Exposed",
      drug_exposure_start_date >= condition_start_date ~ "Unexposed (Post-Diagnosis)"
    )
  )

combined_df <- combined_df %>%
  mutate(
    true_exposure_status = case_when(
      is.na(drug_exposure_start_date) ~ "Unexposed",
      !is.na(drug_exposure_start_date) & is.na(condition_start_date) ~ "Exposed",
      drug_exposure_start_date < condition_start_date ~ "Exposed",
      drug_exposure_start_date >= condition_start_date ~ "Unexposed (Post-Diagnosis)"
    )
  )
"""
nb.code(PASTE, solution=S_TIMING)
nb.answer("Task 3: who was exposed before diagnosis?", note="Test patients: 1 Unexposed, 2 Exposed, 3 Exposed, 4 Unexposed (Post-Diagnosis), 5 Unexposed, 6 Unexposed (Post-Diagnosis). The rules about missing dates come first, because comparing a date with a missing date gives `NA`.", solution=S_TIMING_SHOWN)
nb.md("### Check it yourself\n\nLook at `timing_test`. Does every patient have the status you predicted?")
nb.code(OWN, solution="timing_test\ncombined_df %>% count(true_exposure_status)")
nb.code("""
# Provided check (you do not need to read this code)
check(identical(timing_test$true_exposure_status == "Exposed", c(FALSE, TRUE, TRUE, FALSE, FALSE, FALSE)),
      "test patients 2 and 3 are Exposed; 1, 4, 5, and 6 are not")
check(identical(as.character(timing_test$true_exposure_status),
                c("Unexposed", "Exposed", "Exposed", "Unexposed (Post-Diagnosis)", "Unexposed", "Unexposed (Post-Diagnosis)")),
      "all six test patients have exactly the labels from the table of rules")
check(!anyNA(combined_df$true_exposure_status), "everyone in combined_df has a status")
check(sum(combined_df$true_exposure_status == "Exposed") == 35, "35 people in combined_df are Exposed")
""")
nb.md("""
### Why the test table mattered

Run this:
""")
nb.code("combined_df %>% count(true_exposure_status)", solution="combined_df %>% count(true_exposure_status)")
nb.md("""
(If this gives an error, finish Task 3 first.)

Nobody in this dataset started the drug after their diagnosis. So if the code had **ignored the dates completely** and counted everyone with a prescription as exposed, the count for `combined_df` would have been exactly the same, and that check would still have passed. Only test patients 4 and 6 can reveal that mistake.

> **A check can only catch the mistakes your data are able to show.** When the logic matters, build a small test with cases you know.

## 5. Task 4: variables for analysis

### The goal

Add three columns to `combined_df`:

- `age`: 2026 minus `year_of_birth`.
- `condition_status`: the number 1 if the person has a diagnosis (`condition_concept_id` is not missing), the number 0 otherwise.
- `exposure_status`: the number 1 if `true_exposure_status` is "Exposed", the number 0 otherwise.

You can ask for all three in one prompt. Say that the two status columns should be numeric: statistical models need numbers, not the text "1" and "0".
""")
nb.md(PROMPT_CELL)
S_VARS = """
combined_df <- combined_df %>%
  mutate(
    age = 2026 - year_of_birth,
    condition_status = if_else(is.na(condition_concept_id), 0, 1),
    exposure_status = if_else(true_exposure_status == "Exposed", 1, 0)
  )
"""
nb.code(PASTE, solution=S_VARS)
nb.answer("Task 4: variables for analysis", solution=S_VARS)
nb.md("### Check it yourself\n\nFrom the earlier tasks you already know how many people have a diagnosis and how many are exposed. Do the new columns agree?")
nb.code(OWN, solution="sum(combined_df$condition_status)\nsum(combined_df$exposure_status)\nmean(combined_df$age)")
nb.code("""
# Provided check (you do not need to read this code)
check(abs(mean(combined_df$age) - 52.91) < 0.01, "mean age is 52.91")
check(is.numeric(combined_df$condition_status) && is.numeric(combined_df$exposure_status), "both status columns are numeric")
check(sum(combined_df$condition_status) == 30 && all(combined_df$condition_status %in% c(0, 1)), "condition_status is 1 for 30 people and 0 for the rest")
check(sum(combined_df$exposure_status) == 35 && all(combined_df$exposure_status %in% c(0, 1)), "exposure_status is 1 for 35 people and 0 for the rest")
check(nrow(combined_df) == 100, "combined_df still has 100 rows")
""")

nb.md("""
## 6. Task 5: save your work

Everything you have built exists only in R's memory, which Colab wipes when the session ends.

### The goal

Save `combined_df` as a CSV file called `cleaned_dataset.csv`. You have not learned how to do this, so ask the AI. This one needs only a very short prompt.
""")
nb.code(PASTE, solution='write_csv(combined_df, "cleaned_dataset.csv")')
nb.answer("Task 5: save your work", solution='write_csv(combined_df, "cleaned_dataset.csv")')
nb.code("""
# Provided check (you do not need to read this code)
check(file.exists("cleaned_dataset.csv"), "the file cleaned_dataset.csv exists")
""")
nb.md("""
In Colab, the file appears in the **Files** panel (the folder icon in the left sidebar). It is deleted when the session ends, so download it from that panel if you want to keep it.
""")

nb.finish([
    ("Work out one case by hand first", "You have something to check the code against"),
    ("Name the join you want", "The AI may otherwise choose one that drops people"),
    ("Compare rows with different people after every step", "Catches dropped and duplicated people"),
    ("Build a small test table for any rule-based logic", "Your real data may not contain the cases that expose a mistake"),
    ("Check new columns against numbers you already know", "Catches logic that is the wrong way round"),
], f"Continue with {link('B3')}.", head=("Habit", "Why"), raw=True)
nb.write()

# =====================================================================  B3
nb = NB("B3", [
    "Get summaries by group and cross-check them",
    "Read the code for a plot",
    "Improve a plot through follow-up prompts",
    "Check that a plot shows what you think it shows",
], needs=link("B2"))

nb.md(f"""
## 1. Where we are

The dataset is built. Before any statistical test, get to know it: how the values are distributed and how the groups compare. AI assistants are particularly good at plotting code, which is fiddly to write by hand.

{SETUP_NOTE} It loads the finished dataset from notebook B2, with one extra column: `SBP`, systolic blood pressure.
""")
nb.code("""
library(tidyverse)

study_df <- read_csv("RAW_final_dataset2.csv")

""" + DESCRIBE)
nb.code("describe_columns(study_df)")
nb.md("Keep this output handy: you will paste parts of it into your prompts.")

nb.md("""
## 2. Task 1: a summary by group

### The goal

A table showing, for each `sex_at_birth` group, the number of people and the mean `SBP`.

One thing the AI needs to be told: `SBP` has some missing values. If you do not mention it, the code may return `NA` for every mean, or the AI may deal with the missing values in a way you did not choose.
""")
nb.md(PROMPT_CELL)
S_SUM = """
study_df %>%
  group_by(sex_at_birth) %>%
  summarise(
    n = n(),
    mean_SBP = mean(SBP, na.rm = TRUE)
  )
"""
nb.code(PASTE, solution=S_SUM)
nb.answer("Task 1: a summary by group", note="`group_by()` means \"do the next step separately for each group\", and `summarise()` produces one row of summary per group. `n()` counts the rows. Expected: Female 44 people, mean 115.7; Male 48 people, mean 118.5; Other 8 people, mean 117.3.", solution=S_SUM)
nb.md("""
### Check: get the same number a second way

A good way to check a result is to calculate one piece of it by a different, simpler route. Here is the mean SBP for females, done with tools from the Foundations.
""")
nb.code("""
females <- study_df %>% filter(sex_at_birth == "Female")
nrow(females)
mean(females$SBP, na.rm = TRUE)
""")
nb.md("""
44 females with a mean of about 115.7. Does the "Female" row of your table say the same? (A table may show it rounded, as 116.) If yes, you can be fairly confident in the other rows.

## 3. How to read plotting code

Plots in the tidyverse are made with `ggplot()`. You do not need to write this code, but you need to read it. Every plot has three ingredients, joined with **plus signs**:

1. **The data**: which dataframe.
2. **The mapping**, inside `aes()`: which column goes on which axis.
3. **The shape**, called a geom: `geom_histogram()` for a histogram, `geom_boxplot()` for a box plot, `geom_point()` for a scatter plot.
""")
nb.code("""
ggplot(study_df, aes(x = age)) +
  geom_histogram(binwidth = 5)
""")
nb.md("""
Read it as: make a plot from `study_df`, put `age` on the x axis, and draw a histogram with bars 5 years wide.

**When you read plotting code, look at `aes()` first.** It tells you which columns are being plotted. If the wrong column is in there, the plot is wrong, however good it looks.

## 4. Task 2: a histogram, improved step by step

### The goal

A histogram of `SBP`.

Start with a simple prompt. Do not try to specify everything at once.
""")
nb.md(PROMPT_CELL)
S_HIST = """
ggplot(study_df, aes(x = SBP)) +
  geom_histogram(binwidth = 5, fill = "steelblue", color = "black") +
  labs(
    title = "Systolic Blood Pressure",
    x = "Systolic blood pressure (mmHg)",
    y = "Number of people"
  ) +
  theme_minimal()
"""
nb.code(PASTE, solution="ggplot(study_df, aes(x = SBP)) +\n  geom_histogram()")
nb.md("""
You probably see a **warning** that 5 rows were removed. Those are the 5 people with missing blood pressure. The plot is fine; the warning is a reminder that they are not in it. You may also see a message suggesting you pick a `binwidth`; that is a hint, not a problem.

### Follow up

You do not need to start again to improve the plot. In the same conversation, the AI remembers the code it just wrote. **Describe the change you want in words.** Do not upload a picture of the plot: with real data, a plot can show individual participants (a scatter plot has one point per person).

Send follow-up requests, one or two at a time, and paste the new version below. For example:

- "Make the bars 5 units wide."
- "Add a title, and label the x axis 'Systolic blood pressure (mmHg)'."
- "Use a cleaner theme and blue bars with black outlines."
""")
nb.code("# Paste the improved version here\n", solution=S_HIST)
nb.answer("Task 2: a histogram, improved step by step", note="One possible final version:", solution=S_HIST)
nb.md("**Read the final code.** Can you point to the part that sets the bar width, the part that sets the title, and the part that says which column is plotted?")

nb.md("""
## 5. Task 3: a box plot, and checking it

### The goal

A box plot comparing `SBP` across the three `sex_at_birth` groups, with a title and axis labels.
""")
nb.md(PROMPT_CELL)
S_BOX = """
ggplot(study_df, aes(x = sex_at_birth, y = SBP)) +
  geom_boxplot() +
  labs(
    title = "Systolic Blood Pressure by Sex",
    x = "Sex at birth",
    y = "SBP (mmHg)"
  ) +
  theme_minimal()
"""
nb.code(PASTE, solution=S_BOX)
nb.answer("Task 3: a box plot", solution=S_BOX)
nb.md("""
If you are not sure how to read a box plot, ask the AI: *"What do the parts of a box plot show?"* In short: the thick line in each box is the **median**, and the box covers the middle half of the values.

### Check the plot against numbers

A plot can be wrong in ways that are hard to see: the wrong column, groups mixed up, data silently left out. Check it against numbers you calculate separately. The cell below gives the median SBP in each group. (`group_by()` means "do the next step separately for each group", and `summarise()` produces one row of summary per group.)
""")
nb.code("""
study_df %>%
  group_by(sex_at_birth) %>%
  summarise(median_SBP = median(SBP, na.rm = TRUE))
""")
nb.md("""
The medians are 117 for Female, 120.5 for Male, and 119 for Other. Look at your plot: is the thick line in each box at about that height? Are there three boxes, with the labels you expect?

## 6. Task 4: a scatter plot with a trend line

### The goal

A scatter plot with `age` on the x axis and `SBP` on the y axis, with a straight trend line through the points, a title, and axis labels.
""")
nb.md(PROMPT_CELL)
S_SCATTER = """
ggplot(study_df, aes(x = age, y = SBP)) +
  geom_point(color = "darkblue", alpha = 0.5) +
  geom_smooth(method = "lm", color = "red") +
  labs(
    title = "Systolic Blood Pressure vs. Age",
    x = "Age (years)",
    y = "SBP (mmHg)"
  ) +
  theme_minimal()
"""
nb.code(PASTE, solution=S_SCATTER)
nb.answer("Task 4: a scatter plot with a trend line", note="`geom_smooth(method = \"lm\")` draws the straight line of best fit.", solution=S_SCATTER)
nb.md("""
(A message about `formula = 'y ~ x'` is normal, and the warnings about removed rows are again the 5 people with missing blood pressure.)

### Check it

- Read `aes()`: is `age` on x and `SBP` on y, and not the other way round?
- Does the line rise from left to right? The youngest person is 19 and the oldest is 90; does the x axis cover about that range?
- Ask the AI: *"Which part of this code draws the line, and what kind of line is it?"*

## 7. Which plot when?

| You want to see... | Ask for a... |
|---|---|
| The distribution of one numeric column | Histogram |
| A numeric column compared across groups | Box plot |
| The relationship between two numeric columns | Scatter plot |

If you are not sure which plot suits your question, describe the two columns and their types and ask the AI what it would suggest and why. Then decide for yourself.
""")

nb.finish([
    ("Mention missing values in your prompt", "Otherwise the AI chooses how to handle them"),
    ("Recalculate one number a second, simpler way", "Confirms a summary table"),
    ("Read `aes()` first", "It shows which columns are plotted"),
    ("Improve a plot with short follow-up prompts", "Easier than specifying everything at once"),
    ("Compare a plot with separately calculated numbers", "Catches wrong columns and mixed-up groups"),
    ("Read warnings about removed rows", "They tell you who is missing from the plot"),
], f"Continue with {link('B4')}.", head=("Habit", "Why"), raw=True)
nb.write()

# =====================================================================  B4
nb = NB("B4", [
    "Get useful help from an AI assistant when code gives an error",
    "Spot code that runs without an error but gives a wrong answer",
    "Use a short set of checks that catch the most common mistakes",
], needs=link("B3"), minutes="30 to 40")

nb.md(f"""
## 1. Two kinds of problem

Code can go wrong in two ways.

- **It stops with an error.** This is the easy kind. You know something is wrong, and the message tells you where to look.
- **It runs and gives a wrong answer.** This is the dangerous kind, because nothing tells you. AI-written code fails this way as readily as human-written code.

This notebook practices both.

{SETUP_NOTE}
""")
nb.code("""
library(tidyverse)

person_df    <- read_csv("RAW_demographic_data.csv")
condition_df <- read_csv("RAW_conditions.csv")
study_df     <- read_csv("RAW_final_dataset2.csv")

""" + DESCRIBE)

nb.md("""
## Part 1: When code gives an error

An AI assistant is very good at explaining errors, if you give it the right material.

**Give it:** the code that failed, the complete error message, and your column names and types from `describe_columns()`.

**Do not give it:** rows of data. With real data, that includes the output of `head()`, `str()`, or a printed dataframe. Read an error message before you paste it, and take out any data values it happens to quote.

A prompt that works:

> This R code gives an error. Explain what the error means and how to fix it.
>
> Code: *(paste the code)*
>
> Error: *(paste the whole message)*
>
> My dataframe's columns and types: *(paste the describe_columns() output)*
""")
nb.code("describe_columns(study_df)")
nb.md("""
### Error 1

The cell below is **meant to fail**. Run it, then use the prompt above to find out why. Fix the code in the cell after it.
""")
nb.code("study_df %>% fliter(age >= 65) %>% nrow()", error=True)
nb.code("# Your corrected version\n", solution="study_df %>% filter(age >= 65) %>% nrow()")
nb.md("*Expected result after fixing: 34*")
nb.answer("Error 1", note="`fliter` is a typing mistake for `filter`. The message `could not find function` usually means a misspelled function name or a package that has not been loaded.",
          solution="study_df %>% filter(age >= 65) %>% nrow()")
nb.md("""
### Error 2

Also **meant to fail**. This time the error message is longer. The useful part is near the top.
""")
nb.code("""
study_df %>%
  group_by(sex) %>%
  summarise(mean_SBP = mean(SBP, na.rm = TRUE))
""", error=True)
nb.code("# Your corrected version\n", solution="""
study_df %>%
  group_by(sex_at_birth) %>%
  summarise(mean_SBP = mean(SBP, na.rm = TRUE))
""")
nb.md("*Expected result after fixing: three rows, for Female, Male, and Other*")
nb.answer("Error 2", note="There is no column called `sex`; it is called `sex_at_birth`. Giving the AI your `describe_columns()` output is what lets it spot this.",
          solution="""
study_df %>%
  group_by(sex_at_birth) %>%
  summarise(mean_SBP = mean(SBP, na.rm = TRUE))
""")
nb.md("""
> **Also expect this:** AI assistants sometimes use a function that does not exist, or that only exists in a newer version of a package than the one installed. The symptom is `could not find function`. Tell the AI the exact error and ask for another way to do it.

## Part 2: When code runs but is wrong

Each example below shows a request and the code an AI assistant returned. **Every one runs without an error, and every one is wrong.** For each:

1. Run it and look at the result.
2. Use the clue to work out what is wrong.
3. Write a corrected version.

The Solutions section at the end explains each one. Try first.

### Mistake 1

**The request:** "What is the mean systolic blood pressure among men?"
""")
nb.code("""
study_df %>%
  filter(sex_at_birth == "male") %>%
  summarise(n = n(), mean_SBP = mean(SBP, na.rm = TRUE))
""")
nb.md("(`n()` counts the rows, and `NaN` means \"not a number\".)\n\n**Clue:** look at `n`. Then look at how the categories are spelled: `study_df %>% count(sex_at_birth)`.")
nb.code("# Your corrected version\n", solution="""
study_df %>%
  filter(sex_at_birth == "Male") %>%
  summarise(n = n(), mean_SBP = mean(SBP, na.rm = TRUE))
""")
nb.answer("Mistake 1", note="The category is `\"Male\"` with a capital M. `\"male\"` matched nobody, so the result is based on 0 people, and R gave no error. **The habit:** after a filter, check how many rows are left. **In the prompt:** give the AI the exact category values. Correct result: 48 men, mean SBP 118.5.",
          solution="""
study_df %>%
  filter(sex_at_birth == "Male") %>%
  summarise(n = n(), mean_SBP = mean(SBP, na.rm = TRUE))
""")

nb.md("""
### Mistake 2

**The request:** "Simplify the race variable: change 'Black or African American' to 'Black' and 'Skip' to 'Unknown'."
""")
nb.code("""
person_df %>% count(race)   # before

recoded <- person_df %>%
  mutate(race = case_when(
    race == "Black or African American" ~ "Black",
    race == "Skip" ~ "Unknown"
  ))

recoded %>% count(race)     # after
""")
nb.md("**Clue:** compare the two tables. What happened to everyone who was \"Asian\" or \"White\"?")
nb.code("# Your corrected version\n", solution="""
recoded <- person_df %>%
  mutate(race = case_when(
    race == "Black or African American" ~ "Black",
    race == "Skip" ~ "Unknown",
    .default = race
  ))
recoded %>% count(race)
""")
nb.answer("Mistake 2", note="73 people now have `NA` for race. `case_when()` gives `NA` to every value that matches none of its rules, unless you add `.default = race` to keep the original value. **The habit:** count the categories before and after any recoding. **In the prompt:** say \"leave all other values unchanged\".",
          solution="""
recoded <- person_df %>%
  mutate(race = case_when(
    race == "Black or African American" ~ "Black",
    race == "Skip" ~ "Unknown",
    .default = race
  ))
recoded %>% count(race)
""")

nb.md("""
### Mistake 3

**The request:** "Add each person's diagnosis information to the demographics table."

`person_df` has 100 people.
""")
nb.code("""
with_diagnosis <- person_df %>% left_join(condition_df, by = "person_id")
nrow(with_diagnosis)
""")
nb.md("**Clue:** compare the number of rows with `n_distinct(with_diagnosis$person_id)`. You met this problem in notebook F6.")
nb.code("# Your corrected version\n", solution="""
first_diagnosis <- condition_df %>%
  group_by(person_id) %>%
  slice_min(condition_start_date, n = 1, with_ties = FALSE) %>%
  ungroup()
with_diagnosis <- person_df %>% left_join(first_diagnosis, by = "person_id")
nrow(with_diagnosis)
""")
nb.answer("Mistake 3", note="166 rows for 100 people. `condition_df` has several records for some people, so the join repeats those people. Any count or average taken from this table would count them more than once. First reduce `condition_df` to one row per person, as you did in notebook B2. **The habit:** after every join, compare rows with different people. **In the prompt:** say what one row of each table represents.",
          solution="""
first_diagnosis <- condition_df %>%
  group_by(person_id) %>%
  slice_min(condition_start_date, n = 1, with_ties = FALSE) %>%
  ungroup()
with_diagnosis <- person_df %>% left_join(first_diagnosis, by = "person_id")
nrow(with_diagnosis)
""")

nb.md("""
### Mistake 4

This one is the hardest to spot, because the result looks perfectly reasonable.

**The request:** "The mean of SBP comes back as NA. Fix it."
""")
nb.code("""
study_df %>%
  mutate(SBP = replace_na(SBP, 0)) %>%
  summarise(mean_SBP = mean(SBP))
""")
nb.md("**Clue:** compare with `summary(study_df$SBP)`. Then ask yourself what `replace_na(SBP, 0)` does to the five people whose blood pressure was not measured.")
nb.code("# Your corrected version\n", solution="study_df %>% summarise(mean_SBP = mean(SBP, na.rm = TRUE))")
nb.answer("Mistake 4", note="The code replaced the 5 missing values with 0 and then averaged all 100, giving 111.4. The correct mean of the 95 measured values is 117.2. A blood pressure of 0 is not \"unknown\"; it is a wrong number. The request was the real problem: \"fix it\" let the AI choose how. **The habit:** compare any statistic with `summary()`. **In the prompt:** say how missing values should be treated, for example \"ignore missing values\".",
          solution="study_df %>% summarise(mean_SBP = mean(SBP, na.rm = TRUE))")

nb.md("""
## Part 3: The checks that catch most mistakes

All four mistakes had something in common: the request left something out, the AI filled the gap with a guess, and a simple check would have caught it.

| After you... | Check | It catches |
|---|---|---|
| Filter rows | How many rows are left? | Filters that match nothing or everything |
| Recode a column | `count()` the column before and after | Lost categories, new missing values |
| Join tables | `nrow()` against `n_distinct(person_id)` | Dropped or duplicated people |
| Calculate a statistic | Compare with `summary()`; count the missing values | Missing values handled wrongly |
| Write rule-based logic | Try it on a few cases you know | Rules that are wrong or in the wrong order |

None of these checks takes more than a line of code.
""")

nb.finish([
    ("Give the AI the code, the full error, and the column names", "It can explain and fix most errors"),
    ("Never paste rows of real data", "It violates the Data User Code of Conduct"),
    ("Say how missing values should be handled", "Otherwise the AI decides"),
    ("Say \"leave everything else unchanged\"", "Prevents side effects in recoding"),
    ("Say what one row of each table represents", "Prevents joins that duplicate people"),
    ("Run a check after every step", "Wrong code rarely announces itself"),
], f"Continue with {link('B5')}.", head=("Habit", "Why"), raw=True)
nb.write()

# =====================================================================  B5
nb = NB("B5", [
    "Choose a statistical test before asking for code",
    "Read the output of a t-test, ANOVA, chi-square test, and regression",
    "Get odds ratios from a logistic regression, and interpret them",
    "Carry this way of working over to real *All of Us* data",
], needs=link("B4") + ". This notebook assumes you have met these tests in a statistics course", minutes="30 to 40")

nb.md(f"""
## 1. What the AI will not do for you

An AI assistant will write code for any test you ask for, on any data, whether or not the test is appropriate. It will also produce a confident interpretation of whatever comes out. **Choosing the test and judging what the result means are your job.**

{SETUP_NOTE} It also loads `broom`, a package that turns model results into tidy tables.
""")
nb.code("""
library(tidyverse)
library(broom)

study_df <- read_csv("RAW_final_dataset2.csv")

""" + HELPERS)

nb.md("""
## 2. Which test?

| Outcome | Compared across, or related to | Method |
|---|---|---|
| A number (e.g. blood pressure) | 2 groups | Two-sample t-test |
| A number | 3 or more groups | One-way ANOVA |
| A category (e.g. disease yes/no) | Groups | Chi-square test |
| A number | Another number | Linear regression |
| Yes/no | One or more predictors | Logistic regression |

The last two rows can overlap with the others. When you simply want to know whether two yes/no variables are associated, with no adjustment for anything else, use the chi-square test.

## 3. A worked example: the t-test

**Question:** is mean systolic blood pressure different in people with and without the condition?

**Choose the test.** The outcome, `SBP`, is a number. It is compared across two groups (`condition_status` is 0 or 1). That calls for a two-sample t-test.

**The prompt:**

> In R, I have a dataframe `study_df` with one row per person. `SBP` is numeric, with a few missing values. `condition_status` is numeric, 0 or 1. Run a two-sample t-test comparing mean SBP between the two condition_status groups.

**The code an AI assistant returned:**
""")
nb.code("t.test(SBP ~ condition_status, data = study_df)")
nb.md("""
**Read the code.** `SBP ~ condition_status` is a **formula**: the outcome, a tilde `~`, and the grouping variable. Read it as "SBP by condition status".

**Read the output.**

- **`p-value`**: 0.84. No evidence of a difference in mean blood pressure between the groups.
- **`95 percent confidence interval`**: the plausible range for the difference between the two means, about -5 to 6. It includes 0.
- **`sample estimates`**: the two group means, 117.4 and 116.8.
- **The title**: "Welch Two Sample t-test".

**Ask about what you did not choose.** You asked for "a two-sample t-test"; the output says "Welch". A good follow-up: *"Which version of the t-test is this, and why is it the default?"* (It is the version that does not assume the two groups have equal variance, which is generally the safer choice.) Whenever the output names something you did not ask for, find out what it is.

## 4. Your turn: three more questions

For each question, **decide which method to use before you ask the AI**, using the table in section 2. Write your choice down. Then prompt for the code, run it, and compare with the expected results underneath.

| | Question | My choice of method |
|---|---|---|
| a | Does mean `SBP` differ among the three `sex_at_birth` groups? | |
| b | Is drug exposure (`exposure_status`, 0 or 1) associated with the condition (`condition_status`, 0 or 1)? | |
| c | How does `SBP` change with `age`? | |
""")
nb.md(PROMPT_CELL)
nb.code("# (a) " + PASTE[2:], solution="summary(aov(SBP ~ sex_at_birth, data = study_df))")
nb.code("# (b) " + PASTE[2:], solution="chisq.test(table(study_df$exposure_status, study_df$condition_status))")
nb.code("# (c) " + PASTE[2:], solution="tidy(lm(SBP ~ age, data = study_df))")
nb.md("""
### Expected results

| | Method | Result |
|---|---|---|
| a | One-way ANOVA | p = 0.66 |
| b | Chi-square test | p = 4.76e-06 |
| c | Linear regression | slope for age = 0.51, p < 0.001 |

- `4.76e-06` is scientific notation: move the decimal point 6 places to the left, giving 0.00000476. A very small p-value.
- The slope of 0.51 means blood pressure is higher by about half a mmHg for each additional year of age.

**If your numbers differ, find out why before moving on.** A common reason is that the AI chose a different variant of the test. For (b), for example, R's chi-square test applies a "continuity correction" by default; code that switches it off gives p = 1.56e-06, and Fisher's exact test gives p = 2.9e-06. All three lead to the same conclusion here, but you should know which one you ran. Ask the AI which variant it used and why.
""")
nb.answer("Section 4: three more questions", solution="""
# (a) One-way ANOVA
summary(aov(SBP ~ sex_at_birth, data = study_df))

# (b) Chi-square test
chisq.test(table(study_df$exposure_status, study_df$condition_status))

# (c) Linear regression
tidy(lm(SBP ~ age, data = study_df))
""")

nb.md("""
## 5. Logistic regression and odds ratios

**The research question:** is drug exposure associated with the condition, after adjusting for age and sex?

The outcome, `condition_status`, is yes or no, so the method is **logistic regression**. Three things to know in order to read its output:

- The **odds** of an outcome are the probability that it happens divided by the probability that it does not.
- Logistic regression models the **logarithm of the odds** of the outcome.
- So the coefficient it reports for each predictor is a **log odds ratio**.
- To get an **odds ratio**, the logarithm has to be reversed with the exponential function, which in R is `exp()`. This is called exponentiating.

An odds ratio of 1 means no association; above 1 means higher odds of the outcome; below 1 means lower odds.

### The goal

Fit a logistic regression of `condition_status` on `exposure_status`, adjusting for `age` and `sex_at_birth`. Produce a table of **odds ratios with 95% confidence intervals**, and save that table as `tidy_results`.

In your prompt, ask for the table to be made with `tidy()` from the broom package, keeping its standard column names. The provided check looks for those names.
""")
nb.md(PROMPT_CELL)
S_LOGIT = """
logistic_model <- glm(
  condition_status ~ exposure_status + age + sex_at_birth,
  data = study_df,
  family = "binomial"
)
tidy_results <- tidy(logistic_model, exponentiate = TRUE, conf.int = TRUE)
tidy_results
"""
nb.code(PASTE, solution=S_LOGIT)
nb.answer("Section 5: logistic regression", note="`family = \"binomial\"` makes it a logistic regression. `exponentiate = TRUE` converts the coefficients to odds ratios.", solution=S_LOGIT)
nb.code("""
# Provided check (you do not need to read this code)
or_row <- tryCatch(tidy_results[grepl("exposure_status", tidy_results$term), ][1, ], error = function(e) NULL)
check(abs(or_row$estimate - 8.64) < 0.06, "the odds ratio for exposure_status is about 8.64")
check(or_row$conf.low > 3.1 && or_row$conf.low < 3.5 && or_row$conf.high > 23 && or_row$conf.high < 25, "its 95% confidence interval runs from a little over 3 to about 24")
""")
nb.md("""
If the first line says `NOT YET` and your table shows about 2.16, the coefficients have not been exponentiated. If the table has different column names, ask the AI to use `tidy()` with its standard names.

### Interpret it yourself first

In one or two sentences, say what the odds ratio for `exposure_status` means. Include the confidence interval. **Write your own sentence before asking the AI for one**, then compare the two. To ask the AI, give it only the odds ratio and its confidence interval, not the whole table.

One caution: an odds ratio is not "times as likely". When the outcome is common, as it is here, the odds ratio is much larger than the ratio of the two probabilities.

**My interpretation:** *(double-click to edit)*

(Remember that these data are simulated. The result illustrates the method; it says nothing about real medications.)

### Catch the mistake

Here is a request and an AI's answer.

**The request:** "Fit a logistic regression of the condition on drug exposure, adjusting for age and sex, and tell me the odds ratio for drug exposure."

**The AI's answer:** "The odds ratio for drug exposure is 2.16, so exposed participants have about twice the odds of the condition."
""")
nb.code("""
model <- glm(condition_status ~ exposure_status + age + sex_at_birth,
             data = study_df, family = "binomial")
coef(model)["exposure_status"]
""")
nb.md("**What is wrong?** Use the three things to know at the top of this section. Then calculate the correct value in the cell below.")
nb.code("# The correct odds ratio\n", solution='exp(coef(model)["exposure_status"])')
nb.answer("Catch the mistake", note="2.16 is the model's coefficient, which is a **log** odds ratio. The odds ratio is its exponential: 8.64, not 2.16. Reporting a logistic regression coefficient as an odds ratio is a common and serious error, and an AI can make it as easily as a person can.",
          solution='exp(coef(model)["exposure_status"])')
nb.answer("A sample interpretation of the odds ratio", note="After adjusting for age and sex, people exposed to the drug had 8.6 times the odds of the condition compared with unexposed people (95% confidence interval 3.3 to 24.3).")
nb.md(f"""
### Ask about assumptions

Every statistical model rests on assumptions about the data. Ask the AI: *"What assumptions does this logistic regression make, and how do I check them in R?"* Regression results should not be used to draw conclusions until those checks have been done. See also the [Additional Resources]({SITE}resources.html) page.

## 6. Taking this to the Researcher Workbench

The way of working is the same with real *All of Us* data, with one firm difference: **code goes in; data never comes out.** Write your prompt and get code outside the Workbench, then copy the code into your Workbench notebook and run it there.

Here again is the table from notebook B1.

| Safe to give an AI tool | Never give an AI tool |
|---|---|
| Your code | Rows of data, even one |
| Column names and types (`describe_columns()`) | The output of `head()`, `str()`, or a printed dataframe |
| The names of the categories in a column | `person_id` values, dates, or anything else about one person |
| Error messages, once you have read them and removed any data values they quote | Screenshots or plots that show individual participants |
| Your research question and analysis plan | Tables or counts in which any cell is below 20 |
| Summary statistics with no participant count below 20 | |

See the [*All of Us* policy on AI tools]({POLICY}). When in doubt, ask before you paste.

`describe_columns()` is not built into R. To use it in the Workbench, copy its three lines from this notebook's setup cell into your own notebook.
""")

nb.finish([
    ("Choose the method yourself, before prompting", "The AI will run whatever you ask for"),
    ("Tell the AI each variable's type and values", "It needs them to write the right test"),
    ("Ask about anything in the output you did not request", "Defaults are choices too"),
    ("Exponentiate logistic regression coefficients", "They are log odds ratios"),
    ("Write your own interpretation first", "Then compare it with the AI's"),
    ("Ask what assumptions the method makes", "A result is only as good as its assumptions"),
    ("Code goes in; data never comes out", "The rule for real *All of Us* data"),
], f"""
You have finished Path B. You can now use an AI assistant to clean, combine, explore, and analyze a dataset in R, and you know how to check its work.

The next step is to do the same with real data in the *All of Us* Researcher Workbench. See the [workshop website]({SITE}) for how to get started there.
""", head=("Habit", "Why"), raw=True)
nb.write()
