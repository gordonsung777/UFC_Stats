from cmath import inf
from bs4 import BeautifulSoup
import requests
from csv import writer
import pandas as pd
#%matplotlib inline
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(palette="Paired")
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.backends.backend_pdf


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)  Chrome / 104.0.0.0 Safari / 537.36'
}

url = "https://www.ufc.com/athletes/all?gender=All&search=&page="

not_empty = True
end_page = 500
start_page = 1

f = open(r"UFCstats.csv", 'a', encoding='utf8', newline='')
csv_writer = writer(f)

header = ['Nickname', 'Fullname', 'Weight', 'Record','totalwins', 'totalloss', 'totaldraws', 'totalfights']
csv_writer.writerow(header)

while not_empty:
    pages = np.arange(start_page, end_page, 1)
    
    for page in pages:

        url1 = url + str(page)
        page = requests.get(url1)

        soup = BeautifulSoup(page.content, 'html.parser')
        '''sleep(randint(2,8))'''

        lists = soup.find_all('div', class_="c-listing-athlete__text")
        if len(lists) > 0:
            

            for athlete_card in lists:
                nickname = ""
                fullname = ""
                weight = ""
                record = ""
                winPercentage =[]
                totalwins=""
                totalloss=""
                totaldraws=""
                totalfights=""
                
              

                athlete_name = athlete_card.find('span', class_="c-listing-athlete__nickname")
                if athlete_name is not None:
                    nickname = athlete_name.text.strip()
                athlete_fullname = athlete_card.find('span', class_="c-listing-athlete__name")
                if athlete_fullname is not None:
                    fullname = athlete_fullname.text.strip()
                athlete_weight = athlete_card.find('span', class_="c-listing-athlete__title")
                if athlete_weight is not None:
                    weight = athlete_weight.text.strip()
                athlete_record = athlete_card.find('span', class_="c-listing-athlete__record")
                if athlete_record is not None:
                    record = athlete_record.text.strip()

                values = re.findall(r'\d+|[WDL]', record)
                vdict = dict(zip(values[3:], values[:3]))
                totalwins=vdict["W"]
                totalloss=vdict["L"]

                totaldraws=vdict["D"]


            
        

                info = [nickname, fullname, weight, record,totalwins, totalloss, totaldraws, totalfights]
                totalfights = str(int(info[4])+int(info[5])+int(info[6]))

                info = [nickname, fullname, weight, record,totalwins, totalloss, totaldraws, totalfights]
                if len(info) != 0:
                    print([nickname, fullname, weight, record,totalwins, totalloss, totaldraws,totalfights])

                    csv_writer.writerow(info)
            
        else:
            not_empty = False
            break
f.close()

data_frame = pd.read_csv("UFCstats.csv")

data_frame.head(3000)
df = pd.DataFrame(columns=["totalwins","totalloss"], data=data_frame.head(3000))
pdf = matplotlib.backends.backend_pdf.PdfPages('pic.pdf')

for ind in df.index:
    fig, ax = plt.subplots(1,1)
    fig.set_size_inches(5,5)
    df.iloc[ind].plot(kind='pie', ax=ax, shadow=True, title=data_frame.iloc[ind]["Fullname"], explode=[0.03,0.03], autopct='%1.1f%%')
    ax.set_ylabel("total wins are " + str(data_frame.iloc[ind]["totalwins"]))
    ax.set_xlabel("total losses are " + str(data_frame.iloc[ind]["totalloss"]))
    pdf.savefig(fig)
pdf.close()    
plt.show()
