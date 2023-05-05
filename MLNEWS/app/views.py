import datetime
import os
import random
import warnings

import joblib
import pandas as pd
import statsmodels.api as sm
import tushare as ts
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from statsmodels.tsa.arima.model import ARIMA
from tqdm import tqdm

from app import util
from app.models import *
from app.userBasedCF import UserBasedCF

warnings.filterwarnings('ignore')


# 验证登录
def check_login(func):
    def wrapper(request):
        # print("装饰器验证登录")
        cookie = request.COOKIES.get('uid')
        if not cookie:
            return redirect('/login/')
        else:
            return func(request)

    return wrapper


# Create your views here.
# 股票新闻列表
@check_login
def index(request):
    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name
    today = datetime.datetime.now()  # 日期对象
    today_str = today.strftime('%Y-%m-%d')  # 字符串
    if  not News.objects.filter(today=today_str):
        try:
            end_date = f'{today_str} 00:00:00'
            pro = ts.pro_api(
                '3353a5434adbc0ef40de059735453f3695986c7b87de4093b5f7eb39')  # 去 https://tushare.pro/ 自己注册并且获取apikey
            df = pro.news(src='sina', start_date='2018-11-21 09:00:00', end_date='2018-11-22 10:10:00')
            print(df)
            if not df.empty:
                for i in range(len(df)):
                    title = df.iloc[i]['title']
                    date = df.iloc[i]['pub_time']
                    src = df.iloc[i]['src']
                    if not News.objects.filter(title=title, date=date, src=src, today=today_str):
                        News.objects.create(title=title, date=date, src=src, today=today_str)
        except Exception as e:
            print(e)



    # df = pd.read_csv('haha.csv')
    # if not df.empty:
    #     for i in range(len(df)):
    #         title = df.iloc[i]['title']
    #         date = df.iloc[i]['pub_time']
    #         src = df.iloc[i]['src']
    #         if not News.objects.filter(title=title, date=date, src=src, today=today_str):
    #             News.objects.create(title=title, date=date, src=src, today=today_str)

    newlist = News.objects.all().order_by('-date')[:20]

    return render(request, 'index.html', locals())


def data2sql1(raw_json):
    code = raw_json['代码']
    name = raw_json['简称']
    date = raw_json['日期']

    # 有空的特征
    open = raw_json['开盘价(元)']
    open = float(open)

    high = raw_json['最高价(元)']
    high = float(high)

    low = raw_json['最低价(元)']
    low = float(low)

    close = raw_json['收盘价(元)']
    close = float(close)

    volume = raw_json['成交量(股)']
    try:
        volume = float(volume)
    except:
        volume = None

    price_change = raw_json['涨跌(元)']
    price_change = float(price_change)

    p_change = raw_json['涨跌幅(%)']
    try:
        p_change = float(p_change)
    except:
        p_change = None

    ma = raw_json['均价(元)']
    try:
        ma = float(ma)
    except:
        ma = None

    turnover = raw_json['换手率(%)']
    try:
        turnover = float(turnover)
    except:
        turnover = None

    lastclose = raw_json['前收盘价(元)']
    try:
        lastclose = float(lastclose)
    except:
        lastclose = None

    cjje = raw_json['成交金额(元)']
    try:
        cjje = float(cjje)
    except:
        cjje = None
    if not Stock.objects.filter(code=code, name=name, date=date, open=open, high=high, close=close,
                                low=low, volume=volume, price_change=price_change, ma=ma,
                                turnover=turnover, lastclose=lastclose, cjje=cjje, p_change=p_change):
        Stock.objects.create(code=code, name=name, date=date, open=open, high=high, close=close,
                             low=low, volume=volume, price_change=price_change, ma=ma,
                             turnover=turnover, lastclose=lastclose, cjje=cjje, p_change=p_change)
    # tmp = raw_json['A股流通市值(元)']
    # tmp = raw_json['B股流通市值(元)']
    # tmp = raw_json['总市值(元)']
    # tmp = raw_json['A股流通股本(股)']
    # tmp = raw_json['B股流通股本(股)']
    # tmp = raw_json['总股本(股)']
    # tmp = raw_json['市盈率']
    # tmp = raw_json['市净率']
    # tmp = raw_json['市销率']
    # tmp = raw_json['市现率']
    return 'finished'


