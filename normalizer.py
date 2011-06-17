import redis
from os import system
import csv
from corpus import MAVS, HEAT, FINALS

class DataNormalizer():

    def __init__(self, db):
        """On init, copies archived Redis db to working db location, then restarts
        Redis with new database.

        Also deletes any keys == 'foo'.

        """

        self.db = str(db)

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

        Possible Map-Reduce opportunity here?

        """

        data = csv.reader(open("data/" + self.db + "_clean.txt", "rU"), 
                      delimiter = "\t")
        out = open("data/" + self.db + "_count.txt", "w")
        out.write("MAVS\tHEAT\tFINALS\n")

        for row in data:
            countM = 0
            countH = 0
            countF = 0
            tweet = row[4]

            for s in MAVS:
                if tweet.find(s) > -1:
                    countM += 1

            for s in HEAT:
                if tweet.find(s) > -1:
                    countH += 1

            for s in FINALS:
                if tweet.find(s) > -1:
                    countF += 1

            out.write("%d\t%d\t%d\n" % (countM, countH, countF))

        out.close()
