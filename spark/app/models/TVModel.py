import requests
import time

access_token = 'PUSH ACCESS TOKEN INTO ENVIROMENT VARIABLES AND CALL IT HERE'
class TVModel(object):
    def __init__(self) -> None:
        self.headers = dict(
            accept = 'application/json',
            Authorization = 'Bearer ' + access_token
        )

    def discover(self, start_date, end_date):
        URL = 'https://api.themoviedb.org/3/discover/tv'
        response = requests.get(URL, headers=self.headers, params={
            'first_air_date.gte' : start_date,
            'first_air_date.lte' : end_date,
        }).json()
        res = []
        total_pages = response['total_pages']
        for page in range(1, total_pages+1):
            response = requests.get(URL, headers=self.headers, params={
                'first_air_date.gte' : start_date,
                'first_air_date.lte' : end_date,
                'page' : page
            }).json()
            results = [result for  result in response['results'] if len(result['genre_ids']) > 0 \
                                                                    and result['vote_count'] > 0 \
                                                                    and ('"' not in result['name'])  ]
            res.extend([dict(genre_ids = result['genre_ids'],
                             id = result['id'],
                             origin_country = result['origin_country'],
                             popularity = result['popularity'],
                             name = result['name'],
                             first_air_date = result['first_air_date'],
                             vote_average = result['vote_average'],
                             vote_count = result['vote_count']) for result in results])
            time.sleep(0.1)
        return res
    
    def genres(self):
        URL = 'https://api.themoviedb.org/3/genre/tv/list'
        response = requests.get(URL, headers=self.headers).json()
        genres = {v['id']: v['name'] for v in response['genres']}
        return genres
        
            

if __name__ == '__main__':
    model = TVModel()
    res = model.discover(start_date='2024-05-29', end_date='2024-05-29')
    print(res)
    