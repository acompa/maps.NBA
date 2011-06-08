infile = open("/mcr/home/m1arc02/spool/nbafinals/game1b.txt", "rU")
outfile = open("/mcr/home/m1arc02/spool/nbafinals/game1c.txt", "w")

for row in infile:
    row.strip('"')
    outfile.write(row)

