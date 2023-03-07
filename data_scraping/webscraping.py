import requests, bs4, re, os

def cull_header_footer(text):
    return text.split("Resources\nForms")[-1].split("Financial Aid\n\nDeadlines")[0]

def scrape(url):
    # Parse get webpage and parse its HTML
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    text = re.sub(r'\n\n+', '\n\n', soup.text)

    # Crawling link to find all subpages stemming from this link
    for ref in soup.find_all('a'):
        new_url = ref.get('href')
        # Removes bad links, links already found while crafting, and .pdfs
        if (new_url and urls.count(new_url) == 0 and new_url != '' and urls[0] in new_url):
            urls.append(new_url)

    file_name = re.sub('https://', '', url)
    file_name = re.sub('/', '_', file_name)
    file_name = re.sub('\.', '-', file_name)
    
    try:
        #print(os.path.dirname(__file__))
        with open('{0}/results/{1}.txt'.format(os.path.dirname(__file__), file_name[0:-1]), 'w') as f:
            f.write(cull_header_footer(text))
        print('Scraped {0}'.format(url))
        return len(text)
    except:
        print('Unable to scrape {0}'.format(url))
        return 0

urls = ['https://finaid.utdallas.edu/']
char_count = 0

for url in urls:
    char_count += scrape(url)

print('Approx. {0} tokens will be needed to train a Chat GPT-3 off of this information'.format(char_count / 4))