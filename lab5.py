import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.pdfgen import canvas
import pandas as pd
import numpy as np

# Upload data from excel file
file_path = "Processed_LW3.xlsx"
df = pd.read_excel(file_path)

# Global variable to store graph canvas
graph_canvas = None

# Convert data to dictionary
students = df.to_dict(orient="records")

# Dynamically identify subject columns based on keywords
subject_keywords = ["points", "score", "grade"]
subject_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in subject_keywords)]

def search_student():
    """Search for a student by name"""
    name = entry_name.get()
    result = next((s for s in students if s["Name"].lower() == name.lower()), None)
    if result:
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, f"Student: {result['Name']}\nGroup: {result['Group']}\nAverage Note: {result.get('Average grade', 'N/A')}\nScholarship: {'Yes' if result.get('Scholarship') == '*' else 'No'}")
    else:
        messagebox.showinfo("Result", "No student found")

def search_group():
    """Search for all students in a specific group"""
    group = str(entry_group.get().strip())
    results = [s for s in students if str(s["Group"]).strip().lower() == group.lower()]
    if results:
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, f"Group: {group}\nTotal Students: {len(results)}\n\n")
        for student in results:
            text_result.insert(tk.END, f"{student['Name']} - Avg Score: {student.get('Average grade', 'N/A')} - Scholarship: {'Yes' if student.get('Scholarship') == '*' else 'No'}\n")
    else:
        messagebox.showinfo("Result", f"No students found in group '{group}'. Available groups: {set(df['Group'])}")

def show_student_grades():
    """Show a column chart with a specific student's grades."""
    clear_fields()
    name = entry_name.get().strip()
    student = next((s for s in students if str(s["Name"]).strip().lower() == name.lower()), None)
    
    if not student:
        messagebox.showinfo("Result", "No student found")
        return
    
    scores = [pd.to_numeric(student.get(subject, 0), errors='coerce') for subject in subject_columns]
    scores = [0 if np.isnan(score) else score for score in scores]  # Replace NaN with 0
    
    if all(score == 0 for score in scores):
        messagebox.showinfo("Result", "No valid numeric scores available for this student.")
        return
    
    fig, ax = plt.subplots()
    ax.bar(subject_columns, scores, color='skyblue')
    ax.set_xlabel("Subjects")
    ax.set_ylabel("Scores")
    ax.set_title(f"Grades of {student['Name']}")
    ax.set_xticks(range(len(subject_columns)))
    ax.set_xticklabels(subject_columns, rotation=45, ha="right", fontsize=10)
    
    plt.tight_layout()
    
    global graph_canvas
    graph_canvas = FigureCanvasTkAgg(fig, master=window)
    graph_canvas.get_tk_widget().pack()
    graph_canvas.draw()

def show_scholar():
    """Show all students with scholarships"""
    scholars = [s for s in students if s.get("Scholarship") == "*"]
    if scholars:
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, "Students with Scholarships:\n\n")
        for student in scholars:
            text_result.insert(tk.END, f"{student['Name']} - Group: {student['Group']} - Avg Score: {student.get('Average grade', 'N/A')}\n")
    else:
        messagebox.showinfo("Result", "No students with scholarships found.")

def generate_report(filter_group=None, only_scholarship=False):
    """Generate a PDF report with student performance."""
    filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not filename:
        return
    c = canvas.Canvas(filename)
    c.drawString(100, 750, "Report with student performance")
    y = 720
    for student in students:
        avg_score = student.get("Average grade", "N/A")
        scholarship = student.get("Scholarship", " ")
        if (only_scholarship and scholarship != "*") or (filter_group and student["Group"] != filter_group):
            continue
        c.drawString(100, y, f"{student['Name']}, Group: {student['Group']}, Score: {avg_score}")
        y -= 20
    c.save()
    messagebox.showinfo("Ready", f"Report was saved as {filename}")

def show_pie_chart_group():
    """Show a pie chart for the selected group."""
    clear_fields()
    group = entry_group.get().strip()
    if not group:
        messagebox.showinfo("Error", "Please enter a group number.")
        return
    
    group_students = df[df["Group"].str.lower() == group.lower()]
    if group_students.empty:
        messagebox.showinfo("Error", f"No data available for group '{group}'.")
        return
    
    scholarship_count = group_students[group_students["Scholarship"] == "*"].shape[0]
    non_scholarship_count = group_students.shape[0] - scholarship_count
    
    labels = ["Scholarship", "Non-Scholarship"]
    sizes = [scholarship_count, non_scholarship_count]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(f"Scholarship Distribution in Group {group}")
    
    global graph_canvas
    graph_canvas = FigureCanvasTkAgg(fig, master=window)
    graph_canvas.get_tk_widget().pack()
    graph_canvas.draw()

