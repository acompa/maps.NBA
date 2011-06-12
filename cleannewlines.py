import redis

out = open("./data/game2_clean.txt", "w")
r = redis.Redis(host = 'localhost', port = 6379, db = 0)

for key in r.keys():

    if key == 'foo':
        r.delete('foo')
        continue

    # Strip all newlines. Comment out rpush when not processing Game 1/2 data.
    # text = r.rpop(key)
    #r.rpush(key, text.replace('\n', ' ').strip('"'))

    # Split coordinates into their own variables.
    try:
        coords = r.lindex(key, 1).split(",")
    except:
	coords = 'NA'
	print key

    if len(coords) == 2:
        llong = coords[0].strip("[")
        lat = coords[1].strip("]")
    else:
        llong = 'NA'
        lat = 'NA'

    try:
        text = r.lindex(key, 2).replace('\n', ' ').strip('"')
    except AttributeError:
        continue
    #r.linsert(key, "before", text, llong)
    #r.linsert(key, "before", text, lat)

    # Count # of a's in key, convert to microsecond count.
    aCount = key.count('a')
    newKey = key.strip('a') + ":%0.2d" % aCount

    out.write("%s\t%s\t%s\t%s\t%s\n" % (newKey, r.lindex(key, 0), llong, lat, text))
