import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("Graphs", exist_ok=True)
# Load the dataset
df = pd.read_csv("students.csv")

# Display first 5 rows
print("First 5 Students:")
print(df.head())

# Display dataset size
print("\nDataset Shape:")
print(df.shape)

# Display column information
print("\nDataset Information:")
df.info()

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Calculate Average marks of each student
subjects = ["Maths", "Science", "English", "Computer", "Physics"]
df["Average"] = df[subjects].mean(axis=1)
print("\nStudents Average Marks:")
print(df[["Student", "Average"]])

# Find the top-performing student based on average marks
top_student = df.loc[df["Average"].squeeze().idxmax()]

print("\nTop-Performing Student:")
print("Name:", top_student["Student"])
print("Average Marks:", round(top_student["Average"], 2))

# Rank all students
df["Rank"] = df["Average"].rank(ascending=False, method="dense").astype(int)

# Display students according to rank
print("\nStudent Rankings:")
print(df[["Student", "Average", "Rank"]].sort_values("Rank").to_string(index=False))

# Subject-wise performance analysis
subject_avg = df[subjects].mean()

print("\nSubject-wise Average Marks:")
print(subject_avg.round(2))

print("\nBest Performing Subjects:")
print(subject_avg.idxmax())

print("\nLowest Performing Subject:")
print(subject_avg.idxmin())

# create graph using matplotlib
# Plot subject-wise average marks
plt.figure(figsize=(8, 5))
plt.bar(subject_avg.index, subject_avg.values)

plt.title("Subject-wise Average Marks")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")

plt.ylim(0, 100)

# Show graph as an Image
plt.savefig("Graphs/subject_average.png", dpi=300, bbox_inches="tight")
plt.show()

# Student performance comparison chart
plt.figure(figsize=(10, 5))
plt.bar(df["Student"], df["Average"])

plt.title("Student Performance Comparison")
plt.xlabel("Students")
plt.ylabel("Average Marks")

plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("Graphs/student_performance.png", dpi=300, bbox_inches="tight")
plt.show()


# Grade Distribution Analysis
def assign_grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    else:
        return "F"


# Assign grades to students
df["Grade"] = df["Average"].apply(assign_grade)

# Count students in each grade
grade_counts = df["Grade"].value_counts().sort_index()
print("\nGrade Distribution:")
print(grade_counts)

# Create grade distribution chart
plt.figure(figsize=(8, 5))
plt.bar(grade_counts.index, grade_counts.values)

plt.title("Student Grade Distribution")
plt.xlabel("Grade")
plt.ylabel("Number of Students")

plt.savefig("Graphs/grade_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

# Pass/Fail Analysis
df["Result"] = df[subjects].ge(40).all(axis=1).map({True: "Pass", False: "Fail"})
print("\nPass/Fail Analysis:")
print(df[["Student", "Average", "Result"]])

passed = (df["Result"] == "Pass").sum()
failed = (df["Result"] == "Fail").sum()

print("\nTotal Passed:", passed)
print("Total Failed:", failed)

pass_percentage = (passed / len(df)) * 100
print("Pass Percentage:", round(pass_percentage, 2), "%")

# Export Final Report
df = df.sort_values(by="Average", ascending=False)

df.to_csv("student_performance_report.csv", index=False)
print("\nFinal report saved successfully!")

# Data validation
print("\n--- Data Validation ---")
print("Missing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())
print("\nMarks Outside 0-100:")
for subject in subjects:
    invalid = df[~df[subject].between(0, 100)]
    if not invalid.empty:
        print(subject, ":", len(invalid), "invalid marks")
    else:
        print(subject, ":All marks are valid")
