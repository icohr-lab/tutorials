from nbkit import NB, link

# =====================================================================  F1
nb = NB("F1", [
    "Run code in a notebook",
    "Use R as a calculator",
    "Store values in variables",
    "Use functions",
    "Read an error message without panicking",
])

nb.md("""
## 1. What is this page?

This is a **notebook**. It is made of two kinds of cells:

- **Text cells**, like this one, which explain things.
- **Code cells**, with a grey background, which contain R code that you can run.

When you run a code cell, the result appears directly underneath it. The first cell you run takes a few seconds, because Colab has to connect to a computer that runs R for you.

Run the cell below: click the play button on its left, or click inside it and press **Shift + Enter**.
""")
nb.code("1 + 1")
nb.md("You should see `2` appear underneath. That is all running code is: you give R an instruction, and R gives back a result.")

nb.md("""
## 2. R as a calculator

R can do arithmetic. Run each cell and check the answer is what you expect.
""")
nb.code("100 / 4")
nb.code("(120 + 80) / 2")
nb.code("3 * 5")
nb.code("2^3   # 2 to the power of 3")
nb.md("""
| Symbol | Meaning |
|---|---|
| `+` | add |
| `-` | subtract |
| `*` | multiply |
| `/` | divide |
| `^` | to the power of |
| `( )` | do this part first |

R follows the usual order of arithmetic: powers first, then multiplication and division, then addition and subtraction. Use parentheses when you want a different order.

You can change the numbers in any cell and run it again. Nothing breaks if you experiment.
""")
nb.turn("""
Body mass index (BMI) is weight in kilograms divided by the square of height in meters. Calculate the BMI of a person who weighs 70 kg and is 1.75 m tall. (R squares the height first, because powers come before division.)
""", solution="70 / 1.75^2", expected="22.85714")

nb.md("""
## 3. Comments

Anything after a `#` on a line is a **comment**. R ignores it. Comments are notes for humans: for other people, and for yourself next month.
""")
nb.code("""
# This whole line is a comment. R skips it.
70 / 1.75^2   # BMI for a 70 kg, 1.75 m person
""")

nb.md("""
## 4. Variables: giving a value a name

Typing the same numbers over and over is tedious and error-prone. Instead, you can store a value under a name. The name is called a **variable**.

The arrow `<-` means "store the value on the right under the name on the left".
""")
nb.code("weight_kg <- 70")
nb.md("Nothing appeared, and that is normal. R stored the value quietly. To see what is stored, run the name by itself:")
nb.code("weight_kg")
nb.md("Now you can use the name anywhere you would use the number.")
nb.code("""
height_m <- 1.75
bmi <- weight_kg / height_m^2
bmi
""")
nb.md("""
Two rules for names:

- **Names cannot contain spaces.** Use an underscore instead: `weight_kg`, not `weight kg`.
- **Capital letters matter.** `bmi`, `Bmi`, and `BMI` are three different names.

### A variable keeps its value until you change it

Storing a new value under an existing name replaces the old value.
""")
nb.code("""
weight_kg <- 85
weight_kg
""")
nb.md("**Predict first:** the weight is now 85. What is `bmi` now? Decide, then run the cell.")
nb.code("bmi")
nb.md("""
Still 22.85714. R calculated `bmi` once, earlier, using the weight at that time, and stored the result. It does not go back and update it. To get the new BMI, you have to run the calculation again:
""")
nb.code("""
bmi <- weight_kg / height_m^2
bmi
""")
nb.md("""
This is the most important thing to understand about notebooks: **cells take effect in the order you run them, not the order they appear on the page.** If a result looks wrong, a likely reason is that an earlier cell was changed but not run again.

Now put the weight back to 70 for the rest of the notebook.
""")
nb.code("""
weight_kg <- 70
bmi <- weight_kg / height_m^2
bmi
""")
nb.turn("""
Pulse pressure is systolic blood pressure minus diastolic blood pressure. Store 128 in a variable called `systolic` and 82 in a variable called `diastolic`. Then calculate the pulse pressure and store it in `pulse_pressure`. Finally, show its value.
""", solution="""
systolic <- 128
diastolic <- 82
pulse_pressure <- systolic - diastolic
pulse_pressure
""", expected="46")

