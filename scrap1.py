# import re
# from googlesearch import search
# import warnings
# warnings.filterwarnings("ignore")
# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import threading
# import time

# def scrapper(query:str):
#     try:
#         dis_str = ""
#         results = search(query, num=10, stop=10, pause=5)
#         for sr in results:
#             match=re.search(r'wikipedia',sr)
#             if match:
#               wiki = requests.get(sr,verify=False)
#               soup = BeautifulSoup(wiki.content, 'html5lib')
#               info_table = soup.find("table", {"class":"infobox"})
#               if info_table is not None:
#                 for row in info_table.find_all("tr"):
#                   left=row.find("th",{"scope":"row"})
#                   right=row.find("td")
#                   if left is not None:
#                     dis_str+=left.get_text()+":" + right.get_text()+"\n"
#               break  
#         with open(f'F:/IR project/Disease-Detection-based-on-Symptoms/corpus/{query}.txt','w',encoding='utf-8') as file:
#            file.write(dis_str)
#     except Exception as e:
#        print(e)

# df = pd.read_csv('F:/IR project/Disease-Detection-based-on-Symptoms/Dataset/dis_sym_dataset_norm.csv')
# diseases = list(df['label_dis'])

# threads = []

# for i in diseases:
#     thread = threading.Thread(target=scrapper, args=(i,))
#     threads.append(thread)
#     thread.start()
#     break

# for thread in threads:
#     thread.join()

# print("All threads have finished processing.")

import re
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp

# async def fetch_info(query):
#     try:
#         async with aiohttp.ClientSession() as session:
#             dis_str = ""
#             results = search(query + ' ' + ' wikipedia', num=2, stop=2, pause=0.5)
#             for sr in results:
#                 # print('1:',sr)
#                 match = re.search(r'wikipedia', sr)
#                 if match:
#                     async with session.get(sr, verify_ssl=False) as response:
#                         if response.status == 200:
#                             html = await response.text()
#                             soup = BeautifulSoup(html, 'html5lib')
#                             info_table = soup.find("table", {"class": "infobox"})
#                             if info_table is not None:
#                                 for tr in info_table.find_all("tr"):
#                                     th = tr.find("th")
#                                     td = tr.find("td")
#                                     if th and td:
#                                         dis_str += th.get_text(strip=True) + ": " + td.get_text(strip=True) + "\n"
#                                 break
#                         else:
#                             print(f"Failed to retrieve data for {query}. Status code: {response.status}")
#             if dis_str:
#                 with open(f'F:/IR project/Disease-Detection-based-on-Symptoms/corpus/{query}.txt', 'w',
#                           encoding='utf-8') as file:
#                     file.write(dis_str)
#                     print(f"Data successfully scraped for {query}.")
#             else:
#                 print(f"No infobox found for {query}.")
#     except Exception as e:
#         print(f"Error fetching data for {query}: {e}")

# async def main():
#     df = pd.read_csv('F:/IR project/Disease-Detection-based-on-Symptoms/Dataset/dis_sym_dataset_norm.csv')
#     diseases = list(df['label_dis'])
#     tasks = []
#     for i in diseases[12:]:
#         tasks.append(fetch_info(i))
#     await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     asyncio.run(main())


async def fetch_info(sem, query):
    try:
        async with sem:
            async with aiohttp.ClientSession() as session:
                dis_str = ""
                results = search(query + ' ' + ' wikipedia', num=1, stop=1, pause=5)  # Adjust num to limit search results
                for sr in results:
                    match = re.search(r'wikipedia', sr)
                    if match:
                        async with session.get(sr, verify_ssl=False) as response:
                            if response.status == 200:
                                html = await response.text()
                                soup = BeautifulSoup(html, 'html5lib')
                                info_table = soup.find("table", {"class": "infobox"})
                                if info_table is not None:
                                    for tr in info_table.find_all("tr"):
                                        th = tr.find("th")
                                        td = tr.find("td")
                                        if th and td:
                                            dis_str += th.get_text(strip=True) + ": " + td.get_text(strip=True) + "\n"
                                    break
                            else:
                                print(f"Failed to retrieve data for {query}. Status code: {response.status}")
                if dis_str:
                    with open(f'F:/IR project/Disease-Detection-based-on-Symptoms/corpus/{query}.txt', 'w', encoding='utf-8') as file:
                        file.write(dis_str)
                        print(f"Data successfully scraped for {query}.")
                else:
                    print(f"No infobox found for {query}.")
    except Exception as e:
        print(f"Error fetching data for {query}: {e}")

async def main():
    df = pd.read_csv('F:/IR project/Disease-Detection-based-on-Symptoms/Dataset/dis_sym_dataset_norm.csv')
    diseases = list(df['label_dis'])
    sem = asyncio.Semaphore(5)  # Limit the number of concurrent requests
    tasks = [fetch_info(sem, query) for query in diseases[12:]]  # Adjust starting index
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
