import os
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from markdownify import MarkdownConverter

# Function to scrape a webpage
def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract main content (adjust the tag/class as per your website)
        content = soup.find('main') or soup.find('body')

        if not content:
            print(f"No suitable content found on {url}")
            return
    else:
        print(f"Failed to fetch {url}: {response.status_code}")
        return

    return content


# Function to convert soup object to markdown
def convert_soup(soup_content):
    MarkdownConverter().convert_soup(soup_content)
    markdown_content = md(str(soup_content), heading_style="ATX", bullets="-", strip=['style', 'script', 'img'])  # ATX uses '#' for headings
    return markdown_content


# Main function to scrape and save
def scrape_and_create_knowledge_base(base_url, urls, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for url in urls:
        full_url = f"{base_url}{url}"
        print(f"Scraping: {full_url}")
        soup_object = scrape_page(full_url)
        markdown = convert_soup(soup_object);
        if markdown:
            filename = os.path.join(output_dir, f"{url.strip('/').replace('/', '_')}.md")
            file = open(filename, "w")
            file.write(markdown)
            file.close()
            print(f"Saved: {filename}")
        else:
            print(f"Skipping {full_url} due to missing content")

# Define website and paths
base_url = "https://www.act.com"
page_paths = [
    "/what-is-crm",
    # "/what-is-marketing-automation",
    "/pricing",
    "/products",
    "/products/connections/outlook-integration",
    "/products/custom-tables",
    "/products/sms4act",
    "/products/link2quotes",
    "/products/link2forms",
    "/products/link2events",
    "/what-is-crm",
    "/resources/support-plans",
    "/about-us",
]
output_directory = "knowledge_base_documents"

# Run the script
scrape_and_create_knowledge_base(base_url, page_paths, output_directory)
