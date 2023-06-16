import re

import numpy as np
import pandas as pd

# Copy df
df1 = pd.read_excel('all_details.xlsx', sheet_name='Sheet1', index_col=None)
data = pd.DataFrame.copy(df1)

# Calculate the average price
data['lower_price'] = data['lower_price'].str.replace(',', '').astype(int)
data['higher_price'] = data['higher_price'].str.replace(',', '').astype(int)
data['average_price'] = (data['lower_price'] + data['higher_price']) / 2

# Drop irrelevant columns
cols_to_drop = ['סדרה', 'סוג מעבד', 'דגם מעבד', 'סוג הזכרון', 'סוג כונן קשיח',
                'כונן אופטי', 'רזולוציית מסך', 'סוג מסך', 'מצלמת רשת', 'כרטיס מסך',
                'תצורת 2 in 1', 'רשת אלחוטית', 'מודם סלולארי', 'crawling_time', 'lower_price', 'higher_price']
data = data.drop(cols_to_drop, axis=1)

# Change the col names to english
column_mapping = {
    'יצרן': 'manufacturer',
    'תאריך כניסה לזאפ': 'date_of_entry_to_Zap',
    'התאמה לגיימינג': 'gaming_Compatibility',
    'מערכת הפעלה': 'operating_system',
    'משקל': 'weight',
    'נפח זיכרון RAM': 'RAM_capacity',
    'מהירות מעבד': 'CPU_speed',
    'דור מעבד': 'CPU_generation',
    'נפח אחסון': 'storage_capacity',
    'גודל מסך': 'screen_size',
    'קצב רענון תצוגה': 'refresh_rate',
    'מסך מגע': 'touch_screen',
    'אמצעי אבטחה': 'security_features',
    'חיבורים': 'connections'
}
data.rename(columns=column_mapping, inplace=True)
# check the data
# data.info()
# print(data.describe(include='all'))
# print(data)
# print(data.isnull().sum())
# print(data.duplicated(subset=None).sum())

# convert objects to float
data['weight'] = data['weight'].apply(
    lambda x: float(re.findall(r'\d+(?:\.\d+)?', x)[0]) if re.findall(r'\d+(?:\.\d+)?', x) else None)
data['CPU_speed'] = data['CPU_speed'].apply(
    lambda x: float(re.findall(r'\d+(?:\.\d+)?', x)[0]) if re.findall(r'\d+(?:\.\d+)?', x) else None)
data['screen_size'] = data['screen_size'].apply(
    lambda x: float(re.findall(r'\d+(?:\.\d+)?', x)[0]) if re.findall(r'\d+(?:\.\d+)?', x) else None)

# convert objects to int
data['RAM_capacity'] = data['RAM_capacity'].apply(
    lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else None)
data['RAM_capacity'] = data['RAM_capacity'].astype('Int64')
data['CPU_generation'] = data['CPU_generation'].apply(
    lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else None)
data['CPU_generation'] = data['CPU_generation'].astype('Int64')
data['storage_capacity'] = data['storage_capacity'].apply(
    lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else None)
data['storage_capacity'] = data['storage_capacity'].astype('Int64')
data['refresh_rate'] = data['refresh_rate'].apply(
    lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else None)
data['refresh_rate'] = data['refresh_rate'].astype('Int64')
data['date_of_entry_to_Zap'] = data['date_of_entry_to_Zap'].apply(
    lambda x: int(re.findall(r'\d+', x)[0]) if re.findall(r'\d+', x) else None)
data['date_of_entry_to_Zap'] = data['date_of_entry_to_Zap'].astype('Int64')
data['CPU_mark'] = data['CPU_mark'].fillna('0').str.replace(',', '').astype('int64')
data['connections'] = [len(row.split(', ')) for row in data['connections']]

# convert objects to categorical
data['gaming_Compatibility'] = [1 if x == 'גיימינג' else 0 for x in data['gaming_Compatibility']]
data['gaming_Compatibility'] = data['gaming_Compatibility'].astype('category')
data['touch_screen'] = [1 if x in ['כולל', 'מסך מגע משני'] else 0 for x in data['touch_screen']]
data['touch_screen'] = data['touch_screen'].astype('category')
data['operating_system'] = data['operating_system'].apply(lambda x: 1 if x != 'ללא' else 0)
data['operating_system'] = data['operating_system'].astype('category')
data['security_features'] = [
    0 if x in ['לא כולל', 'לא רלוונטי', 'לא זמין'] else 1 for x in data['security_features']]
data['security_features'] = data['security_features'].astype('category')

# Remove outliers
new_df = data.copy()
numeric_cols = new_df.select_dtypes(include=np.number).columns
for col in numeric_cols:
    z_score = (data[col] - data[col].mean()) / data[col].std()
    outliers = abs(z_score) > 3
    new_df.loc[outliers, col] = np.nan

data_no_outliers = new_df

# check the data again
print(data_no_outliers.isnull().sum())
data_no_outliers.dropna(inplace=True)
print(data_no_outliers.isnull().sum())
print(data_no_outliers.duplicated(subset=None).sum())
data_no_outliers = data_no_outliers.drop_duplicates()
print(data_no_outliers.duplicated(subset=None).sum())
data_no_outliers.to_excel("all_details_cleaned.xlsx", index=False)

