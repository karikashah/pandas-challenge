# Importing libraries
import pandas as pdk

# Specify path to files
schools_csv = "../../../Python Resources/schools_complete.csv"
students_csv = "../../../Python Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
schools_df = pdk.read_csv(schools_csv)
students_df = pdk.read_csv(students_csv)

# Combine the data into a single dataset
school_data_complete = pdk.merge(schools_df, students_df, how="left", on=["school_name", "school_name"])

##################### CALCULATIONS FOR DISTRICT SUMMARY DATAFRAME ------------------------------------------------------
# calculate total # of schools
num_of_schools = school_data_complete["school_name"].nunique()

# calculate the total number of students
num_of_students = school_data_complete["student_name"].count()

# calculate the total budget
total_budget = schools_df["budget"].sum()

# calculate the average math, reading scores & overall passing rate
avg_math = school_data_complete["math_score"].mean()
avg_reading = school_data_complete["reading_score"].mean()
overall_pass_rate = (avg_math+avg_reading)/2
print(f"Average Math score is {avg_math}")
print(f"Average Reading score is {avg_reading}")

# calculate the percentage of students with a passing math & reading score (70 or greater)
num_passing_math = students_df.loc[students_df['math_score'] >= 70]['math_score'].count()
perc_pass_math = (num_passing_math/num_of_students)*100

num_passing_reading = students_df.loc[students_df['reading_score'] >= 70]['reading_score'].count()
perc_pass_reading = (num_passing_reading/num_of_students)*100

district_summary = pdk.DataFrame({
        "Total Schools" : [num_of_schools],
        "Total Students": [num_of_students],
        "Total Budget": [total_budget],
        "Average Math Score": [avg_math],
        "Average Reading Score": [avg_reading],
        "% Passing Math": [perc_pass_math],
        "% Passing Reading": [perc_pass_reading],
        "Overall Passing Rate": [overall_pass_rate]
    }
)

# formating & styling the district summary data frame
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

print(district_summary.head())