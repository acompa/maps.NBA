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
tweets_full <- merge(tweets_times, count, by.x='V1', by.y='TIME')
tweets_full <- transform(tweets_full, V4=as.numeric(as.character(V4)))

## Setting up US map. Refer to Nathan's tutorial for a nice-looking map.
## Modify xlim, ylim s.t. tweets aren't floating in whitespace.
xlim <- c(-171.738281, -56.601563)
ylim <- c(12.039321, 71.856229)

## Creating list of coordinates for every tweet.
for ( j in 1:5) {
    longMavs_t_1 = c()
    longMavs_t_2 = c()
    longMavs_t_3 = c()
    longMavs_t_4 = c()
    longMavs_t_5 = c()

    latMavs_t_1 = c()
    latMavs_t_2 = c()
    latMavs_t_3 = c()
    latMavs_t_4 = c()
    latMavs_t_5 = c()

    longHeat_t_1 = c()
    longHeat_t_2 = c()
    longHeat_t_3 = c()
    longHeat_t_4 = c()
    longHeat_t_5 = c()

    latHeat_t_1 = c()
    latHeat_t_2 = c()
    latHeat_t_3 = c()
    latHeat_t_4 = c()
    latHeat_t_5 = c()
}
longMavs_t = c()
latMavs_t = c()
longHeat_t = c()
latHeat_t = c()

for ( tt in max(tweets_full$DELTA):min(tweets_full$DELTA) ) {
    
    filename = paste("~/Desktop/ps/", GAME, "_", tt, ".ps", sep="")
    postscript(filename, width=11, height=7)
    m <- map('world', col="#f0f0f0", bg = "#ffffff", fill = TRUE, lwd=0.001,
             ylim = ylim, xlim = xlim)
    
    longMavs_t = longMavs_t_1
    latMavs_t = latMavs_t_1
    longHeat_t = longHeat_t_1
    latHeat_t = latHeat_t_1
    
    longMavs_t_2 = longMavs_t_1
    longMavs_t_3 = longMavs_t_2
    longMavs_t_4 = longMavs_t_3
    longMavs_t_5 = longMavs_t_4

    latMavs_t_2 = latMavs_t_1
    latMavs_t_3 = latMavs_t_2
    latMavs_t_4 = latMavs_t_3
    latMavs_t_5 = latMavs_t_4

    longHeat_t_2 = longHeat_t_1
    longHeat_t_3 = longHeat_t_2
    longHeat_t_4 = longHeat_t_3
    longHeat_t_5 = longHeat_t_4

    latHeat_t_2 = latHeat_t_1
    latHeat_t_3 = latHeat_t_2
    latHeat_t_4 = latHeat_t_3
    latHeat_t_5 = latHeat_t_4

    tempData = subset(tweets_full, DELTA == tt)    
    for ( i in 1:nrow(tempData) ) {
        long = tempData$V3[i]
        if ( !is.na(long) ) {
            lat = tempData$V4[i]
            if ( tempData$MAVS[i] > tempData$HEAT[i] ) {
                longMavs_t = append(longMavs_t, long)
                latMavs_t = append(latMavs_t, lat)
            } else if ( tempData$MAVS[i] < tempData$HEAT[i] ) {
                longHeat_t = append(longHeat_t, long)
                latHeat_t = append(latHeat_t, lat)
            }
        }
    }

    ## Also, use col = HEX to color the points.
    ## Mavs = #0065B0, Heat = #BA3636
    points(longMavs_t, latMavs_t, col = '#0065B0', pch = ".", cex = 2)
    points(longMavs_t_1, latMavs_t_1, col = '#0065B0', pch = ".", cex = 2)
    points(longMavs_t_2, latMavs_t_2, col = '#0065B0', pch = ".", cex = 2)
    points(longMavs_t_3, latMavs_t_3, col = '#0065B0', pch = ".", cex = 2)
    points(longMavs_t_4, latMavs_t_4, col = '#0065B0', pch = ".", cex = 2)
    points(longMavs_t_5, latMavs_t_5, col = '#0065B0', pch = ".", cex = 2)

    points(longHeat_t, latHeat_t, col = '#BA3636', pch = ".", cex = 2)
    points(longHeat_t_1, latHeat_t_1, col = '#BA3636', pch = ".", cex = 2)
    points(longHeat_t_2, latHeat_t_2, col = '#BA3636', pch = ".", cex = 2)
    points(longHeat_t_3, latHeat_t_3, col = '#BA3636', pch = ".", cex = 2)
    points(longHeat_t_4, latHeat_t_4, col = '#BA3636', pch = ".", cex = 2)
    points(longHeat_t_5, latHeat_t_5, col = '#BA3636', pch = ".", cex = 2)

    dev.off()
}

# NEXT:
# DONE> Do tweets have NBA finals references? If so, add to coords.
# 2. Do this for every second of data in the set.
#   >> Test with Mavs data for a small subset first.
# 3. Create maps for every second of the game.
# 4. Stitch together using...what?
