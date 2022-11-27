# Recommender-system
Movie Recommender Systems using Collaborative Filtering

Dataset:  
MovieLens dataset collected by GroupLens Research.
Dataset with 100,000 ratings given by 943 users for 1682 movies, with each user having rated at least 20 movies.

The approach is to generate a random user from the dataset and to find the most similar users to him, and try to predict the movies that he could like most

To do this, we find for each user in the dataset the "similarity" with our random user_id, and select the 10 users with the most similar preferences.

After that, for each movie viewed by more similar users but not by our user_id, we compute a prediction rating weighted by the rating given by the user and the similarity with our user_id.

Finally we return as advice the 10 movies with higher predicted rating.

 
