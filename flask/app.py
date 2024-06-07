# Libraries
from flask import Flask, render_template
from flask_cqlalchemy import CQLAlchemy
import os
from utils import genres as get_genres

MOVIE_URL = 'https://api.themoviedb.org/3/genre/movie/list'
TV_URL = 'https://api.themoviedb.org/3/genre/tv/list'

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# App configuration
app.config['CASSANDRA_USER'] = os.getenv("CASSANDRA_USER","cassandra")
app.config['CASSANDRA_PASSWORD'] = os.getenv("CASSANDRA_PASSWORD","cassandra")
app.config['CASSANDRA_HOSTS'] = {os.getenv("CASSANDRA_HOSTS","cassandra")}
app.config['CASSANDRA_KEYSPACE'] = os.getenv("CASSANDRA_KEYSPACE","mainkeyspace")
app.config['CASSANDRA_SETUP_KWARGS'] = {'port': 9042}

db = CQLAlchemy(app)

# Object to be synchronized with Cassandra
class Movies(db.Model):
	__keyspace__ = app.config['CASSANDRA_KEYSPACE']
	__table_name__ = 'Movies'
	id = db.columns.Integer(primary_key=True)
	popularity = db.columns.Float()
	title = db.columns.Text()
	release_date = db.columns.Date()
	vote_average = db.columns.Float()
	vote_count = db.columns.Integer()
	genres = db.columns.Text()


	@property
	def list(self):
		return [self.id, self.popularity, self.title, self.release_date, self.vote_average, self.vote_count, self.genres]
	

	@property
	def column_list(self):
		return ["id", "popularity", "title", "release_date", "vote_average", "vote_count", "genres"]
	


class TVs(db.Model):
	__keyspace__ = app.config['CASSANDRA_KEYSPACE']
	__table_name__ = 'TVs'
	id = db.columns.Integer(primary_key=True)
	origin_country = db.columns.Text()
	popularity = db.columns.Float()
	name = db.columns.Text()
	first_air_date = db.columns.Date()
	vote_average = db.columns.Float()
	vote_count = db.columns.Integer()
	genres = db.columns.Text()

	@property
	def list(self):
		return [self.id, self.popularity, self.name, self.first_air_date, self.vote_average, self.vote_count, self.genres, self.origin_country]
	

	@property
	def column_list(self):
		return ["id", "popularity", "name", "first_air_date", "vote_average", "vote_count", "genres", "origin_country"]
	

# Home page
@app.route("/")
def home():
	n_movies = len([ v for v in Movies.objects()])
	n_TVs = len([v for v in TVs.objects()])
	return render_template("index.html", data = dict(Movies = n_movies, TVs = n_TVs))

# Table view
@app.route("/movies", methods = ['GET'])
def data():
	data_list = [track.list for track in Movies.objects()]
	genres = get_genres(MOVIE_URL)
	#[self.id, self.popularity, self.title, self.release_date, self.vote_average, self.vote_count, self.genres]
	vote_sum = {genre : 0 for genre in genres}
	vote_count = {genre: 0 for genre in genres}
	popularity_sum = {genre: 0 for genre in genres}
	num_movies = {genre: 0 for genre in genres}
	for data in data_list:
		_, popularity, _ , _, vote_avg, vote_cnt, genres_str = data
		for genre in genres:
			if genre in genres_str:
				vote_sum[genre] += vote_avg * vote_cnt
				vote_count[genre] += vote_cnt
				popularity_sum[genre] += popularity
				num_movies[genre] += 1
	vote_avg = {genre: vote_sum[genre]/vote_count[genre] for genre in genres}
	return render_template("movies.html", data_list = dict(full_data = data_list, vote_avg = vote_avg, vote_count = vote_count, popularity = popularity_sum, num_movies = num_movies))

# Chart view
@app.route("/tvshows", methods = ['GET', 'POST'])
def visuals():	
	data_list = [track.list for track in TVs.objects()]
	genres = get_genres(TV_URL)
	print(genres)
	#[self.id, self.popularity, self.name, self.first_air_date, self.vote_average, self.vote_count, self.genres, self.origin_country]
	vote_sum = {genre : 0 for genre in genres}
	vote_count = {genre: 0 for genre in genres}
	popularity_sum = {genre: 0 for genre in genres}
	num_TVs = {genre: 0 for genre in genres}
	country_code = dict()
	for data in data_list:
		_, popularity, _ , _, vote_avg, vote_cnt, genres_str, origin_country = data
		for genre in genres:
			if genre in genres_str:
				vote_sum[genre] += vote_avg * vote_cnt
				vote_count[genre] += vote_cnt
				popularity_sum[genre] += popularity
				num_TVs[genre] += 1
		for v in origin_country.split('|'):
			if v not in country_code.keys():
				country_code[v] = 1
			else:
				country_code[v] += 1

	vote_avg = dict()
	for i, genre in enumerate(genres):
		if vote_count[genre] == 0:
			del vote_sum[genre]
			del vote_count[genre]
			del popularity_sum[genre]
			del num_TVs[genre]
		else:
			vote_avg[genre] = vote_sum[genre]/vote_count[genre]
	return render_template("tvshows.html", data_list = dict(full_data = data_list, vote_avg = vote_avg, vote_count = vote_count, popularity = popularity_sum, num_TVs = num_TVs, country_code = country_code))

if __name__ == "__main__":
	db.sync_db()
	db.set_keyspace(app.config['CASSANDRA_KEYSPACE'])
	app.run(debug = True)