nb.md("""
## 5. Functions: asking R to do something

A **function** is a named action. You write its name, then parentheses, and put what it should work on inside the parentheses.
""")
nb.code("sqrt(16)   # square root")
nb.code("round(22.85714)   # round to a whole number")
nb.md("""
The things inside the parentheses are called **arguments**. Many functions take more than one, separated by commas. The second argument of `round()` says how many decimal places to keep.
""")
nb.code("round(22.85714, 1)")
nb.md("You can also write the argument's name. This does exactly the same thing and is easier to read:")
nb.code("round(22.85714, digits = 1)")
nb.md("Functions work on variables too, and the result of a function can be stored in a variable.")
nb.code("""
bmi_rounded <- round(bmi, digits = 1)
bmi_rounded
""")
nb.turn("Use `round()` to show `pulse_pressure / 3` with 2 decimal places.",
        solution="round(pulse_pressure / 3, digits = 2)", expected="15.33")

nb.md("""
## 6. Text values

Values do not have to be numbers. Text goes inside quotation marks.
""")
nb.code("""
city <- "Moscow"
city
""")
nb.code("toupper(city)   # a function that works on text")
nb.md("""
The quotation marks matter. With quotes, `"Moscow"` is a piece of text. Without quotes, `Moscow` is a variable name, and R will go looking for a variable called `Moscow`.
""")

nb.md("""
## 7. Errors are normal

Everyone who writes code sees error messages many times a day. An error does not mean you broke anything. It means R could not follow an instruction, and it is telling you why.

The next three cells are **meant to fail**. Run each one and read the message.

**Error 1: a name R does not know.** We created `weight_kg`. Here it is typed with a capital W.
""")
nb.code("Weight_kg", error=True)
nb.md("""
`object 'Weight_kg' not found` means R has no variable with exactly that name. The usual causes are a typo, a wrong capital letter, or not having run the cell that creates the variable.

**Error 2: a function R does not know.**
""")
nb.code("rond(bmi)", error=True)
nb.md("""
`could not find function "rond"` means the function name is misspelled (it should be `round`), or it belongs to a package that has not been loaded yet. You will meet packages in notebook F4.

**Error 3: something left unfinished.**
""")
nb.code("round(bmi, 1", error=True)
nb.md("""
The closing parenthesis is missing. Messages that mention `unexpected` usually mean a missing or extra parenthesis, comma, or quotation mark.

### When you get an error

1. Read the message. The key words are usually `not found`, `could not find function`, or `unexpected`.
2. Check spelling and capital letters.
3. Check that every `(` has a `)` and every `"` has a partner.
4. Check that you ran the earlier cells. After a break, Colab may have disconnected and forgotten your variables. Run the cells again from the top.

> **Still stuck?** An AI assistant is good at explaining error messages. Paste the code and the error message and ask what it means. One rule for later, when you work with real research data: never paste the data itself into an AI tool.

A **warning** is different from an error. A warning means the code ran, but R wants you to double-check something. Do not ignore warnings; read them.
""")
nb.turn("""
Each of these three lines has one mistake. Type a corrected version of each into the cell below and run it.

```r
Round(3.14159, 2)
sqrt(81
toupper(Boise)
```
""", solution="""
round(3.14159, 2)
sqrt(81)
toupper("Boise")
""", expected='3.14, then 9, then "BOISE"',
        note="`Round` needs a lowercase r. `sqrt(81` is missing its closing parenthesis. `Boise` needs quotation marks, because it is text and not a variable.")

nb.finish([
    ("+  -  *  /  ^", "Arithmetic"),
    ("# note", "Comment; R ignores it"),
    ("x <- 5", "Store the value 5 under the name `x`"),
    ("x", "Show what is stored in `x`"),
    ("sqrt(x)", "Square root"),
    ("round(x, digits = 1)", "Round to 1 decimal place"),
    ('"text"', "A text value"),
], f"""
Continue with {link('F2')}.
""")
nb.write()

# =====================================================================  F2
nb = NB("F2", [
    "Store many values together in a vector",
    "Summarize a vector with functions such as `mean()`",
    "Tell numbers, text, and TRUE/FALSE values apart, and see why it matters",
    "Recognize and handle missing values (`NA`)",
], needs=link("F1"))

nb.md("""
## 1. Vectors: many values under one name

In research you rarely have one number. You have a column of them: the ages of all your patients, or all their blood pressures. In R, a sequence of values is called a **vector**. You create one with the function `c()`, which stands for "combine".

Here are the ages of eight patients.
""")
nb.code("""
ages <- c(23, 18, 32, 56, 15, 25, 24, 16)
ages
""")
nb.md("Functions can work on the whole vector at once.")
nb.code("length(ages)   # how many values")
nb.code("mean(ages)     # average")
nb.code("max(ages)      # largest value")
nb.md("Other useful ones: `min()`, `median()`, `sum()`, and `sd()` for standard deviation.")
nb.turn("""
Five patients have these systolic blood pressures: 118, 135, 122, 141, 109. Store them in a vector called `sbp`. Then find the mean and the highest value.
""", solution="""
sbp <- c(118, 135, 122, 141, 109)
mean(sbp)
max(sbp)
""", expected="mean 125, highest 141")

