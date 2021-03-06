# -*- coding: utf-8 -*-
"""MODUL6-Python.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11K6YOegsQUv4E6Nkw3i7DCtZ4Fdw9jxd

# Modul 6 - Praca domowa - Python

Zwykle istnieje wiele sposobów, żeby rozwiązać zadanie w Python. Także czasami warto spróbować opracować kod na 1-2 sposoby :)

## Zadanie

<img src="https://bit.ly/2QvpWV7" width="800">

> Wykorzystaj [Źródło Danych od NASA](https://bit.ly/2EuNqqk) do znajdowania potencjalnie niebezpiecznych oraz bezpiecznych asteroid. Dane dotyczą Asteroid - NeoWs. NeoWs (Near Earth Object Web Service) to usługa internetowa dostępna dla informacji o asteroidach bliskich ziemi. Postępuj wg. kroków:

>1.   Wczytaj dane wykorzystując link: https://bit.ly/2CV8tlG
"""

# import bibliotek
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np

from sklearn import preprocessing
from sklearn import compose
from sklearn import covariance
from sklearn import impute
from sklearn import model_selection

#wczytanie danych i wyswietlenie 5 początkowych wierszy
URL = "https://bit.ly/2CV8tlG"
dane_nasa = pd.read_csv(URL)
dane_nasa.head(5)

dane_nasa.shape

""">2. Usuń cechy nieistotne, przykładowo:<br>**Reference ID, Name, Close Approach Date, Epoch Date Close Approach, Orbit Determination Date, Orbiting Body, Equinox**"""

#ununięcie nie istotnych cech
dane_2 = dane_nasa.drop(columns=["Neo Reference ID",
                                 "Est Dia in Miles(min)",
                                 "Est Dia in Miles(max)",
                                 "Est Dia in Feet(min)",
                                 "Est Dia in Feet(max)",
                                 "Close Approach Date",
                                 "Epoch Date Close Approach",
                                 "Miles per hour",
                                 "Miss Dist.(Astronomical)",
                                 "Miss Dist.(lunar)",
                                 "Miss Dist.(kilometers)",
                                 "Miss Dist.(miles)",
                                 "Orbit Determination Date",
                                 "Orbiting Body",
                                 "Minimum Orbit Intersection",
                                 "Jupiter Tisserand Invariant",
                                 "Epoch Osculation",
                                 "Eccentricity",
                                 "Semi Major Axis",
                                 "Orbital Period",
                                 "Equinox"])
dane_2.shape

""">3. Przygotuj podstawową analizę dotyczącą rozkładu cech oraz zależności między nimi."""

dane_2.describe(include ='all')

dane_2.columns

dane_2.info

dane_2.corr()

korelacja = dane_2.corr(method='pearson').abs()
print(korelacja)

kolumny = pd.Index(dane_2.columns[1:16]).tolist()
korelacja = dane_2[kolumny].corr()
korelacja.style.background_gradient( cmap="autumn_r")

kolumny = pd.Index(dane_2.columns[1:18]).tolist()
wykres_px = px.scatter_matrix(dane_2, dimensions=kolumny[1:-1], color= 'Absolute Magnitude')
wykres_px.update_layout(autosize=False, width=1400, height=1400)
wykres_px.show()

wykresy = dane_2
for column in wykresy.columns:
  wykres = px.histogram(wykresy[column], x= column, width=800, height=400)
  wykres.show()

# sprawdzenie wariancji
np.var(dane_2)

""">4. Spradź czy występują braki danych oraz wartości odstające, w razie potrzeby wyeliminuj problemy wykorzystując omawiane poprzednio podejścia (Lekcja 6 i 7)."""

print("Braki danych: ", dane_2[dane_2.isnull().any(axis=1)])

#nowy zestaw
dane_3 = dane_2.drop(columns= ["Name"])
print(dane_3)

dane_3.head()

for column in dane_3.columns:
  wykres = px.box(x= column, data_frame = dane_3, title = column, orientation = 'h', notched = True, width=800, height=400)   
  wykres.show()

from sklearn import covariance
# utworzenie detektora wartości odstających na podstawie elipsy wokół danych
detektor = covariance.EllipticEnvelope(contamination=0.1, support_fraction=1)
# użycie detektora
detektor.fit(dane_3)
# wykrywanie wartości odstających
flaga_odstajace = detektor.predict(dane_3)
flaga_odstajace

