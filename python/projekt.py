# -*- coding: utf-8 -*-

import pandas
import numpy
# %% Ładujemy plik od poczatku zmienna df w postaci DataFrame
df= pandas.read_csv('C:\\Users\mdawi\Desktop\Programowanie\python\EURUSD_H4.csv')
# %% Wybieramy 2500 początkowych rekordów
df = pandas.DataFrame(df[0:2500])
# %% Usuwamy kolumny oznaczone jako SMA14IND oraz SMA50IND; 
df.drop('SMA14IND', axis = 1, inplace = True)
df.drop('SMA50IND', axis = 1, inplace = True)
# %% Obliczamy ilosc wystąpień wartosci pustych w kolumnie Close
ilosc_NaN = df['Close'].isnull().sum()
print('W kolumnie Close znajduje się {} sztuk wartosci NaN'.format(ilosc_NaN))
# %% Usredniamy wartosci puste poprzez srednia dwóch najbliższych rekordów NaN.
df['Close'] = df['Close'].interpolate()
#Sposób z zmienną
#seria_close = df['Close']
#poprawiona_seria_close = seria_close.interpolate()

# Usredniamy wartosci puste poprzez srednia dwóch najbliższych rekordów NaN.
# Działanie wykonuję na kolumnie SMA14 oraz SMA50
df['SMA14'] = df['SMA14'].interpolate()
df['SMA50'] = df['SMA50'].interpolate()

# %% Uzupełniam wartosci puste zerami
df['Bulls'] = df['Bulls'].fillna(0)
# To jest w sumie zbędne.
"""
df['CCI'] = df['CCI'].fillna(0) # brak wartosci pustych
df['DM'] = df['DM'].fillna(0) # brak wartosci pustych
df['OSMA'] = df['OSMA'].fillna(0) # brak wartosci pustych
df['RSI'] = df['RSI'].fillna(0) # brak wartosci pustych
df['Stoch'] = df['Stoch'].fillna(0) # brak wartosci pustych   
df['Decision'] = df['Decision'].fillna(0) # brak wartosci pustych
"""
# Dla potwierdzona brak wartosci pustych w wszystkich kolumnach
print(df.isnull().sum())

# %% Korelacje
# Korelacja pomiędzy SMA14 i SMA50
k_SMA14_to_SMA50 = df['SMA14'].corr(df['SMA50'])
# Korelacja pomiędzy Close oraz SMA14
k_Close_to_SMA14 = df['Close'].corr(df['SMA14'])
# Korelacja pomiędzy Close oraz SMA50
k_Close_to_SMA50 = df['Close'].corr(df['SMA50'])

# %% Warunek usuwjący korelację o większej wartosci
if k_Close_to_SMA14 > k_Close_to_SMA50:
    df.drop('SMA14', axis = 1, inplace = True)
elif k_Close_to_SMA14 < k_Close_to_SMA50:
    df.drop('SMA50', axis = 1, inplace = True)

# %% Liczba elementów ujemnych dla atrybutu CCI

ujemnie_dla_CCI = df['CCI'].lt(0)
print(ujemnie_dla_CCI.sum())

# Liczba elementów ujemnych dla atrybutu CCI sposób z pętlą.

licznik = 0 
for i in df['CCI']:
    if i < 0:
        licznik += 1
print('Liczba elementów ujemnych dla atrybutu CCI wynosi {}'.format(licznik))

# %% Wartosc maksymalna oraz minimalna dla każdego atrybutu
for atrybuty in pandas.DataFrame(df):
    maksy = df.max()
    minimum = df.min()
print('Maksymalne wartosci dla wszystkich atrybutów:\n{}'.format(maksy ))
print('Minimalne wartosci dla wszystkich atrybutów:\n{}'.format(minimum))

# %% Wykonuję normalizację
    
wybrane_atrybuty = ['Close', 'SMA50']

for k in wybrane_atrybuty:
    maksy_wybrane = df[k].max()
    minimum_wybrane =  df[k].min()
    df[k] = (df[k] - minimum_wybrane) / (maksy_wybrane - minimum_wybrane)
# %%
       
# Dyskretyzacja dwóch kategorii

etykiety_dwie_kategorie = ['Up', 'Down']
seria_1 = pandas.Series(numpy.array(df['Bulls']))     
wynik_1 = pandas.cut(seria_1, 2, labels = etykiety_dwie_kategorie)

