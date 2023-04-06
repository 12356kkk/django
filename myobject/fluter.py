# coding:utf-8
import MySQLdb
#connect() 方法用于创建数据库的连接，里面可以指定参数：用户名，密码，主机等信息。
#这只是连接到了数据库，要想操作数据库需要创建游标。
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='12345678',
        db ='osdb',
        charset='utf8'
        )

#通过获取到的数据库连接conn下的cursor()方法来创建游标。
cur = conn.cursor()

tinydict = {'company_name': ['广东众图科技有限公司', '杭州艾航科技有限公司', '比亚迪股份有限公司', '江苏富士通通信技术有限公司', '咪付（广西）网络技术有限公司', '上海财才网信息科技有限公司', '珠海市智图数研信息技术有限公司', '深圳市闪易云科技有限公司', '雨浩科技（深圳）有限公司', '吉林省汇杰科技有限公司', '深圳弘杉数据科技有限公司', '小火花（西安）网络技术有限公司', '江苏鲲腾软件科技有限公司', '广州时时美电子商务有限公司', '迪爱斯信息技术股份有限公司', '上海游斐网络科技有限公司', '上海宇佑船舶科技有限公司', '青岛同济孵化器有限公司', '深圳市由你创科技有限公司', '南京鼎阳科技有限公司', '仁中（上海）股权投资基金管理有限公司', '深圳睿心智能医疗科技有限公司', '深圳艾融科技有限公司', '上海百秋新网商数字科技有限公司', '杭州杰毅生物技术有限公司', '北京华美汉盛信息技术有限公司', '广州天鹏计算机科技有限公司', '北京创新在线电子产品销售有限公司', '北京创腾科技有限公司', '杰创智能科技股份有限公司', '杭州泛利科技有限公司', '深圳乐能电子有限公司', '上海研鼎信息技术有限公司', '广州市宇华网络科技有限公司', '上海知汇云信息技术股份有限公司', '浙江森马服饰股份有限公司', '诚迈科技（南京）股份有限公司', '天津市华春能源集团有限公司', '上海国时资产管理有限公司', '北京金信润天信息技术股份有限公司武汉分公司', '上海鸿辰信息科技有限公司', '南京民基悠步信息技术有限公司', '施达汽车工程咨询（上海）有限公司', '北京百奥智汇科技有限公司', '广州立功科技股份有限公司', '蓝聪科技（上海）股份有限公司', '重庆道微投资管理有限公司', '北京多铁克数字技术有限公司', '上海川源信息科技有限公司', '擎翌（上海）智能科技有限公司'], 'job_name': ['Python开发高级工程师', 'Python开发工程师', 'Python开发工程师', 'JAVA\\/Python开发工程师', 'Python开发工程师', 'python后端开发', 'python爬虫开发工程师', 'Python开发工程师\\/薪资福利好', 'python数据开发\\/双休', 'python工程师', 'python实习生7K+奖金', 'Python开发工程师', 'Python开发工程师', 'Python爬虫工程师', 'Python开发工程师', '服务端软件工程师(Python）（BG）', 'Python 算法工程师', 'python 爬虫开发', 'Python 开发工程师', 'Python开发工程师', 'python量化开发工程师', 'Python后台开发工程师', 'Python开发工程师（双休学历不限）', 'Python工程师', 'Python开发工程师', 'Python开发工程师', 'Python高级开发工程师', 'python后端开发工程师', 'Python开发工程师', 'Python高级开发工程师', 'Python开发工程师', 'Python开发工程师', 'Python Web开发工程师', 'Python开发工程师', 'Python开发工程师', 'Python开发工程师', 'Python开发工程师（深圳）', 'Python开发工程师', '数据库及python工程师', 'Python开发工程师', '高级开发（Python\\/Java）', 'Python开发工程师', 'Python开发工程师', '后端开发工程师 （Python\\/数据分析和可视化）', 'Python开发工程师', 'Python开发工程师', 'Python开发工程师', 'Python开发工程师', 'Python软件工程师（OpenStack）', 'Python 后端开发'], 'company_size': ['150-500人', '少于50人', '10000人以上', '150-500人', '50-150人', '50-150人', '少于50人', '', '', '1000-5000人', '', '少于50人', '少于50人', '500-1000人', '500-1000人', '150-500人', '少于50人', '少于50人', '少于50人', '500-1000人', '少于50人', '150-500人', '150-500人', '1000-5000人', '500-1000人', '50-150人', '150-500人', '150-500人', '50-150人', '500-1000人', '50-150人', '150-500人', '50-150人', '少于50人', '50-150人', '1000-5000人', '1000-5000人', '50-150人', '少于50人', '50-150人', '少于50人', '50-150人', '50-150人', '150-500人', '1000-5000人', '少于50人', '少于50人', '50-150人', '50-150人', '少于50人'], 'city': ['佛山-南海区', '杭州-钱塘区', '西安-高新技术产业开发区', '苏州-高新区', '南宁', '上海-静安区', '珠海-横琴新区', '深圳-龙岗区', '深圳-宝安区', '长春', '深圳-宝安区', '西安-雁塔区', '无锡-无锡新区', '广州-荔湾区', '南京', '上海-长宁区', '上海-浦东新区', '青岛-黄岛区', '深圳-龙华区', '南京', '上海-浦东新区', '深圳-南山区', '深圳-福田区', '上海-长宁区', '杭州-余杭区', '北京-海淀区', '广州-天河区', '深圳-福田区', '苏州-工业园区', '广州-黄埔区', '杭州-钱塘区', '深圳-龙华区', '上海-浦东新区', '上海-虹口区', '上海-浦东新区', '上海-闵行区', '深圳-福田区', '天津-西青区', '上海-浦东新区', '武汉-洪山区', '郑州-金水区', '东莞', '上海-嘉定区', '北京-海淀区', '成都-金牛区', '上海', '重庆', '北京-海淀区', '上海-浦东新区', '上海-浦东新区'], 'salary': ['0.8-2万/月', '0.8-1.2万/月', '1.5-2万/月', '0.6-1万/月', '0.7-1万/月', '2-3万/月', '5-8千/月', '1.5-2万/月', '6-8千/月', '3-5千/月', '0.8-1万/月', '1-1.5万/月', '0.8-1.2万/月', '0.8-1.5万/月', '1-1.5万/月', '1.3-2万/月', '1.3-1.8万/月', '5-9千/月', '1-1.5万/月', '15-20万/年', '1.5-2万/月', '1.5-2.5万/月', '1-1.4万/月', '1-1.5万/月', '1-1.5万/月', '1.2-1.6万/月', '1.5-2.5万/月', '0.9-1.8万/月', '1.5-2万/月', '1.5-2.5万/月', '0.8-1.3万/月', '1.5-2万/月', '0.8-1.5万/月', '1.3-1.8万/月', '1-1.5万/月', '0.8-1.1万/月', '1.5-2万/月', '7-9千/月', '1.5-2.5万/月', '0.8-1.3万/月', '1-1.5万/月', '1-1.5万/月', '1-1.5万/月', '1.2-2.4万/月', '0.8-1.4万/月', '1-2万/月', '1-1.5万/月', '0.6-1.1万/月', '1.5-3万/月', '1-1.4万/月'], 'attribute_text': ['佛山-南海区|2年经验|大专|招若干人', '杭州-钱塘区|1年经验|本科|招1人', '西安-高新技术产业开发区|3-4年经验|本科|招若干人', '苏州-高新区|2年经验|本科|招1人', '南宁|5-7年经验|本科|招2人', '上海-静安区|3-4年经验|本科|招1人', '珠海-横琴新区|1年经验|大专|招2人', '深圳-龙岗区|2年经验|本科|招2人', '深圳-宝安区|无需经验|大专|招2人', '长春|2年经验|本科|招5人', '深圳-宝安区|1年经验|大专|招4人', '西安-雁塔区|1年经验|本科|招1人', '无锡-无锡新区|2年经验|本科|招2人', '广州-荔湾区|2年经验|大专|招1人', '南京|2年经验|本科|招若干人', '上海-长宁区|2年经验|大专|招若干人', '上海-浦东新区|3-4年经验|本科|招1人', '青岛-黄岛区|1年经验|本科|招3人', '深圳-龙华区|2年经验|大专|招1人', '南京|3-4年经验|大专|招2人', '上海-浦东新区|5-7年经验|本科|招2人', '深圳-南山区|1年经验|本科|招1人', '深圳-福田区|1年经验|大专|招1人', '上海-长宁区|2年经验|本科|招1人', '杭州-余杭区|2年经验|硕士|招2人', '北京-海淀区|3-4年经验|本科|招2人', '广州-天河区|2年经验|本科|招1人', '深圳-福田区|1年经验|本科|招5人', '苏州-工业园区|3-4年经验|本科|招1人', '广州-黄埔区|5-7年经验|本科|招若干人', '杭州-钱塘区|无需经验|本科|招5人', '深圳-龙华区|2年经验|本科|招1人', '上海-浦东新区|2年经验|本科|招1人', '上海-虹口区|2年经验|本科|招1人', '上海-浦东新区|3-4年经验|本科|招1人', '上海-闵行区|2年经验|大专|招1人', '深圳-福田区|3-4年经验|大专|招1人', '天津-西青区|无需经验|本科|招1人', '上海-浦东新区|3-4年经验|本科|招若干人', '武汉-洪山区|3-4年经验|大专|招5人', '郑州-金水区|3-4年经验|本科|招若干人', '东莞|2年经验|本科|招4人', '上海-嘉定区|1年经验|本科|招2人', '北京-海淀区|1年经验|本科|招1人', '成都-金牛区|2年经验|本科|招1人', '上海|1年经验|本科|招2人', '重庆|1年经验|本科|招1人', '北京-海淀区|无需经验|大专|招1人', '上海-浦东新区|5-7年经验|本科|招1人', '上海-浦东新区|3-4年经验|本科|招若干人'], 'category': ['互联网/电子商务', '计算机软件', '汽车', '通信/电信运营、增值服务', '计算机软件', '专业服务(咨询、人力资源、财会)', '互联网/电子商务', '计算机软件', '计算机软件', '计算机服务(系统、数据服务、维修)', '计算机软件', '计算机软件', '计算机软件', '贸易/进出口', '通信/电信/网络设备', '网络游戏', '计算机软件', '中介服务', '计算机软件', '机械/设备/重工', '金融/投资/证券', '计算机软件', '计算机软件', '互联网/电子商务', '制药/生物工程', '计算机软件', '计算机软件', '计算机软件', '计算机软件', '通信/电信/网络设备', '计算机软件', '互联网/电子商务', '仪器仪表/工业自动化', '计算机软件', '计算机软件', '多元化业务集团公司', '计算机软件', '新能源', '金融/投资/证券', '通信/电信/网络设备', '电子技术/半导体/集成电路', '计算机软件', '专业服务(咨询、人力资源、财会)', '制药/生物工程', '电子技术/半导体/集成电路', '计算机软件', '金融/投资/证券', '电子技术/半导体/集成电路', '计算机软件', '计算机软件'], 'job_welfare': ['五险一金 周末双休 带薪年假 专业培训 绩效奖金 团队聚餐 员工旅游', '五险一金 员工旅游 餐饮补贴 专业培训 绩效奖金 弹性工作 周末双休 年终奖金 交通补贴 股票期权', '五险一金 补充医疗保险 通讯补贴 交通补贴 定期体检 绩效奖金 免费班车', '五险一金 补充医疗保险 员工旅游 餐饮补贴 绩效奖金 定期体检 交通补贴 提供住宿 年终奖金', '交通补贴 餐饮补贴 年终奖金', '', '五险一金 餐饮补贴 交通补贴 周末双休 免费班车 员工旅游', '五险一金 节日福利 周末双休 朝九晚六', '五险一金 绩效奖金 年终奖金 员工旅游 出国机会', '餐饮补贴 通讯补贴 年终奖金 加班补贴 五险一金 免费班车 定期体检', '五险一金 员工旅游 定期体检 弹性工作 年终奖金 绩效奖金 项目奖金 朝九晚六 周末双休', '', '周末双休 五险一金 带薪年假 绩效奖金 做五休二 定期体检', '五险一金 全勤奖 餐饮补贴 专业培训 每年调薪', '五险一金 补充公积金 补充医疗保险 年终奖金 定期体检 餐饮补贴 绩效奖金', '', '五险一金 绩效奖金 年终奖金 员工宿舍', '五险一金 年终奖金 绩效奖金 年终分红 餐饮补贴 带薪年假 周末双休', '五险一金 专业培训 年终奖金 员工旅游', '五险一金 员工旅游 交通补贴 餐饮补贴 通讯补贴 绩效奖金 年终奖金 定期体检 周末双休', '绩效奖金 年终奖金 弹性工作 专业培训 五险一金 出国机会 股票期权', '五险一金 专业培训 绩效奖金 年终奖金 弹性工作 巨大发展空间 先进技术培训', '五险一金 员工旅游 餐饮补贴 弹性工作 定期体检', '绩效奖金 餐饮补贴 带薪年假 五险一金', '五险一金 员工旅游 交通补贴 餐饮补贴 专业培训 绩效奖金 年终奖金 定期体检', '五险一金 补充医疗保险 员工旅游 交通补贴 餐饮补贴 弹性工作 定期体检 周末双休', '周末双休 带薪年假 餐饮补贴 绩效奖金 丰厚奖金 股票期权 六险一金 定期体检 弹性工作', '周末双休 带薪年假 五险一金 节日福利 餐饮补贴', '五险一金 补充医疗保险 补充公积金 交通补贴 餐饮补贴 通讯补贴 年终奖金 定期体检 弹性工作', '五险一金 餐饮补贴 定期体检 专业培训 免费班车 员工旅游 补充公积金 年终奖金', '五险一金 员工旅游 绩效奖金 年终奖金 股票期权 弹性工作', '带薪年假 绩效奖金 全勤奖 节日福利 专业培训 年终奖金 员工晋升', '五险一金 绩效奖金 员工旅游 餐饮补贴 年终奖金 定期体检', '带薪年假 年终奖金 定期体检 弹性工作', '五险一金 员工旅游 绩效奖金 年终奖金 定期体检', '绩效奖金 节日福利 上市公司 专业培训 五险一金 定期体检 弹性工作 通讯补贴 交通补贴', '五险一金 周末双休 弹性工作 节日福利 带薪年假', '五险一金 交通补贴 领导好 员工旅游 通讯补贴 管理规范 岗位晋升 餐饮补贴 津贴福利', '五险一金 交通补贴 餐饮补贴 通讯补贴 专业培训 晋升通道', '五险一金 员工旅游 年终奖金 绩效奖金 专业培训 定期体检', '五险一金 餐饮补贴 年终奖金 绩效奖金 定期体检 专业培训 员工旅游', '五险一金 年终奖金', '定期体检 员工旅游 五险一金 补充医疗保险 年终奖金', '五险一金 通讯补贴 年终奖金 定期体检 意外险 弹性工作 餐饮补贴 交通补贴 年度体检', '五险一金 周末双休 带薪年假 员工旅游 年终奖金 定期体检 绩效奖金', '', '五险一金 绩效奖金 年终奖金 弹性工作 员工旅游 股票期权 专业培训 餐饮补贴', '周末双休 带薪年假 五险一金 餐饮补贴 年终奖金 员工旅游', '五险一金 年终奖金 弹性工作', '五险一金 员工旅游 定期体检']}

list= ['company_name','job_name','company_size','city','salary','attribute_text','category','job_welfare']

for i  in range(50):
    u0 = int(i+1)
    u1 = tinydict[list[0]][i]
    u2 = tinydict[list[1]][i]
    u3 = tinydict[list[2]][i]
    u4 = tinydict[list[3]][i]
    u5 = tinydict[list[4]][i]
    u6 = tinydict[list[5]][i]
    u7 = tinydict[list[6]][i]
    u8 = tinydict[list[7]][i]
    sql = "insert into info (id,company_name,job_name,company_size,city,salary,attribute_text,category,job_welfare)"\
          " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(query=sql, args=[u0,u1,u2,u3,u4,u5,u6,u7,u8])
    print("****第"+str(i+1)+"行插入成功****!")


#conn.commit()方法在提交事物，在向数据库插入一条数据时必须要有这个方法，否则数据不会被真正的插入。
conn.commit()

#cur.close() 关闭游标
cur.close()

#conn.close()关闭数据库连接
conn.close()