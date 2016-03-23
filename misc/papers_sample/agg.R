library(ggplot2)

# aggregate data set
data = data.frame()
for(i in 1:length(dir())) {
  if(sum(grep(".csv",dir()[i])) > 0) {
    if(sum(grep("all_papers.csv",dir()[i])) == 0) {
      if(length(data) == 0) {
        data = read.csv(dir()[i],header=TRUE) 
      } else {
        temp = read.csv(dir()[i],header=TRUE)
        data = rbind(data,temp[2:dim(temp)[1],])
        }
      }
    }
}

# safety check
data = data[data$Source != "Source",]

# diagnostics
qplot(data$Source)

# save aggregate
write.csv(data,file="all_papers.csv",fileEncoding = "ascii",row.names=FALSE)