nb.md("""
## 2. Picking out values

Square brackets pick values by position. The first value is position 1.
""")
nb.code("ages[2]     # the second value")
nb.md("`1:3` is a short way of writing the whole numbers from 1 to 3.")
nb.code("ages[1:3]   # the first three values")

nb.md("""
## 3. Arithmetic on a whole vector

Arithmetic is applied to every value in the vector.
""")
nb.code("ages * 12   # each age in months")
nb.code("""
heights_cm <- c(170, 162, 181, 175)
heights_m <- heights_cm / 100
heights_m
""")

nb.md("""
## 4. Text vectors

A vector can hold text instead of numbers. Each value needs its own quotation marks.
""")
nb.code("""
patient_names <- c("Josh", "Evelyn", "Olivia", "Liam", "Adrian", "Tamara", "Teddy", "Allison")
cities <- c("Moscow", "Moscow", "Troy", "Viola", "Moscow", "Pullman", "Lewiston", "Moscow")
cities
""")
nb.md("Two functions are especially useful for text: `unique()` lists the distinct values, and `table()` counts how often each one appears.")
nb.code("unique(cities)")
nb.code("table(cities)")

nb.md("""
## 5. Data types

Every value in R has a **type**. The function `class()` tells you what it is.
""")
nb.code("class(ages)")
nb.code("class(cities)")
nb.md("""
`numeric` means numbers. `character` means text. This matters because R can only do arithmetic on numbers.

The next cell is **meant to fail**. The value `"70"` has quotation marks, so R treats it as text, even though it looks like a number.
""")
nb.code('"70" + 5', error=True)
nb.md("""
`non-numeric argument` means you tried to do arithmetic on something that is not a number. This happens often with real data, when a column that looks numeric was read in as text.

You can convert text to a number with `as.numeric()`:
""")
nb.code('as.numeric("70") + 5')
nb.md("""
**A vector holds only one type.** If you mix numbers and text, R quietly turns everything into text. Look at what happens when a lab value is recorded as a word:
""")
nb.code("""
lab_values <- c(5.1, 4.8, "pending", 5.6)
lab_values
class(lab_values)
""")
nb.md("Every value now has quotation marks. One text entry turned the whole vector into text. Now try to take the mean:")
nb.code("mean(lab_values)")
nb.md("""
The result is `NA`, with a **warning**: `argument is not numeric or logical`. This is what a warning looks like. The code ran, but R is telling you the result is not what you probably wanted. When a calculation gives a strange result, `class()` is one of the first things to check.
""")
nb.turn("""
A colleague sends you three weights that were typed in as text: "70", "82.5", and "64". Store them in a vector called `weights_text`, exactly as given, with the quotation marks. Use `class()` to confirm they are text. Then convert them with `as.numeric()` and find the mean.
""", solution='''
weights_text <- c("70", "82.5", "64")
class(weights_text)
mean(as.numeric(weights_text))
''', expected='"character", then a mean of 72.16667')

nb.md("""
## 6. TRUE and FALSE

You can ask R a yes-or-no question about every value in a vector. The answer is a vector of `TRUE` and `FALSE` values, called **logical** values.
""")
nb.code("ages >= 18   # is each patient 18 or older?")
nb.code('cities == "Moscow"   # does each patient live in Moscow?')
nb.md("""
| Symbol | Meaning |
|---|---|
| `==` | equal to (two equals signs) |
| `!=` | not equal to |
| `>`  `<` | greater than, less than |
| `>=`  `<=` | greater than or equal to, less than or equal to |

Note the **double** equals sign for "is equal to". A single `=` does a different job: it names an argument inside a function, as in `round(x, digits = 1)`.

A useful trick: R counts `TRUE` as 1 and `FALSE` as 0. So `sum()` of a logical vector counts how many are `TRUE`.
""")
nb.code("sum(ages >= 18)   # how many patients are 18 or older?")
nb.turn("How many of the eight patients live in Moscow? How many are younger than 21? Use `sum()` for each.",
        solution='sum(cities == "Moscow")\nsum(ages < 21)', expected="4 live in Moscow; 3 are younger than 21")

