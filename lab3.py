import pandas as pd
import matplotlib.pyplot as plt

def grade_scale(score):
    """
    Assigns a grade based on the national grading scale.
    """
    if 60 <= score <= 74:
        return "Good enough"
    elif 75 <= score <= 89:
        return "Good"
    elif 90 <= score <= 100:
        return "Perfect"
    return "Error"

# Step 1: Load the data
FILE_PATH = "LW3.xlsx"
df = pd.read_excel(FILE_PATH)

# Step 2: Ensure correct column names
df.columns = df.columns.str.strip()  # Removes leading/trailing spaces
# print("Column names:", df.columns)  # Debugging step

# Step 3: Convert all grade columns to numeric, forcing non-numeric values to NaN
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Ensures numeric data

# Check for missing values and handle them (optional)
# sprint(df.isna().sum())  # Debugging step
df.fillna(60, inplace=True)

# Apply the filtering safely
for col in df.columns[1:]:
    df = df[(df[col] >= 60) & (df[col] <= 100)]

# Step 4: Remove duplicates based on 'Name'
if "Name" not in df.columns:
    print(" Column 'Name' not found! Check Excel file headers.")
else:
    df = df.drop_duplicates(subset=["Name"])
    print("Duplicates removed successfully!")

# Step 5: Assign grades based on the national grading scale
for col in df.columns[1:]:
    df[f"{col}_grade"] = df[col].apply(grade_scale)

# Step 6: Compute Average Score
df["Average grade"] = df.iloc[:, 1:len(df.columns) // 2 + 1].mean(axis=1)

# Step 7: Scholarship Ranking
# Select top 60% students by average score
top_students = df.nlargest(int(len(df) * 0.6), "Average grade")

df["Scholarship"] = df["Name"].apply(
    lambda x: "*" if x in top_students["Name"].values else ""
)

# Step 8: Identify the top and bottom students
highest_scorer = df.loc[df["Average grade"].idxmax(), "Name"]
lowest_scorer = df.loc[df["Average grade"].idxmin(), "Name"]
num_scholarship = df["Scholarship"].value_counts().get("*", 0)

# Display results
# print(f"Max grade: {highest_scorer}")
# print(f"Min grade: {lowest_scorer}")
# print(f"Students with scholarship: {num_scholarship}")

# Step 9: Save the results to a new file
OUTPUT_FILE = "Processed_LW3.xlsx"
df.to_excel(OUTPUT_FILE, index=False)
print(f"File saved: {OUTPUT_FILE}")
