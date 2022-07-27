import operator
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure
import datetime

# 1. soru / Veri setine göre uzun soluklu filmler hangi dilde oluşturulmuştur? Görselleştirme yapınız.
df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
plt.rcParams["figure.dpi"]=100
plt.rcParams["figure.autolayout"]=True
plt.rcParams.update({'font.size': '9'})

sumRuntime = 0;a=0
while True:
    sumRuntime += df["Runtime"][a]
    a += 1
    if a >= 584:
        a = 0
        break
avgRuntime = sumRuntime / 584
avgRuntime = round(avgRuntime)

df.groupby("Language").agg({"Runtime": "mean"}).sort_values(by="Runtime", ascending=False)
df_sorted = df.groupby("Language").agg({"Runtime": "mean"}).sort_values(by="Runtime", ascending=False).reset_index()
sns.lineplot(y=df_sorted["Language"], x=df_sorted.loc[(df_sorted["Runtime"] >= avgRuntime)]["Runtime"])

plt.show()

# 2. soru / 2019 Ocak ile 2020 Haziran tarihleri arasında 'Documentary' türünde çekilmiş filmlerin IMDB değerlerini
# bulup görselleştiriniz.

df=pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
df["Date"] = pd.to_datetime(df.Premiere)

df[(df["Genre"] == "Documentary") & (df["Date"] > "2019-01-01") & (df["Date"] <= "2020-06-30")]

file = df[(df["Genre"] == "Documentary") & (df["Date"] > "2019-01-01") & (df["Date"] <= "2020-06-30")]



print(df[(df["Genre"] == "Documentary") & (df["Date"] > "2019-01-01") & (df["Date"] <= "2020-06-30")])
plt.rcParams["figure.dpi"]=100
plt.rcParams["figure.autolayout"]=True
plt.rcParams.update({'font.size': '5'})
plt.plot(file["IMDB Score"],file.Title)
plt.title("2019 Ocak ile 2020 Haziran tarihleri arasında 'Documentary' türünde çekilmiş filmlerin IMDB değerleri")
plt.xlabel("IMDB Score")
plt.ylabel("Filmler")
plt.axis([0,9,0,53])
plt.show()

# 3. soru / İngilizce çekilen filmler içerisinde hangi tür en yüksek IMDB puanına sahiptir?

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
df_engOnly = df[df['Language'] == 'English'].sort_values(by="IMDB Score", ascending=False)
df_engOnly = df_engOnly.reset_index(level=None, drop=False, inplace=False, col_level=0, col_fill='')
print("İngilizce filmler arasında IMDB puanı en yüksek olan tür: ", df_engOnly["Genre"][0])

# 4. soru / 'Hindi' Dilinde çekilmiş olan filmlerin ortalama 'runtime' suresi nedir?

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
data3 = df[["Genre", "Title", "Runtime", "Language"]]
hindu_movie_meantime = data3[(data3["Language"] == "Hindi")].mean(numeric_only=True)

print(hindu_movie_meantime)

# 5. soru / 'Genre' Sütunu kaç kategoriye sahiptir ve bu kategoriler nelerdir? Görselleştirerek ifade ediniz.

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
kategori = {}
for i in df.index:
    column_values = df.loc[i, "Genre"].split("/")
    for j in range(len(column_values)):
        if column_values[j] in kategori:
            kategori[column_values[j]] += 1  # Language daha önce oluşturulmuşsa değerini 1 artır.
        else:
            kategori[column_values[j]] = 1  # Language yoksa sözlüğe oluştur ve değerini 1 yap

kategori = pd.DataFrame.from_dict(kategori, orient='index')
kategori.columns = ['adet']
kategori.sort_values(by="adet", ascending=False, inplace=True)

sayi = len(kategori)
fig1, ax1 = plt.subplots(figsize=(14, 7), dpi=256)
plt.xticks(rotation=90)
plt.tight_layout()
plt.rcParams.update({'font.size': '8'})
plt.rcParams["figure.autolayout"] = True
ax1.scatter(kategori.index, kategori["adet"])
ax1.set_title(str(sayi) + " adet kategorinin dağılımı", color='#003366', size=50);

plt.show()

# 6. soru / Veri setinde bulunan filmlerde en çok kullanılan 3 dili bulunuz

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
dil = {}
for i in df.index:
    column_values = df.loc[i, "Language"].split("/")
    for j in range(len(column_values)):
        if column_values[j] in dil:
            dil[column_values[j]] += 1  # Language daha önce oluşturulmuşsa değerini 1 artır.
        else:
            dil[column_values[j]] = 1  # Language yoksa sözlüğe oluştur ve değerini 1 yap

