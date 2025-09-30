import pandas as pd

df = pd.read_excel('gas.xls', engine='xlrd')
df.to_csv('gas.csv', index=False)