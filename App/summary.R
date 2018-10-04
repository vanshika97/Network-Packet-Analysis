library(dplyr)
library(ggplot2)
df <- read.csv("fakepath//temp.csv" , stringsAsFactors = FALSE)
#remove values greater than -90
signalless <- df[df$Signal_strength < -90, ]

final <- data.frame( matrix(ncol = 16, nrow = 0))
# creating smaller clusters of dataframes
demo <- aggregate(signalless$Data_speed  , by = list(signalless$Operator, signalless$LSA, signalless$Technology, signalless$Test_type), FUN =length)
last <- aggregate(signalless$Data_speed, by = list(signalless$Operator, signalless$LSA), FUN = length)
colnames(last) <- c("Operator","Licence_Area","Total_Samples")
last$Good_Samples <- floor(0.9 *log(last$Total_Samples))
for (j in 1:nrow(last)) {
  if(last[j,3] < 20)
    last[j,4] <- NA
  
}
colnames(last) <- c("Operator","Licence_Area","Total_Samples", "Good_Samples")
last$Good_Samples <- as.character(last$Good_Samples)
p <- ggplot(last, aes(Operator, Licence_Area)) + geom_raster(aes(fill = Good_Samples)) + theme_classic() + 
  scale_fill_manual(breaks = c("0", "1","2", "3","4", "5", "6","7", "8", "9"),
                    values = c("#FBEEE6","#F7DC6F","#F8C471","#F0B27A", "#E59866","#D98880", "#F1948A", "#C0392B","#7B241C"), na.value="Grey")  
print(p)
write.csv(last, file = "fakepath//good_samples.csv")


