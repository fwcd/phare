import asyncio
import os

from phare.auth import Auth
from phare.lighthouse import Lighthouse
from phare.constants import LIGHTHOUSE_URL

async def main():
    user = os.environ['LIGHTHOUSE_USER']
    token = os.environ['LIGHTHOUSE_TOKEN']
    url = os.environ.get('LIGHTHOUSE_URL', LIGHTHOUSE_URL)

    with await Lighthouse.connect(Auth(user, token), url) as lh:
        pass

asyncio.run(main())