# 加载数据到数据库中  并且对数据进行一定的清洗
def data2mysql(request):
    Stock.objects.all().delete()
    cnt = 0  # 统计股票数量
    for file in os.listdir(os.path.join('data', '上证A股')):
        if '.CSV' not in file:
            continue
        file_path = os.path.join('data', '上证A股', file)
        raw_json = pd.read_csv(file_path, encoding='gbk')

        for i in tqdm(range(len(raw_json))):
            code = raw_json.iloc[i]['代码']
            name = raw_json.iloc[i]['简称']
            date = raw_json.iloc[i]['日期']

            # 有空的特征
            open = raw_json.iloc[i]['开盘价(元)']
            open = float(open)

            high = raw_json.iloc[i]['最高价(元)']
            high = float(high)

            low = raw_json.iloc[i]['最低价(元)']
            low = float(low)

            close = raw_json.iloc[i]['收盘价(元)']
            close = float(close)

            volume = raw_json.iloc[i]['成交量(股)']
            try:
                volume = float(volume)
            except:
                volume = None

            price_change = raw_json.iloc[i]['涨跌(元)']
            price_change = float(price_change)

            p_change = raw_json.iloc[i]['涨跌幅(%)']
            try:
                p_change = float(p_change)
            except:
                p_change = None

            ma = raw_json.iloc[i]['均价(元)']
            try:
                ma = float(ma)
            except:
                ma = None

            turnover = raw_json.iloc[i]['换手率(%)']
            try:
                turnover = float(turnover)
            except:
                turnover = None

            lastclose = raw_json.iloc[i]['前收盘价(元)']
            try:
                lastclose = float(lastclose)
            except:
                lastclose = None

            cjje = raw_json.iloc[i]['成交金额(元)']
            try:
                cjje = float(cjje)
            except:
                cjje = None
            if not Stock.objects.filter(code=code, name=name, date=date, open=open, high=high, close=close,
                                        low=low, volume=volume, price_change=price_change, ma=ma,
                                        turnover=turnover, lastclose=lastclose, cjje=cjje, p_change=p_change):
                Stock.objects.create(code=code, name=name, date=date, open=open, high=high, close=close,
                                     low=low, volume=volume, price_change=price_change, ma=ma,
                                     turnover=turnover, lastclose=lastclose, cjje=cjje, p_change=p_change)
        cnt += 1
        if cnt >= 20:
            break

    return JsonResponse({'status': 1, 'msg': '操作成功'})


# 股票列表
class gupiaoList(View):
    def get(self, request):
        uid = int(request.COOKIES.get('uid', -1))
        if uid != -1:
            username = User.objects.filter(id=uid)[0].name
        raw_data = Stock.objects.all()

        code_list = list(set([i.code for i in raw_data]))
        code_list = sorted(code_list)

        if 'code' in request.GET:
            code = request.GET.get('code')
            History.objects.create(user_id=uid,code=code)
        else:
            code = code_list[0]
        # 是否收藏
        isstar = True if Star.objects.filter(user_id=uid,code=code) else False
        # 没有就需要爬取了
        # if not GuPiao.objects.filter(code=code):
        #     df = ts.get_hist_data(code)
        #
        #     df['date'] = df.index
        #     for i in tqdm(range(len(df))):
        #         date = df.iloc[i]['date']
        #         open = df.iloc[i]['open']
        #         high = df.iloc[i]['high']
        #         close = df.iloc[i]['close']
        #         low = df.iloc[i]['low']
        #         volume = df.iloc[i]['volume']
        #         price_change = df.iloc[i]['price_change']
        #         p_change = df.iloc[i]['p_change']
        #         ma5 = df.iloc[i]['ma5']
        #         ma10 = df.iloc[i]['ma10']
        #         ma20 = df.iloc[i]['ma20']
        #         v_ma5 = df.iloc[i]['v_ma5']
        #         v_ma10 = df.iloc[i]['v_ma10']
        #         v_ma20 = df.iloc[i]['v_ma20']
        #         turnover = df.iloc[i]['turnover']
        #         if not GuPiao.objects.filter(date=date, open=open, high=high, close=close, low=low, volume=volume,
        #                                      price_change=price_change, p_change=p_change,
        #                                      ma5=ma5, ma10=ma10, ma20=ma20, v_ma5=v_ma5, v_ma10=v_ma10, v_ma20=v_ma20,
        #                                      turnover=turnover, code=code):
        #             GuPiao.objects.create(date=date, open=open, high=high, close=close, low=low, volume=volume,
        #                                   price_change=price_change, p_change=p_change,
        #                                   ma5=ma5, ma10=ma10, ma20=ma20, v_ma5=v_ma5, v_ma10=v_ma10, v_ma20=v_ma20,
        #                                   turnover=turnover, code=code)

        if 'page' not in request.GET:
            page = 1
        else:
            page = int(request.GET.get('page'))
        data_list = Stock.objects.filter(code=code)[(page - 1) * 20: page * 20]
        return render(request, 'gupiaoList.html', locals())

    def post(self, request):

        return JsonResponse({'status': 1, 'msg': '操作成功'})