for (i in 1:nrow(demo) ){
  var <- demo[i,]
  per <- floor(0.05*demo[i,"x"])
  if(demo[i,"x"] < 20){
    comb <- data.frame(matrix(ncol = 18, nrow = 1))
    colnames(comb) <- c("Operator","Licence_area","Technology","Link_type","Throughput0_5","Throughput5_25","Throughput25_50","Throughput50_75","Throughput75_95","Throughput95_100","Overall_mean","min_5","min_25","min_50","min_75","max_95","Total_Samples","Good_Samples")
    
    comb$Operator <- var$Group.1
    comb$Licence_area <- var$Group.2
    comb$Technology <- var$Group.3
    comb$Link_type <- var$Group.4
    comb$Throughput0_5 <- NA
    comb$Throughput5_25 <- NA
    comb$Throughput25_50 <- NA
    comb$Throughput50_75 <- NA
    comb$Throughput75_95 <- NA
    comb$Throughput95_100 <- NA
    temp <- signalless[signalless$Operator == demo[i,"Group.1"] & signalless$LSA == demo[i,"Group.2"] & signalless$Technology == demo[i,"Group.3"] & signalless$Test_type == demo[i,"Group.4"], ]
    temp <- temp[order(temp$Data_speed, decreasing = FALSE), ]
    comb$Overall_mean <- mean(temp$Data_speed)
    comb$min_25 <- NA
    comb$min_5 <- NA
    comb$min_50 <- NA
    comb$min_75 <- NA
    comb$max_95 <- NA
    comb$Total_Samples <- var$x
    comb$Good_Samples <- NA
    
  }
  else {
    temp <- signalless[signalless$Operator == demo[i,"Group.1"] & signalless$LSA == demo[i,"Group.2"] & signalless$Technology == demo[i,"Group.3"] & signalless$Test_type == demo[i,"Group.4"], ]
    temp <- temp[order(temp$Data_speed, decreasing = FALSE), ]
    first5 <- head(temp, per)         #5%
    second25 <- head(temp,(per*5))    #25%
    third50 <- head(temp, (per*10))   #50%
    fourth75 <- head(temp,(per*15))   #75%
    fifth95 <- head(temp, (per*19))   #95%
    #Division of dataframe into smaller tables i.e. 5%, 5-25%, 25-50% etc
    df5_25 <- setdiff(second25, first5)
    df25_50 <- setdiff(third50, second25)
    df50_75 <- setdiff(fourth75, third50)
    df75_95 <- setdiff(fifth95, fourth75)
    df95_100 <- setdiff(temp, fifth95)
    df_overall <- setdiff(fifth95, first5)
    df_overall <-  aggregate(df_overall$Data_speed, by = list(df_overall$Operator, df_overall$LSA, df_overall$Technology, df_overall$Test_type), FUN =mean)
    df_overall$min5 <- min(df5_25$Data_speed)
    df_overall$min25 <- min(df25_50$Data_speed)
    df_overall$min50 <- min(df50_75$Data_speed)
    df_overall$min75 <- min(df75_95$Data_speed)
    df_overall$max95 <- max(df75_95$Data_speed)
    df_overall$Total_samples <- demo[i, "x"]
    df_overall$goodSamples <- nrow(fifth95) - nrow(first5)
    # df_overall$goodSamples<- sum(c(nrow(df5_25) , nrow(df25_50) , nrow(df50_75)), nrow(df75_95))
    first5 <- aggregate(first5$Data_speed  , by = list(first5$Operator, first5$LSA, first5$Technology, first5$Test_type), FUN =mean)
    df5_25   <- aggregate(df5_25$Data_speed  , by = list(df5_25$Operator, df5_25$LSA, df5_25$Technology, df5_25$Test_type), FUN =mean)
    df25_50  <- aggregate(df25_50$Data_speed , by = list(df25_50$Operator, df25_50$LSA, df25_50$Technology, df25_50$Test_type), FUN =mean)
    df50_75  <- aggregate(df50_75$Data_speed , by = list(df50_75$Operator, df50_75$LSA, df50_75$Technology, df50_75$Test_type), FUN =mean)
    df75_95  <- aggregate(df75_95$Data_speed , by = list(df75_95$Operator, df75_95$LSA, df75_95$Technology, df75_95$Test_type), FUN =mean)
    df95_100 <- aggregate(df95_100$Data_speed, by = list(df95_100$Operator, df95_100$LSA, df95_100$Technology, df95_100$Test_type), FUN =mean)
    
    colnames(first5) <- c("Operator", "Licence_area", "Technology", "Link_type", "Throughput0_5")
    colnames(df5_25) <- c("Operator", "Licence_area", "Technology", "Link_type", "Throughput5_25")
    colnames(df25_50) <- c("Operator", "Licence_area", "Technology", "Link_type", "Throughput25_50")
    colnames(df50_75) <- c("Operator", "Licence_area", "Technology", "Link_type", "Throughput50_75")
    colnames(df75_95) <- c("Operator", "Licence_area", "Technology", "Link_type", "Throughput75_95")
    colnames(df95_100) <- c("Operator", "Licence_area", "Technology", "Link_type", "Throughput95_100")
    colnames(df_overall) <- c("Operator", "Licence_area", "Technology", "Link_type",  "Overall_mean", "min_5", "min_25", "min_50", "min_75", "max_95", "Total_Samples", "Good_Samples")
    comb <- merge(first5, df5_25, by = c("Operator", "Licence_area", "Technology", "Link_type"), all = TRUE)
    comb <- merge(x = comb, y = df25_50, by = c("Operator", "Licence_area", "Technology", "Link_type"), all = TRUE)
    comb <- merge(x = comb, y = df50_75, by = c("Operator", "Licence_area", "Technology", "Link_type"), all = TRUE)
    comb <- merge(x = comb, y = df75_95, by = c("Operator", "Licence_area", "Technology", "Link_type"), all = TRUE)
    comb <- merge(x = comb, y = df95_100, by = c("Operator", "Licence_area", "Technology", "Link_type"), all = TRUE)
    comb <- merge(x = comb, y = df_overall, by = c("Operator", "Licence_area", "Technology", "Link_type"), all = TRUE)
  }
  final <- rbind(final, comb)
}
write.csv(final, file = "fakepath//summary.csv")
