import hug

@hug.get('/analyze')
def analyze(tweet: dict):
    """Identifies location and time of food trucks from their tweets"""
    return {}


app = __hug_wsgi__
