# 基于Python2.7
# 数据集为MovieLens100k数据集
# -*-coding=utf-8 -*-
import math
from texttable import Texttable
import importlib, sys


# 算法流程：
# 1、建立电影-用户的倒排表，表示电影被那些用户看过
# 2、从目标用户看过的每一步电影开始遍历
# 3、寻找和目标用户有共同看过电影交集的所有用户作为初始邻居
# 4、对初始邻居里边的每一个邻居，计算和目标用户的余弦夹角相似度
# 5、建立相似度到用户的倒排表，相似度从高到低排列
# 6、根据相似度找出最近k邻居
# 7、从最近k邻看过的所有的电影开始遍历
#  这里的推荐思路是：对于最近k邻居看过的所有电影中的某一电影m
#  如果m仅仅被一个邻居看过，那么目标用户对此电影的的兴趣度就是目标用户和这个邻居的相似度
#  如果m被多个邻居看过，那么目标用户对此电影的相似度为目标用户与这些邻居相似度之和
# 8、建立目标用户兴趣度-电影id的倒排表
# 9、根据兴趣度由大到小进行推荐

# 计算余弦距离
# listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
# dist = getCosDist(listUser2Score[userId], listUser2Score[neighbor])
def getCosDist(user1, user2):
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    for key1 in user1:
        for key2 in user2:
            # key1[0]表示电影id，key1[1]表示对电影的评分
            # 如果是两个用户共同评价的一部电影
            if key1[0] == key2[0]:
                sum_x += key1[1] * key1[1]
                sum_y += key2[1] * key2[1]
                sum_xy += key1[1] * key2[1]
    if sum_xy == 0.0:
        return 0
    demo = math.sqrt(sum_x * sum_y)
    return sum_xy / demo


# 读取文件，读取以行为单位，每一行是列表里的一个元素
def readFile(filename):
    contents = []
    f = open(filename, "r")
    contents = f.readlines()
    f.close()
    return contents


# 数据格式化为二维数组
def getRatingInfo(ratings):
    rates = []
    for line in ratings:
        rate = line.split("\t")
        #  u.data
        #  user id | item id | rating | timestamp.
        rates.append([int(rate[0]), int(rate[1]), int(rate[2])])
    return rates


# 生成用户评分数据结构
def getUserScoreDataStructure(rates):
    # listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
    listUser2Score = {}
    # dictItem2Users{},key=item id,value=user id list
    dictItem2Users = {}
    for k in rates:
        #  u.data
        #  user id | item id | rating | timestamp.
        user_rank = (k[1], k[2])
        if k[0] in listUser2Score:
            listUser2Score[k[0]].append(user_rank)
        else:
            listUser2Score[k[0]] = [user_rank]

        if k[1] in dictItem2Users:
            dictItem2Users[k[1]].append(k[0])
        else:
            dictItem2Users[k[1]] = [k[0]]
    return listUser2Score, dictItem2Users


# 计算与目标用户
def getNearestNeighbor(userId, listUser2Score, dictItem2Users):
    neighbors = []
    # listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
    # 对于目标用户userId的每一个评价过的项目item
    for item in listUser2Score[userId]:
        # dictItem2Users{},key=item id,value=user id list
        # item[0]表示电影id，item[1]表示电影评分
        # dictItem2Users[item[0]]=dictItem2Users[电影id]=value=评价过这个电影的用户列表
        # 从评价过这个电影的用户列表里，计算目标用户和这个列表里边所有用户的相似度
        for neighbor in dictItem2Users[item[0]]:
            # 如果这个邻居不是目标用户并且这个邻居还没有被加入邻居集就加进来
            if neighbor != userId and neighbor not in neighbors:
                neighbors.append(neighbor)
    neighbors_dist = []
    # 里边存储的是[相似度，邻居id]
    for neighbor in neighbors:
        # listUser2Score[2]=[(1,5),(4,2)].... 表示用户2对电影1的评分是5，对电影4的评分是2
        dist = getCosDist(listUser2Score[userId], listUser2Score[neighbor])
        neighbors_dist.append([dist, neighbor])
    #  按照相似度倒排，相似度从道到低
    neighbors_dist.sort(reverse=True)
    return neighbors_dist


