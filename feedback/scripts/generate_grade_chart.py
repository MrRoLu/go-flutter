import csv
import matplotlib.pyplot as plt
from collections import Counter

# Read grades from CSV
with open('feedback/data/grades.csv', encoding='utf-8-sig') as file:  # Handle BOM
    reader = csv.reader(file)
    grades = [row[0].strip() for row in reader]  # Strip whitespace

# Debug: Show unique grades
print("Unique grades found:", set(grades))

# Count grades
grade_counts = Counter(grades)

# Debug: Print raw counts
print("Raw grade counts:")
for grade, count in grade_counts.items():
    print(f"  '{grade}': {count}")

# Create pie chart
plt.figure(figsize=(10, 8))
labels = list(grade_counts.keys())
sizes = list(grade_counts.values())
colors = ['#2E8B57', '#4682B4', '#DAA520', '#DC143C', '#8B0000']  # Green, Blue, Gold, Red, Dark Red

# Calculate percentages
total = sum(sizes)
percentages = [f'{100 * size/total:.1f}%' for size in sizes]

# Create pie chart with percentages
plt.pie(sizes, labels=[f'{label} ({count})' for label, count in zip(labels, sizes)], 
        autopct='%1.1f%%', colors=colors[:len(labels)], startangle=90)
plt.title('Course Grade Distribution', fontsize=16, pad=20)

# Add total students count
plt.figtext(0.5, 0.02, f'Total Students: {total}', ha='center', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))

plt.axis('equal')
plt.tight_layout()
plt.savefig('feedback/figures/grades.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\nGrade chart generated: feedback/figures/grades.png")
print(f"Total students: {total}")
print("Grade distribution:")
# Sort grades in order A, B, C, D, F
grade_order = ['A', 'B', 'C', 'D', 'F']
for grade in grade_order:
    if grade in grade_counts:
        count = grade_counts[grade]
        percentage = 100 * count / total
        print(f"  {grade}: {count} students ({percentage:.1f}%)") 