def  star(request):
    code = request.POST.get('code')
    print(code)
    uid = int(request.COOKIES.get('uid', -1))

    if Star.objects.filter(user_id=int(uid),code=code):
        Star.objects.filter(user_id=int(uid), code=code).delete()
        return  JsonResponse({'color':'black','msg':'取消收藏啦'})
    else:
        Star.objects.create(user_id=int(uid), code=code)
        return  JsonResponse({'color':'red','msg':'收藏啦'})


# ================================================= #
# ****************** 推荐   ******************* #
# ================================================= #
def tuijian(request):
    uid = int(request.COOKIES.get('uid', -1))
    train = dict()
    # 首先进行推荐
    # 收藏
    history = Star.objects.all()  # 10
    for item in history:
        if item.user_id not in train.keys():
            train[item.user_id] = {item.code: 1}
        else:
            train[item.user_id][item.code] = train[item.user_id].get(item.code, 0) + 10
    # 浏览历史
    history = History.objects.all()  # 0.1
    for item in history:
        if item.user_id not in train.keys():
            train[item.user_id] = {item.code: 0.1 * 1}
        else:
            train[item.user_id][item.code] = train[item.user_id].get(item.code, 0) + 1
    # 声明一个ItemBasedCF的对象
    try:
        item = UserBasedCF(train)
        recommedDict = item.Recommend(int(uid))  # 字典

    except:
        print("协同过滤异常啦")
        recommedDict = {}
    stockinfo = {i.code: i.name for i in Stock.objects.all()}
    stock_list = [
        {
            'code': k,
            'name': v,
            'score': 0,
        }
        for k, v in stockinfo.items()
    ]

    if len(recommedDict) == 0:
        msg = "你还没有在该网站有过收藏、浏览行为，请去浏览吧！"
    else:
        msg = ""
        for i in range(len(stock_list)):
            stock_list[i]['score'] = recommedDict[ stock_list[i]['code'] ]
    for i in range(len(stock_list)):
        code = stock_list[i]['code']
        url = f'https://stock.quote.stockstar.com/{code}tml'
        url = url.lower()
        stock_list[i]['url'] = url
        stock_list[i]['star'] = Star.objects.filter(code = code).count()
        stock_list[i]['history'] = History.objects.filter(code = code).count()
        stock_list[i]['is_star'] = True if Star.objects.filter(user_id=uid,code=code) else False
    data_list = stock_list
    # 判断升降
    code_list = list(set([item.code for item in Stock.objects.all()]))
    code_list = sorted(code_list)
    # 股票上涨的code
    add_list = []
    for code in tqdm(code_list):
        # 获取代码数据
        raw_data = Stock.objects.filter(code=code).order_by('date')
        # 找到最后的价格
        last_price = raw_data[len(raw_data)-1].close
        stock_train = pd.DataFrame()

        stock_train['开盘价'] = [i.open for i in raw_data]
        stock_train['最高价'] = [i.high for i in raw_data]
        stock_train['最低价'] = [i.low for i in raw_data]
        stock_train['收盘价'] = [i.close for i in raw_data]
        stock_train.index = pd.to_datetime([i.date for i in raw_data])
        stock_train = stock_train['收盘价']
        # print(stock_train)
        if os.path.exists(os.path.join('model', code + '.pkl')):
            model = joblib.load(os.path.join('model', code + '.pkl'))
        else:
            # 确定模型参数p q
            stock_diff_1 = stock_train.diff(1)

            stock_diff = stock_diff_1.dropna()
            # print(stock_diff)
            # 再次检验adf中p的值
            # dftest = adfuller(stock_diff)
            # print('adf检验之后的p的值：', dftest[1])
            # 使用aic 准则法   确定p和q的值
            res = sm.tsa.arma_order_select_ic(stock_diff, max_ar=5, max_ma=5, ic=['aic'])
            # print(res.aic_min_order)
            p, q = res.aic_min_order
            model = ARIMA(stock_train, order=(p, 1, q))
            model = model.fit()

            # 保存模型
            joblib.dump(model, os.path.join('model', code + '.pkl'))
        true_y = list(stock_train.values)
        # pre_y = list(pre_1.values)
        legend = ['预测值']
        date_x = [str(i.date) for i in raw_data]
        # 预测未来十天
        num = 10
        pre_1 = model.forecast(num)
        pre_y = list(pre_1.values)

        avg_price = sum(pre_y) / len(pre_y)
        # 如果是升值的股票，添加进去
        if avg_price > last_price:
            add_list.append(code)
    print(add_list)
    tmp = []
    for i in range(len(stock_list)):
        code = stock_list[i]['code']
        if code in add_list:
            tmp.append(stock_list[i])
    data_list = tmp
    return render(request,'tuijian.html',locals())


