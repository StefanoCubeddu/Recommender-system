import pandas as pd
import numpy as np
from scipy import spatial



#create hash map where user_id is the key and item_id with his rating is the value
def get_user_item_rating(df):
    user_item_rating = {}
    for index, row in df.iterrows():
        if row['user_id'] in user_item_rating:
            user_item_rating[row['user_id']].append((row['item_id'], row['rating']))
        else:
            user_item_rating[row['user_id']] = [(row['item_id'], row['rating'])]
    return user_item_rating

def normalize_rating(user_item_rating):
    mean=[]
    for u in user_item_rating.keys():
        val=0
        for f,r in user_item_rating[u]:
            val+=r
        mean=val/len(user_item_rating[u])
        for i in range(len(user_item_rating[u])):
            user_item_rating[u][i]=(user_item_rating[u][i][0],user_item_rating[u][i][1]-mean)
    return user_item_rating

def cosine_similarity(user1, user2, user_item_rating):
    #get the item_id and rating for user1
    user1_item_rating = user_item_rating[user1]
    #get the item_id and rating for user2
    user2_item_rating = user_item_rating[user2]
    #create a list of common item_id
    common_item_id = [item_rating[0] for item_rating in user1_item_rating if item_rating[0] in [x[0] for x in user2_item_rating]]

    #create a list of rating for common item_id for user1
    if len(common_item_id) < 10:
        return None  
    user1_common_item_rating = [(item_rating[0],item_rating[1]) for item_rating in user1_item_rating if item_rating[0] in common_item_id]
    #create a list of rating for common item_id for user2
    user2_common_item_rating = [(item_rating[0],item_rating[1]) for item_rating in user2_item_rating if item_rating[0] in common_item_id]
    

    user1_common_item_rating=sorted(user1_common_item_rating,key=lambda x:x[0])
    user2_common_item_rating=sorted(user2_common_item_rating,key=lambda x:x[0])
    #compute the similarity between user1 and user2
    #compute the centered cosine similarity
    distance=0
    j=0
    for i in range(len(user1_common_item_rating)):
        distance+=abs(user1_common_item_rating[i][1]-user2_common_item_rating[i][1])
        j+=1
    return -distance/j
    # return 1 - spatial.distance.cosine(user1_common_item_rating[1], user2_common_item_rating[1])
        
#find the 10 most similar user to the random user
def get_most_similar_user(user_id, user_item_rating):
    similar_user = []
    for user in user_item_rating.keys():
        if user != user_id:
            similarity = cosine_similarity(user_id, user, user_item_rating)
            if similarity:
                similar_user.append((user, similarity))
    similar_user = np.asarray(sorted(similar_user, key=lambda x: x[1], reverse=True)[:10])
    return similar_user[:,0]
    

def get_reccomendation(user_id,similar_user, user_item_rating):
    predict_rating = {}
    #get the item_is and rating common from all the similar user
    for i,user in enumerate(similar_user):
        for item_id, rating in user_item_rating[user]:
            if item_id in predict_rating:
                predict_rating[item_id][0]+=rating*(1-(i*0.2))
                predict_rating[item_id][1]+=(1-(i*0.2))
            else:
                predict_rating[item_id]=[rating*(1-(i*0.2)),(1-(i*0.2))]
    #compute the reting
    for item_id in predict_rating.keys():
        predict_rating[item_id]=predict_rating[item_id][0]/predict_rating[item_id][1]
    #sort the rating
    predict_rating = sorted(predict_rating.items(), key=lambda x: x[1], reverse=True)
    #get the top 10 movie that the user has not seen
    top_10_movie = []
    for item_id, rating in predict_rating:
        if item_id not in [x[0] for x in user_item_rating[user_id]]:
            top_10_movie.append((item_id, rating))
        if len(top_10_movie) == 10:
            break
    #get the movie title
    top_10_movie_title = [movie_titles[item[0]] for item in top_10_movie]
    return top_10_movie_title

#read the data from u.data.txt with pandas
df = pd.read_csv('u.data.txt', sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])
#drop the timestamp column
df = df.drop('timestamp', axis=1)
#drop the nan values from the data frame and substitute them with 0
df = df.fillna(0)
#read the data from u.item.txt with pandas
df1 = pd.read_csv('u.item.txt', sep='|', names=['item_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'], encoding='latin-1')
#drop the columns from df1 except item_id and movie_title
df1 = df1.drop(['release_date', 'video_release_date', 'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'], axis=1)
#create hash map for item_id and movie_title
movie_titles = df1.set_index('item_id')['movie_title'].to_dict()
     

user_id = np.random.choice(df['user_id'].unique())
user_item_rating = get_user_item_rating(df)
user_item_rating=normalize_rating(user_item_rating)
similar_user = get_most_similar_user(user_id, user_item_rating)
top_10_movie_title = get_reccomendation(user_id,similar_user, user_item_rating)
#if the user has rated one of the top 10 movie in the test set, print the movie title and the rating

print('user_id: ', user_id)
print('top 10 movie title: ', top_10_movie_title)



            




        
















