# R Practice Notebooks

A self-paced introduction to R for students with no programming experience, using simulated data laid out like *All of Us* Research Program data. Each notebook opens in Google Colab with the R runtime already selected and takes roughly 20 to 40 minutes.

Everyone starts with the Foundations, then follows one of two paths.

## Foundations

| Notebook | Covers |
|---|---|
| [F1: First Steps in R](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/F1_First_Steps.ipynb) | Running code, arithmetic, variables, functions, reading error messages |
| [F2: Vectors and Data Types](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/F2_Vectors_and_Data_Types.ipynb) | Vectors, numbers vs. text, TRUE/FALSE, dates, missing values |
| [F3: Dataframes](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/F3_Dataframes.ipynb) | Building and inspecting a table; one row per person or many |
| [F4: Choosing Rows and Columns](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/F4_Choosing_Rows_and_Columns.ipynb) | Packages, `select()`, `filter()`, the pipe |
| [F5: New Columns and Data Files](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/F5_New_Columns_and_Data_Files.ipynb) | `mutate()`, `if_else()`, reading a CSV file, exploring a new dataset |
| [F6: Combining Tables](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/F6_Combining_Tables.ipynb) | Inner and left joins, missing values from joins, duplicated rows |

## Path A: Write It Yourself

Students write the code.

| Notebook | Covers |
|---|---|
| [A1: Cleaning Real Data](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/A1_Cleaning_Real_Data.ipynb) | Recoding categories with `if_else()` and `case_when()` |
| [A2: One Row per Person](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/A2_One_Row_per_Person.ipynb) | Earliest record per person, merging three tables, long to wide |
| [A3: Dates and New Variables](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/A3_Dates_and_New_Variables.ipynb) | Date logic, exposure before diagnosis, analysis variables, saving |
| [A4: Exploring and Plotting](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/A4_Exploring_and_Plotting.ipynb) | Group summaries, histogram, box plot, scatter plot |
| [A5: Statistical Tests](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/A5_Statistical_Tests.ipynb) | t-test, ANOVA, chi-square, Fisher's exact test |
| [A6: Regression](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/A6_Regression.ipynb) | Linear and logistic regression, odds ratios |

## Path B: AI-Assisted

Students describe what they want to an AI chat assistant, then read and check the code it returns.

| Notebook | Covers |
|---|---|
| [B1: Your First Prompts](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/B1_First_Prompts.ipynb) | The describe-generate-read-run-check loop; what may be shared with an AI tool |
| [B2: Building a Dataset with AI](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/B2_Building_a_Dataset_with_AI.ipynb) | Prompting for one row per person, merging, date logic; test cases |
| [B3: Exploring and Plotting with AI](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/B3_Exploring_and_Plotting_with_AI.ipynb) | Summaries and plots by prompt; checking a plot against numbers |
| [B4: Catching Mistakes](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/B4_Catching_Mistakes.ipynb) | Debugging errors with AI; four mistakes that run without an error |
| [B5: Statistics with AI](https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/B5_Statistics_with_AI.ipynb) | Choosing the test, reading output, odds ratios, moving to the Workbench |

## For students

1. Click a notebook link above.
2. Sign in with a Google account.
3. Choose **File > Save a copy in Drive** and work in your copy.

## Notes for instructors

- The links above, and the "Next" links inside the notebooks, assume the files are in a folder called `notebooks` on the `main` branch of this repository.
- The data are read from the `data` folder of this repository. No real participant data are used.
- Every exercise has a solution at the end of its notebook.
- Some cells fail on purpose (in F1, F2, and B4), and in A2, A3, and B2 a few cells depend on an exercise being completed first. **Runtime > Run all** therefore stops partway in those notebooks.
- Path B asks students to use an AI chat tool in a separate window. Tell them which tool to use.
