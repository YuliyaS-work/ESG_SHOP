import pandas as pd

df = pd.read_excel('santeh.xls', engine='xlrd')
df.to_csv('santeh.csv', index=False)