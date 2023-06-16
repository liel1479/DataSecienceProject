import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# Load the data
df = pd.read_excel('all_details_cleaned.xlsx', sheet_name='Sheet1', index_col=None)

# Separate features and target variable
X = df.drop(["average_price", "manufacturer"], axis=1)  # Features
y = df["average_price"]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Linear Regression
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
lr_predictions = lr.predict(X_test_scaled)
lr_r2 = r2_score(y_test, lr_predictions)
mse = mean_squared_error(y_test, lr_predictions)
print("Linear Regression results:")
print("R^2 Score:", lr_r2)
print("Mean Squared Error (MSE):", mse)

# First
# Calculate the difference between predicted and actual values
residuals = lr_predictions - y_test

# Assign colors to point based on the difference
colors = np.where(residuals >= 0, 'g', 'r')

# Create scatter plot of predicted vs actual values with colors
plt.scatter(y_test, lr_predictions, c=colors)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Linear Regression: Actual vs Predicted Prices")
# Add the linear regression line with colors
plt.plot(y_test, y_test, color='blue', linewidth=3)
plt.fill_between(y_test, y_test, lr_predictions, where=(lr_predictions >= y_test), facecolor='green', alpha=0.3)
plt.fill_between(y_test, y_test, lr_predictions, where=(lr_predictions == y_test), facecolor='pink', alpha=0.3)
plt.fill_between(y_test, y_test, lr_predictions, where=(lr_predictions < y_test), facecolor='red', alpha=0.3)
plt.show()

# second
# Create scatter plot of predicted vs actual values
plt.scatter(y_test, lr_predictions, color='black')
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Linear Regression: Actual vs Predicted Prices")

# Add the linear regression line
plt.plot(y_test, y_test, color='blue', linewidth=3)
plt.show()

# k-Nearest Neighbors (k-NN)
knn = KNeighborsRegressor(n_neighbors=11)
knn.fit(X_train_scaled, y_train)
knn_predictions = knn.predict(X_test_scaled)
knn_r2 = r2_score(y_test, knn_predictions)
mse = mean_squared_error(y_test, knn_predictions)
print("k-NN results:")
print("R^2 Score:", knn_r2)
print("Mean Squared Error (MSE):", mse)

# Decision Tree
dt = DecisionTreeRegressor()
dt.fit(X_train, y_train)
dt_predictions = dt.predict(X_test)
dt_r2 = r2_score(y_test, dt_predictions)
mse = mean_squared_error(y_test, dt_predictions)
print("Decision Tree results:")
print("R^2 Score:", dt_r2)
print("Mean Squared Error (MSE):", mse)

# Random Forest Regression
rf = RandomForestRegressor(random_state=42)
rf.fit(X_train, y_train)
rf_predictions = rf.predict(X_test)
rf_r2 = r2_score(y_test, rf_predictions)
mse = mean_squared_error(y_test, rf_predictions)
print("Random Forest results:")
print("R^2 Score:", rf_r2)
print("Mean Squared Error (MSE):", mse)


# Plot actual vs predicted values
plt.scatter(y_test, rf_predictions, alpha=0.5)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs. Predicted Values (Random Forest Regression)")
plt.show()

# Plot actual vs predicted values with colors
plt.scatter(y_test, rf_predictions, c=y_test, cmap='coolwarm', alpha=0.5)
plt.colorbar()
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs. Predicted Values (Random Forest Regression)")
plt.show()
