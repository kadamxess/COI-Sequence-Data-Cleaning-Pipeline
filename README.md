# COI Sequence Data Cleaning Pipeline

##  Overview

This project provides a simple and reproducible **ETL (Extract–Transform–Load) pipeline** for cleaning DNA barcode sequence data (COI region). It is designed for datasets exported from platforms like BOLD or similar biodiversity databases.

The script processes raw sequence data (CSV or Excel), applies multiple quality filters, and outputs a cleaned dataset ready for downstream bioinformatics analysis.

---

##  Features

* Supports both **CSV and Excel input files**
* Removes **duplicate nucleotide sequences**
* Filters out rows with **missing essential metadata**
* Cleans nucleotide sequences (keeps only `A, T, G, C`)
* Removes **short sequences (< 500 bp)**
* Standardizes **taxonomy formatting**
* Fills missing **phylum data (default: Chordata)**
* Saves **filtered-out data separately** for transparency

---

## File Structure

```
project/
│── script.py
│── input/
│   └── AWS_test.xlsx
│── output/
│   ├── COI5P.csv
│   ├── removed_duplicates.csv
│   ├── removed_missing.csv
│   ├── removed_short.csv
```

---

##  Input Requirements

The input file must contain at least the following columns:

* `nucleotides` → DNA sequence
* `species_name` → Species identifier

Optional but recommended columns:

* `processid`
* `phylum_name`
* `class_name`
* `order_name`
* `family_name`
* `genus_name`
* `country`
* `sequenceID`

---

##  Data Processing Steps

### 1. Load Data

* Automatically detects file format (`.csv` or `.xlsx`)
* Handles encoding issues (`utf-8`, fallback to `cp1252`)

### 2. Remove Duplicates

* Based on `nucleotides` column
* Saved to: `removed_duplicates.csv`

### 3. Remove Missing Data

* Drops rows missing:

  * `nucleotides`
  * `species_name`
* Saved to: `removed_missing.csv`

### 4. Clean Sequences

* Converts sequences to uppercase
* Removes invalid characters (keeps only `A, T, G, C`)

### 5. Filter Short Sequences

* Removes sequences < **500 base pairs**
* Saved to: `removed_short.csv`

### 6. Standardize Taxonomy

* Strips whitespace
* Capitalizes taxonomy fields:

  * phylum → species level

### 7. Handle Missing Phylum

* Default value set to **"Chordata"**

### 8. Select Final Columns

Only retains relevant columns for downstream use.

---

## Output Files

| File Name                | Description               |
| ------------------------ | ------------------------- |
| `COI5P.csv`              | Final cleaned dataset     |
| `removed_duplicates.csv` | Duplicate entries         |
| `removed_missing.csv`    | Rows with missing values  |
| `removed_short.csv`      | Short sequences (<500 bp) |

---

## How to Run

### 1. Install Dependencies

```bash
pip install pandas openpyxl
```

### 2. Update File Paths

Modify these variables in the script:

```python
input_file = "path_to_input_file"
output_file = "path_to_output_file"
```

### 3. Execute Script

```bash
python script.py
```

---

##  Compatibility

* Works in:

  * VS Code
  * Jupyter Notebook
  * Google Colab

Includes automatic display of the first few rows after processing.

---

## Use Cases

* DNA barcoding projects (COI region)
* Biodiversity informatics
* Preprocessing data for:

  * Phylogenetics
  * Species identification
  * Machine learning models

---

## Notes

* Sequence length threshold (500 bp) can be adjusted:

```python
df["nucleotides"].str.len() >= 500
```

* Ensure column names match expected schema.

---

## Author

**Kadam Xess**
Bioinformatics & Clinical Research Enthusiast

---

## License

This project is open-source and available under the MIT License.


