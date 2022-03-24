import requests
import functools
import shutil
import codecs
import sys
import os

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# URL of the web page you want to extract data from
url = "https://google.com"
use_tor_network = False


if len(sys.argv) > 1: url = sys.argv[1]
output_folder = urlparse(url).netloc

# initialize a session
session = requests.session()
if use_tor_network:
    session.request = functools.partial(session.request, timeout=30)
    session.proxies = {'http':  'socks5h://localhost:9050',
                        'https': 'socks5h://localhost:9050'}

# define workspace from script location
workspace = os.path.dirname(os.path.realpath(__file__))

class Extractor:
    def __init__(self, url):
        self.url = url
        self.soup = BeautifulSoup(self.get_page_content(url), "html.parser")

        self.scraped_urls = self.scrap_all_urls()
    
    def run(self):
        self.save_files(self.scraped_urls)
        self.save_html()
    
    def get_page_content(self, url):
        try: 
            content = session.get(url)
            content.encoding = 'utf-8'
            return content.text
        except: return None

    # get the script files    
    def scrap_scripts(self):
        script_urls = []
        for script_tag in self.soup.find_all("script"):
            # if the tag has the attribute 'script'
            script_url = script_tag.attrs.get("src")
            if script_url:
                if not script_url.startswith('http'): script_url = urljoin(self.url, script_url)
                else: continue

                new_url = self.url_to_local_path(script_url, keepQuery=True)

                if new_url:
                    script_tag['src'] = new_url
                    script_urls.append(script_url.split('?')[0])
        
        return list(dict.fromkeys(script_urls))

    #  get attributes
    def scrap_form_attr(self):
        urls = []
        for form_tag in self.soup.find_all("form"):
            # if the tag has the attribute 'action'
            form_url = form_tag.attrs.get("action")
            if form_url:
                if not form_url.startswith('http'): form_url = urljoin(self.url, form_tag.attrs.get("action"))

                new_url = self.url_to_local_path(form_url, keepQuery=True)

                if new_url:
                    form_tag['action'] = new_url

                    urls.append(form_url.split('?')[0])

        return list(dict.fromkeys(urls))

    def scrap_a_attr(self):
        urls = []
        for link_tag in self.soup.find_all('a'):
            # if the tag has the attribute 'href'
            link_url = link_tag.attrs.get('href')
            if link_url:
                if not link_url.startswith('http'): link_url = urljoin(self.url, link_tag.attrs.get('href'))

                new_url = self.url_to_local_path(link_url, keepQuery=True)
                if new_url:
                    link_tag['href'] = new_url
                    urls.append(link_url.split('?')[0])

        return list(dict.fromkeys(urls))          
                

    def scrap_img_attr(self):
        urls = []
        for img_tag in self.soup.find_all('img'):
            # if the tag has the attribute 'src'
            img_url = img_tag.attrs.get('src')
            if img_url:
                if not img_url.startswith('http'): img_url = urljoin(self.url, img_tag.attrs.get('src'))

                new_url = self.url_to_local_path(img_url, keepQuery=True)
                if new_url:
                    img_tag['src'] = new_url
                    urls.append(img_url.split('?')[0])

        return list(dict.fromkeys(urls))
    
    def scrap_link_attr(self):
        urls = []
        for link_tag in self.soup.find_all('link'):
            # if the tag has the attribute 'href'
            link_url = link_tag.attrs.get('href')
            if link_url:
                if not link_url.startswith('http'): link_url = urljoin(self.url, link_tag.attrs.get('href'))

                new_url = self.url_to_local_path(link_url, keepQuery=True)
                if new_url:
                    link_tag['href'] = new_url
                    urls.append(link_url.split('?')[0])

        return list(dict.fromkeys(urls))
    
    def scrap_btn_attr(self):
        urls = []
        for buttons in self.soup.find_all('button'):
            button_url = buttons.attrs.get('onclick')
            if not button_url: return None

            button_url = button_url.replace(' ','')
            button_url = button_url[button_url.find('location.href='):].replace('location.href=','')
            button_url = button_url.replace('\'', '')
            button_url = button_url.replace('\"', '')
            button_url = button_url.replace('`', '')

            if button_url and button_url.startswith('/'):
                if not button_url.startswith('http'): button_url = urljoin(self.url, buttons.get('onclick'))

                new_url = self.url_to_local_path(button_url, keepQuery=True)
                if new_url:
                    buttons['onclick'] = new_url
                    urls.append(button_url.split('?')[0])

        return list(dict.fromkeys(urls))
                

    # get assets (img and more)
    def scrap_assets(self):
        assets_urls = []

        form_attr = self.scrap_form_attr()
        a_attr = self.scrap_a_attr()
        img_attr = self.scrap_img_attr()
        link_attr = self.scrap_link_attr()
        btn_attr = self.scrap_btn_attr()
        
        if form_attr: assets_urls = list(set(assets_urls + form_attr))
        if a_attr: assets_urls = list(set(assets_urls + a_attr))
        if img_attr: assets_urls = list(set(assets_urls + img_attr))
        if link_attr: assets_urls = list(set(assets_urls + link_attr))
        if btn_attr: assets_urls = list(set(assets_urls + btn_attr))

        return assets_urls

    # scrap every urls
    def scrap_all_urls(self):
        urls = []
        urls.extend(self.scrap_scripts())
        urls.extend(self.scrap_assets())
        return list(dict.fromkeys(urls))
    
    # convert url to into local path
    def url_to_local_path(self, url, keepQuery=False):
        try:
            new_url = urlparse(url).path
            query = urlparse(url).query
            if keepQuery and query: new_url += '?' + urlparse(url).query
            if (new_url[0] == '/') or (new_url[0] == '\\'): new_url = new_url[1:]
        except:
            return None

        return new_url

    # download file from URL
    def download_file(self, url, output_path):

        # Remove query string and http from URL
        url = url.split('?')[0]
        file_name = url.split('/')[-1]

        if len(file_name) == 0: return False

        # Create output directory
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        # Get file content and save it
        response = session.get(url)
        with open(output_path, "wb") as file:
            file.write(response.content)
            print(f"Downloaded {file_name} to {os.path.relpath(output_path)}")
        
        return True
    
    def save_files(self, urls):
        shutil.rmtree(os.path.join(workspace, output_folder), ignore_errors=True)
        for url in urls:
            output_path = self.url_to_local_path(url, keepQuery=False)
            output_path = os.path.join(workspace, output_folder, output_path)

            self.download_file(url, output_path)
        
        return True
    
    # save the HTML file
    def save_html(self):
        output_path = os.path.join(workspace, output_folder,'index.html')
        prettyHTML = self.soup.prettify()
        with codecs.open(output_path, 'w', 'utf-8') as file:
            file.write(prettyHTML)
            file.close()
            print(f"Saved index.html to {os.path.relpath(output_path)}")
        
        return True

extractor = Extractor(url)

print(f"Extracting files from {url}\n")
extractor.run()
print(f"\nTotal extracted files: {len(extractor.scraped_urls)}")