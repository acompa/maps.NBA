import redis

out = open("./data/game1_clean.txt", "w")
r = redis.Redis(host = 'localhost', port = 6379, db = 0)

for key in r.keys():

    # Strip all newlines. Comment out rpush when not processing Game 1/2 data.
    text = r.rpop(key)
    r.rpush(key, text.replace('\n', ' ').strip('"'))

    # Split coordinates into their own variables.
    coords = r.lindex(key, 2).split(",")

    if len(coords) == 2:
        long = coords[0].strip("[")
        lat = coords[1].strip("]")

    text = r.lindex(key, 3)
    r.linsert(key, before, text, long)
    r.linsert(key, before, text, lat)

    out.write("%s\t%s\t%s\t%s\n" % (key, r.lindex(key, 0), r.lindex(key, 1), r.lindex(key, 2)))
