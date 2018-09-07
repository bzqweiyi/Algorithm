# -*- coding:utf-8 -*-
'''
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
user_similarity = pairwise_distances(R, metric='cosine')
item_similarity = pairwise_distances(R.T, metric='cosine')

# predict function
def predict(R, similarity, type='item'):
    if type == "user":
        mean_user_rating = R.mean(axis=1) # axis=1 计算每行
        rating_d = (R - mean_user_rating[:, np.newaxis]) # np.newaxis 根据R调整矩阵
        prediction = mean_user_rating[:, np.newaxis] + similarity.dot(rating_d) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        prediction = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return prediction
'''
# james
# 2018.08.24
import math
import sys
from texttable import Texttable

# use |A&B|/sqrt(|A || B|) calculate cosine
def calcCosDistSpe(user1, user2):
    avg_x = 0.0
    avg_y = 0.0
    for key in user1:
        avg_x += key[1]
    avg_x = avg_x / len(user1)

    for key in user2:
        avg_y += key[1]
    avg_y = avg_y / len(user2)

    u1_u2 = 0.0
    for key1 in user1:
        for key2 in user2:
            if key1[1] > avg_x and key2[1] > avg_y and key1[0] == key2[0]:
                u1_u2 += 1
    u1u2 = len(user1) * len(user2) * 1.0
    sx_sy = u1_u2 / math.sqrt(u1u2)
    return sx_sy

# calculate cosine distance
def calcCosDist(user1, user2):
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    for key1 in user1:
        for key2 in user2:
            if key1[0] == key2[0]:
                sum_xy += key1[1] * key2[1]
                sum_y += key2[1] * key2[1]
                sum_x += key1[1] * key1[1]

    if sum_xy == 0.0:
        return 0
    sx_sy = math.sqrt(sum_x * sum_y)
    return sum_xy /sx_sy

# calculate similarity cosine distance
def calcSimlaryCosDist(user1, user2):
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    avg_x = 0.0
    avg_y = 0.0
    for key in user2:
        avg_y += key[1]
    avg_y = avg_y / len(user2)

    for key1 in user1:
        for key2 in user2:
            if key1[0] == key2[0]:
                sum_xy += (key1[1] - avg_x) * (key2[1] - avg_y)
                sum_y += (key2[1] - avg_y) * (key2[1] -avg_y)
        sum_x += (key1[1] - avg_x) * (key1[1] - avg_x)

    if sum_xy == 0.0:
        return 0
    sx_sy = math.sqrt(sum_x * sum_y)
    return sum_xy / sx_sy

# Read file
def readFile(filename):
    contents_lines = []
    f = open(filename, 'r', encoding='utf-8')
    contents_lines = f.readlines()
    f.close()
    return contents_lines

# Extract rating information, Format: User id\t hard disk id \t user rating \t time
# Input: dataset
# Output: sort information with extract.
def getRatingInformation(ratings):
    rates=[]
    for line in ratings:
        rate = line.split("\t")
        rates.append([int(rate[0]), int(rate[1]), int(rate[2])])
    return rates

# Generate user score datastruct
# Input: [[2,1,5],[2,4,2]...]
# Output: 1. 用户打分字典 2.电影字典
# Use dictionary, key is user id, value is user comments to the movie.
# rate_dic[2]=[(1,5),(4,2)]... it means that user2 to movie 1 score 5, to movie 4 score is 2
def createUserRankDic(rates):
    user_rate_dic = {}
    item_to_user = {}  # {} is dictionary
    for i in rates:
        user_rank = (i[1], i[2])
        if i[0] in user_rate_dic:
            user_rate_dic[i[0]].append(user_rank)
        else:
            user_rate_dic[i[0]] = [user_rank]

        if i[1] in item_to_user:
            item_to_user[i[1]].append(i[0])
        else:
            item_to_user[i[1]] = [i[0]]
    return user_rate_dic, item_to_user

# Calculate with particular user the most near neighborhood
# Input: User id, user data, all physical data
# Output: with particular near list
def calcNearestNeighbor(userid, users_dic, item_dic):
    neighbors = []
    for item in users_dic[userid]:
        for neighbor in item_dic[item[0]]:
            if neighbor != userid and neighbor not in neighbors:
                neighbors.append(neighbor)

    neighbors_dist = []
    for neighbor in neighbors:
        dist = calcSimlaryCosDist(users_dic[userid], users_dic[neighbor])
        neighbors_dist.append([dist, neighbor])
    neighbors_dist.sort(reverse=True)
    return neighbors_dist

# use UserFC to recommend
# Input: filename, user id, neighbor number.
# Output: recommend movie id, input user's movie list, movie to user's reverse table, neighbor list.
def recommendByUserFC(file_name, userid, k=5):
    # read file.
    test_contents = readFile(file_name)
    test_rates = getRatingInformation(test_contents)
    # Format dictionary data
    test_dic, test_item_to_user = createUserRankDic(test_rates)
    # find neighbor
    neighbors = calcNearestNeighbor(userid, test_dic, test_item_to_user)[:k]
    recommend_dic = {}
    for neighbor in neighbors:
        neighbor_user_id = neighbor[1]
        movies = test_dic[neighbor_user_id]
        for movie in movies:
            if movie[0] not in recommend_dic:
                recommend_dic[movie[0]] = neighbor[0]
            else:
                recommend_dic[movie[0]] += neighbor[0]

    # establish recommend table
    recommend_list = []
    for key in recommend_dic:
        recommend_list.append([recommend_dic[key], key])

    recommend_list.sort(reverse=True) # high value is first
    user_movies = [i[0] for i in test_dic[userid]]
    return [i[1] for i in recommend_list], user_movies, test_item_to_user, neighbors

# get movie list
def getMoviesList(file_name):
    movies_contents = readFile(file_name)
    movies_info = {}
    for movie in movies_contents:
        movies_info = movie.split("|")
        movies_info[int(movies_info[0])] = movies_info[1:]
    return movies_info

# main function
# input: test datasat
if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    movies = getMoviesList("u.item") # where to find this movie list
    recommend_list, user_movie, items_movie, neighbors = recommendByUserFC("u.data", 179, 80)
    neighbors_id = [i[1] for i in neighbors]
    table = Texttable()
    table.set_cols_dtype(['t',  # text
                          't'   # float(decimal)
                          't']) # automatic
    table.set_cols_align(["1", "1", "1"])
    rows = []
    rows.append([u"movie name", u"release", u"from userid"])  # what's u's function
    for movie_id in recommend_list[:20]:
        from_user = []
        for user_id in items_movie[movie_id]:
            if user_id in neighbors_id:
                from_user.append(user_id)
        rows.append([movies[movie_id][0], movies[movie_id][1], ""])
    table.add_rows(rows)
    print(table.draw())

