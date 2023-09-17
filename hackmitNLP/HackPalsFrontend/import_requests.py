import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://hackthenorth2022.devpost.com/project-gallery?page='

def get_project_links(page_num):
    response = requests.get(BASE_URL + str(page_num))
    soup = BeautifulSoup(response.text, 'lxml')


    project_links = [a['href'] for a in soup.select('.link-to-software')]
    return project_links

def extract_project_info(project_url):
    response = requests.get(project_url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    data = {}
    headers = ['Inspiration', 'What it does', 'How we built it']
    
    for header in headers:
        h2_tag = soup.find('h2', text=header)
        if h2_tag:
            p_tag = h2_tag.find_next('p')
            if p_tag:
                data[header] = p_tag.text
            else:
                data[header] = None
        else:
            data[header] = None
            
    return data

def main():
    page_num = 1
    all_project_data = []

    while True:
        project_links = get_project_links(page_num)
        if not project_links:
            break

        for link in project_links:
            project_data = extract_project_info(link)
            all_project_data.append(project_data)

        print(f"Scraped page {page_num}")
        page_num += 1


    file = open('projects.txt', 'w', encoding='utf-8')
    for project in all_project_data:
        for header, content in project.items():
            if header in ['Inspiration', 'What it does']:
                file.write(f"{header}: {content}\n")
        file.write("\n\n")
    file.close()



    with open('tech.txt', 'w', encoding='utf-8') as file:
        for project in all_project_data:
            header = 'How we built it'
            content = project.get(header)
            print(header, ":", content)  # Adding this line
            if content:
                file.write(f"{header}: {content}\n\n")

    print("done")

if __name__ == "__main__":
    main()