# 可视化
# @method_decorator(check_login,name='get') #
class plot(View):
    def get(self, request):

        """
        1 股票走势图 折线图
        2 股票 4个指数图折线图
        3 价格区间个数
        4 价格排行榜
        5 成交量和价格散点图
        :param request:
        :return:
        """
        uid = int(request.COOKIES.get('uid', -1))
        if uid != -1:
            username = User.objects.filter(id=uid)[0].name
        code_list = list(set([itme.code for itme in Stock.objects.all()]))
        if 'code' in request.GET:
            code = request.GET.get('code')
        else:
            code = code_list[0]

        raw_data = Stock.objects.filter(code=code)
        # 1 股票走势图

        main1 = raw_data.order_by('date')
        main1_x = [str(itme.date) for itme in main1]

        main1_y = [itme.close for itme in main1]

        # 2 股票 五个指数图折线图
        main2_legend = ['开盘价', '最高价', '收盘价', '最低价']
        main2 = raw_data.order_by('date')
        main2_x = [str(itme.date) for itme in main1]
        main2_y = [
            {
                'name': '开盘价',
                'type': 'line',
                'data': [itme.open for itme in main1]
            },
            {
                'name': '最高价',
                'type': 'line',
                'data': [itme.high for itme in main1]
            },
            {
                'name': '收盘价',
                'type': 'line',
                'data': [itme.close for itme in main1]
            },
            {
                'name': '最低价',
                'type': 'line',
                'data': [itme.low for itme in main1]
            },
        ]

        # 3 价格区间个数 2-10，
        main3_raw = raw_data
        main3 = [f'成交价{i}-{i + 1}区间' for i in range(2, 10)]
        main3_data = [{'name': item, 'value': 0} for item in main3]
        for item in main3_raw:
            close = item.close
            if close < 3:
                main3_data[0]['value'] = main3_data[0]['value'] + 1
            elif close < 4:
                main3_data[1]['value'] = main3_data[1]['value'] + 1
            elif close < 5:
                main3_data[2]['value'] = main3_data[2]['value'] + 1
            elif close < 6:
                main3_data[3]['value'] = main3_data[3]['value'] + 1
            elif close < 7:
                main3_data[4]['value'] = main3_data[4]['value'] + 1
            elif close < 8:
                main3_data[5]['value'] = main3_data[5]['value'] + 1
            elif close < 9:
                main3_data[6]['value'] = main3_data[6]['value'] + 1
            else:
                main3_data[7]['value'] = main3_data[7]['value'] + 1

        # 4 价格排行榜
        main4 = raw_data.order_by('-close')[:10]
        main4_x = [str(itme.date) for itme in main4]
        main4_y = [itme.close for itme in main4]

        # 5 成交量和价格散点图

        main5 = [[_.volume, _.close] for _ in raw_data if _.volume and _.close]
        print(main5)

        return render(request, 'plot.html', locals())

    def post(self, request):
        return HttpResponse('post方法')
        return JsonResponse({'status': 1, 'msg': '操作成功'})

