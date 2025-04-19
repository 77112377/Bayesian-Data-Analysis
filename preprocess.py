import pandas as pd
import numpy as np
import os

def data_preprocess_feature(path, eachname):

    # load csv and dropduplicates and dropNAN and drop the feature we dont need
    dataset = pd.read_csv(path)
    dataset.drop(columns='Pollutant', inplace=True)
    dataset.drop(columns='Status', inplace=True)
    dataset.drop(columns='Longitude', inplace=True)
    dataset.drop(columns='Latitude', inplace=True)
    dataset.drop(columns='SiteId', inplace=True)
    dataset.drop(columns='County', inplace=True)
    dataset.drop(columns='WindSpeed', inplace=True)
    dataset.drop(columns='WindDirec', inplace=True)
    dataset.drop_duplicates(inplace=True)
    dataset.replace('-', np.nan, inplace=True)
    dataset.dropna(inplace=True)
    dataset.sort_values(by=['SiteName', 'PublishTime'], inplace=True)
    dataset.reset_index(inplace=True, drop=True)

    # tokenize the SiteName
    sitename = dataset['SiteName'].to_list()
    sitename = [eachname.index(i) for i in sitename]

    # read PublishTime and split it into year/month/day/time
    publishtime = dataset['PublishTime'].to_list()
    timesplit = np.array([i.split(' ') for i in publishtime])
    ymd = timesplit[:, 0]
    time = timesplit[:, 1]

    if '-' in ymd[0]:
        ymdsplit = np.array([i.split('-') for i in ymd])
    else:
        ymdsplit = np.array([i.split('/') for i in ymd])
    y = ymdsplit[:, 0]
    m = ymdsplit[:, 1]
    d = ymdsplit[:, 2]
    print(type(y[0]))

    time = np.array([i.split(':') for i in time])
    time = time[:, 0]
    time = [int(i) for i in time]

    # calculate the num of days after 2021/1/1
    days = countdays(y, m, d)

    # insert new columns
    dataset.insert(1, column='time', value=time)
    dataset.insert(1, column='siteid', value=sitename)
    dataset.insert(1, column='days', value=days)

    # drop PublishTime
    dataset.drop(columns='PublishTime', inplace=True)

    dataset.to_csv(path, index=False)

def countdays(y, m, d):
    time = []
    month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for i, j, k in zip(y, m, d):
        tmp = 0
        if i == '2022':
            tmp += 365
        if j != 1:
            for mday in range(int(j)-1):
                tmp += month[mday]
        tmp += int(k)
        time.append(tmp)
    return time

def data_preprocess_concat():
    csvname = get_file_name()
    df = []

    for path in csvname:
        df.append(pd.read_csv(path))
    
    allcsv = pd.concat(df)
    allcsv.drop_duplicates(inplace=True)
    allcsv.sort_values(by=['SiteName', 'days', 'time'], inplace=True)
    allcsv.reset_index(drop=True, inplace=True)
    allcsv.to_csv('alldata.csv', index=False)

def get_file_name():
    csvname=[]

    for home, dirs, files in os.walk('EPA_data2'):
        for filename in files:
            csvname.append(os.path.join(home, filename))

    return csvname

def data_preprocess_getAVG(path):
    data = pd.read_csv(path)
    data.sort_values(by=['SiteName', 'days', 'time'], inplace=True)
    data.reset_index(drop=True, inplace=True)

    site = np.unique(data['SiteName']).tolist()
    days = np.unique(data['days']).tolist()
    avg = []

    for s in site:
        for d in days:
            tmp = data.loc[(data['SiteName']==s) & (data['days']==d)]
            mean = tmp.mean(numeric_only=True)
            mean['SiteName'] = s
            avg.append(mean)

    df = pd.concat(avg, axis=1).T
    df.dropna(inplace=True)
    df.to_csv(path, index=False)


e = ['三義', '三重', '中壢', '中山', '二林', '仁武', '冬山', '前金', '前鎮', '南投', 
 '古亭', '善化', '嘉義', '土城', '埔里', '基隆', '士林', '大同', '大園', '大城', 
 '大寮', '大里', '安南', '宜蘭', '富貴角', '小港', '屏東', '屏東(枋寮)', '屏東(琉球)', 
 '崙背', '左營', '平鎮', '彰化', '彰化(員林)', '彰化(大城)', '復興', '忠明', '恆春', 
 '斗六', '新北(樹林)', '新店', '新港', '新營', '新竹', '新竹(北區)', '新莊', '朴子', 
 '松山', '板橋', '林口', '林園', '桃園', '桃園(三民)', '桃園(竹圍)', '桃園(蘆竹)', 
 '楠梓', '橋頭', '永和', '永和(環河)', '汐止', '沙鹿', '淡水', '湖口', '潮州', '竹山', 
 '竹東', '線西', '美濃', '臺南', '臺南(北門)', '臺南(學甲)', '臺南(麻豆)', '臺東', 
 '臺西', '花蓮', '苗栗', '菜寮', '萬華', '萬里', '西屯', '觀音', '豐原', '金門', 
 '關山', '陽明', '頭份', '馬公', '馬祖', '高雄(湖內)', '鳳山', '麥寮', '龍潭']
csvname = get_file_name()
for c in csvname:
    data_preprocess_feature(c, e)
    data_preprocess_getAVG(c)
    print(c, 'finish')
data_preprocess_concat()