nb.md("""
## 7. Dates

Dates are a type of their own. You will use them later to work out which came first, a prescription or a diagnosis. `as.Date()` turns text written as year-month-day into a real date, and R can then do arithmetic with it.
""")
nb.code("""
diagnosis_date <- as.Date("2024-10-31")
first_visit <- as.Date("2024-01-15")
class(diagnosis_date)
diagnosis_date - first_visit   # number of days between them
""")

nb.turn("""
A patient was admitted on 2025-03-01 and discharged on 2025-12-25. Use `as.Date()` and subtraction to find how many days that is.
""", solution='as.Date("2025-12-25") - as.Date("2025-03-01")', expected="299 days")

nb.md("""
## 8. Missing values

Real data always has gaps: a measurement that was not taken, a question left blank. R marks a missing value as `NA`, which stands for "not available". `NA` has no quotation marks. It is not text and it is not zero. It means "we do not know".

Here are BMI values for six patients. Two were never measured.
""")
nb.code("""
bmi_values <- c(20.2, NA, 32.1, 27.9, NA, 21.6)
mean(bmi_values)
""")
nb.md("""
The answer is `NA`. R is being careful: if two values are unknown, the average of all six is unknown too.

To calculate the mean of the values you do have, tell R to remove the missing ones with `na.rm = TRUE` ("NA remove").
""")
nb.code("mean(bmi_values, na.rm = TRUE)")
nb.md("`is.na()` asks of each value, \"is this missing?\" Combined with `sum()`, it counts the missing values.")
nb.code("is.na(bmi_values)")
nb.code("sum(is.na(bmi_values))   # how many are missing?")
nb.md("""
> **A habit for all your research:** before calculating anything, find out how many values are missing. A mean based on 6 of 100 patients is very different from a mean based on 98 of 100.
""")
nb.turn("""
Six patients have these systolic blood pressures, two of them missing: 118, NA, 122, 141, NA, 109. Store them in a vector called `sbp_measured`. Count the missing values, then calculate the mean of the rest.
""", solution="""
sbp_measured <- c(118, NA, 122, 141, NA, 109)
sum(is.na(sbp_measured))
mean(sbp_measured, na.rm = TRUE)
""", expected="2 missing; mean 122.5")

nb.finish([
    ("c(1, 2, 3)", "Combine values into a vector"),
    ("length(x)", "How many values"),
    ("mean(x)  median(x)  min(x)  max(x)  sum(x)  sd(x)", "Summaries of a numeric vector"),
    ("x[2]", "The second value"),
    ("x[1:3]", "The first three values"),
    ("unique(x)", "The distinct values"),
    ("table(x)", "How often each value appears"),
    ("class(x)", "The type of data"),
    ("as.numeric(x)", "Convert to numbers"),
    ("x >= 18", "Compare every value; gives TRUE/FALSE"),
    ("sum(x >= 18)", "Count how many are TRUE"),
    ('as.Date("2024-10-31")', "Make a date"),
    ("mean(x, na.rm = TRUE)", "Mean, ignoring missing values"),
    ("sum(is.na(x))", "Count missing values"),
], f"Continue with {link('F3')}.")
nb.write()

# =====================================================================  F3
nb = NB("F3", [
    "Build a table of data, called a dataframe",
    "Inspect a dataframe: its size, its columns, and its first rows",
    "Pull out one column and summarize it",
    "Check whether a table has more than one row per person",
], needs=link("F2"))

