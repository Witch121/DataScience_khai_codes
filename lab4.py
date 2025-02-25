import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sys

sys.stdout.reconfigure(encoding="utf-8")

def grade_scale(score):
    if 60 <= score <= 74:
        return "Good enough"
    elif 75 <= score <= 89:
        return "Good"
    elif 90 <= score <= 100:
        return "Perfect"
    return "Error"

# data loading
FILE_PATH = "LW3_english.xlsx"
df = pd.read_excel(FILE_PATH)
df.columns = df.columns.str.strip()
numeric_cols = df.select_dtypes(include=['number']).columns

df[numeric_cols] = df[numeric_cols].fillna(60)
df = df.drop_duplicates(subset=["Name"])
df["Average grade"] = df[numeric_cols].mean(axis=1)

top_students = df.nlargest(int(len(df) * 0.6), "Average grade")
df["Scholarship"] = df["Name"].apply(lambda x: "*" if x in top_students["Name"].values else "")

def search_student(name):
    student = df[df["Name"].str.contains(name, case=False, na=False)]
    if not student.empty:
        print(student.to_string(index=False))
    else:
        print("No student found.")

def search_group(group):
    group_students = df[df["Group"] == group]
    if not group_students.empty:
        print(f"Number of students in the group: {len(group_students)}")
        print(f"Number of students with scholarship: {group_students['Scholarship'].value_counts().get('*', 0)}")
    else:
        print("No group found.")

def students_with_scholarship():
    scholars = df[df["Scholarship"] == "*"]["Name"]
    print("Students with scholarship:")
    print(scholars.to_string(index=False))

def plot_group_performance(group):
    group_students = df[df["Group"] == group]
    if group_students.empty:
        print("No group found.")
        return
    
    labels = ["3 points", "4 points", "5 points"]
    counts = [
        sum((group_students["Average grade"] >= 60) & (group_students["Average grade"] <= 74)),
        sum((group_students["Average grade"] >= 75) & (group_students["Average grade"] <= 89)),
        sum((group_students["Average grade"] >= 90) & (group_students["Average grade"] <= 100))
    ]
    
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f'Student success rate of the group {group}')
    plt.show()

def plot_student_performance(name):
    student = df[df["Name"].str.contains(name, case=False, na=False)]
    if student.empty:
        print("No student found.")
        return
    
    plt.figure(figsize=(8, 6))
    plt.bar(numeric_cols, student.iloc[0][numeric_cols])
    plt.xlabel("Subjects")
    plt.ylabel("Grades")
    plt.title(f'Student success: {name}')
    plt.xticks(rotation=45)
    plt.show()

def generate_report(group):
    group_students = df[df["Group"] == group]
    if group_students.empty:
        print("No group found.")
        return
    
    pdf_path = f"Report_{group}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, f"Group report {group}")
    c.drawString(100, 730, f"Number of students: {len(group_students)}")
    c.drawString(100, 710, f"Number of students with scholarships: {group_students['Scholarship'].value_counts().get('*', 0)}")
    
    subjects_avg = group_students[numeric_cols].mean()
    c.drawString(100, 690, "Average grades by subject:")
    y = 670
    for subj, avg in subjects_avg.items():
        c.drawString(120, y, f"{subj}: {avg:.2f}")
        y -= 20
    
    c.drawString(100, y - 20, "Students with scores below 65 points:")
    y -= 40
    for name in group_students[group_students["Average grade"] < 65]["Name"]:
        c.drawString(120, y, name)
        y -= 20
    
    c.drawString(100, y - 20, "Students with scores above 95 points:")
    y -= 40
    for name in group_students[group_students["Average grade"] > 95]["Name"]:
        c.drawString(120, y, name)
        y -= 20
    
    c.save()
    print(f"Report saved as {pdf_path}")

if __name__ == "__main__":
    while True:
        print("\nChoose an option:")
        print("1. Search for a student by full name")
        print("2. Search by group")
        print("3. Display the full names of everyone receiving a scholarship")
        print("4. Graphical analysis of the group")
        print("5. Graphical analysis of the student")
        print("6. Report generation")
        print("7. Exit")
        
        choice = input("Enter option number: ")
        
        if choice == "1":
            search_student(input("Enter the student's full name: "))
        elif choice == "2":
            search_group(input("Enter group number: "))
        elif choice == "3":
            students_with_scholarship()
        elif choice == "4":
            plot_group_performance(input("Enter group number: "))
        elif choice == "5":
            plot_student_performance(input("Enter the student's full name: "))
        elif choice == "6":
            generate_report(input("Enter group number: "))
        elif choice == "7":
            break
        else:
            print("Incorrect choice, try again.")
