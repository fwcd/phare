import os

from phare.auth import Auth
from phare.lighthouse import Lighthouse
from phare.constants import LIGHTHOUSE_URL

user = os.environ['LIGHTHOUSE_USER']
token = os.environ['LIGHTHOUSE_TOKEN']
url = os.environ.get('LIGHTHOUSE_URL', LIGHTHOUSE_URL)

lh = Lighthouse(Auth(user, token), url)

# TODO