nb.md("""
## 1. What is a dataframe?

A **dataframe** is a table, like a spreadsheet. Each **row** is one record (for example, one patient). Each **column** is one variable (for example, age). Nearly all the data you will analyze in R lives in dataframes.

A dataframe is built from vectors: each column is one vector. Run the cell below to recreate the vectors from the last notebook.
""")
nb.code("""
patient_names <- c("Josh", "Evelyn", "Olivia", "Liam", "Adrian", "Tamara", "Teddy", "Allison")
ages <- c(23, 18, 32, 56, 15, 25, 24, 16)
cities <- c("Moscow", "Moscow", "Troy", "Viola", "Moscow", "Pullman", "Lewiston", "Moscow")
""")
nb.md("The function `data.frame()` puts them side by side. On the left of each `=` is the column name you choose; on the right is the vector that fills it.")
nb.code("""
patients <- data.frame(Name = patient_names, Age = ages, City = cities)
patients
""")
nb.md("""
Eight rows, one per patient, and three columns. Colab may label the table with its size (8 × 3) and show each column's type in small print under its name: `<chr>` means character (text) and `<dbl>` means a number.

In practice you will rarely type a dataframe in by hand; you will read it from a file. This small one is useful for learning because you can see all of it at once.

## 2. Inspecting a dataframe

A real dataset may have thousands of rows, so you cannot just look at it. These functions tell you what you have.
""")
nb.code("dim(patients)   # number of rows, then number of columns")
nb.code("nrow(patients)  # number of rows")
nb.code("ncol(patients)  # number of columns")
nb.code("names(patients) # the column names")
nb.code("head(patients)  # the first 6 rows")
nb.md("`head()` shows 6 rows unless you ask for a different number. `tail()` does the same for the last rows.")
nb.code("head(patients, 3)")
nb.code("tail(patients, 2)")
nb.md("`str()` shows the **structure**: each column, its type, and its first few values.")
nb.code("str(patients)")
nb.md("""
How to read this: `8 obs. of 3 variables` means 8 observations (rows) and 3 variables (columns). Then there is one line per column, starting with a `$`: the column's name, its type (`chr` for text, `num` for a number), and its first few values.

`summary()` gives a quick summary of every column.
""")
nb.code("summary(patients)")
nb.md("For the numeric column you get the smallest value, the largest, the mean, the median, and the quartiles (`1st Qu.` and `3rd Qu.`: the values a quarter and three quarters of the way up). For text columns, `summary()` can only tell you how many values there are.")
nb.md("""
> **A habit:** every time you create or load a dataframe, look at it with `dim()` and `head()` before doing anything else.

## 3. One column at a time: the `$` sign

To work with a single column, write the dataframe's name, a dollar sign, and the column's name.
""")
nb.code("patients$Age")
nb.md("What you get back is a vector. So everything you learned about vectors in the last notebook works here.")
nb.code("mean(patients$Age)")
nb.code("table(patients$City)")
nb.code("sum(patients$Age >= 18)   # how many adults?")
nb.md("Column names are case-sensitive too. `patients$age` (lowercase a) does not exist, and R returns `NULL`, which means \"nothing\".")
nb.code("patients$age")
nb.turn("""
Using the `patients` dataframe and `$`:

1. Find the median age.
2. List the distinct cities with `unique()`.
3. Count how many patients are 21 or older.
""", solution="""
median(patients$Age)
unique(patients$City)
sum(patients$Age >= 21)
""", expected="median 23.5; five distinct cities; 5 patients are 21 or older")

nb.md("""
## 4. How many different values?

You can put one function inside another. R works from the inside out. Here, `unique()` first lists the distinct cities, and then `length()` counts them.
""")
nb.code("length(unique(patients$City))")

nb.md("""
## 5. One row per person, or many?

In the `patients` table, each person appears once. Health record data is often not like that. A table of clinic visits has one row per **visit**, so a person who came three times appears three times.

Here is a small visits table. The `person_id` column identifies the patient. Notice that the instruction is spread over several lines to make it easier to read. That is allowed: R keeps reading until the opening parenthesis has been closed.
""")
nb.code("""
visits <- data.frame(
  person_id  = c(1, 1, 2, 3, 3, 3),
  visit_year = c(2019, 2021, 2020, 2018, 2019, 2022)
)
visits
""")
nb.md("How many rows are there, and how many different people?")
nb.code("nrow(visits)                       # number of rows")
nb.code("length(unique(visits$person_id))   # number of different people")
nb.md("""
Six rows but only three people. **Whenever the number of rows is larger than the number of unique person IDs, some people appear more than once.** This check comes up constantly with health record data, and forgetting it leads to counting the same patient several times.

`table()` shows how many rows each person has.
""")
nb.code("table(visits$person_id)")
nb.turn("""
Make a dataframe called `prescriptions` with two columns:

- `person_id` containing 10, 10, 10, 11, 12, 12
- `drug` containing "A", "A", "B", "A", "B", "B"

Then find the number of rows and the number of different people.
""", solution="""
prescriptions <- data.frame(
  person_id = c(10, 10, 10, 11, 12, 12),
  drug      = c("A", "A", "B", "A", "B", "B")
)
nrow(prescriptions)
length(unique(prescriptions$person_id))
""", expected="6 rows, 3 different people")

nb.finish([
    ("data.frame(A = x, B = y)", "Build a dataframe from vectors"),
    ("dim(df)  nrow(df)  ncol(df)", "Size of the dataframe"),
    ("names(df)", "Column names"),
    ("head(df)  tail(df)", "First or last rows"),
    ("str(df)", "Columns, their types, and first values"),
    ("summary(df)", "Quick summary of every column"),
    ("df$Age", "One column, as a vector"),
    ("table(df$City)", "Count each value in a column"),
    ("length(unique(df$person_id))", "Number of different people"),
], f"Continue with {link('F4')}.")
nb.write()

