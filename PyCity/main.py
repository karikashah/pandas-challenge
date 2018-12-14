# Key observations
#------------------
# 1. Charter schools with lesser # of kids have better passing rates than district schools
# 2. Overall irrespective of school type & grades, the math passing score is lower than reading passing score
# 3. There is a significance drop in % passing Math for:
#     - District level schools vs Charter (66% vs 94%) also, 
#     - When school size is bigger i.e. large size (2000-5000) vs. small size (<1000), & 
#     - When average spending per student is more than $645.

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

# created new function to perform repeated task of calculating math, reasing & overall score based on different groupby string
def score_by_func(str_by_type):
    group_by_string = school_data_complete.groupby(str_by_type)

    # calculating math & reading average & percentage. Also calculate the overall
    avg_math = group_by_string['math_score'].mean()
    avg_read = group_by_string['reading_score'].mean()
    stu_count = group_by_string['Student ID'].count()
    pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby(str_by_type)['Student ID'].count()/stu_count
    pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby(str_by_type)['Student ID'].count()/stu_count
    overall = (pass_math + pass_read)/2

    # create dataframe for scores by spending            
    scores_by_string = pdk.DataFrame({
        "Average Math Score": avg_math,
        "Average Reading Score": avg_read,
        '% Passing Math': pass_math,
        '% Passing Reading': pass_read,
        "Overall Passing Rate": overall
    })

    # formating & styling the school summary data frame
    scores_by_string["Average Math Score"] = scores_by_string["Average Math Score"].map("{:.2f}".format)
    scores_by_string["Average Reading Score"] = scores_by_string["Average Reading Score"].map("{:.2f}".format)
    scores_by_string["% Passing Math"] = scores_by_string["% Passing Math"].map("{:.6%}".format)
    scores_by_string["% Passing Reading"] = scores_by_string["% Passing Reading"].map("{:.6%}".format)
    scores_by_string["Overall Passing Rate"] = scores_by_string["Overall Passing Rate"].map("{:.6%}".format)

    return scores_by_string

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
district_summary["% Passing Math"] = district_summary["% Passing Math"].map("{:.6%}".format)
district_summary["% Passing Reading"] = district_summary["% Passing Reading"].map("{:.6%}".format)
district_summary["Overall Passing Rate"] = district_summary["Overall Passing Rate"].map("{:.6%}".format)
print (district_summary.head())

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
school_summary["% Passing Math"] = school_summary["% Passing Math"].map("{:.6%}".format)
school_summary["% Passing Reading"] = school_summary["% Passing Reading"].map("{:.6%}".format)
school_summary["Overall Passing Rate"] = school_summary["Overall Passing Rate"].map("{:.6%}".format)

print(school_summary.head(20))

####################### Top Performing Schools (By Passing Rate) -----------------------------------------------------------
# sort values by passing rate and then only print top 5 schools
top_5 = school_summary.sort_values("Overall Passing Rate", ascending = False)
print(top_5.head(5))

####################### Bottom  Performing Schools (By Passing Rate) -----------------------------------------------------------
# sort values by passing rate and then only print worst 5 schools
bottom_5 = top_5.tail()
updated_bottom_5 = bottom_5.sort_values("Overall Passing Rate") #sorted based on overall passing rate in ascending order
print(updated_bottom_5.head(5))

###################### Math Scores by Grade --------------------------------------------------------------------------------
#creates grade level average math scores for each school 
ninth_math = students_df.loc[students_df['grade'] == '9th'].groupby('school_name')["math_score"].mean()
tenth_math = students_df.loc[students_df['grade'] == '10th'].groupby('school_name')["math_score"].mean()
eleventh_math = students_df.loc[students_df['grade'] == '11th'].groupby('school_name')["math_score"].mean()
twelfth_math = students_df.loc[students_df['grade'] == '12th'].groupby('school_name')["math_score"].mean()

math_scores = pdk.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
del math_scores.index.name # to remove the index name - school name#
print(math_scores.head(20))

###################### Reading Scores by Grade --------------------------------------------------------------------------------
#creates grade level average reading scores for each school 
ninth_math = students_df.loc[students_df['grade'] == '9th'].groupby('school_name')["reading_score"].mean()
tenth_math = students_df.loc[students_df['grade'] == '10th'].groupby('school_name')["reading_score"].mean()
eleventh_math = students_df.loc[students_df['grade'] == '11th'].groupby('school_name')["reading_score"].mean()
twelfth_math = students_df.loc[students_df['grade'] == '12th'].groupby('school_name')["reading_score"].mean()

reading_scores = pdk.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
del reading_scores.index.name # to remove the index name - school name#
print(reading_scores.head(20))

###################### Scores by School Spending --------------------------------------------------------------------------------
# create spending bins
bins = [0, 585, 615, 645, 675]
group_name = ["< $585", "$585 - 615", "$616 - 645", "> $645"]
school_data_complete['spending_bins'] = pdk.cut(school_data_complete['budget']/school_data_complete['size'], bins, labels = group_name)

# Calling the common function to prepare dataframe based on groupby string sent. This function returns dataframe
# with math, reading & overall passing score based on string passed as input parameter
scores_by_spend = score_by_func("spending_bins")
scores_by_spend.index.name = "Spending Ranges (Per Student)"
print(scores_by_spend.head(20))

###################### Scores by School Size --------------------------------------------------------------------------------
# create school size bins
size_bins = [0, 1000, 2000, 5000]
group_name = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
school_data_complete['school_size_bins'] = pdk.cut(school_data_complete['size'], size_bins, labels = group_name)

# Calling the common function to prepare dataframe based on groupby string sent. This function returns dataframe
# with math, reading & overall passing score based on string passed as input parameter
scores_by_size = score_by_func("school_size_bins")
scores_by_size.index.name = "School Size"
print(scores_by_size.head(20))

###################### Scores by School Type --------------------------------------------------------------------------------
# Calling the common function to prepare dataframe based on groupby string sent. This function returns dataframe
# with math, reading & overall passing score based on string passed as input parameter
scores_by_type = score_by_func("type")
scores_by_type.index.name = "Type of School"
print(scores_by_type.head(20))