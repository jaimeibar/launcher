# -*- coding: utf-8 -*-


'''
Created on Mar 30, 2014

@author: jaime
'''


import urlparse


class UrlException(Exception):
    def __init__(self, value):
        self._value = value
        
    def __str__(self):
        return repr(self._value)


class UrlChecker(object):
    def __init__(self, url):
        self._url = urlparse.urlparse(url)

    def check_url_protocol(self):
        """
        Allowed protocols: http and https.
        """
        allowed_protocols = ['http', 'https']
        if self._url.scheme not in allowed_protocols:
            raise UrlException('Bad protocol')
        else:
            return True

    def check_url_port(self):
        port = self._url.netloc.split(':')[1]
        if not int(port) == 5000:
            raise UrlException('Bad port')
        else:
            return True