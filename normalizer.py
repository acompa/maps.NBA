import redis
from os import system
import csv
from corpus import MAVS, HEAT, FINALS
from datetime import datetime, timedelta
from time import mktime

class DataNormalizer():
    
    def __init__(self, db):
        """Sets db name and tipoff time on init. """

        self.db = str(db)
        if self.db == "game1":
            self.tipoff = datetime(2011, 05, 31, hour=21, minute=6, second=00)
        elif self.db == "game2":
            self.tipoff = datetime(2011, 06, 02, hour=21, minute=7, second=00)
        elif self.db == "game4":
            self.tipoff = datetime(2011, 06, 07, hour=21, minute=7, second=00)
        elif self.db == "game6":
            self.tipoff = datetime(2011, 06, 12, hour=21, minute=10, second=00)
        

    def clean_data(self):
        """ Cleans the data as follows:
        1. Splits coords in Redis DB into their own lat/long variables.
        2. Removes all potentially troublesome characters from text.
        3. Reformats timestamps from all games.

        All cleaned data is then written out to a tab-delimited file.

        """

        self.red = redis.Redis(host = 'localhost', port = 6379)

        red.shutdown()
        system("cp data/" + self.db + ".db ../dump.rdb")
        system("redis-server /usr/local/bin/redis.conf")
        # does red persist? do i need to re-init?
        if self.red.exists('foo'):
            self.red.delete('foo')

        out = open("./data/" + self.db + "_clean.txt", "w")
        for key in self.red.keys():
            try:
                coords = red.lindex(key, 1).split(",")
            except:
                coords = 'NA'
                print key

            if len(coords) == 2:
                long = coords[0].strip('[')
                lat = coords[1].strip(']')
            else:
                long = 'NA'
                lat = 'NA'

            try:
                text = red.lindex(key, 2)
                for s in ['\n', '"', '\t', '\015']:
                    text = text.replace(s, ' ')
            except AttributeError:
                continue

            # Count # of a's in key, convert to microsecond count.
            aCount = key.count('a')
            newKey = key.strip('a') + ":%0.2d" % aCount


            out.write("%s\t%s\t%s\t%s\t%s\n" % (newKey, red.lindex(key, 0), 
                      llong, lat, text))

    def check_corpus(self):
        """ Checks text in each tweet for Finals references. Creates new file 
        with count for Mavs, Heat, and Finals references.
        
        """

        data = csv.reader(open("data/" + self.db + "_clean.txt", "rU"), 
                          delimiter = "\t")
        out = open("data/" + self.db + "_count.txt", "w")
        out.write("TIME\tMAVS\tHEAT\tFINALS\n")

        total = 0
        for row in data:
            countM = 0
            countH = 0
            countF = 0
            reference = False
            tweet = row[4].lower()

            for s in MAVS:
                if tweet.find(s.lower()) > -1:
                    reference = True
                    countM += 1

            for s in HEAT:
                if tweet.find(s.lower()) > -1:
                    reference = True
                    countH += 1

            for s in FINALS:
                if tweet.find(s.lower()) > -1:
                    reference = True
                    countF += 1

            if reference:
                total += 1
                
            out.write("%s\t%d\t%d\t%d\n" % (row[0], countM, countH, countF))

        print "%d tweets mention %s of the Finals" % (total, self.db)
        out.close()
    
    def adjust_time(self):
        """ Convert times from DAY HH:MM:SS format to second format. """
        
        data = csv.reader(open("data/" + self.db + "_clean.txt", "rU"), 
                          delimiter = "\t")
        out = open("data/" + self.db + "_time.txt", "w")
        out.write("TIME\tDELTA\n")
        
        for row in data:
            t = datetime.strptime(row[0][:19], "%Y-%m-%d %H:%M:%S")
            timestamp = t - timedelta(hours=4)
            delta = timestamp - self.tipoff
            delta_s = delta.seconds + (delta.days * 86000)
            out.write("%s\t%d\n" % (row[0], delta_s))
            
        out.close()