# Dyskretyzacja czterech kategori
"""
etykiety_cztery_kategorie = ['Upper', 'Up', 'Down', 'Downer']
seria_2 = pandas.Series(numpy.array(df['SMA50']))     
wynik_2 = pandas.cut(seria_2, 4, labels = etykiety_cztery_kategorie)
"""
# Dyskretyzacja przedziałowa mniej czytelny sposób
seria_2 = pandas.cut(pandas.Series(numpy.array(df['SMA50'])),4, labels = ['Upper', 'Up', 'Down', 'Downer'])
# %%
# Dyskretyzacja przedziałowa mniej czytelny sposób
# Info z wykładu bez zamieniania series na tablice na series
seria_3 = pandas.cut(df['SMA50'],4, labels = ['Upper', 'Up', 'Down', 'Downer'])
# Dla dyskretyzacji czestosciowej wykorzystujemy metode pandas.qcat


# %% Zliczam ile razy występuje dana wartosc w kolumnie Decision z użyciem Counter

from collections import Counter

print(Counter(df['Decision']))

lista_decision = Counter(df['Decision'])

zlicz = Counter(lista_decision)  


# %% Zliczam ile razy występuje dana wartosc w kolumnie Decision

kolumna_decyzja = df['Decision'].tolist()
print(kolumna_decyzja.count('BUY'))


v_buy = kolumna_decyzja.count('BUY')
v_sell = kolumna_decyzja.count('SELL')
v_strongbuy = kolumna_decyzja.count('STRONGBUY')
v_strongsell = kolumna_decyzja.count('STRONGSELL')
v_wait = kolumna_decyzja.count('WAIT')

pusta = [v_buy, v_sell, v_strongbuy, v_strongsell, v_wait]
etykiety = ['Bull', 'Sell', 'Strongbuy', 'Strongsell', 'Wait']

# %% Wykres kołowy

import matplotlib.pyplot as plt

fig, axes = plt.subplots()

axes.pie(pusta, labels=etykiety, autopct='%1.1f%%')
axes.set_title('Rozkład wartosci decyzji')
plt.savefig('result.png', dpi=300)
plt.show()

# %% Wykres liniowy 

""" Inny sposób, mniej dokładny
kolumna_close = df['Close']
wykres_liniowy = kolumna_close.plot.line(figsize=(20,8))
"""
x = df.index
y = df['Close'].tolist()

figure2, axes2 = plt.subplots()
axes2.plot(x, y, linewidth = 3.0,)
axes2.set(xlabel = 'Pomiar jednostkowy', ylabel = 'Wartosc Close')
axes2.set_title('Wykres zmiennosci atrybutu Close')
#axes2.figsize=(200,8)
plt.savefig('result2.png', dpi=(300))
plt.show()

# %% Zapisywanie dawnych do pliku w formacie JSON
import json

df.to_json('C:\\Users\\placz\\repos\\ue_3sem\\projekt_1.json', orient='split')

with open('projektunio.json', 'w') as file:
    for i in df:
        print(i, file=file)
 
      
# %% Projekt częsc 2

# %% Generuje losowe dane
import random

nowe_dane = []
z = random.random()
for i in range(2500):
    
    if z > random.uniform(z-z*0.01,z+z*0.01):
        z = z+z*0.01
    elif z < random.uniform(z-z*0.01,z+z*0.01):
        z = z+z*0.01
    else:
        z = random.uniform(z-z*0.01,z+z*0.01)
        
    nowe_dane.append(z)       
      

# %% Dodaje to głownego DataFrame'a tablice z losowo wygenerowanymi danymi
df['NoweDane'] = nowe_dane

# %% Obliczam korelacje danych z kolumny NoweDane do pozostałych atrybutów
kor_nowe_dane_df_to_Close = df['NoweDane'].corr(df['Close'])
kor_nowe_dane_df_to_SMA50 = df['NoweDane'].corr(df['SMA50'])
kor_nowe_dane_df_to_Bulls = df['NoweDane'].corr(df['Bulls'])
kor_nowe_dane_df_to_CCI = df['NoweDane'].corr(df['CCI'])
kor_nowe_dane_df_to_DM = df['NoweDane'].corr(df['DM'])
kor_nowe_dane_df_to_OSMA = df['NoweDane'].corr(df['OSMA'])
kor_nowe_dane_df_to_RSI = df['NoweDane'].corr(df['RSI'])
kor_nowe_dane_df_to_Stoch = df['NoweDane'].corr(df['Stoch'])

