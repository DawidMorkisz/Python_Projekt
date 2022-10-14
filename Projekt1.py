import os
import pandas as pd

#pobeiranie pierwszych 2500 elementów z pliku
Relative_Path = os.path.join(os.path.dirname(__file__),'EURUSD_H4 - EURUSD_H4.csv')
File = pd.read_csv(Relative_Path,nrows=2500)
df = pd.DataFrame(File)

#usunięcie koluomn SMA14IND i SMA50IND
df = df.drop(['SMA14IND','SMA50IND'], axis=1)

#zliczneie wartości NaN i uśrednienie kolumny Close
Number_of_NaNs=df['Close'].isna().sum()
df['Close']=df['Close'].interpolate(method ='linear', limit_direction ='forward')

df[['Bulls','CCI','DM','OSMA','RSI','Stoch','Decision']]=df[['Bulls','CCI','DM','OSMA','RSI','Stoch','Decision']].fillna(value=0)

print(df)
print("Number of NaNs: ",Number_of_NaNs)
