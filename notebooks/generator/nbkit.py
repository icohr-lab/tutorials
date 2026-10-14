"""Small toolkit for writing the notebook series and its R test scripts."""
import json
import os
import re

RAW = "https://raw.githubusercontent.com/icohr-lab/aou-workshop/refs/heads/main/data/"
SITE = "https://icohr-lab.github.io/aou-workshop/"  # the AoU workshop site (Workbench setup)
POLICY = "https://support.researchallofus.org/hc/en-us/articles/34814131370388"
COLAB = "https://colab.research.google.com/github/icohr-lab/tutorials/blob/main/notebooks/"
TUTORIALS = "https://icohr-lab.github.io/tutorials/"
# NHIS teaching file; NB_NHIS_DATA can point at a local folder (ending in /) to test before pushing
NHIS = os.environ.get("NB_NHIS_DATA", "https://raw.githubusercontent.com/icohr-lab/tutorials/refs/heads/main/data/nhis/")
CODEBOOK = "https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHIS/2025/adult-codebook.pdf"
HERE = os.path.dirname(os.path.abspath(__file__))
# Notebooks go to the folder above generator/ (notebooks/); test scripts to generator/tests/.
# Override with NB_OUT / NB_TEST, e.g. to build into a scratch folder and compare.
OUT = os.environ.get("NB_OUT", os.path.dirname(HERE))
TEST = os.environ.get("NB_TEST", os.path.join(HERE, "tests"))

FILES = {
    "F1": ("F1_First_Steps", "First Steps in R"),
    "F2": ("F2_Vectors_and_Data_Types", "Vectors and Data Types"),
    "F3": ("F3_Dataframes", "Dataframes"),
    "F4": ("F4_Choosing_Rows_and_Columns", "Choosing Rows and Columns"),
    "F5": ("F5_New_Columns_and_Data_Files", "New Columns and Data Files"),
    "F6": ("F6_Combining_Tables", "Combining Tables"),
    "A1": ("A1_Cleaning_Real_Data", "Cleaning Real Data"),
    "A2": ("A2_One_Row_per_Person", "One Row per Person"),
    "A3": ("A3_Dates_and_New_Variables", "Dates and New Variables"),
    "A4": ("A4_Exploring_and_Plotting", "Exploring and Plotting"),
    "A5": ("A5_Statistical_Tests", "Statistical Tests"),
    "A6": ("A6_Regression", "Regression"),
    "B1": ("B1_First_Prompts", "Your First Prompts"),
    "B2": ("B2_Building_a_Dataset_with_AI", "Building a Dataset with AI"),
    "B3": ("B3_Exploring_and_Plotting_with_AI", "Exploring and Plotting with AI"),
    "B4": ("B4_Catching_Mistakes", "Catching Mistakes"),
    "B5": ("B5_Statistics_with_AI", "Statistics with AI"),
    "N1": ("N1_Meet_the_NHIS", "Meet the NHIS"),
    "N2": ("N2_Preparing_Variables", "Preparing Variables"),
}
SERIES = {"F": ("Foundations", 6), "A": ("Path A: Write It Yourself", 6), "B": ("Path B: AI-Assisted", 5),
          "N": ("R for Survey Data", 7)}


def link(key):
    fname, title = FILES[key]
    return f"[{key}: {title}]({COLAB}{fname}.ipynb)"


def split_at_headings(text):
    """Split markdown so each heading starts a new chunk; ignores '#' lines inside ``` code blocks.
    A chunk holding only a '---' rule stays attached to the heading after it."""
    chunks, in_fence = [[]], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        is_heading = not in_fence and re.match(r"#{1,6} ", line)
        if is_heading and any(l.strip() not in ("", "---") for l in chunks[-1]):
            chunks.append([])
        chunks[-1].append(line)
    return [c for c in ("\n".join(lines).strip("\n") for lines in chunks) if c.strip()]


def sub(t):
    return (t.replace("NHIS_DATA_", NHIS).replace("RAW_", RAW).replace("SITE_", SITE)
            .replace("POLICY_", POLICY)).strip("\n")


