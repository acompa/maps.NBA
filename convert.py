import redis

r = redis.Redis(host = 'localhost', port = 6379, db = 0)
out = open("./game1b.txt", "w")

for key in r.keys():
	out.write("%s\t%s\t%s\t%s\n" % (key, r.lindex(key, 0), r.lindex(key, 1), r.lindex(key, 2)))


