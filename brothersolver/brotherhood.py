from urllib.request import urlopen
from urllib.parse import urlencode

API_BASE = 'http://ocrhood.gazcad.com/'

class BrotherhoodException(Exception):
    pass

class Captcha:

    def __init__(self, brotherhood, cid):
        self.brotherhood = brotherhood
        self.cid = cid
        self.image = None

    def solve(self, answer):
        args = {
                'captchaID': self.cid,
                'captchaAnswer': answer,
                }

        print(self.brotherhood.call('setCaptchaResult', args, True))

    def get_image(self):
        if self.image:
            return self.image
        else:
            self.image = self.fetch_image()
            return self.image

    def fetch_image(self):
        args = {
                'captchaID': self.cid,
                }

        return self.brotherhood.call('showcaptcha', args, True)

class Brotherhood:

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def call(self, method_name, args={}, binary=False):
        args['username'] = self.user
        args['password'] = self.password
        args['version'] = '1.1.7'

        query = urlencode(args)

        url = '%s%s.aspx?%s' % (API_BASE, method_name, query)

        response = urlopen(url)

        if binary:
            return response.read()
        else:
            status, data = response.read().decode('utf-8').split('-', 1)

            if status == 'OK':
                return data
            else:
                raise BrotherhoodException(data)

    def get_captcha(self):
        result = self.call('getCaptcha2Solve')

        if result == 'No Captcha':
            return None
        else:
            return Captcha(self, result)

    def get_credits(self):
        return int(self.call('askCredits'))

