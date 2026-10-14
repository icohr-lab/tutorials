# NHIS 2025 teaching file

`nhis2025_adult.csv` is a subset of the **2025 National Health Interview Survey (NHIS) Sample Adult public-use file**, produced by the National Center for Health Statistics (NCHS). It keeps all 24,215 sample adults and 16 of the 577 columns, with the original NCHS codes unchanged.

- Source data and documentation: <https://www.cdc.gov/nchs/nhis/>
- Codebook: <https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHIS/2025/adult-codebook.pdf>
- Survey description (design and weights): <https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_Documentation/NHIS/2025/srvydesc-508.pdf>

NHIS public-use data are public domain. Suggested citation: National Center for Health Statistics. National Health Interview Survey, 2025. Public-use data file and documentation. 2026.

| Column | Description |
|---|---|
| `HHX` | Household identifier |
| `WTFA_A` | Final annual sample adult weight |
| `PSTRAT` | Variance estimation stratum |
| `PPSU` | Variance estimation primary sampling unit |
| `PHSTAT_A` | Self-rated general health |
| `CANEV_A` | Ever told had cancer |
| `NUMCAN_A` | Number of reported cancer types |
| `SKNNMCAN_A` | Non-melanoma skin cancer mentioned |
| `POVRATTC_A` | Family income-to-poverty ratio (top-coded at 12; includes imputed values) |
| `EDUCP_A` | Educational attainment |
| `NOTCOV_A` | Health insurance coverage status |
| `AGEP_A` | Age (top-coded at 85) |
| `SEX_A` | Sex |
| `HISPALLP_A` | Race and Hispanic origin |
| `REGION` | Census region |
| `URBRRL23` | 2023 NCHS urban-rural classification of county |

To rebuild the file from the NCHS download, run `Rscript data/nhis/make_teaching_file.R path/to/adult25.csv` from the project root.
