import requests, bs4, re, os

def cull_header_footer(text):
    return text.split("Resources\nForms")[-1].split("Financial Aid\n\nDeadlines")[0]

def scrape(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    text = re.sub(r'\n\n+', '\n\n', soup.text)

    for ref in soup.find_all('a'):
        new_url = ref.get('href')
        if (urls.count(new_url) == 0 and new_url != '' and urls[0] in new_url):
            urls.append(new_url)

    file_name = re.sub('https://', '', url)
    file_name = re.sub('/', '_', file_name)
    file_name = re.sub('\.', '-', file_name)
    
    try:
        #print(os.path.dirname(__file__))
        with open('{0}/results/{1}.txt'.format(os.path.dirname(__file__), file_name[0:-1]), 'w') as f:
            f.write(cull_header_footer(text))
        print('Scraped {0}'.format(url))
    except:
        print('Unable to scraped {0}'.format(url))

urls = ['https://finaid.utdallas.edu/']

for url in urls:
    scrape(url)

print(urls)