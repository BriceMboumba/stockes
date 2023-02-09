import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# data generale description:
# Date: date
# Open: le cours d'ouverture de l'action
# High: le prix élevé du jour
# Low: le prix bas du jour
# Close: le cours de clôture du jour
# Adj Close: le cours de clôture du jour Ajusté
# Volume: Le nombre d'actions achetées et vendues par jour


def linear_regression(df, open_value, high_value, low_value, volume) -> float:
    # Printing statistical information of the dataset
    description = df.describe()
    # Checking for empty data fields in the dataset
    is_null = df.isnull().sum()
    # Checking data types of all column
    # information = df.info()

    # Dropping date column from our dataset
    df = df.drop(['stock_date', 'id'], axis=1)

    # Seperating Target variables and features
    # Target Variable
    y = df["close"]

    # Features
    x = df.drop(["close", "adj_close"], axis=1)

    # Spliting the data in 80%, 20% for training and testing
    # And normalize x in Gaustianne (0 or 1 value)
    xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size=0.2)

    # Making the model using LinearRegression()
    model = LinearRegression()
    # Fiting the training data in the model
    scoring = model.fit(xTrain, yTrain)

    # Making predictions using predict function and xTest data
    predictions = model.predict(xTest)

    # predict new value
    result_dict = {
        "open": [open_value],
        "high": [high_value],
        "low": [low_value],
        "volume": [volume]
    }
    # convert all value to a dataframe
    result = pd.DataFrame(result_dict)
    # result
    close_generated = model.predict(result)

    return round(close_generated.item(0), 2)