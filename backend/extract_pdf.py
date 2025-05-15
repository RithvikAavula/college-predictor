import pdfplumber
import pandas as pd

all_rows = []

with pdfplumber.open("E:/college-predictor/backend/TS-EAMCET-2022-FINAL-PHASE-Cutoff-Ranks.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages):
        print(f"Processing Page {page_num + 1}")
        table = page.extract_table()
        if table:
            for row in table[1:]:  # skip header
                all_rows.append(row)

# Define columns manually since pdfplumber might not extract headers correctly
columns = [
    "INST_CODE", "INSTITUTE_NAME", "PLACE", "DIST", "COED", "TYPE", "YEAR_OF_ESTB", "BRANCH", "BRANCH_NAME",
    "OC_BOYS", "OC_GIRLS", "BC_A_BOYS", "BC_A_GIRLS", "BC_B_BOYS", "BC_B_GIRLS", "BC_C_BOYS", "BC_C_GIRLS",
    "BC_D_BOYS", "BC_D_GIRLS", "BC_E_BOYS", "BC_E_GIRLS", "SC_BOYS", "SC_GIRLS", "ST_BOYS", "ST_GIRLS",
    "EWS_GEN_OU", "EWS_GIRLS_OU", "TUITION_FEE", "AFFILIATED"
]

# Convert to DataFrame
df = pd.DataFrame(all_rows, columns=columns)

# Clean numeric columns
for col in columns[9:-2]:  # rank columns
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Save to CSV
df.to_csv("cutoff_data.csv", index=False)
print("✅ Extraction complete. Saved to cutoff_data.csv")
