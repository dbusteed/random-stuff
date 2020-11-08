#
#   messing around with the `neuralnet` library
#   in R. kinda unfinished
#

library(neuralnet)
library(fastDummies)
library(tidyverse)
library(caret)

normalize_series <- function(x) {
  return ((x - min(x)) / (max(x) - min(x)))
}

normalize_x <- function(xi, min, max) {
  return ((xi - min) / (max - min))
}

unnormalize_x <- function(zi, min, max) {
  return ((zi * (max - min)) + min)
}

df <- read.csv("~/tmp/insurance.csv") %>%
      dummy_cols(select_columns=c("sex", "smoker", "region"),
                 remove_first_dummy=TRUE,
                 remove_selected_columns=TRUE) %>%
      select(-id)

max_charges <- max(df$charges)
min_charges <- min(df$charges)

df <- mutate_all(df, normalize_series)

sample <- sample.int(n=nrow(df), size=.75 * (nrow(df)))
train <- df[sample, ]
test  <- df[-sample, ]

nn_grid <- expand.grid(layer1 = c(2,3,4),
                       layer2 = c(2),
                       layer3 = c(2))

cv <- trainControl(method = "cv",
                   number = 5)

nn_mdl <- train(charges~.,
                data = train,
                trControl = cv,
                tuneGrid = nn_grid,
                method = "neuralnet")
                
pred <- predict(nn_mdl, test)
r2 <- R2(pred, test[["charges"]])
print(r2)
