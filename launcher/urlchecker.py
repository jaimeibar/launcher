# -*- coding: utf-8 -*-


'''
Created on Mar 30, 2014

@author: jaime
'''


import urlparse



class UrlChecker(object):
    def __init__(self, url):
        self._url = urlparse.urlparse(url)
        
    @property
    def scheme(self):
        return self._url.scheme

    @property
    def netloc(self):
        return self._url.netloc

    def check_url_protocol(self):
        """
        Allowed protocols: http and https.
        """
        allowed_protocols = ['http', 'https']
        if self._url.scheme not in allowed_protocols:
            return False
        else:
            return True

    def check_url_port(self):
        if self._url.netloc:
            port = int(self._url.netloc.split(':')[1])
            if port == 5000:
                return True
        return False