import pandas as pd
import numpy as np

# 将数据集中--转化成Nan
def replace_null(df):
    df = df.replace('--', np.nan)
    df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric)
    return df

# 处理数据集年份一列
def replace_year(df):
    # 去掉字符串中的 "年" 字符，然后转换为数字
    year_numbers = df["Unnamed: 0"].str.replace('年', '').astype(int)
    df["Unnamed: 0"] = year_numbers
    df.rename(columns={"Unnamed: 0": "年份"}, inplace=True)
    return df

# 使用线性插值填充缺失值
def fill_missing_values(df):
    df = df.infer_objects()
    df = df.interpolate(method='linear', limit_direction='both')
    return df

# 导入数据
med_fee = pd.read_excel('./data/指标/财政支出中卫生经费(万元).xlsx')
med_beds = pd.read_excel('./data/指标/卫生机构床位数(张).xlsx')
med_personnels = pd.read_excel('./data/指标/卫生技术人员数(人).xlsx')
med_professors = pd.read_excel('./data/指标/执业(助理)医师人员数(人).xlsx')
med_nurse = pd.read_excel('./data/指标/注册护士数(人).xlsx')

tables = {'fee': med_fee, 'beds': med_beds, 'personnels': med_personnels, 'professors': med_professors, 'nurse': med_nurse}

# 预处理指标数据
for name in tables.keys():
    table = tables[name]
    table.drop(index=[0], inplace=True)
    table = replace_null(table)
    table = replace_year(table)
    if name == 'beds':
        # 恢复小于100的数到十万级，并保留缺失值
        table = table.map(lambda x: x * 10000 if pd.notnull(x) and x < 100 else x)
    table = fill_missing_values(table)
    table.to_csv(f'./data/index/{name}.csv', index=False)
    print(f'{name}处理完成')