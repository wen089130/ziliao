import jieba
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class fenci():
    def cut_word(text):
        # 传入一个词组然后进行自动分词
        # print("中文输入的内容为：" + text)
        # 用空格来连接结巴分词之后的列表
        result = " ".join(list(jieba.cut(text)))
        # print("默认的结巴分词的结果为：")
        # print(result)
        return result

    def count_ch1(self):
        # 中文特征提取，自动分词
        data = ["今天的天气很晴朗", "心情也跟着好起来", "学习机器学习真有意思"]
        # 进行分词
        data_cut = []
        for text in data:
            data_cut.append(self.cut_word(text))
        # 实例化一个转换器类
        transfor = CountVectorizer()
        # 调用fit_transform()
        data_new = transfor.fit_transform(data_cut)

        # print(transfor.get_feature_names())
        # print(data_new)
        # print("转换成n维数组：")
        # print(data_new.toarray())

    def tfidf(self):
        # 使用TF-idf进行文本特征提取
        # data = ["工程材料/构配件/设备供应单位资格报审表", "心情也跟着好起来", "学习机器学习真有意思"]
        data = ["工程材料/构配件/设备供应单位资格报审表"]
        # 进行分词
        data_cut = []
        for text in data:
            data_cut.append(fenci.cut_word(text))
        # 实例化一个转换器类
        transfor = TfidfVectorizer()
        # 调用fit_transform()
        data_new = transfor.fit_transform(data_cut)
        aa = transfor.get_feature_names()
        return aa
        # for i in range(0, len(aa)):
        #    if aa[i].endswith('报审'):
        #         print(aa[i])
        #    if aa[i].endswith('构配件'):
        #         print(aa[i])
        #         # b = str(result['words_result'][i]['words'])
        # print(transfor.get_feature_names())
        # print(transfor.get_feature_names())
        # print(data_new)
        #
        # print("转换成n维数组：")
        # print(data_new.toarray())
        # return None
    # tfidf()
