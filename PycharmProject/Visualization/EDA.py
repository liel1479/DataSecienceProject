import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the DataFrame
df = pd.read_excel('all_details_cleaned.xlsx', sheet_name='Sheet1', index_col=None)


# Histograms
df.hist(figsize=(10, 8))
plt.tight_layout()
plt.show()

# Bar plots
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x="manufacturer")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='manufacturer', y='average_price', data=df)
plt.xlabel('Manufacturer')
plt.ylabel('Average Price')
plt.title('Average Price by Manufacturer')
plt.xticks(rotation=45)  # Rotate x-axis labels if needed
plt.show()

# Heatmap
plt.figure(figsize=(10, 7))
sns.heatmap(df.corr(), annot=True)
plt.show()

# Line plot: Price over time
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x="date_of_entry_to_Zap", y="average_price", hue="manufacturer")
plt.xlabel("Date of Entry to Zap")
plt.ylabel("Average Price")
plt.title("Price Over Time by Manufacturer")
plt.xticks(rotation=45)
plt.legend(loc="best")
plt.show()
