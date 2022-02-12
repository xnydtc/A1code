import pandas as pd
import numpy as np
import datetime
import numpy_financial as npf
import matplotlib.pyplot as plt
data = pd.read_csv('A1d.csv')
now = datetime.datetime.now().strftime('%Y-%m-%d')
now = datetime.datetime.strptime(now, '%Y-%m-%d')
data['maturity date'] = data['maturity date'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y'))


def calculate_ytm(price, coupon, maturity_date, par_value=100, start_date=now):
    intervals = (maturity_date - start_date).days * 2 / 365
    if intervals < 1:
        intervals = 0
    n = round(intervals)
    res = iy(n, coupon*par_value, par_value, price)
    return res


def iy(n, pmt=0, fv=0, pv=0):
    values = []
    values.append(-pv)
    for i in range(n):
        values.append(pmt)
    values[-1] += fv
    iy = npf.irr(values)
    return round(iy, 6) * 100


origin = pd.DataFrame()
for i in ['10', '11', '12', '13', '14', '17', '18', '19', '20', '21']:
    empty = []
    for x in range(10):
        s = calculate_ytm(data[i].iloc[x], data['coupon'].iloc[x], data['maturity date'].iloc[x])
        empty.append(s)
    res = pd.DataFrame(empty)
    res.columns = [i]
    origin = pd.concat([origin, res], axis=1)
res = origin
origin = origin.fillna(0).T
# Yield curve
# origin.plot()
# plt.xlabel('days')
# plt.ylabel('ytm')
# plt.show()

one_year_spot = res['10'].iloc[1] / 100


def cal_spot(coupon, n_period, pre_rate, ytm):
    ytm = ytm/100
    left = 0
    for i in range(n_period):
        left = left + coupon / ((ytm+1) ** (i + 1))
    left = (left + 100) / (ytm + 1) ** n_period

    rigt = 0
    for x in range(len(pre_rate)):
        rigt = coupon / (pre_rate[x] + 1) ** (x + 1) + rigt

    res = ((coupon + 100) / (left - rigt))**(1/n_period) - 1
    return res


def forward(spot_1, spot_2,n1,n2):
    res = ((1 + spot_1) ** n1 / (1+spot_2) ** n2) **(1/(n1-n2)) - 1
    return res


matr = pd.DataFrame()
for i in [1, 2, 4, 6, 9]:
    matrix_1 = res.iloc[i, :]
    temp = matrix_1.shift(-1)
    w = pd.concat([matrix_1,temp],axis=1)
    w.columns = ['x','y']
    w['res'] = np.log(w['y']/w['x'])
    w.dropna(inplace=True)
    del w['x']
    del w['y']
    matr = pd.concat([matr, w], axis=1)

matrix_first = matr.T
matrix_two = pd.DataFrame()
for i in range(10, 22):
    if str(i) in ['15','16']:
        ...
    else:
        r12 = cal_spot(0.0175, 2, [one_year_spot], res[str(i)].iloc[2])
        r23 = cal_spot(0.0125, 3, [one_year_spot,r12],res[str(i)].iloc[4])
        r34 = cal_spot(0.0025, 4, [one_year_spot,r12,r23],res[str(i)].iloc[6])
        r45 = cal_spot(0.0125, 5, [one_year_spot,r12,r23,r34],res[str(i)].iloc[9])
        f11 = forward(r12, one_year_spot,2,1)
        f12 = forward(r23, one_year_spot,3,1)
        f13 = forward(r34, one_year_spot,4,1)
        f14 = forward(r45, one_year_spot,5,1)
        temp = pd.DataFrame([f11,f12,f13,f14])
        matrix_two = pd.concat([matrix_two,temp],axis=1)

m1 = matrix_first.values
m2 = matrix_two.values

z = np.zeros((max(m1.shape), max(m1.shape)))
z[:m1.shape[0],:m1.shape[1]] = m1
m1 = z

eigenvalue_1, feature_1 = np.linalg.eig(m1)

z = np.zeros((max(m2.shape), max(m2.shape)))
z[:m2.shape[0],:m2.shape[1]] = m2
m2 = z
eigenvalue_2, feature_2 = np.linalg.eig(m2)
print(eigenvalue_1, feature_1)
print(eigenvalue_2, feature_2)

if __name__ == '__main__':
    d1 = data
    print((d1['maturity date'].iloc[0]-now).days)
    # s = calculate_ytm(d1['10'].iloc[1], d1['coupon'].iloc[1], d1['maturity date'].iloc[1])
    r12 = cal_spot(0.0175, 2, [one_year_spot], res['10'].iloc[2])
    r23 = cal_spot(0.0125, 3, [one_year_spot,r12],res['10'].iloc[4])
    r34 = cal_spot(0.0025, 4, [one_year_spot,r12,r23],res['10'].iloc[6])
    r45 = cal_spot(0.0125, 5, [one_year_spot,r12,r23,r34],res['10'].iloc[9])
    y = [one_year_spot*100, r12*100, r23*100, r34*100, r45*100]
    x = ['one_year', 'two_year', 'three_year',  'four_year','five_year']
    plt.scatter(x, y, alpha=0.6)
    plt.xlabel('spot_rate_range')
    plt.ylabel('rate')
    plt.show()

    f11 = forward(r12, one_year_spot,2,1)
    f12 = forward(r23, one_year_spot,3,1)
    f13 = forward(r34, one_year_spot,4,1)
    f14 = forward(r45, one_year_spot,5,1)
    y1 = [f11*100, f12*100, f13*100, f14*100]
    x1 = ['f11', 'f12', 'f13',  'f14']
    plt.scatter(x1, y1)
    plt.xlabel('forward_rate_range')
    plt.ylabel('rate')
    plt.show()



