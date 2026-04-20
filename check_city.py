import pandas as pd
df = pd.read_csv('dataset/retail_sales.csv')
city = df.groupby('Place')['Total Amount'].sum().sort_values(ascending=False)
print("City revenues:")
print(city.to_string())
print("\nTop city:", city.idxmax())
