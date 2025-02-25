import pandas as pd
import matplotlib.pyplot as plt
import sys

# Force UTF-8 encoding for console output (Windows fix)
sys.stdout.reconfigure(encoding="utf-8")

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
FILE_PATH = "LW3_english.xlsx"
df = pd.read_excel(FILE_PATH)

# Step 2: Ensure correct column names
df.columns = df.columns.str.strip()  # Removes leading/trailing spaces

# Step 3: Convert only grade columns to numeric, preserving text columns
grade_cols = [col for col in df.columns if "points" in col.lower() or "grade" in col.lower()]
for col in grade_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")  # Ensures numeric data

# Check for missing values and fill only numeric columns
df[grade_cols] = df[grade_cols].fillna(60)

# Step 4: Remove duplicates based on 'Name'
if "Name" not in df.columns:
    print(" Column 'Name' not found! Check Excel file headers.")
else:
    df = df.drop_duplicates(subset=["Name"])
    print("Duplicates removed successfully!")

# Step 5: Assign grades based on the national grading scale
for col in grade_cols:
    df[f"{col}_grade"] = df[col].apply(grade_scale)

# Step 6: Compute Average Score
df["Average grade"] = df[grade_cols].mean(axis=1)

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

# Step 9: Select students from the specific group
group_number = "535ст2"
if "Group" in df.columns:
    group_students = df[df["Group"] == group_number]
    if not group_students.empty:
        highest_in_group = group_students.loc[group_students["Average grade"].idxmax(), "Name"]
        lowest_in_group = group_students.loc[group_students["Average grade"].idxmin(), "Name"]
        num_scholarship_group = group_students["Scholarship"].value_counts().get("*", 0)
    else:
        highest_in_group, lowest_in_group, num_scholarship_group = "None", "None", 0
else:
    print("Column 'Group' not found! Check the data format.")
    highest_in_group, lowest_in_group, num_scholarship_group = "None", "None", 0

# Display results
print(f"Max grade overall: {highest_scorer}")
print(f"Min grade overall: {lowest_scorer}")
print(f"Students with scholarship overall: {num_scholarship}")
print(f"Max grade in group {group_number}: {highest_in_group}")
print(f"Min grade in group {group_number}: {lowest_in_group}")
print(f"Students with scholarship in group {group_number}: {num_scholarship_group}")

# Step 10: Save the results to a new file
OUTPUT_FILE = "Processed_LW3.xlsx"
df.to_excel(OUTPUT_FILE, index=False)
print(f"File saved: {OUTPUT_FILE}")