# 使用UserFC进行推荐，输入：文件名,用户ID,邻居数量
def recommendByUserFC(filename, userId, k=5):
    # 读取文件
    contents = readFile(filename)
    # 文件格式数据转化为二维数组
    rates = getRatingInfo(contents)
    # 格式化成字典数据
    listUser2Score, dictItem2Users = getUserScoreDataStructure(rates)
    # 找邻居
    # 找出最相似的前五个邻居
    neighborsTopK = getNearestNeighbor(userId, listUser2Score, dictItem2Users)[:5]
    # neighborsTopK存储了相似度和邻居id的倒排表
    # 所以neighbor[1]表示邻居id，neighbor[0]表示相似度
    # 这里的推荐思路是：对于最近k邻居看过的所有电影中的某一电影m
    # 如果m仅仅被一个邻居看过，那么目标用户对此电影的的兴趣度就是目标用户和这个邻居的相似度
    # 如果m被多个邻居看过，那么目标用户对此电影的相似度为目标用户与这些邻居相似度之和
    # 建立推荐字典
    recommand_dict = {}
    for neighbor in neighborsTopK:
        neighbor_user_id = neighbor[1]
        # 找出这个邻居看过的所有电影信息
        movies = listUser2Score[neighbor_user_id]
        for movie in movies:
            if movie[0] not in recommand_dict:
                recommand_dict[movie[0]] = neighbor[0]
            else:
                recommand_dict[movie[0]] += neighbor[0]
    # 建立推荐列表
    recommand_list = []
    for key in recommand_dict:
        # 建立目标用户兴趣度-电影id的倒排表
        recommand_list.append([recommand_dict[key], key])
    recommand_list.sort(reverse=True)
    # listUser2Score列表里边的元素是电影id到电影评分的键值对
    # 所以这里的k[0]表示电影id，k[1]表示电影评分
    user_movies = [k[0] for k in listUser2Score[userId]]
    # recommand_list存储的是目标用户兴趣度到电影id的倒排表
    # 所以这里的的k[1]表示的是电影id，k[0]表示的是兴趣度
    return [k[1] for k in recommand_list], user_movies, dictItem2Users, neighbors


# 获取电影的列表
def getMovieList(filename):
    contents = readFile(filename)
    movies_info = {}
    for movie in contents:
        single_info = movie.split("|")
        movies_info[int(single_info[0])] = single_info[1:]
    return movies_info


# 从这里开始运行
if __name__ == '__main__':
    filename = r""
    importlib.reload(sys)  # reload(sys) # this is used for python2.x
    # sys.setdefaultencoding('utf-8')
    # 获取所有电影的列表,所有电影id到电影名字的键值对
    dictMovieId2Info = getMovieList("u.item")
    listRecommendMovieId, user_movie, items_movie, neighbors = recommendByUserFC("u.data", 50, 80)
    neighbors_id = [i[1] for i in neighbors]
    table = Texttable()
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 't', 't'])
    table.set_cols_align(["l", "l", "l"])
    rows = []
    rows.append([u"movie name", u"release time", u"from userid"])
    # 打印推荐列表的前20项数据，listRecommendMovieId里边存储的仅仅是id
    for movie_id in listRecommendMovieId[:20]:
        from_user = []
        for user_id in items_movie[movie_id]:
            if user_id in neighbors_id:
                from_user.append(user_id)
        # dictMovieId2Info[movie_id][0]表示电影名 dictMovieId2Info[movie_id][1]表示时间
        rows.append([dictMovieId2Info[movie_id][0], dictMovieId2Info[movie_id][1], from_user])
    table.add_rows(rows)
    print(table.draw())
