# Starships
Simple flask app to view and store starships. Fetches additional information via [swapi.dev](https://swapi.dev) API. Written in Python 3.9

## Usage
```
pip install -r requirements.txt
cp .env.example .env
flask run
```

## Testing
```
python -m pytest
```

## Considerations
With more time I would have secured the POST endpoint with a JWT token or basic auth. In addition to that I would have
cached the technial information about the ships in separate database columns for each field instead of one text blob. This would've made it possible to
query ships by technical info.

The unit tests are quite minimal as well, with more time I would extend the test cases and provide data fixtures to test the GET endpoints isolated from the POST endpoint.

A last thing I would've done with more time is to make the error handling more consistent and clear. When the SWAPI API returns a 404 I just pass the error on instead of making a custom error message indicating where exactly the error happened.