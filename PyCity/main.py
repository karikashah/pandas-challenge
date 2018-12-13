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

# calculate the percentage of students with a passing math & reading score (70 or greater)
perc_pass_math = students_df.loc[students_df['math_score'] >= 70]['math_score'].count()/num_of_students
perc_pass_reading = students_df.loc[students_df['reading_score'] >= 70]['reading_score'].count()/num_of_students

overall_pass_rate = (perc_pass_math+perc_pass_reading)/2

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
district_summary["Average Math Score"] = district_summary["Average Math Score"].map("{:.2f}".format)
district_summary["Average Reading Score"] = district_summary["Average Reading Score"].map("{:.2f}".format)
district_summary["% Passing Math"] = district_summary["% Passing Math"].map("{:.2%}".format)
district_summary["% Passing Reading"] = district_summary["% Passing Reading"].map("{:.2%}".format)
district_summary["Overall Passing Rate"] = district_summary["Overall Passing Rate"].map("{:.2%}".format)

print (district_summary.head())

#format cells
# district_summary.style.format({
#                         'Total Students':'{:,}',
#                         "Total Budget": "${:,.2f}", 
#                        "Average Reading Score": "{:.2f}", 
#                        "Average Math Score": "{:.2f}", 
#                        "% Passing Math": "{:.2%}", 
#                        "% Passing Reading": "{:.2%}", 
#                        "Overall Passing Rate": "{:.2f}"})

# print(district_summary.head())

##################### CALCULATIONS FOR SCHOOL SUMMARY DATAFRAME ------------------------------------------------------
# sort the complete dataframe based on school name
by_school = school_data_complete.set_index("school_name").groupby(["school_name"])

schools_name = schools_df['school_name']
schools_type = schools_df.set_index('school_name')['type']

# total students by school
stu_per_sch = by_school['Student ID'].count()
# total school budget
sch_budget = schools_df.set_index('school_name')['budget']

# per student budget
stu_budget = schools_df.set_index('school_name')['budget']/schools_df.set_index('school_name')['size']

# avg scores by school
avg_math = by_school['math_score'].mean()
avg_read = by_school['reading_score'].mean()

# % passing scores
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('school_name')['Student ID'].count()/stu_per_sch 
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('school_name')['Student ID'].count()/stu_per_sch 
overall = (pass_math + pass_read)/2

# creating school summary dataframe
school_summary = pdk.DataFrame({
    "School Type": schools_type,
    "Total Students": stu_per_sch,
    "Total School Budget": sch_budget,
    "Per Student Budget": stu_budget,
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall
})

# sorting the school dataframe based on School type
school_summary = school_summary.sort_values("School Type")

# formating & styling the school summary data frame
school_summary["Total Students"] = school_summary["Total Students"].map("{:,}".format)
school_summary["Total School Budget"] = school_summary["Total School Budget"].map("${:,.2f}".format)
school_summary["Per Student Budget"] = school_summary["Per Student Budget"].map("${:,.2f}".format)
school_summary["Average Math Score"] = school_summary["Average Math Score"].map("{:.2f}".format)
school_summary["Average Reading Score"] = school_summary["Average Reading Score"].map("{:.2f}".format)
school_summary["% Passing Math"] = school_summary["% Passing Math"].map("{:.2%}".format)
school_summary["% Passing Reading"] = school_summary["% Passing Reading"].map("{:.2%}".format)
school_summary["Overall Passing Rate"] = school_summary["Overall Passing Rate"].map("{:.2%}".format)

print(school_summary.head(20))