def clear_fields():
    """Clear text box and graphs while preserving input fields."""
    global graph_canvas
    text_result.delete("1.0", tk.END)  # Clear text output
    
    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()
        graph_canvas = None

# Create the main window
window = tk.Tk()
window.title("Student Performance Analysis")
window.geometry("700x600")
window.configure(bg="#adade8")

# Title Label
label_title = tk.Label(window, text="Student Performance Analysis", font=("Arial", 18, "bold"), bg="#adade8")
label_title.pack(pady=10)

# Frame for search section
frame_search = tk.Frame(window, bg="#adade8")
frame_search.pack(pady=10)

# Row 1: Find Student & Show Grades
label_name = tk.Label(frame_search, text="Full Name:", font=("Arial", 12), bg="#adade8")
label_name.grid(row=0, column=0, padx=5)
entry_name = tk.Entry(frame_search, font=("Arial", 12), width=30)
entry_name.grid(row=0, column=1, padx=5)
btn_search = tk.Button(frame_search, text="Find Student", font=("Arial", 12, "bold"), bg="#2d8659", fg="white", command=search_student)
btn_search.grid(row=0, column=2, padx=5)
btn_show_grades = tk.Button(frame_search, text="Show Grades", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", command=show_student_grades)
btn_show_grades.grid(row=0, column=3, padx=5)

# Row 2: Find Group & Show Group Diagram
label_group = tk.Label(frame_search, text="Group:", font=("Arial", 12), bg="#adade8")
label_group.grid(row=1, column=0, padx=5)
entry_group = tk.Entry(frame_search, font=("Arial", 12), width=30)
entry_group.grid(row=1, column=1, padx=5)
btn_search_group = tk.Button(frame_search, text="Find Group", font=("Arial", 12, "bold"), bg="#2d8659", fg="white", command=search_group)
btn_search_group.grid(row=1, column=2, padx=5)
btn_pie_chart_group = tk.Button(frame_search, text="Show Group Diagram", font=("Arial", 12, "bold"), bg="#2196F3", fg="black", command=show_pie_chart_group)
btn_pie_chart_group.grid(row=1, column=3, padx=5)

# Row 3: Show Scholars
btn_scholar = tk.Button(frame_search, text="Show Scholars", font=("Arial", 12, "bold"), bg="#c2f0c2", fg="black", command=show_scholar)
btn_scholar.grid(row=2, column=1, columnspan=2, pady=5)
btn_clear = tk.Button(frame_search, text="Clear Fields", font=("Arial", 12, "bold"), bg="#ff6666", fg="white", command=clear_fields)
btn_clear.grid(row=2, column=3, padx=5)

# Results Text Box
text_result = tk.Text(window, height=5, width=60, font=("Arial", 12), padx=10, pady=10)
text_result.pack(pady=10)

# Buttons Frame for Report Generation
frame_buttons = tk.Frame(window, bg="#adade8")
frame_buttons.pack(pady=10)

btn_report_all = tk.Button(frame_buttons, text="Generate PDF (All)", font=("Arial", 12, "bold"), bg="#cc6600", fg="white", command=lambda: generate_report())
btn_report_all.grid(row=0, column=1, padx=10, pady=5)
btn_report_scholarship = tk.Button(frame_buttons, text="PDF (Scholarship Only)", font=("Arial", 12, "bold"), bg="#FF5722", fg="white", command=lambda: generate_report(only_scholarship=True))
btn_report_scholarship.grid(row=0, column=2, padx=10, pady=5)

# Frame for Group Filtering for Report Generation
frame_group = tk.Frame(window, bg="#adade8")
frame_group.pack(pady=10)

label_group_for_report = tk.Label(frame_group, text="Group Filter:", font=("Arial", 12), bg="#adade8")
label_group_for_report.grid(row=0, column=0, padx=5)
entry_group_for_report = tk.Entry(frame_group, font=("Arial", 12), width=15)
entry_group_for_report.grid(row=0, column=1, padx=5)
btn_report_group_for_report = tk.Button(frame_group, text="Generate PDF (Group)", font=("Arial", 12, "bold"), bg="#993366", fg="white", command=lambda: generate_report(filter_group=entry_group.get()))
btn_report_group_for_report.grid(row=0, column=2, padx=5)

window.mainloop()
