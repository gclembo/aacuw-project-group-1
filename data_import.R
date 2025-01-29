devtools::install_github("tylerferguson/NBAinjuries")

library(NBAinjuries)

data(injuries)

write.csv(injuries, file = "data/injuries.csv", row.names = FALSE)