#Wyswietlenie wartosci odstajacych - pętla upraszcza :) -> mniej wysiłku
for i in dane_3.columns:
  wykres = px.scatter(dane_3, y= i, color=flaga_odstajace, width=700, height=350)
  wykres.show()

def IQR_outliers(a):
  Q1, Q3 = np.percentile(a, [25, 75])
  IQR = Q3 - Q1

  gorne_ograniczenie  = Q3 + (1.5 * IQR)
  dolne_ograniczenie  = Q1 - (1.5 * IQR)
  print("Górne ograniczenie:", gorne_ograniczenie)
  print("Dolne ograniczenie:", dolne_ograniczenie)

  indeksy = np.where((a > gorne_ograniczenie) | (a < dolne_ograniczenie))
  b = np.full(shape=a.shape[0], fill_value=1)
  b[indeksy] = -1
  
  return b

for i in dane_3.columns[:-1]:
  flaga_IQR = IQR_outliers(dane_3[i][0:])
  wykres_2 = px.scatter(dane_3, y=dane_3[i][0:], color=flaga_IQR, width=800, height=400)
  print(i, flaga_IQR, wykres_2.show())

dane_3.info()

for column in dane_3.columns:
  flaga_IQR = IQR_outliers(dane_3[column])
  print("Kolumna: \t", column, "\n", flaga_IQR, "\n")

# Usuwam wartości odstające
del_raw_1 = dane_3[dane_3["Absolute Magnitude"] == 32.1 ].index
del_raw_2 = dane_3[dane_3["Absolute Magnitude"] == 13.5 ].index

# Wartości usuwam z dane_3
dane_3.drop(del_raw_1 , inplace=True)
dane_3.drop(del_raw_2 , inplace=True)

# Usuwam wartości odstające
for i in dane_3.index: 
    if (dane_3['Est Dia in KM(min)'][i] > 0.584) | (dane_3['Est Dia in KM(min)'][i] < -0.297): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index: 
    if (dane_3['Est Dia in KM(max)'][i] > 1.306) | (dane_3['Est Dia in KM(max)'][i] < -0.664): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index: 
    if (dane_3['Est Dia in M(max)'][i] > 1306.756) | (dane_3['Est Dia in M(max)'][i] < -664.335): 
        dane_3.drop(index=i , inplace=True)

    if (dane_3['Relative Velocity km per sec'][i] > 32.5448) | (dane_3['Relative Velocity km per sec'][i] <  -6.034311022925): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index: 
    if (dane_3['Perihelion Distance'][i] > 1.5468159285733845) | (dane_3['Perihelion Distance'][i] < 0.0812453233971352): 
        dane_3.drop(index=i , inplace=True)

    if (dane_3['Perihelion Arg'][i] > 536.0050183415999) | (dane_3['Perihelion Arg'][i] < -168.60154554641338): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index: 
    if (dane_3['Relative Velocity km per hr'][i] > 117161.368) | (dane_3['Relative Velocity km per hr'][i] <  -21723.51968): 
        dane_3.drop(index=i , inplace=True)

    if (dane_3['Inclination'][i] > 41.33569228557059) | (dane_3['Inclination'][i] <  -16.86166986169293): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index:    
    if (dane_3['Mean Anomaly'][i] > 560.819) | (dane_3['Mean Anomaly'][i] < -197.28): 
        dane_3.drop(index=i , inplace=True) 

    if (dane_3['Mean Motion'][i] > 1.7817399641776035) | (dane_3['Mean Motion'][i] < -0.34378216968735376): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index: 
    if (dane_3['Aphelion Dist'][i] > 4.228840718818297) | (dane_3['Aphelion Dist'][i] < -0.5116107929318325): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index: 
    if (dane_3['Asc Node Longitude'][i] > 512.945) | (dane_3['Asc Node Longitude'][i] < -174.837): 
        dane_3.drop(index=i , inplace=True)

for i in dane_3.index: 
    if (dane_3['Perihelion Time'][i] >2458547.8966178712) | (dane_3['Perihelion Time'][i] < 2457375.480764561): 
        dane_3.drop(index=i , inplace=True)

""">5. Wyeliminuj mało istotne oraz silnie zależne cechy. Przeprowadź kodowanie cech kategorycznych, np. `Orbit ID`."""

dane_5 = pd.get_dummies(dane_3, columns=["Orbit ID"], prefix_sep="_")
pd.get_dummies(dane_5, columns=["Orbit Uncertainity"], prefix_sep="_")
#dane_5.head()

