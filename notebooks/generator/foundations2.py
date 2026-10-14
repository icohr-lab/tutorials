from nbkit import NB, link

PATIENTS = """
patients <- data.frame(
  Name = c("Josh", "Evelyn", "Olivia", "Liam", "Adrian", "Tamara", "Teddy", "Allison"),
  Age  = c(23, 18, 32, 56, 15, 25, 24, 16),
  City = c("Moscow", "Moscow", "Troy", "Viola", "Moscow", "Pullman", "Lewiston", "Moscow")
)
"""

# =====================================================================  F4
nb = NB("F4", [
    "Load a package",
    "Choose columns with `select()`",
    "Choose rows with `filter()`",
    "Chain steps together with the pipe, `%>%`",
], needs=link("F3"))

nb.md("""
## 1. Packages

R comes with many functions built in. **Packages** add more. The one used most for working with data is called **tidyverse**. A package has to be loaded with `library()` every time you open the notebook, and again if Colab disconnects and reconnects.

Run the cell below. It prints several lines, including something about "Conflicts". **That is normal and not an error.**
""")
nb.code("library(tidyverse)")
nb.md("Now recreate the small `patients` table from the last notebook.")
nb.code(PATIENTS.strip() + "\npatients")

nb.md("""
## 2. Choosing columns: `select()`

`select()` keeps only the columns you name. The first thing inside the parentheses is the dataframe; after that come the columns you want.
""")
nb.code("select(patients, Name, Age)")

nb.md("""
## 3. The pipe: "and then"

There is a second way to write the same thing, using the symbol `%>%`, called the **pipe**. Read it as "and then".
""")
nb.code("patients %>% select(Name, Age)")
nb.md("""
Read this as: take `patients`, **and then** select Name and Age. The pipe passes whatever is on its left into the function on its right.

For one step, the pipe makes little difference. It becomes very useful when you have several steps in a row, because the code reads top to bottom like a recipe. You will use it from here on.

(You may also see `|>` in other people's code. It is another way of writing the pipe.)
""")
nb.turn("Use the pipe and `select()` to show only the `Name` and `City` columns of `patients`.",
        solution="patients %>% select(Name, City)", expected="8 rows and 2 columns")

nb.md("""
## 4. Choosing rows: `filter()`

`filter()` keeps only the rows that pass a test. The tests are the comparisons you learned in notebook F2.
""")
nb.code("patients %>% filter(Age >= 21)")
nb.code('patients %>% filter(City == "Moscow")')
nb.md("""
Remember: text needs quotation marks and must match exactly, including capital letters. `"moscow"` would match nothing, and R would **not** give an error; it would just return zero rows.

### Keeping the result

`filter()` does not change `patients`. It gives you a new, smaller table. To keep that table, store it under a name. Then you can use it like any other dataframe.
""")
nb.code("""
adults <- patients %>% filter(Age >= 18)
nrow(adults)
""")
nb.turn("""
Create a table called `minors` containing the patients who are younger than 18. Show the table, then use `nrow()` to count its rows.
""", solution="""
minors <- patients %>% filter(Age < 18)
minors
nrow(minors)
""", expected="2 rows: Adrian and Allison")

nb.md("""
## 5. Two tests at once

Use `&` when **both** tests must be true ("and"). Use `|` when **either** one is enough ("or"). On a US keyboard, `|` is typed with Shift and the backslash key.
""")
nb.md("**Predict first:** which patients are 21 or older **and** live in Moscow? Decide, then run it.")
nb.code('patients %>% filter(Age >= 21 & City == "Moscow")')
nb.md("**Predict first:** which patients are 30 or older **or** live in Moscow?")
nb.code('patients %>% filter(Age >= 30 | City == "Moscow")')
nb.md("""
With `&`, only Josh passes both tests. With `|`, six patients pass at least one: the four who live in Moscow, plus Olivia and Liam, who are 30 or older.
""")
nb.turn("""
Create a table called `young_moscow` containing the patients who are **younger than 21 and live in Moscow**. Show the table.
""", solution="""
young_moscow <- patients %>% filter(Age < 21 & City == "Moscow")
young_moscow
""", expected="3 rows: Evelyn, Adrian, and Allison")

nb.md("""
## 6. Counting: `count()`

`count()` counts the rows for each value in a column. It does the same job as `table()`, but it gives its answer as a dataframe, and it includes a row for missing values if there are any.
""")
nb.code("patients %>% count(City)")

