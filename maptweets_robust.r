library(mapproj)

GAME = "game6"
## Instantiating data.frames with data.
tweets <- read.delim(paste("data/", GAME, "_clean.txt", sep=""), 
                     header=FALSE, sep="\t", quote=NULL, row.names=NULL,
                     encoding = 'UTF-8')
timestamps <- read.delim(paste("data/", GAME, "_time.txt", sep=""), 
                         header=TRUE, sep='\t', row.names=NULL)
count <- read.delim(paste("data/", GAME, "_count.txt", sep=""), 
                    header=TRUE, sep='\t', row.names=NULL)

tweets_times <- merge(tweets, timestamps, by.x='V1', by.y='TIME')
tweets_gametime <- merge(tweets_times, count, by.x='V1', by.y='TIME')
tweets_gametime <- transform(tweets_gametime, V4=as.numeric(as.character(V4)))

## Setting up US map. Refer to Nathan's tutorial for a nice-looking map.
## Modify xlim, ylim s.t. tweets aren't floating in whitespace.
xlim <- c(-171.738281, -56.601563)
ylim <- c(12.039321, 71.856229)

## Creating list of coordinates for every tweet.
longMavs = c()
latMavs = c()

longHeat = c()
latHeat = c()

# Tossing out extraneous data (too early or too late relative to tipoff).
tweets_gametime = subset(tweets_full, tweets_full$DELTA > -3600, 
                         tweets_full$DELTA < 14400)

for ( tt in max(tweets_gametime$DELTA):min(tweets_gametime$DELTA) ) {
    
    filename = paste("~/Desktop/ps/", GAME, "_", tt, ".ps", sep="")
    postscript(filename, width=11, height=7)
    m <- map('world', col="#f0f0f0", bg = "#ffffff", fill = TRUE, lwd=0.001,
             ylim = ylim, xlim = xlim)
    
    # longMavs_t = longMavs_t_1
    # latMavs_t = latMavs_t_1
    # longHeat_t = longHeat_t_1
    # latHeat_t = latHeat_t_1
    # 
    # longMavs_t_2 = longMavs_t_1
    # longMavs_t_3 = longMavs_t_2
    # longMavs_t_4 = longMavs_t_3
    # longMavs_t_5 = longMavs_t_4
    # 
    # latMavs_t_2 = latMavs_t_1
    # latMavs_t_3 = latMavs_t_2
    # latMavs_t_4 = latMavs_t_3
    # latMavs_t_5 = latMavs_t_4
    # 
    # longHeat_t_2 = longHeat_t_1
    # longHeat_t_3 = longHeat_t_2
    # longHeat_t_4 = longHeat_t_3
    # longHeat_t_5 = longHeat_t_4
    # 
    # latHeat_t_2 = latHeat_t_1
    # latHeat_t_3 = latHeat_t_2
    # latHeat_t_4 = latHeat_t_3
    # latHeat_t_5 = latHeat_t_4

    # tempData = subset(tweets_gametime, DELTA == tt)    
    for ( i in 1:nrow(tweets_gametime) ) {
        long = tweets_gametime$V3[i]
        if ( !is.na(long) ) {
            lat = tweets_gametime$V4[i]
            if ( tweets_gametime$MAVS[i] > tweets_gametime$HEAT[i] ) {
                longMavs = append(longMavs, long)
                latMavs = append(latMavs, lat)
            } else if ( tweets_gametime$MAVS[i] < tweets_gametime$HEAT[i] ) {
                longHeat = append(longHeat, long)
                latHeat = append(latHeat, lat)
            }
        }
    }

    ## Also, use col = HEX to color the points.
    ## Mavs = #0065B0, Heat = #BA3636
    points(longMavs, latMavs, col = '#0065B0', pch = ".", cex = 2)
    points(longHeat, latHeat, col = '#BA3636', pch = ".", cex = 2)

    dev.off()
}

# NEXT:
# DONE> Do tweets have NBA finals references? If so, add to coords.
# 2. Do this for every second of data in the set.
#   >> Test with Mavs data for a small subset first.
# 3. Create maps for every second of the game.
# 4. Stitch together using...what?