""">6. Podziel zbiór danych na zbiór uczący i testowy (proporcja `80%` i `20%` odpowiednio), definiując cechę `Hazardous` jako target/zmienną objaśnianą (Y)."""

# utworzenie zbioru cech objaśniających i zmiennej objaśnianej

zbior_cech = dane_5.drop("Hazardous", axis = 1)

X = zbior_cech
y = dane_5["Hazardous"]

dane_5["Hazardous"]

# tworzenie zbiorów test i train
from sklearn import model_selection
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y,test_size=.2, random_state=2020)

print("X train info: ")
X_train.info()
print("\nY trin info: ")
X_test.info()
print("\ny_train: \n", y_train)
print("\ny_test: \n", y_test)

""">7. Przprowadź standaryzację danych na podstawie zbioru uczącego."""

# zdefiniowanie standaryzatora
stand = preprocessing.StandardScaler()

# standaryzacja danych
stand_X_train = stand.fit_transform(X_train)
stand_X_test = stand.fit_transform(X_test)

print("Dane stand_X_train zestandaryzowane:\n", stand_X_train)
print("\n")
print("Średnia:", stand_X_train.mean(axis=0).round())
print("Odch. standardowe:", stand_X_train.std(axis=0))

print("\n\nDane stand_X_test zestandaryzowane:\n", stand_X_test)
print("\n")
print("Średnia:", stand_X_test.mean(axis=0).round())
print("Odch. standardowe:", stand_X_test.std(axis=0))

# rozkład pierwszej kolumny
ff.create_distplot([stand_X_train[:,0]], ["standaryzacja"])

""">8. Przygotuj model klasyfikatora binarnego wykorzystując `LogisticRegression()`. Oblicz współczynnik dokładności (AUC) dla zbioru testowego."""

from sklearn import linear_model
# wybranie algorytmu
algo = linear_model.LogisticRegression(n_jobs=-1)
# wyuczenie modelu
algo.fit(stand_X_train, y_train)

# predykcja na wyuczonym modelu
predykcja = algo.predict(stand_X_test)

# wyliczenie dokładności modelu
algo.score(stand_X_test, y_test)

from sklearn import metrics
# więcej metryk
print(metrics.classification_report(y_test, predykcja))

""">9. Przygotuj macierz błędów (confusion matrix). Ile asteroidów niebezpiecznych/bezpiecznych ze zbioru testowego zostało błędnie/prawidłowo zaklasyfikowano?"""

# macierz błędów
metrics.confusion_matrix(y_test, predykcja, labels=np.unique(y_test))

# macierz błędów - wizualizacja
metrics.plot_confusion_matrix(algo, stand_X_test, y_test, normalize="pred")
#plt.show()

""">10. Opracuj wykres krzywej `ROC` oraz oblicz współczynnik powierzchni pod krzywą `ROC` (`AUCROC`)."""

# pobranie prawdopodobieństwa z predykcji
pred_prawd = algo.predict_proba(X_test)[:,1]
#print(pred_prawd)
np.round(algo.predict_proba(X_test)[1,], decimals=2)

# wyliczenie metryk TPR(true positive rate) i FPR(false positive rate)
FP_value, TP_value, prog_prawd = metrics.roc_curve(y_test, pred_prawd)
# powierzchnia pod krzywą ROC
ROC_score = metrics.roc_auc_score(y_test, pred_prawd)
print(ROC_score)

# wykrwes krzywej ROC
import matplotlib.pyplot as plt
plt.plot(FP_value, TP_value, "b", label = "AUCROC = %0.2f" % ROC_score)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0, 1])
plt.ylim([0, 1])
plt.legend(loc = "upper left")
plt.ylabel("Wartości TPR")
plt.xlabel("Wartości FPR")
plt.title("Wykres krzywa ROC")
plt.show()

""">11. Przeprowadź proces walidacji krzyrzowej `cross_val_score()` (gdzie `n_splits=5`) wykorzystując cały zbiór danych przed podziałem na zbiór uczący i treningowy."""

print(X)
print(y)

np.unique(y.values)

from sklearn import pipeline
# utworzenie metody standaryzacji danych
standaryzacja = preprocessing.StandardScaler()
# wybranie metody modelowania
algo = linear_model.LogisticRegression()
# utworzenie procesu standaryzacji i wykorzystania algorytmu regresji liniowej
proces = pipeline.make_pipeline(standaryzacja, algo)
# ustawienia walidacji krzyżowej
walidacja = model_selection.KFold(n_splits=10, shuffle=True, random_state=2020)

