import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


print('doing webscraping please wait')
res = requests.get('https://ontheworldmap.com/all/cities/')
res = BeautifulSoup(res.text, 'html.parser')

res = res.find('div',attrs={'class':'col-3'})

cities = []
populations = []
for i in res.find_all('a', href=True):
    cities.append(f"https:{i['href']}")
for i in cities:
    res = requests.get(i)
    res = BeautifulSoup(res.text, 'html.parser')
    res = res.find('div',attrs={'class':'map-desc'}).text.split('\n')
    for j in res:
        if (j.find('Population: ~ ')) == 0:
            _, population = j.split('~ ')
            population, _ = population.split('.')
            try:
                population, _ = population.split(' (')
            except:
                pass
            populations.append(population.replace(',',''))

print("done")
populations = [int(i) for i in populations]

zero_to_thousand = [i for i in populations if i<1_000]
thousand_to_ten_thousand = [i for i in populations if i>1_000 and i<10_000]
ten_thousand_to_hundred_thousand = [i for i in populations if i>10_000 and i<100_000]
hundred_thousand_to_mil = [i for i in populations if i>100_000 and i<1_000_000]
mil_to_ten_mil = [i for i in populations if i>1_000_000 and i<10_000_000]
ten_mil_to_hundred_mil = [i for i in populations if i>10_000_000 and i<100_000_000]


data = {'under thousand':len(zero_to_thousand), 'thousand to 10 thousand':len(thousand_to_ten_thousand), '10 thousand to 100 thousand':len(ten_thousand_to_hundred_thousand), '100 thousand to mil':len(hundred_thousand_to_mil), 'mil to ten mil':len(mil_to_ten_mil), 'ten mil to 100 mil':len(ten_mil_to_hundred_mil)}
part = list(data.keys())
population_data = list(data.values())

fig, ax = plt.subplots(1,1, figsize=(10, 7))

plt.xticks(rotation=15)

bars = plt.bar(part, population_data, color ='maroon',width = 0.5)
ax.bar_label(bars)
 
plt.ylabel("number of cities this big")
plt.title("population of cities")
plt.show()  