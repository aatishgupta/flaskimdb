# flaskimdb

API for register 
http://localhost:5000/register?username=test&password=password&role=A

Role can be A or U where A is admin username
Role A can only able to create movies

Curl request
curl -d "username=test&password=password&role=A" -X POST http://localhost:5000

curl http://localhost:5000/register?username=test&password=password&role=A



API for login 
curl http://127.0.0.1:5000/login?username=test&password=password
curl -d "username=test&password=password" -X POST http://127.0.0.1:5000/login



API for logout
curl http://127.0.0.1:5000/logout
curl -X POST http://127.0.0.1:5000/logout



API to get user rated or commented movie details
curl http://127.0.0.1:5000/users/movies



API to add  movie
curl -d "title=joker&description=description&image_file=image_url&release_date=1542542254566" http://127.0.0.1:5000/movie/


API for search movies
syntax http://127.0.0.1:5000/movie/search/<string:keyword>
example searchs all movies which contains keyword joker which return list of movies along with ratings and comments
curl http://127.0.0.1:5000/movie/search/joker



API to do ratings
syntax /movie/<int:movie_id>/rating
example
curl http://127.0.0.1:5000/movie/1/rating -X POST -d "rating = 10"


API to do comments
syntax /movie/<int:movie_id>/comment
example
curl http://127.0.0.1:5000/movie/1/comment -X POST -d "comment = Good Movie"




