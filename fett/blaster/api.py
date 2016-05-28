import hug
from marshmallow import Schema, fields
from falcon import HTTP_400

class TruckTweet(Schema):
    handle = fields.Str()
    text = fields.Str()
    latitude = fields.Float()
    longitude = fields.Float()
    place = fields.Str()

@hug.get('/analyze')
def analyze(tweet: TruckTweet(), response):
    """Identifies location and time of food trucks from their tweets"""
    if not tweet:
        response.status = HTTP_400
        return
    print(tweet)
    return {}

app = __hug_wsgi__
