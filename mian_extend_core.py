#--*--coding:utf-8--*--
from selenium import webdriver
# from lxml import etree
from selenium.webdriver.common.by import By
from  selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re,time,datetime
#平均抢一张票需要2.5秒
class Qiangpiao():
    def __init__(self):
        #使用火狐浏览器登录
        # self.driver =  webdriver.Firefox()
        #使用谷歌浏览器登录
        self.driver = webdriver.Chrome(executable_path="./chromedriver/chromedriver.exe")
        self.driver.add_cookie({})

        self.accurate_time_am = "{} 06:00:00".format(datetime.date.today().strftime("%Y-%m-%d"))
        self.accurate_time_pm = "{} 12:30:00".format(datetime.date.today().strftime("%Y-%m-%d"))
        # self.login_url = "https://kyfw.12306.cn/otn/login/init"
        self.login_url = "https://kyfw.12306.cn/otn/resources/login.html"
        self.index_url = "https://kyfw.12306.cn/otn/view/index.html"
        self.left_ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc"
        self.submit_order_url = "https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        self.pay_url = "https://kyfw.12306.cn/otn//payOrder/init?random=1545913901298"
        # self.html = etree.HTML(self.driver.page_source)

    def _wait(self):
        # self.passengers = input("请输入乘客姓名(乘客信息一定你已经保存在12306账户里面)，如有多人请用‘,’隔开，例如（张三,李四,王五）：").split(',')
        self.passengers = "刘伦杰".split(',')
        # self.train = input("请输入需要乘坐的车次：（若有多个车次请用‘,’隔开，例如：Z202,Z4190,Z264,T370,Z90,T155,Z190,Z36,Z14,T124,Z98,T96,T254,Z236,T180,Z122,Z168,3064,3016,G1032,G844,G470,G1122,G1032,G826,G840,G1012,G544,G554,G546,G1156,G1028,G1130,G1018,G1036,G1014,G650,G548,G1162,G1020,G1136,G1134,G1138,G1022,G1140").split(',')
        # 火车
        self.train = "Z202,Z4190,Z264,T370,Z90,T155,Z190,Z36,Z14,T124,Z98,T96,T254,Z236,T180,Z122,Z168".split(',')
        #高铁
        # self.train ={
        #     "高铁":"G1032,G844,G470,G1122,G1032,G826,G840,G1012,G544,G554,G546,G1156,G1028,G1130,G1018,G1036,G1014,G650,G548,G1162,G1020,G1136,G1134,G1138,G1022,G1140".split(','),
        #     "火车":"Z202,Z4190,Z264,T370,Z90,T155,Z190,Z36,Z14,T124,Z98,T96,T254,Z236,T180,Z122,Z168,3064".split(',')
        #              }
        # self.start = input("请输入出发地：")
        self.start = "广州"
        # self.destination = input("请输入目的地：")
        self.destination = "武汉"
        # self.start_date = input("请输入出发日（例如：2019-01-28）：")
        self.start_date = "2019-02-04"

    def _login(self):
        self.driver.get(self.login_url)
        self.driver.maximize_window()
        #等待访问网页是否加载
        WebDriverWait(timeout=600,driver=self.driver).until(EC.url_to_be(self.index_url))
        print("登录成功")

    def _order_ticket(self):
        flag = False
        while True:
            for one_train in self.train:
                s = time.time()
                print("=="*100)
                print("开始抢{}车次的票".format(one_train))
                try:
                    #跳转到搜索页面
                    self.driver.get(self.left_ticket_url)
                    print('到达车次搜索页面')
                    #等待出发地是否输入
                    WebDriverWait(timeout=1000,driver=self.driver).until(
                        EC.text_to_be_present_in_element_value((By.ID,"fromStationText"),self.start))
                    #等待目的地是否输入
                    WebDriverWait(timeout=1000,driver=self.driver).until(
                        EC.text_to_be_present_in_element_value((By.ID,"toStationText"),self.destination))
                    #等待出发日期是否输入
                    WebDriverWait(timeout=1000,driver=self.driver).until(
                        EC.text_to_be_present_in_element_value((By.ID,"train_date"),self.start_date))
                    #等待查询按钮是否能够被点击
                    WebDriverWait(timeout=1000, driver=self.driver).until(
                        EC.element_to_be_clickable((By.ID, "query_ticket")))
                    #获取查询车次列表按钮
                    search_submit = self.driver.find_element_by_id("query_ticket")
                    # 点击查询
                    search_submit.click()
                    #如果没有到点，每隔30秒刷新页面，准点再开抢
                    # if not flag:
                    #     am_number = time.mktime(time.strptime(self.accurate_time_am, '%Y-%m-%d %H:%M:%S'))
                    #     pm_number = time.mktime(time.strptime(self.accurate_time_pm, '%Y-%m-%d %H:%M:%S'))
                    #     while True:
                    #         now_number = time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
                    #         self.driver.refresh()
                    #         # if(pm_number>=now_number>=am_number):
                    #         #     # 等待查询按钮是否能够被点击
                    #         #     WebDriverWait(timeout=1000, driver=self.driver).until(
                    #         #         EC.element_to_be_clickable((By.ID, "query_ticket")))
                    #         #     # 获取查询车次列表按钮
                    #         #     search_submit = self.driver.find_element_by_id("query_ticket")
                    #         #     # 点击查询
                    #         #     search_submit.click()
                    #         #     flag = True
                    #         #     break
                    #         if ( now_number >= am_number):
                    #             # 等待查询按钮是否能够被点击
                    #             WebDriverWait(timeout=1000, driver=self.driver).until(
                    #                 EC.element_to_be_clickable((By.ID, "query_ticket")))
                    #             # 获取查询车次列表按钮
                    #             search_submit = self.driver.find_element_by_id("query_ticket")
                    #             # 点击查询
                    #             search_submit.click()
                    #             flag = True
                    #             break
                    #等待车次列表是否加载出来
                    WebDriverWait(timeout=1000,driver=self.driver).until(EC.presence_of_all_elements_located((By.XPATH,"//tbody[@id='queryLeftTable']/tr")))
                    print("进入车次详细列表页面")
                    # 获取目标车次的tr标签中的id值
                    try:
                        price_id = self.driver.find_element_by_xpath("//tr[@datatran='" + one_train + "']").get_attribute("id")
                    except:
                        print("没有{}车次的信息".format(one_train))
                        continue
                    ticket_id = price_id.replace("price","ticket")
                    tr = self.driver.find_element_by_xpath("//tr[@id='" + ticket_id + "']")

                    #遍历车次列表
                    train_info = {}
                    #过滤掉不需要的标签,只保留余票信息的标签
                    tds = tr.find_elements_by_xpath("./td[@hbdata]")
                    left_ticket = list(map(lambda x: x.text, tds))
                    train_info[one_train] = {
                        "商务座特等座": left_ticket[0],
                        "一等座": left_ticket[1],
                        "二等座": left_ticket[2],
                        "高级软卧": left_ticket[3],
                        "软卧": left_ticket[4],
                        "动卧": left_ticket[5],
                        "硬卧": left_ticket[6],
                        "软座": left_ticket[7],
                        "硬座": left_ticket[8],
                        "无座": left_ticket[9],
                        "其他": left_ticket[10],
                    }
                    print(train_info)
                    if "有" in train_info[one_train].values() or True in list(
                            map(lambda x: x.isdigit(), train_info[one_train].values())):
                        while True:
                            #获取预定按钮
                            Orderbtn72 = tr.find_element_by_class_name("btn72")
                            if Orderbtn72:
                                #提交预定按钮
                                Orderbtn72.click()
                                break
                        # 等待是否进入了提交订单页面
                        WebDriverWait(timeout=1000, driver=self.driver).until(EC.url_to_be(self.submit_order_url))
                        print("到达乘客订票确认页面")
                        # 等待乘客按钮是否加载完毕
                        WebDriverWait(timeout=1000, driver=self.driver).until(
                            EC.presence_of_all_elements_located((By.XPATH, "//ul[@id='normal_passenger_id']/li/label")))
                        passenger_labels = self.driver.find_elements_by_xpath("//ul[@id='normal_passenger_id']/li/label")
                        for passenger_label in passenger_labels:
                            if passenger_label.text in self.passengers:
                                passenger_label.click()
                        #选取票的类别（如果是高铁则选择二等座,普通货车将选择硬座,相应类型的票没有按照默认的选票）
                        select = self.driver.find_element_by_id("seatType_1")
                        select.click()
                        #1代表火车硬座,O代表高铁二等座,M代表高铁一等座
                        seat_type = {'火车硬座':'1','高铁二等座':'O','高铁一等座':'M',"火车硬卧":'3',"火车软卧":"4"}
                        seat_options= self.driver.find_elements_by_xpath("//select[@id='seatType_1']/option")
                        marking = 0
                        for seat_option in seat_options:
                            value = seat_option.get_attribute("value")
                            if value == seat_type["高铁二等座"] or value == seat_type["火车硬卧"]:
                                seat_option.click()
                                marking = 1
                                break
                        if not marking:
                            continue
                        # 获取确认订单按钮
                        submitbtn = self.driver.find_element_by_id("submitOrder_id")
                        submitbtn.click()
                        #等待提交按钮是否出来
                        WebDriverWait(timeout=1000,driver=self.driver).until(EC.presence_of_all_elements_located((By.ID,"qr_submit_id")))
                        print("确认按钮加载完毕")
                        #循环点击N次
                        while True:
                            count =1
                            confirm_btn = self.driver.find_element_by_id("qr_submit_id")
                            # 等待提交按钮是否出来
                            WebDriverWait(timeout=1000, driver=self.driver).until(
                                EC.element_to_be_clickable((By.ID, "qr_submit_id")))
                            if confirm_btn:
                                print("开始点击")
                                try:
                                    confirm_btn.click()
                                    print("成功抢到"+one_train+"车次的票")
                                    e = time.time()
                                    print("本次抢" + one_train + "车次的票总共花了" + str(e - s) + "秒")
                                    print("**" * 100)
                                    return
                                except:
                                    print("点击失败")
                                break

                                # time.sleep(1)
                                # print("当前网址：",self.driver.current_url)
                                #判断是否到达支付页面
                                # if "https://kyfw.12306.cn/otn//payOrder/init?" in self.driver.current_url:
                                #     print("订票结束")
                                #     return
                            else:
                                print("第{}次没有找到确定按钮".format(count))
                                count += 1
                    else:
                        print("暂时无票")
                        print("**" * 100)

                except Exception as e:
                    print("没有抢到{}车次的票".format(one_train))
                e = time.time()
                print("本次抢"+one_train+"车次的票总共花了"+str(e-s)+"秒")
                print("**" * 100)

    def run(self):
        self._wait()
        self._login()
        self._order_ticket()

if "__main__" == __name__:
    q_ticket = Qiangpiao()
    q_ticket.run()