dil = pd.DataFrame.from_dict(dil, orient='index')
dil.columns = ['adet']
dil.sort_values(by="adet", ascending=False, inplace=True)
encokUcdil = dil.head(3)
sns.barplot(y=encokUcdil["adet"], x=encokUcdil.index, data=encokUcdil);
encokUcdil.plot.pie(y="adet", figsize=(5, 5))
plt.title("Veri setinde bulunan filmlerde en çok kullanılan 3 dil")

plt.show()

# 7. soru IMDB puanı en yüksek olan ilk 10 film hangileridir?

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
data4 = df[["Title", "IMDB Score"]]
maximum_ten_film = data4.sort_values(by='IMDB Score', ascending=False).head(10)

print(maximum_ten_film)

# 8. soru // IMDB puanı ile 'Runtime' arasında nasıl bir korelasyon vardır? İnceleyip görselleştiriniz.
import scipy.stats

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')

r, p = scipy.stats.pearsonr(df['IMDB Score'], df['Runtime'])

pearsoncorr = df.corr(method="pearson")
sns.heatmap(pearsoncorr,
            xticklabels=pearsoncorr.columns,
            yticklabels=pearsoncorr.columns,
            annot=True,
            linewidth=4)
plt.show()

# 9. soru IMDB Puanı en yüksek olan ilk 10 'Genre' hangileridir?

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
data5 = df[["Title", "Genre", "IMDB Score"]].sort_values(by='IMDB Score', ascending=False)

a = 0
genre = list(data5["Genre"])
imdb = list(data5["IMDB Score"])
d = np.column_stack((genre, imdb))
plt.xticks(rotation=90)
genre_imdb = []
genre_set = set()

for item in d:
    if item[0] not in genre_set:
        genre_set.add(item[0])
        genre_imdb.append(item)
    else:
        pass
genre_imdb = genre_imdb[:10]
a = 9
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.title("IMDB puanı en yüksek olan 10 Genre")
while True:
    plt.scatter(genre_imdb[a][0], genre_imdb[a][1], s=300)
    a -= 1
    if a < -1:
        a = 0
        break

plt.show()

# 10. soru / 'Runtime' değeri en yüksek olan ilk 10 film hangileridir? Görselleştiriniz.
# daha geniş olması için birkaç düzenleme
figure(num=None, figsize=(18.5, 10.5), dpi=144, facecolor='w', edgecolor='r')
plt.rcParams["figure.autolayout"] = True
plt.rcParams.update({'font.size': '18'})

# utf-8 encoding için çözümü böyle buldum ne kadar doğru bilmiyorum
data_set = pd.read_csv("NetflixOriginals.csv", encoding="ISO-8859-1")

# film isimlerini key, sürelerini de value'ya atadım,film sürelerine göre en uzundan en kısaya doğru sıraladım
f = dict(
    sorted((pd.Series(data_set.Runtime.values, index=data_set.Title).to_dict()).items(), key=operator.itemgetter(1),
           reverse=True))
########

movies = list(f.keys())
runtimes = list(f.values())
y = movies[:10]
y_pos = range(len(y))
x = runtimes[:10]
# film ve sürelerini ayrı list'lere ayırdım

plt.bar(range(len(y)), x, tick_label=y)
plt.xticks(y_pos, y, rotation=-90)
plt.title("The Longest 10 Movie")

plt.show()

# 11. soru / (Hangi yılda en fazla film yayımlanmıştır? Görselleştiriniz.)

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
day = []
month = []
year = []
for i in range(len(df)):
    x = df["Premiere"][i].split()
    ay = x[0]
    gun = int(x[1].strip(",").strip("."))
    yil = int(x[2])
    day.append(gun)

    if ay == "January":
        ay = 1
    elif ay == "February":
        ay = 2
    elif ay == "March":
        ay = 3
    elif ay == "April":
        ay = 4
    elif ay == "May":
        ay = 5
    elif ay == "June":
        ay = 6
    elif ay == "July":
        ay = 7
    elif ay == "August":
        ay = 8
    elif ay == "September":
        ay = 9
    elif ay == "October":
        ay = 10
    elif ay == "November":
        ay = 11
    elif ay == "December":
        ay = 12
    month.append(ay)
    year.append(yil)

df["gun"] = pd.Series(day)
df["ay"] = pd.Series(month)
df["yil"] = pd.Series(year)

data = df[["Genre", "IMDB Score", "yil", "ay", "gun"]]

