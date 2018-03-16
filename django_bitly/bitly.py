# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import logging

from django.conf import settings
from .exceptions import BittleException
from .conf import BITLY_TIMEOUT, BITLY_API_VERSION
import requests

logger = logging.getLogger(__name__)

class Bitly(object):
    
    def __init__(self, 
                 login=settings.BITLY_LOGIN, 
                 api_key=settings.BITLY_API_KEY, 
                 **kwargs):
        self.api_key = api_key
        self.login = login
        if not (self.api_key and self.login):
            raise BittleException("Bit.ly credentials not found in settings.")
    
    def shorten(self, url, version=BITLY_API_VERSION):
        #===========================================================================
        # # We could use bitly_api's APIs but there are no updates from 2014!
        #
        # import bitly_api
        # c = bitly_api.Connection(settings.BITLY_LOGIN,
        #                          settings.BITLY_API_KEY)
        # bitlified_url = c.shorten(value)
        #===========================================================================
        api_url = 'http://api.bit.ly/shorten'
        data = dict(version=version, 
                    longUrl=url, 
                    login=self.login,
                    apiKey=self.api_key, 
                    history=1)
        response = requests.post(api_url, data=data, timeout=BITLY_TIMEOUT)
        if response.status_code != requests.codes.OK: # @UndefinedVariable
            raise BittleException("Bitly Error Response: %s" % response.status_code)
        response = response.json()
        if response["errorCode"] == 0 and response["statusCode"] == "OK":
            return response["results"][url]
        else:
            raise BittleException("Bitly Error Response: %s" % response)
    
    def shorten_url(self, url, version=BITLY_API_VERSION):
        return self.shorten(url, version=version).get('shortUrl')