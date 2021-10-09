# Starships
Simple flask app to view and store starships. Fetches additional information via swapi.dev API. Written in Python 3.9

## Usage
```
pip install -r requirements.txt
flask run
```

## Testing
```
python -m pytest
```

## Considerations
With more time I would have secured the POST endpoint with a JWT token or basic auth. In addition to that I would
cache the technial information about the ships in separate database columns for each field instead of one text blob. This would make it possible to
query ships by technical info.

The unit tests are quite minimal as well, with more time I would extend the test cases and provide data fixtures to test the list endpoint isolated from the create endpoints.