nb.md("""
## 7. Several steps in a row

Here is where the pipe pays off. Each line does one thing, and you can read the steps in order: take patients, **and then** keep the people aged 21 or older, **and then** keep two columns.

When a pipeline continues on the next line, the `%>%` goes at the **end** of the line.
""")
nb.code("""
patients %>%
  filter(Age >= 21) %>%
  select(Name, City)
""")
nb.turn("""
Write a pipeline with two steps: keep the patients who live in Moscow, and then show only their `Name` and `Age`.
""", solution="""
patients %>%
  filter(City == "Moscow") %>%
  select(Name, Age)
""", expected="4 rows: Josh (23), Evelyn (18), Adrian (15), Allison (16)")

nb.finish([
    ("library(tidyverse)", "Load the tidyverse package (every time you open the notebook)"),
    ("df %>% ...", 'The pipe: "take df, and then..."'),
    ("select(Name, Age)", "Keep these columns"),
    ("filter(Age >= 21)", "Keep rows that pass the test"),
    ("filter(a & b)", "Keep rows where both tests are true"),
    ("filter(a \\| b)", "Keep rows where either test is true"),
    ("count(City)", "Count rows for each value"),
], f"Continue with {link('F5')}.")
nb.write()

# =====================================================================  F5
nb = NB("F5", [
    "Create new columns with `mutate()`",
    "Give a column one value or another with `if_else()`",
    "Read a data file into R",
    "Explore a dataset you have not seen before",
], needs=link("F4"))

nb.md("""
## 1. Setup

Run the setup cell. The lines printed by `library(tidyverse)` are normal.
""")
nb.code("library(tidyverse)\n\n" + PATIENTS.strip() + "\npatients")

nb.md("""
## 2. Creating new columns: `mutate()`

`mutate()` adds a column. On the left of the `=` is the new column's name; on the right is how to calculate it.
""")
nb.code("patients %>% mutate(Age_months = Age * 12)")
nb.md("A new column can hold `TRUE`/`FALSE` values, using the comparisons from notebook F2:")
nb.code("patients %>% mutate(Adult = Age >= 18)")

nb.md("""
## 3. `if_else()`: one value if true, another if false

Often you want labels rather than `TRUE` and `FALSE`. `if_else()` takes three things, separated by commas: a test, the value to use when the test is true, and the value to use when it is false.
""")
nb.code("""
patients %>% mutate(Age_group = if_else(Age >= 18, "Adult", "Minor"))
""")

nb.md("""
## 4. Keeping the new column

Look at `patients` again:
""")
nb.code("patients")
nb.md("""
The new columns are gone. Like `filter()`, `mutate()` does not change the original table; it shows you a changed copy. To keep a new column, store the result. If you store it under the same name, the table is replaced by the version with the new column.
""")
nb.code("""
patients <- patients %>% mutate(Age_group = if_else(Age >= 18, "Adult", "Minor"))
patients
""")
nb.md("Now the column is part of `patients`, and you can use it in later steps.")
nb.code("patients %>% count(Age_group)")
nb.turn("""
Add a column called `Local` to `patients` that says `"Yes"` if the patient lives in Moscow and `"No"` otherwise. Store the result back in `patients`, then use `count()` to count the Yes and No values.
""", solution="""
patients <- patients %>% mutate(Local = if_else(City == "Moscow", "Yes", "No"))
patients %>% count(Local)
""", expected="4 No, 4 Yes")

nb.md("""
## 5. Reading a data file

Research data usually arrives as a **CSV file**: a plain-text table that any program can open. `read_csv()` reads one into a dataframe. Normally you give it a file name. Here the file is on the web, so you give it a web address.

This file holds demographic information for 100 people. **The data are simulated: randomly generated and completely fake**, but laid out like data from the *All of Us* Research Program.

`read_csv()` prints a message describing the columns it found. That is normal.
""")
nb.code("""
person_df <- read_csv("RAW_demographic_data.csv")
""")
nb.md("""
## 6. Explore it

You have never seen this table. Use what you know to find out what is in it.
""")
nb.code("dim(person_df)")
nb.code("head(person_df)")
nb.md("""
100 rows and four columns: an ID number, year of birth, race, and sex at birth. (Colab may call this table a "tibble". That is the tidyverse's name for a dataframe; treat it as the same thing.)

Is there one row per person? Use the check from notebook F3.
""")
nb.code("""
nrow(person_df)
length(unique(person_df$person_id))
""")
nb.md("100 rows and 100 different IDs, so each person appears once. Now look at a column of categories.")
nb.code("person_df %>% count(sex_at_birth)")
nb.md("""
Besides "Female" and "Male", there are a few other answers, including "Skip" for people who skipped the question. Survey data looks like this, and you will learn to tidy it up later.

Here is one more worked example before your turn. How many people were born in 2000 or later?
""")
nb.code("""
born_2000_or_later <- person_df %>% filter(year_of_birth >= 2000)
nrow(born_2000_or_later)
""")
nb.md("Now it is your turn. Everything you need is in this notebook and the last one.")
nb.turn("How many people were born before 1960? Use `filter()` and store the result in `born_before_1960`, then use `nrow()`.",
        solution="""
born_before_1960 <- person_df %>% filter(year_of_birth < 1960)
nrow(born_before_1960)
""", expected="29")
nb.turn("Use `count()` to see how many people are in each `race` category. How many categories are there?",
        solution="person_df %>% count(race)", expected="7 categories; the largest is White with 38")
