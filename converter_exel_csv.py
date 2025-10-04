import pandas as pd

df = pd.read_excel('electro.xls', engine='xlrd')
df.to_csv('electro.csv', index=False)