library(dplyr)
path <- "fakepath//data//"
files <- list.files(path)
quaterly <- data.frame(matrix(ncol = 6, nrow = 0))
for(i in paste(path, files, sep = "")) {
  elements <- read.csv(i, stringsAsFactors = FALSE)
  quaterly <- rbind.data.frame(quaterly, elements)
}
quaterly <- na.omit(quaterly)
July <- quaterly[!quaterly$Signal_strength == "na" , ]

write.csv(July, "fakepath//temp.csv", row.names = FALSE)
July <- read.csv("fakepath//temp.csv" , stringsAsFactors = FALSE)
#July<- subset( July, Signal_strength < -85)
July <- July[abs(July$Signal_strength) > 85,]

df <- data.frame(matrix(ncol = 6, nrow = 0))

#clean <- function(data){
  # jio4udelhi <- data[data$Operator == "JIO" & data$Technology == "4G" & data$Test_type == 'upload' & data$LSA == "Delhi", ]
  for (i in unique(July$Operator)) {
    temp.operator <- July[July$Operator ==i , ]
    for (j in unique(temp.operator$Technology)) {
      temp.operator.tech <- temp.operator[temp.operator$Technology == j, ]
      for (k in unique(temp.operator.tech$Test_type)) {
        temp.operator.tech.type <- temp.operator.tech[temp.operator.tech$Test_type ==k, ]
        for (l in unique(temp.operator.tech.type$LSA)) {
           temp.operator.tech.type.area <- temp.operator.tech.type[temp.operator.tech.type$LSA == l, ]
           temp.operator.tech.type.area <- temp.operator.tech.type.area[with(temp.operator.tech.type.area, order( Data_speed)), ]
           #temp.operator.tech.type.area <- subset( temp.operator.tech.type.area, Signal_strength < -85)
           num <- round(0.05 * nrow(temp.operator.tech.type.area))
           temp.operator.tech.type.area <- tail(temp.operator.tech.type.area, -num)
           temp.operator.tech.type.area <- head(temp.operator.tech.type.area, -num)
           df <- rbind.data.frame(df, temp.operator.tech.type.area)
           #print(num)
        }
      }
    }
  }
write.csv(df, "fakepath//quarter.csv", row.names = FALSE)