class NB:
    def __init__(self, key, learn, needs=None, minutes="20 to 30"):
        self.key = key
        self.cells = []  # dict(kind, text, solution, error)
        self.solutions = []  # (label, code, note)
        self.n_ex = 0
        fname, title = FILES[key]
        series, total = SERIES[key[0]]
        num = int(key[1:])
        unit = "lesson" if key[0] == "N" else "notebook"  # the survey series mixes notebooks and RStudio lessons
        bullets = "\n".join(f"- {b}" for b in learn)
        need = f"\n\n**Before this notebook:** {needs}." if needs else ""
        self.md(f"""
# {key} · {title}

*{series}, {unit} {num} of {total} · about {minutes} minutes*

**In this notebook you will learn to:**

{bullets}{need}

> **Before you start:** click **File > Save a copy in Drive** and work in your copy. Run a code cell by clicking the play button to its left, or press **Shift + Enter**. Go in order from top to bottom.
""")

    # -- basic cells
    def md(self, text):
        # One heading per cell: Colab's table of contents only lists a cell's first heading
        for chunk in split_at_headings(sub(text)):
            self.cells.append(dict(kind="markdown", text=chunk, solution=None, error=False))

    def code(self, text, error=False, solution=None):
        self.cells.append(dict(kind="code", text=sub(text), solution=sub(solution) if solution else None, error=error))

    # -- exercises
    def turn(self, prompt, solution=None, expected=None, note=None, starter="# Your code here\n"):
        """A 'Your turn' exercise: prompt, empty code cell, optional expected result."""
        self.n_ex += 1
        label = f"Your turn {self.n_ex}"
        exp = f"\n\n*Expected result: {expected}*" if expected else ""
        self.md(f"**{label}.** {prompt.strip()}{exp}")
        self.code(starter, solution=solution)
        if solution or note:
            self.solutions.append((label, sub(solution) if solution else None, note))
        return label

    def answer(self, label, note=None, solution=None):
        """Register an answer for the Solutions section without creating an exercise cell."""
        self.solutions.append((label, sub(solution) if solution else None, note))

    def finish(self, recap, next_md, head=("Code", "What it does"), raw=False):
        rows = "\n".join((f"| {c} | {d} |" if raw else f"| `{c}` | {d} |") for c, d in recap)
        self.md(f"""
---
## Recap

| {head[0]} | {head[1]} |
|---|---|
{rows}
""")
        if self.solutions:
            parts = ["---\n## Solutions\n\nTry each exercise before looking. There is often more than one correct way to write it."]
            for label, codetxt, note in self.solutions:
                p = f"**{label}**"
                if note:
                    p += f"\n\n{note}"
                if codetxt:
                    p += f"\n\n```r\n{codetxt}\n```"
                parts.append(p)
            self.md("\n\n".join(parts))
        self.md(f"---\n## Next\n\n{next_md.strip()}")

    # -- output
    def write(self):
        os.makedirs(OUT, exist_ok=True)
        os.makedirs(TEST, exist_ok=True)
        fname, title = FILES[self.key]
        nb_cells = []
        for i, c in enumerate(self.cells):
            lines = c["text"].split("\n")
            src = [l + "\n" for l in lines[:-1]] + [lines[-1]]
            cell = {"cell_type": c["kind"], "metadata": {"id": f"{self.key.lower()}_{i:03d}"}, "source": src}
            if c["kind"] == "code":
                cell["execution_count"] = None
                cell["outputs"] = []
            nb_cells.append(cell)
        nb = {
            "nbformat": 4,
            "nbformat_minor": 0,
            "metadata": {
                "colab": {"provenance": [], "toc_visible": True, "name": f"{fname}.ipynb"},
                "kernelspec": {"name": "ir", "display_name": "R"},
                "language_info": {"name": "R"},
            },
            "cells": nb_cells,
        }
        with open(f"{OUT}/{fname}.ipynb", "w") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        for mode in ("blank", "solved"):
            with open(f"{TEST}/{self.key}_{mode}.R", "w") as f:
                for c in self.cells:
                    if c["kind"] != "code":
                        continue
                    body = c["solution"] if (mode == "solved" and c["solution"]) else c["text"]
                    if c["error"]:
                        # intentional error cells: must actually fail
                        f.write("cat('EXPECTED-ERROR-CELL:', inherits(try(eval(parse(text = " + json.dumps(body) + ")), silent = TRUE), 'try-error'), '\\n')\n\n")
                    else:
                        f.write(body + "\n\n")
        ncode = sum(1 for c in self.cells if c["kind"] == "code")
        print(f"{self.key}: {len(self.cells)} cells ({ncode} code, {self.n_ex} exercises)")
