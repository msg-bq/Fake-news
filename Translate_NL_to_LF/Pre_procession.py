import re
file_path = 'total-副-完整-5月特殊符号.xls'

def read_pd(file_path, type_data):  # type_data = Real or Fake
    train_df = pd.read_excel(file_path, header=0)
    train_df['text'] = train_df.iloc[:, 1]
    # train_df['text'] = train_df.iloc[:, 1] + train_df.iloc[:, 2] + train_df.iloc[:, 3] + train_df.iloc[:, 4]
    train_df = train_df.drop(train_df.columns[[2, 3, 4]], axis=1)
    train_df.columns = ['label', 'text']
    train_df = train_df[['text', 'label']]
    train_df['text'] = train_df['text'].apply(lambda x: x.replace('\\', ' '))

    def filter_str(desstr, restr=''):
    # 保留中英文及数字（不确定是否过于严格？比如起码保留句号逗号和问号）
        res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9^.^,^?^'^ ]")
        return res.sub(restr, desstr)

    for i in range(len(train_df['text'])):
        tmp = train_df['text'][i].lower()
        train_df['text'][i] = filter_str(tmp)

    if(type_data == 'train'):
        for i in range(3):
            train_df = train_df.sample(frac=1.0, random_state=1234)
        train_data = train_df[:int(len(train_df) * 0.7)] #
        eval_data = train_df[int(len(train_df) * 0.7):]
        return train_data, eval_data
    else:
        return train_df
