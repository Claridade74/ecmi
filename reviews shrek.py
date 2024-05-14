from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://letterboxd.com/film/shrek/reviews/by/activity/'

pagina_lb = requests.get(url)
pagina_lb.content

base_url = "https://letterboxd.com/"
current_page = 1
next_page = True

lista_reviews = []

while next_page:
    url = f"{base_url}/film/shrek/reviews/by/activity/page/{current_page}/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        reviews = soup.find_all('div', class_='film-detail-content')

        for review in reviews:
            user = review.find('strong', {'class': 'name'})
            if user:
              usuario = user.get_text(strip=True)
            else:
              usuario = 'N/A'

            stars = review.find('p', {'class': 'attribution'})
            if stars:
                estrelas = stars.find('span').get_text(strip=False)
                estrelas = estrelas.strip().split('>')
                if estrelas[0].find('★')!=-1 or estrelas[0].find('½')!=-1:
                  estrelas=estrelas[0]
                else:
                  estrelas = 'N/A'
            date = review.find('span', {'class': 'date'})
            if date:
                data = date.find('span', {'class': '_nobr'}).get_text(strip=True)
            else:
                data = "N/A"

            text = review.find('div', {'class': 'body-text'})
            if text:
                texto = text.get_text(strip=True)
            else:
                texto = "N/A"

            dados = {'Usuário': usuario,
            'Estrelas': estrelas,
            'Data': data,
            'Review': texto}

            lista_reviews.append(dados)

        next_button = soup.find('a', class_='next')
        if next_button:
            current_page += 1
        else:
            next_page = False
    else:
        print("Erro ao acessar a página:", url)
        break

lista_reviews = pd.DataFrame(lista_reviews)
lista_reviews