nb.turn("""
Add a column called `age` to `person_df`, calculated as 2026 minus `year_of_birth`. Store the result back in `person_df`. Then find the mean age, using `$`.
""", solution="""
person_df <- person_df %>% mutate(age = 2026 - year_of_birth)
mean(person_df$age)
""", expected="52.91")
nb.turn("""
A harder one, combining two tests. How many people are **female and were born in 1990 or later**? Store the filtered table in `young_women`, then count its rows.
""", solution="""
young_women <- person_df %>% filter(sex_at_birth == "Female" & year_of_birth >= 1990)
nrow(young_women)
""", expected="13")

nb.finish([
    ("mutate(new = ...)", "Add a column"),
    ('if_else(test, "yes", "no")', "One value if the test is true, another if false"),
    ("df <- df %>% mutate(...)", "Keep the new column by storing the result"),
    ('read_csv("file.csv")', "Read a CSV file into a dataframe"),
    ("dim(df)   head(df)", "First look at a new table"),
    ("df %>% count(x)", "See the categories in a column"),
], f"Continue with {link('F6')}.")
nb.write()

# =====================================================================  F6
nb = NB("F6", [
    "Combine two tables that share a column",
    "Tell an inner join from a left join",
    "Deal with the missing values a join creates",
    "Check a join for accidentally duplicated rows",
], needs=link("F5"))

nb.md("""
## 1. Why combine tables?

Health record data does not come as one big table. Demographics are in one table, diagnoses in another, prescriptions in a third. To study whether a drug is related to a disease, you need to bring them together. Combining tables is called a **join**.

Run the setup cell. (The lines printed by `library(tidyverse)` are normal.)
""")
nb.code("library(tidyverse)\n\n" + PATIENTS.strip() + "\npatients")
nb.md("Here is a second table. It has BMI measurements, but only for four of the eight patients.")
nb.code("""
bmi <- data.frame(
  Name = c("Evelyn", "Liam", "Olivia", "Tamara"),
  BMI  = c(20.2, 27.9, 32.1, 21.6)
)
bmi
""")
nb.md("""
Both tables have a `Name` column. That shared column is what lets R match the rows: Evelyn's row in one table belongs with Evelyn's row in the other. The shared column is called the **key**.

## 2. Inner join: only the matches

`inner_join()` keeps only the people who appear in **both** tables. `by = "Name"` says which column to match on. Here, unlike in `select()` and `filter()`, the column name goes in quotation marks.
""")
nb.code('inner_join(patients, bmi, by = "Name")')
nb.md("""
Four rows: the four people who have a BMI. Josh, Adrian, Teddy, and Allison have disappeared. An inner join can silently drop people, so use it only when that is what you want.

## 3. Left join: keep everyone in the first table

`left_join()` keeps **every row of the first (left) table** and adds information from the second table where there is a match.

**Predict first:** how many rows will the result have? What will be in the BMI column for Josh?
""")
nb.code('left_join(patients, bmi, by = "Name")')
nb.md("""
All eight patients are still there. Where there was no BMI to add, R put `NA`: missing.

In research you usually start from your list of participants and add information to it, so `left_join()` is the join you will use most.

With the pipe, the same join is written like this. Read it as: take `patients`, and then left-join `bmi` onto it.
""")
nb.code("""
patients_bmi <- patients %>% left_join(bmi, by = "Name")
patients_bmi
""")

nb.md("""
## 4. Joins create missing values

The join gave you four `NA` values, and from notebook F2 you know what they do to a calculation:
""")
nb.code("mean(patients_bmi$BMI)")
nb.code("mean(patients_bmi$BMI, na.rm = TRUE)")
nb.md("""
Before analyzing a joined table, find out how much is missing. `is.na()` works on a whole table as well as on a vector, and `colSums()` adds up each column. Together they count the missing values in every column at once.
""")
nb.code("colSums(is.na(patients_bmi))")
nb.md("To look at the rows where a value is missing, put `is.na()` inside `filter()`:")
nb.code("patients_bmi %>% filter(is.na(BMI))")
nb.md("To remove those rows, use `drop_na()`. Do this only when you have decided those people should not be in your analysis.")
nb.code("patients_bmi %>% drop_na(BMI)")
nb.turn("""
Using `patients_bmi`, add a column called `Overweight` that says `"Yes"` if BMI is greater than 25 and `"No"` otherwise. Look at the result. What happened to the people with no BMI?
""", solution="""
patients_bmi %>% mutate(Overweight = if_else(BMI > 25, "Yes", "No"))
""", expected="Olivia and Liam are Yes; Evelyn and Tamara are No; the other four are NA",
        note="R cannot say whether an unknown BMI is greater than 25, so the answer is also unknown: `NA`. Missing values carry through into anything calculated from them.")

