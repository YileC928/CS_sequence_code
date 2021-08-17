# Question 1
[see code in Question1_EDA.jpynb]

![Figure 1](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/star_dis.png)

- First, I made a bar plot of star rating to see how the reviews are distributed. We can see that the number of 5-star reviews is significantly larger than the others. Lower star reviews are in general less than higher star reviews (# 5-star > #4-star > #3-star > #1-star > #2-star). People give much more good reviews (reviews with more than 4 stars) than bad reviews, which raises the need to balance the data in Question2.

![Figure 2](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/mktplc.png)

- I was also interested in exploring whether rating in different market places varies. This plot shows that average star rating in the 5 market places are quite similar. Average star ratings in Japan is slightly higher than the others, and France is the country with lowest average star ratings.

![Figure 3](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/heatmap.png)

- This is a heatmap exhibiting correlation between selected features. There are few notably strong correlations except for helpful votes and total votes. Helpful votes are positively correlated with total votes, meaning that when there are more helpful votes in the review, there also tend to be more total votes.
In addition, we can also see that total_votes is slightly negatively correlated with star_rating and verified purchase_code is slightly positively correlated with star_rating.

![Figure 4](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/avg_tot_votes.png)

- To inspect the above-mentioned relations further, I plot star_rating against their average total_votes. It is shown that 1-star-rating views have the highest average total votes, which is two times higher than that of 2-star-rating reviews. Higher star rating reviews have less average total votes, with echoes with the heatmap.

![Figure 5](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/avg_vpur.png)

- Here I plot star_rating against their average verified_purchase_code. 5-star reviews have the highest rate of verified purchase. In general, reviews of higher star rating also have higher rate of verified purchase, this also echoes with the heatmap. 

![Figure 6](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/scatter.png)

The scatter plot shows the relationship between helpful_votes and total_votes. It exhibits a positive linear relationship between the two features and verified what mentioned above that when there are more helpful votes in the review, there also tend to be more total votes.

![Figure 7](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/avg_vine.png)

Finally, we can also explore that is there any interesting patterns haven’t been captured by linear correlation. For example, this plot suggests that 3-star rated reviews have the highest rate of being towards a ‘Amazon Vine product’, higher and lower star rating than 3 all tend to have lower is_vine rate. The relationship between star_rating and is_vine is non-linear.

# Question 2
[see code in Question2-4.jpynb] 

![Figure 8](https://github.com/lsc4ss-s21/assignment-3-YileC928/blob/main/balance.png)
Tables above show the count of each label (“bad” and “good”) before and after downsampling.

# Question 3
[see code in Question2-4.jpynb]

`(a)`

Additional features:
- is_purchase (categorical): In the EDA part, we see that verified purchase_code is positively correlated with star_rating, therefore, I expect it to be a possible predictor for review label.
- is_vine (categorical): Though the relationship between is_vine and star_rating is non-linear, in general good reviews (5-star review) have lower is_vine rate than the others.
- review_length (from text): By exploring the data, I noticed that good reviews tend to be shorter, and thus expect it to predict review label.
- helpful_votes: From EDA, we also know that number of helpful votes is negatively correlated with star rating, I therefore include it as well.

`(c)`

By specifying a series of transformations in a pipeline, we record stages that workers could follow in actual executions. The DataFrame is not processed when I chain together this sequence of transformation in a pipeline, because we have only specified the steps but not yet started any execution. Spark will actually process the DataFrame according to the transformations when we fit the model with data – when the cross-validation sets are feeded to it. Dask’s execution model is somewhat similar, that Dask could hold (delay) functions and execute them by compute().

# Question 4
[see code in Question2-4.jpynb]

My model achieved an testing AUC of 0.6728784403669726 and a training AUC of 0.7605820105820108, which are better than the lab results but are still not very satisfactory. It performs well in predicting good review but not so well in identifying bad ones. The model tend to misclassify bad reviews as good reviews. Possible ways to improve the model includes: 
- Extract more meaningful features from the text, e.g., use TF-IDF, and perhaps include sentiment scores as predictors.
- Feeding more data into it (because of unstable internet connection, I was not able to train the model with full dataset, and trained with a sample of it. I think my solution could scale up to larger sets of data).
