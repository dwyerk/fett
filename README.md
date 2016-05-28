# fett

# Setup environment
```
mkvirtualenv -p `which python3.5` fett
add2virtualenv .
```

# Install requiremnts
`pip install -r requirements.txt`

# run the blaster api
```
workon fett
gunicorn -c fett/gunicorn.config.py fett.blaster.api:app
# or: hug -f blaster/api.py
```

# visit the api
- Linux: `xdg-open http://localhost:8000`
- OSX: `open http://localhost:8000`

