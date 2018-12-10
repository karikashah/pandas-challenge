# Importing libraries
import pandas as pdk

# Specify path to files
schools_csv = "../../../Python Resources/schools_complete.csv"
students_csv = "../../../Python Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
schools_df = pdk.read_csv(schools_csv)
students_df = pdk.read_csv(students_csv)

# print its first 5 rows & also count of row n column
# print(schools_df.head())
# print(schools_df.shape)
# print("------------------------------------------------------------------")
# print(students_df.head())
# print(students_df.shape)
# print("------------------------------------------------------------------")

# Combine the data into a single dataset
school_data_complete = pdk.merge(schools_df, students_df, how="left", on=["school_name", "school_name"])

# print(school_data_complete.head())
# print(school_data_complete.shape)
# print("------------------------------------------------------------------")

# calculate total # of schools
num_of_schools = school_data_complete["school_name"].nunique()
print("------------------------------------------------------------------")
print(f"Total # of Schools are {num_of_schools}")

# calculate the total number of students
num_of_students = school_data_complete["student_name"].nunique()
print(f"Total # of Students are {num_of_students}")

# calculate the total budget
total_budget = schools_df["budget"].sum()
print(f"Total budget for school is ${total_budget}") # !!!need to take care of formating!!!

# calculate the average math & reading scores 
avg_math = school_data_complete["math_score"].mean()
avg_reading = school_data_complete["reading_score"].mean()
print(f"Average Math score is {avg_math}")
print(f"Average Reading score is {avg_reading}")