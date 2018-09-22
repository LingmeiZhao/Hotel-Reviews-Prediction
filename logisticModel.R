train <- read.csv("train_new.csv",header=TRUE, sep=",")
model <- glm(rating ~ . - id - rating, data = train, family= "binomial")
model_p <- summary(model)$coefficients[, 4]



test <- read.csv("test.csv", header = TRUE, sep =",")
result <- predict(model,test)
test[["prediction"]] <- exp(result)/(1+exp(result))
test[["predicted_binary"]] <- test[["prediction"]] > 0.5
test[["predicted_binary"]] <- as.numeric(test[["predicted_binary"]])
write.csv(test[["predicted_binary"]], file ="prediction.csv",row.names = TRUE)
