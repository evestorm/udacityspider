import jieba
import jieba.analyse
from snownlp import SnowNLP

STOP_WORDS = '../config/stopwords.txt'
BOSON_SENTIMENT_SCORE = '../config/sentiment/BosonNLP_sentiment_score.txt'
NEGATIVE_COMMENT_WORDS = '../config/sentiment/negativecommentCN.txt'
DEGREE_WORDS = '../config/sentiment/degreewordsCN.txt'


def cal_sentiment(text):
    """
    calculate the sentiment value of a particular sentence powered by SnowNLP
    :param text: 
    :return: 
    """
    s = SnowNLP(text)

    return s.sentiments


def sentence2word(sentence):
    """
    cut the sentence into words and return the new words list without stop words 
    :param sentence: 
    :return: 
    """
    result_list = []
    original_list = jieba.cut(sentence, cut_all=True)
    stopwords_list = read_lines(STOP_WORDS)
    for _ in original_list:
        if _ not in stopwords_list:
            result_list.append(_)

    return result_list


def read_lines(filepath):
    word_list = list()
    with open(filepath, mode='rt', encoding='UTF-8') as f:
        for _ in f.readlines():
            word_list.append(_.replace('\n', ''))

    return word_list


if __name__ == '__main__':
    text = '面试效率很高，各环节之间并没有太多等待时间；各位面试官、HR都挺好。'
    sentiment = cal_sentiment(text)
    print(sentiment)
