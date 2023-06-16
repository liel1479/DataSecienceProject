import pandas as pd

# Read the input files
df1 = pd.read_excel('output.xlsx', sheet_name='Sheet1', index_col=None)
df1 = df1.drop(columns=df1.columns[0])
df2 = pd.read_excel('benchmark.xlsx', sheet_name='Sheet1', index_col=None)
df2 = df2.drop(columns=df2.columns[0])

# Create a copy of the DataFrames
data = pd.DataFrame.copy(df1)
cpu_benchmark = pd.DataFrame.copy(df2)


# Function to get the CPU mark based on the processor model and type
def get_cpu_mark(row):
    processor_model = row['דגם מעבד']
    processor_type = row['סוג מעבד']
    matched_row = cpu_benchmark[cpu_benchmark['CPU_name'].str.contains(processor_model, case=False)]
    if not matched_row.empty:
        return matched_row['CPU_mark'].values[0]
    matched_row = cpu_benchmark[cpu_benchmark['CPU_name'].str.contains('Apple ' + processor_type, case=False)]
    if not matched_row.empty:
        return matched_row['CPU_mark'].values[0]
    else:
        return None


# Add CPU_mark column to data using apply function
data['CPU_mark'] = data.apply(lambda row: get_cpu_mark(row), axis=1)
data.to_excel("all_details.xlsx", index=False)