nb.md("""
## 5. The trap: a join can multiply rows

So far, each person appeared once in each table. Now look at a table of clinic visits, where a person can have several rows.
""")
nb.code("""
visits <- data.frame(
  Name       = c("Josh", "Josh", "Evelyn", "Liam", "Liam", "Liam"),
  Visit_year = c(2019, 2021, 2020, 2018, 2019, 2022)
)
visits
""")
nb.md("**Predict first:** `patients` has 8 rows. How many rows will this join produce?")
nb.code("""
patients_visits <- patients %>% left_join(visits, by = "Name")
patients_visits
""")
nb.code("nrow(patients_visits)")
nb.md("""
Eleven rows, from a table of eight patients. Josh now appears twice and Liam three times, once for each visit. (The five patients with no visits have `NA`, as before.) Nothing is wrong with the join; it did what it was asked. But if you now counted rows to find out how many patients you have, or calculated the mean age, Josh and Liam would be counted more than once.

**This is the most common silent mistake when working with health record data.** No error message appears. The protection is a habit:

> **After every join, compare the number of rows with the number of different people.**
""")
nb.code("""
nrow(patients_visits)                  # rows
n_distinct(patients_visits$Name)       # different people
""")
nb.md("`n_distinct()` is a shorter way of writing `length(unique(...))`. When the two numbers differ, some people appear more than once.")

nb.md("""
## 6. The same thing with a larger dataset

Now load two of the simulated research tables: the 100 people from the last notebook, and their diagnosis records.
""")
nb.code("""
person_df <- read_csv("RAW_demographic_data.csv")
condition_df <- read_csv("RAW_conditions.csv")
""")
nb.code("head(condition_df)")
nb.md("""
Each row of `condition_df` is one diagnosis record: who (`person_id`), what (`condition_source_value`), and when (`condition_start_date`). Because the data are simulated, some dates are in the future. Here, `person_id` is the key that links the two tables.

Do some people have more than one record?
""")
nb.code("""
nrow(condition_df)                     # diagnosis records
n_distinct(condition_df$person_id)     # different people with a diagnosis
""")
nb.md("96 records, but only 30 different people. So joining this table to `person_df` will multiply rows:")
nb.code("""
joined <- person_df %>% left_join(condition_df, by = "person_id")
nrow(joined)
n_distinct(joined$person_id)
""")
nb.md("""
166 rows for 100 people. To get a table with one row per person, you first have to reduce `condition_df` to one row per person, for example by keeping each person's earliest diagnosis. You will do that early in the next part of the course.
""")
nb.turn("""
Read the prescription records into a dataframe called `drug_df` from this address:

`RAW_drug_exposures.csv`

Find how many records it has and how many different people. Then start from `person_df` and left-join `drug_df` onto it, as was done with `condition_df` above. How many rows does the result have?
""", solution="""
drug_df <- read_csv("RAW_drug_exposures.csv")
nrow(drug_df)
n_distinct(drug_df$person_id)

joined_drug <- person_df %>% left_join(drug_df, by = "person_id")
nrow(joined_drug)
""", expected="267 records for 35 different people; the join has 332 rows")

nb.finish([
    ('inner_join(a, b, by = "key")', "Keep only rows that match in both tables"),
    ('left_join(a, b, by = "key")', "Keep every row of `a`; add columns from `b` where they match"),
    ('a %>% left_join(b, by = "key")', "The same left join, written with the pipe"),
    ("colSums(is.na(df))", "Count missing values in every column"),
    ("filter(is.na(BMI))", "Show the rows where BMI is missing"),
    ("drop_na(BMI)", "Remove the rows where BMI is missing"),
    ("n_distinct(df$person_id)", "Number of different people"),
], f"""
You have finished the Foundations. From here the course continues on one of two paths. Your instructor will tell you which one to follow.

- **Path A: Write It Yourself.** You write the code. Start with {link('A1')}.
- **Path B: AI-Assisted.** You describe what you want to an AI assistant, then read and check the code it writes. Start with {link('B1')}.
""")
nb.write()