film_count_years = data.groupby('yil')["Genre"].count()

names = list(film_count_years.keys())
values = list(film_count_years.values)
plt.xticks(rotation=90)
sns.barplot(y=values, x=names)

plt.ylabel("Yıl içinde çekilen film sayısı")
plt.xlabel("Yıl")
plt.rcParams["figure.autolayout"] = True

plt.show()

# 12. soru : (Hangi dilde yayımlanan filmler en düşük ortalama IMBD puanına sahiptir? Görselleştiriniz)

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
data6 = df[["Title", "Language", "IMDB Score"]]
film_avarage_imdb = data6.groupby('Language')["IMDB Score"].mean().tail(5)

names = list(film_avarage_imdb.keys())
values = list(film_avarage_imdb.values)
plt.xticks(rotation=90)
sns.barplot(y=values, x=names)
plt.xlabel("En düşük IMDB puanına sahip diller")
plt.rcParams["figure.autolayout"] = True

plt.show()

# 13. soru: (Hangi yılın toplam "runtime" süresi en fazladır?)

df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
day = []
month = []
year = []
for i in range(len(df)):
    x = df["Premiere"][i].split()
    ay = x[0]
    gun = int(x[1].strip(",").strip("."))
    yil = int(x[2])
    day.append(gun)

    if ay == "January":
        ay = 1
    elif ay == "February":
        ay = 2
    elif ay == "March":
        ay = 3
    elif ay == "April":
        ay = 4
    elif ay == "May":
        ay = 5
    elif ay == "June":
        ay = 6
    elif ay == "July":
        ay = 7
    elif ay == "August":
        ay = 8
    elif ay == "September":
        ay = 9
    elif ay == "October":
        ay = 10
    elif ay == "November":
        ay = 11
    elif ay == "December":
        ay = 12
    month.append(ay)
    year.append(yil)

df["gun"] = pd.Series(day)
df["ay"] = pd.Series(month)
df["yil"] = pd.Series(year)

data = df[["Runtime", "yil"]]

film_sum_runtime = data.groupby('yil')["Runtime"].sum()
names = list(film_sum_runtime.keys())
values = list(film_sum_runtime.values)
plt.xticks(rotation=90)
sns.barplot(y=values, x=names)
plt.ylabel("Runtime süresi")
plt.xlabel("Yıl")
plt.rcParams["figure.autolayout"] = True

plt.show()

# 14. soru / Her bir dilin en fazla kullanıldığı "Genre" nedir?
df = pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
df.groupby(["Language"])["Genre"].value_counts(sort=True).groupby(level=0).head(1)

#%% soru-15 Veri setinde outlier veri var mıdır? Açıklayınız.)
# veri setinde runtime değerine göre analiz yapıldığında outlier değerlerinin olduğu görülmüştür.
# Üst sınır 141  alt sınır ise 53 olarak belirlenmiştir. Bu değerlerin dışında kalan değerler aykırı değer olarak belirlenmiştir.
df=pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
df=df.copy()
df=df.select_dtypes(include=["float64","int64"])

df_table=df["Runtime"].copy()

sns.boxplot(x=df_table)

Q1=df_table.quantile(0.25)
Q3=df_table.quantile(0.75)
IQR=Q3-Q1

alt_sinir=Q1-1.5*IQR
ust_sinir=Q3+1.5*IQR
print("alt sınır:"+str(alt_sinir))
print("üst sınır:"+str(ust_sinir))
outliers=(df_table<(alt_sinir)) | (df_table>(ust_sinir))

outliers=df_table[outliers]

plt.show()
#%% soru-15(Devam) veri setinde IMDB Score değerine göre analiz yapıldığında outlier değerlerinin olduğu görülmüştür.
# Üst sınır 8.95  alt sınır ise 3.75 olarak belirlenmiştir. Bu değerlerin dışında kalan değerler aykırı değer olarak belirlenmiştir.
df=pd.read_csv("NetflixOriginals.csv", encoding='ISO-8859-1')
df=df.copy()
df=df.select_dtypes(include=["float64","int64"])
df_table=df["IMDB Score"].copy()
sns.boxplot(x=df_table)
Q1=df_table.quantile(0.25)
Q3=df_table.quantile(0.75)
IQR=Q3-Q1

alt_sinir=Q1-1.5*IQR
ust_sinir=Q3+1.5*IQR
print("alt sınır:"+str(alt_sinir))
print("üst sınır:"+str(ust_sinir))
outliers=(df_table<(alt_sinir)) | (df_table>(ust_sinir))

outliers=df_table[outliers]

plt.show()


