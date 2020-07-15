import os
import requests # to sent GET requests
from bs4 import BeautifulSoup # to parse HTML
import tkinter as tk
from tkinter import simpledialog

yahoo_img = \
    'https://in.images.search.yahoo.com/search/images;_ylt=AwrwJSJD2Q1fTlkATCK8HAx.;_ylc=X1MDMjExNDcyMzAwNARfcgMyBGZyAwRncHJpZAN6VDFjeUl0WlFfLnRqMGU1YlNTTGVBBG5fc3VnZwMxMARvcmlnaW4DaW4uaW1hZ2VzLnNlYXJjaC55YWhvby5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMEcXN0cmwDNARxdWVyeQNkb2dzBHRfc3RtcAMxNTk0NzQzMTEw?fr2=sb-top-in.images.search&'

user_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}
save_folder = 'imagesdl'

 

def main():
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    download_images()


ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
data = USER_INP = simpledialog.askstring(title="Test",
                                  prompt="What are you looking for ?:")

# check it out
print("searching web for", USER_INP)

     
def download_images():
     
    #data = input('What are you looking for? ')
    n_images = int(input('How many images do you want? '))

    print('Start searching for ',USER_INP)
   
    # get url query string
    searchurl = yahoo_img + 'q=' + data
    #print(searchurl)

    # request url, without user_agent the permission gets denied
    response = requests.get(searchurl, headers=user_agent)
    html = response.text
    #print(html)
    # find all divs where class='rg_i Q4LuWd tx8vtf'
    soup = BeautifulSoup(html, 'html.parser')
    #soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), 'lxml')
    #print(soup.prettify)
    #results = soup.find_all('div', class_= 'jsaction',limit=n_images)
    results = soup.find_all('img',class_= 'process',limit=n_images)


    # extract the link from the img tag
    
    imagelinks= []
    
    for re in results:
        url1=re.attrs.get('data-src')
        imagelinks.append(url1)
#        if url1==None:
#            url1=re.attrs.get('src')
#            imagelinks.append(url1) 
#        else:
#            imagelinks.append(url1) 
                

    #print(imagelinks)
    print(f'found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        # open image link and save as file
        response = requests.get(imagelink)
        
        imagename = save_folder + '/' + data + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Done')


if __name__ == '__main__':
    main()
