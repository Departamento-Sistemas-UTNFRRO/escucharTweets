# -*- coding: utf-8 -*-

#    This file is part of escucharTweets.
#
#    escucharTweets is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    escucharTweets is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with escucharTweets; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import logging
logger = logging.getLogger(__name__)

from tweepy.streaming import StreamListener
from JsonFileStorage import JsonFileStorage
import time

class FileStorageListener(StreamListener):
    def __init__(self, start_time, time_limit=2, filePrefix='tweets', tweetsPerOutputFile=40000):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []
        self.TweetStorage = JsonFileStorage(filePrefix, tweetsPerOutputFile)

    def on_data(self, data):
        logger.info("Tweet received")
        logger.info(data)

        try:
            self.TweetStorage.saveTweet(data)
            return True
        except BaseException as e:
            logger.error('failed ondata: %s', str(e))
            time.sleep(5)

    def on_error(self, status):
        logger.error('Error Status: %s', status)

        with open('logError.json', 'a') as errfile:
            errfile.write(str(status))
            errfile.write('\n')

    def on_timeout(self):
        logger.error("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 