# tworzenie modelu ze sprawdzeniem krzyżowym dokładności
model_selection.cross_val_score(proces, X, y, cv = walidacja, #None - domyślnie 5CV
                                scoring = "accuracy", 
                                n_jobs = -1).mean()

""">12. Porównaj wyniki modelu z/bez walidacji krzyrzowej, poprzez wyliczenie: **dokładności, pewności, precyzji i wskaźnika F1.** <br>
Wskazówka: przy podejściu walidacji krzyrzowej, są to wartości średnie.
"""

# METRYKI DLA MODELU BEZ WALIDACJI KRZYŻOWEJ:
print(metrics.classification_report(y_test, predykcja))

# tworzenie modelu ze sprawdzeniem krzyżowym dokładności
model_selection.cross_val_score(proces, X, y, cv = walidacja, #None - domyślnie 5CV
                                scoring = "accuracy", 
                                n_jobs = -1).mean()

# tworzenie modelu ze sprawdzeniem krzyżowym pewności
model_selection.cross_val_score(proces, 
                                X, 
                                y, 
                                cv = walidacja,
                                scoring = "recall", 
                                n_jobs = -1).mean()

# tworzenie modelu ze sprawdzeniem krzyżowym precyzji
model_selection.cross_val_score(proces, 
                                X, 
                                y, 
                                cv = walidacja,
                                scoring = "precision", 
                                n_jobs = -1).mean()

""">13. Sprawdź czy różni się poziom **pewności, precyzji i wskaźnik F1**, jeżeli uwzględnimy fakt nierówności liczby obserwacji w różnych klasach. Przykładowo, możesz to zrobić poprzez wykorzystanie: `cross_val_score(...scoring = "f1_weighted"...)` dla wskaźnika F1."""

# tworzenie modelu ze sprawdzeniem krzyżowym wskaźnika F1
model_selection.cross_val_score(proces, 
                                X, 
                                y, 
                                cv = walidacja,
                                scoring = "f1", 
                                n_jobs = -1).mean()

model_selection.cross_val_score(proces, 
                                X, 
                                Y, 
                                cv = walidacja,
                                scoring = "f1_macro", 
                                n_jobs = -1).mean()

# tworzenie modelu ze sprawdzeniem krzyżowym dokładności
model_selection.cross_val_score(algo, 
                                X, 
                                y, 
                                cv=10,
                                scoring = "accuracy", 
                                n_jobs = -1).mean()

# tworzenie modelu ze sprawdzeniem krzyżowym F1
model_selection.cross_val_score(algo, 
                                X, 
                                y, 
                                scoring = "f1_micro", 
                                n_jobs = -1).mean()

# tworzenie modelu ze sprawdzeniem krzyżowym F1
model_selection.cross_val_score(algo, 
                                X, 
                                y, 
                                scoring = "f1_weighted", 
                                n_jobs = -1).mean()

print(metrics.classification_report(y_test, predykcja))

""">14. Przeprowadź redukcję wymiarowości poprzez analizę głównych składowych PCA. Zredukuj liczbę zmiennych objaśniających do 3 wymiarów. Zwizualizuj przygotowane zmienne na wykresie 3D, dodając informację o przynależności do klasy `Hazardous`, np. poprzez zmianę koloru. Czy na wykresie widać jawne skupiska klas?<br> *Wskazówka: przykładowe metody do wizualizacji znajdziesz w Lekcji 7.*"""

from sklearn import decomposition
## Redukcja zbioru do 3 wymiarów
# tworzenie kompresora
kompresor_pca = decomposition.PCA(n_components=3)
# wyuczenie kompresora
fit_pca = kompresor_pca.fit(X)
# użycie kompresora
X_3D = fit_pca.transform(X)
print(X_3D)

print(dane_5["Hazardous"])

# wykres dla 3 wymiarów - 1
X_3D_df = pd.DataFrame(X_3D, columns=["x1", "x2", "x3"])
X_3D_df["Hazardous"] = y
wykres_3D = px.scatter_3d(X_3D_df,
                          x="x1",
                          y="x2",
                          z="x3",
                          color="Hazardous")
wykres_3D.show()

""">15. Podziel się wynikiem w grupie na [FB](https://bit.ly/2OSyHaG) podając hashtag `#modul6`."""