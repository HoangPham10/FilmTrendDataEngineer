import requests
import time

access_token = 'PUSH ACCESS TOKEN INTO ENVIROMENT VARIABLES AND CALL IT HERE'
class MovieModel(object):
    def __init__(self) -> None:
        self.headers = dict(
            accept = 'application/json',
            Authorization = 'Bearer ' + access_token
        )

    def discover(self, start_date, end_date):
        URL = 'https://api.themoviedb.org/3/discover/movie'
        response = requests.get(URL, headers=self.headers, params={
            'primary_release_date.gte' : start_date,
            'primary_release_date.lte' : end_date,
        }).json()
        res = []
        total_pages = response['total_pages']
        for page in range(1, total_pages+1):
            response = requests.get(URL, headers=self.headers, params={
                'primary_release_date.gte' : start_date,
                'primary_release_date.lte' : end_date,
                'page' : page
            }).json()
            results = [result for  result in response['results'] if len(result['genre_ids']) > 0 \
                                                                    and result['vote_count'] > 0 \
                                                                    and ('"' not in result['title'])  ]
            res.extend([dict(genre_ids = result['genre_ids'],
                             id = result['id'],
                             popularity = result['popularity'],
                             title = result['title'],
                             release_date = result['release_date'],
                             vote_average = result['vote_average'],
                             vote_count = result['vote_count']) for result in results])
            time.sleep(0.1)
        return res
    
    def genres(self):
        URL = 'https://api.themoviedb.org/3/genre/movie/list'
        response = requests.get(URL, headers=self.headers).json()
        genres = {v['id']: v['name'] for v in response['genres']}
        return genres
        
            

if __name__ == '__main__':
    model = MovieModel()
    res = model.discover(start_date='2024-05-29', end_date='2024-05-29')
    print(len(res))
    