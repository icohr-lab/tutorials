# Tutorials

Self-paced lessons in data analysis for health research, published at <https://icohr-lab.github.io/tutorials/>.

## Series

| Folder | Series | Format |
|---|---|---|
| `foundations/` | R Foundations | Google Colab notebooks |
| `aou/` | R for *All of Us* | Google Colab notebooks |
| `survey/` | R for Survey Data (NHIS) | Colab notebooks, then RStudio lessons |

Each series has its own sidebar, defined in `_quarto.yml`. To add a series, create its folder, add a sidebar and a navbar entry in `_quarto.yml`, and add a button to `index.qmd`.

## Layout

- `_quarto.yml`: site settings and one sidebar per series
- `styles/theme.scss`: fonts, colors, and the landing-page buttons
- `index.qmd`: landing page

## Build and publish

```bash
quarto preview                 # local preview
quarto publish gh-pages        # build and publish to GitHub Pages
```