# 预测
# @method_decorator(check_login,name='get') #
class predict(View):
    def get(self, request):
        uid = int(request.COOKIES.get('uid', -1))
        if uid != -1:
            username = User.objects.filter(id=uid)[0].name
        code_list = list(set([item.code for item in Stock.objects.all()]))
        code_list = sorted(code_list)

        if 'code' in request.GET:
            code = request.GET.get('code')
        else:
            code = code_list[0]

        # 获取代码数据
        raw_data = Stock.objects.filter(code=code).order_by('date')
        stock_train = pd.DataFrame()

        stock_train['开盘价'] = [i.open for i in raw_data]
        stock_train['最高价'] = [i.high for i in raw_data]
        stock_train['最低价'] = [i.low for i in raw_data]
        stock_train['收盘价'] = [i.close for i in raw_data]
        stock_train.index = pd.to_datetime([i.date for i in raw_data])
        stock_train = stock_train['收盘价']
        print(stock_train)
        if os.path.exists(os.path.join('model', code + '.pkl')):
            model = joblib.load(os.path.join('model', code + '.pkl'))
        else:
            # 确定模型参数p q
            stock_diff_1 = stock_train.diff(1)

            stock_diff = stock_diff_1.dropna()
            # print(stock_diff)
            # 再次检验adf中p的值
            # dftest = adfuller(stock_diff)
            # print('adf检验之后的p的值：', dftest[1])
            # 使用aic 准则法   确定p和q的值
            res = sm.tsa.arma_order_select_ic(stock_diff, max_ar=5, max_ma=5, ic=['aic'])
            # print(res.aic_min_order)
            p, q = res.aic_min_order
            model = ARIMA(stock_train, order=(p, 1, q))
            model = model.fit()

            # 保存模型
            joblib.dump(model, os.path.join('model', code + '.pkl'))
        true_y = list(stock_train.values)
        # pre_y = list(pre_1.values)
        legend = ['预测值']
        date_x = [str(i.date) for i in raw_data]
        # 预测未来十天
        num = 10
        pre_1 = model.forecast(num)
        pre_y = list(pre_1.values)
        date_x = []
        now_time = raw_data[len(raw_data)-1].date  # 日期对象
        for i in range(1, num+1):
            tmp_time = now_time + datetime.timedelta(days=i)
            tmp_str = datetime.datetime.strftime(tmp_time, '%Y-%m-%d')
            date_x.append(tmp_str)
        data = [{
            'name': '预测值',
            'type': 'line',
            'data': pre_y
        }]

        return render(request, 'predict.html', locals())

    def post(self, request):
        return HttpResponse('post方法')
        return JsonResponse({'status': 1, 'msg': '操作成功'})


# @method_decorator(check_login,name='get') #


@check_login
def my(request):
    uid = int(request.COOKIES.get('uid', -1))
    if uid != -1:
        username = User.objects.filter(id=uid)[0].name
    if request.method == "POST":
        name, tel, password = request.POST.get('name'), request.POST.get('tel'), request.POST.get('password1')
        User.objects.filter(id=uid).update(name=name, tel=tel, password=password)
        return redirect('/')
    else:
        my_info = User.objects.filter(id=uid)[0]
        return render(request, 'my.html', locals())


def test(request):
    return HttpResponse('测试完成')

# 登录
def login(request):
    if request.method == "POST":
        tel, pwd = request.POST.get('tel'), request.POST.get('pwd')
        if User.objects.filter(tel=tel, password=pwd):

            obj = redirect('/')
            obj.set_cookie('uid', User.objects.filter(tel=tel, password=pwd)[0].id, max_age=60 * 60 * 24)
            return obj
        else:
            msg = "用户信息错误，请重新输入！！"
            return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())

# 注册
def register(request):
    if request.method == "POST":
        name, tel, pwd = request.POST.get('name'), request.POST.get('tel'), request.POST.get('pwd')
        print(name, tel, pwd)
        if User.objects.filter(tel=tel):
            msg = "你已经有账号了，请登录"
        else:
            User.objects.create(name=name, tel=tel, password=pwd)
            msg = "注册成功，请登录！"
        return render(request, 'login.html', locals())
    else:
        msg = ""
        return render(request, 'register.html', locals())

# 注销
def logout(request):
    obj = redirect('/')
    obj.delete_cookie('uid')
    return obj

################################下面可能没用的


