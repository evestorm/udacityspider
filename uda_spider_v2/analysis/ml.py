"""
build for machine learning processing
"""
import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression


def normalise(csv_filepath):
    """
    load csv data and normalize it
    :param csv_filepath:
    :return:
    """
    df = pd.read_csv(csv_filepath)[[
        'companyScore', 'describeScore', 'comprehensiveScore', 'interviewerScore', 'usefulCount', 'myScore',
        'replyCount', 'isAnonymous']][1:]
    senti_df = pd.read_csv(csv_filepath)['sentiment'][1:]
    labels_ = [1 if _ > 0.9 else 0 for _ in senti_df]
    df['isAnonymous'] = [int(_) for _ in df['isAnonymous']]
    df_scaled = pd.DataFrame(preprocessing.scale(df))

    return df_scaled, labels_


def logistic_regression_classify(dataframe, labels_):
    logistic_reg = LogisticRegression()
    index = int(len(dataframe) * 0.7)
    X_train = dataframe[:index][:]
    X_test = dataframe[index + 1:][:]

    y_train = labels_[:index][:]
    y_test = labels_[index + 1:][:]

    logistic_reg.fit(X_train, y_train)
    accuracy = logistic_reg.score(X_test, y_test)

    return accuracy


if __name__ == '__main__':
    df, labels_ = normalise('../spider/data/lagou_interviewee.csv')
    accuracy = logistic_regression_classify(df, labels_)
    print('The accuracy on test set is {:%}'.format(accuracy))
