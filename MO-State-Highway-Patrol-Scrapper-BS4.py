#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests


# In[2]:


url = 'https://www.mshp.dps.missouri.gov/HP68/SearchAction'


# In[3]:


r = requests.get(url)


# In[4]:


r.ok


# In[5]:


r.status_code


# In[6]:


r.content


# In[7]:


type(r.content)


# In[8]:


r.text


# In[9]:


type(r.text)


# In[10]:


with open('homepage.html', 'w') as f:
    f.write(r.text)


# In[11]:


r = requests.post(url, data = {'searchInjury': 'FATAL'})


# In[12]:


r.ok


# In[13]:


with open ('search-results.html', 'w') as f:
    f.write(r.text)


# In[14]:


from bs4 import BeautifulSoup


# In[15]:


soup = BeautifulSoup(r.text)


# In[16]:


type(soup)


# In[17]:


dir(soup)


# In[18]:


table = soup.find('table', class_ = 'accidentOutput')


# In[19]:


type(table)


# In[20]:


dir(table)


# In[21]:


th_all = table.find('thead').find_all('th')


# In[22]:


type(th_all)


# In[23]:


th_all


# In[24]:


headers = []

for th in th_all:
    header = th.text.strip().replace(' ', '_').lower()
    headers.append(header)


# In[25]:


headers


# In[26]:


tr_all = table.find_all('tr')[1:]


# In[27]:


len(tr_all)


# In[28]:


tr_all


# In[29]:


for tr in tr_all:
    print(tr.text)
    print ('-------------')


# In[50]:


def clean_row(tds):
    row = {
        'details_url': tds[0].find('a').attrs['href'],
        'name': tds[1].text.strip(),
        'age': int(tds[2].text.strip()),
        'person_city_state': tds[3].text.strip(),
        'personal_injury': tds[4].text.strip(),
        'date': tds[5].text.strip(),
        'time': tds[6].text.strip(),
        'crash_county': tds[7].text.strip(),
        'crash_location': tds[8].text.strip(),
        'troop': tds[9].text.strip(),
    }
    return row


# In[53]:


rows = []


# In[54]:


for tr in tr_all:
    tds = tr.find_all('td')
    row = clean_row(tds)
    rows.append(row)


# In[56]:


len(rows)


# In[57]:


rows


# In[58]:


import csv


# In[60]:


rows[0].keys()


# In[62]:


with open ('crashes.csv', 'w', newline = '') as f:
    writer = csv.DictWriter(
        f, fieldnames = rows[0].keys()
    )
    
    writer.writeheader()
    for row in rows:
        writer.writerow(row)


# In[ ]:




