import pandas as pd
import os

# ========== FILE PATHS ==========
input_file = r"C:\Users\it_ka\Desktop\ETL test\final etl\AWS_test.xlsx"
output_file = r"C:\Users\it_ka\Desktop\ETL test\final etl\COI5P.csv"

removed_duplicates = r"C:\Users\it_ka\Desktop\ETL test\final etl\removed_duplicates.csv"
removed_missing = r"C:\Users\it_ka\Desktop\ETL test\final etl\removed_missing.csv"
removed_short = r"C:\Users\it_ka\Desktop\ETL test\final etl\removed_short.csv"


# ========== READ FILE (CSV + EXCEL) ==========
ext = os.path.splitext(input_file)[1].lower()

try:
    if ext == ".csv":
        try:
            df = pd.read_csv(input_file, encoding="utf-8")
        except:
            df = pd.read_csv(input_file, encoding="cp1252")
    else:
        df = pd.read_excel(input_file)

    print(f"[INFO] Loaded {len(df)} rows.")

except Exception as e:
    raise SystemExit(f"[ERROR] Cannot read file: {e}")


# ========== CLEANING STARTS ==========

#  Remove duplicates
dup = df[df.duplicated("nucleotides")]
dup.to_csv(removed_duplicates, index=False)
df = df.drop_duplicates("nucleotides")

#  Remove rows missing essential fields
required = ["nucleotides", "species_name"]
missing = df[df[required].isna().any(axis=1)]
missing.to_csv(removed_missing, index=False)
df = df.dropna(subset=required)

#  Clean sequence
df["nucleotides"] = (
    df["nucleotides"]
    .astype(str)
    .str.upper()
    .str.replace(r"[^ATGC]", "", regex=True)
)

#  Remove short sequences (<500 bp)
short = df[df["nucleotides"].str.len() < 500]
short.to_csv(removed_short, index=False)
df = df[df["nucleotides"].str.len() >= 500]

#  Clean taxonomy capitalization
tax_cols = ["processid","phylum_name","class_name","order_name",
            "family_name","genus_name","species_name"]

for c in tax_cols:
    if c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.capitalize()

#  Set missing phylum to Chordata
df["phylum_name"] = df.get("phylum_name", "Chordata")
df["phylum_name"] = df["phylum_name"].fillna("Chordata")

#  Keep final columns only
final_cols = ["processid","phylum_name","class_name","order_name",
              "family_name","genus_name","species_name","country",
              "sequenceID","nucleotides"]

df = df[[c for c in final_cols if c in df.columns]]

print(f"[INFO] Final cleaned rows: {len(df)}")


# ========== SAVE OUTPUT ==========
df.to_csv(output_file, index=False)
print(f"[INFO] Saved cleaned file to: {output_file}")
print("[INFO] Removed rows stored separately.")

#  Step 5: Display first few rows (works in both Colab and VS Code)
try:
    from IPython.display import display
    display(df.head())
except ImportError:
    print(df.head())
