from stocks.schema import df


# return dataset description
def dataset_description(df):
    df = df.drop(['stock_date', 'id'], axis=1)
    df = df.describe()
    statistic = df.to_dict('dict')
    items = list(statistic.keys())
    result = []
    getter_items_sub = {}
    getter = []
    data = []

    for k, v in statistic.items():
        for n_k, n_v in v.items():
            if n_k == '25%':
                n_k = 'Q1'
                n_v = round(n_v, 2)
            elif n_k == '50%':
                n_k = 'Q2'
                n_v = round(n_v, 2)
            elif n_k == '75%':
                n_k = 'Q3'
                n_v = round(n_v, 2)
            elif n_k == 'mean':
                n_v = round(n_v, 2)
            elif n_k == 'std':
                n_v = round(n_v, 2)
            elif n_k == 'max':
                n_v = round(n_v, 2)
            elif n_k == 'min':
                n_v = round(n_v, 2)
            elif n_k == 'count':
                n_v = round(n_v, 2)
            getter_items_sub.update({n_k: n_v})
        result.append(getter_items_sub)
        getter_items_sub = {}

    for index, item in enumerate(items):
        getter.append({"name": item})
    #
    for i in range(len(items)):
        res = {**result[i], **getter[i]}
        data.append(res)

    return data


description = dataset_description(df)
