import pdb
import csv
from math import sqrt
"""
基于用户的协同过滤推荐
"""
class UserBasedCF:
    def __init__(self, dataset={}, k=2, cnt=10):
        """
        :param dataset: 是一个字典值 表示为用户-物品-评分 类似于{uid:{gooid:score,...}.....}
        :param k:  相邻的用户个数
        :param cnt: 推荐商品个数
        """
        self.k = k
        self.cnt = cnt
        if type(dataset).__name__ == 'dict':
            self.dataset = dataset
    def get_data(self,filename):
        """
        该函数主要是为了 测试数据用的 从一个文件中读取数据
        :param filename:
        :return:
        """
        rows = []
        csvFile = open(filename, 'r')
        reader = csv.reader(csvFile)
        for row in reader:
            rows.append(row)
        rows.remove(rows[0])
        print("数据:\n%s\n" % rows)
        csvFile.close()
        # 数据集 是一个字典值 表示为用户-物品-评分 类似于{uid:{gooid:score,...}.....}
        dataset = {}
        for row in rows:
            if row[0] not in dataset:
                dataset[row[0]] = {}
            dataset[row[0]][row[2]] = float(row[1])
        self.dataset = dataset
        print("数据集:\n%s\n" % dataset)
    # 皮尔逊相关系数
    def pearson(self, touser, dataset):
        """
        计算两个用户的皮尔逊系数
        :param touser: 推荐的用户
        :param dataset: 比较用户
        :return: 系数
        """
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_xx = 0
        sum_yy = 0
        n = 0
        for key in touser:
            if key in dataset:
                n += 1
                x = touser[key]
                y = dataset[key]
                sum_x += x
                sum_y += y
                sum_xy += x * y
                sum_xx += pow(x, 2)
                sum_yy += pow(y, 2)
        # 如果没有用户 则退出
        if n == 0:
            return 0
        a = sqrt(sum_xx - pow(sum_x, 2) / n)
        b = sqrt(sum_yy - pow(sum_y, 2) / n)
        denominator =  a * b
        if denominator == 0:
            return 0
        else:
            tmp = (sum_x * sum_y) / n
            numerator = sum_xy - tmp
            distance = numerator / denominator
            distance = round(distance,2)
            return distance

    # 紧邻
    def neighbors(self, username):
        """
        求和用户username 相邻的用户
        :param username: 用户
        :return: 距离元组（用户, 距离） 排序后的
        """
        distances = []
        for key in self.dataset:
            if key != username:
                # 得到两个用户的皮尔逊距离
                distance = self.pearson(self.dataset[username],self.dataset[key])
                distances.append((key, distance))
        # 排序
        distances.sort(key=lambda x: x[1],reverse=True)
        return distances
    
    # 给用户推荐
    def Recommend(self, user):
        #  存储 推荐的id 和分数
        recommendations = {}
        # 紧邻的
        neighborlist = self.neighbors(user)
        # 用户的评分
        user_dict = self.dataset[user]
        #
        totalDistance = 0.0
        
        # 最近k个邻居的总距离
        for i in range(self.k):
            totalDistance += neighborlist[i][1]
        if totalDistance==0.0:
            totalDistance=1.0
 
        # 向从不阅读的用户推荐书籍
        for i in range(self.k):
            weight = neighborlist[i][1] / totalDistance
            
            neighbor_name = neighborlist[i][0]
            # 得到推荐的商品和评分
            neighbor_books = self.dataset[neighbor_name]
            for bookid in neighbor_books:
                if not bookid in user_dict:
                    if bookid not in recommendations:
                        recommendations[bookid] = neighbor_books[bookid] * weight
                    else:
                        recommendations[bookid] += neighbor_books[bookid] * weight
                        
        # 转化为列表
        recommendations = list(recommendations.items())
        
        # 进行排序 使得结果都是从大到小
        recommendations.sort(key=lambda x: x[1], reverse = True)
        result = recommendations[:self.cnt]
        result = dict(result)
        return result

        
if __name__ == '__main__':
    bookid_list = []
    r = UserBasedCF()
    r.get_data("user_book.csv")
    bookid_and_weight_list = r.Recommend("Li Si")

    print("推荐的字典:", bookid_and_weight_list)
    pass
