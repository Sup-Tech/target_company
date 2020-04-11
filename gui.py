from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, \
    QGridLayout, QScrollArea, QScrollBar, QHBoxLayout, QLayout, QSizePolicy, \
    QProgressBar, QStatusBar, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QWaitCondition, QMutex, QTimer
from model.widgets_models import *
import sqlite3
import requests


class Thread(QThread):

    valueChange = pyqtSignal(int)
    id_pipLine = pyqtSignal(list)
    task_finished = pyqtSignal()

    def __init__(self, results, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        # results 是从raw_datas查询的所有数据 一般以城市为条件查询
        self.results = results
        self._isPause = True
        self._value = 1
        self.cond = QWaitCondition()
        self.mutex = QMutex()

    def next(self):
        print("下一组数据")
        self._isPause = False
        self.cond.wakeAll()
        self._isPause = True

    def run(self):
        while True:
            self.mutex.lock()
            if self._isPause:
                print('run')
                for i in self.results:
                    id = i[0]
                    company_id = i[1]
                    job_id = i[2]
                    item = [id, company_id, job_id]
                    print(item)
                    self.id_pipLine.emit(item)
                    print('发送item')
                    self.cond.wait(self.mutex)
                    if self._value == len(self.results):
                        self.task_finished.emit()
                    print('_value', self._value)
                    self.valueChange.emit(self._value)
                    self._value += 1
            self.mutex.unlock()


class DatasFilterWindow(QWidget):

    def __init__(self):
        super(DatasFilterWindow, self).__init__()
        self.setWindowTitle('数据筛选')
        self.setFixedSize(650, 600)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint|Qt.WindowCloseButtonHint)
        self.setup_ui()
        self.conn = sqlite3.connect('target_company.db')
        self.signal_slot()

        self.area = ''
        self.Id = None
        self.jobId = None
        # 标志
        self.is_begined = False

    def setup_ui(self):
        # 创建布局

        layout_1 = QVBoxLayout()
        layout_1_1 = QHBoxLayout()
        layout_1_1_1 = QGridLayout()
        layout_1_1_2 = QGridLayout()

        # 创建QSizePolicy
        fixed_sp = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # 创建控件
        company_name_tag = QLabel('公司名称')
        self.company_name = QLabel('')
        company_addr_tag = QLabel('公司地址')
        self.company_addr = QLabel('')
        company_scale_tag = QLabel('公司规模')
        self.company_scale = QLabel('')
        company_area_tag = QLabel('所处地区')
        self.company_area = QLabel('')
        job_name_tag = QLabel('职位名称')
        self.job_name = QLabel('')
        self.status_tag = QLabel('')
        # QTextBrowser
        self.company_desc_browser = QTextBrowser()
        self.job_desc_browser = QTextBrowser()
        # QLineEdit
        self.note_ledit = QLineEdit()
        self.note_ledit.setPlaceholderText('备注')
        self.possible_ledit = QLineEdit()
        self.possible_ledit.setPlaceholderText('可能性')
        self.keyword_edit = QLineEdit()
        self.keyword_edit.setPlaceholderText('城市')
        self.keyword_edit.setFixedWidth(62)
        self.keyword_edit.setSizePolicy(fixed_sp)
        # 按钮
        self.save_btn = QPushButton('保存')
        self.save_btn.setSizePolicy(fixed_sp)
        self.begin_btn = QPushButton('开始')
        self.begin_btn.setSizePolicy(fixed_sp)
        self.del_btn = QPushButton('删除')
        self.del_btn.setSizePolicy(fixed_sp)
        self.process_bar = QProgressBar()
        self.process_bar.setFormat('%v/%m')
        # 创建滚动区域 & 滚动条
        self.scroll_area_company = QScrollArea()
        scroll_bar_company = QScrollBar()
        self.scroll_area_job = QScrollArea()
        scroll_bar_job = QScrollBar()
        # 添加滚动区域widget对象
        self.scroll_area_company.setWidget(self.company_desc_browser)
        self.scroll_area_job.setWidget(self.job_desc_browser)
        # 添加滚动条
        self.scroll_area_company.addScrollBarWidget(scroll_bar_company, Qt.AlignLeft)
        self.scroll_area_job.addScrollBarWidget(scroll_bar_job, Qt.AlignLeft)

        # 布置布局
        layout_1.addLayout(layout_1_1)
        layout_1_1.addLayout(layout_1_1_1)
        layout_1_1_1.addWidget(job_name_tag, 1,1,1,1)
        layout_1_1_1.addWidget(self.job_name, 1,2,1,3)
        layout_1_1_1.addWidget(company_name_tag, 2,1,1,1)
        layout_1_1_1.addWidget(self.company_name, 2,2,1,3)
        layout_1_1_1.addWidget(company_scale_tag, 3,1,1,1)
        layout_1_1_1.addWidget(self.company_scale,3,2,1,1)
        layout_1_1_1.addWidget(company_area_tag, 3,3,1,1)
        layout_1_1_1.addWidget(self.company_area, 3,4,1,1)
        layout_1_1_1.addWidget(company_addr_tag, 4,1,1,1)
        layout_1_1_1.addWidget(self.company_addr, 4,2,1,3)
        layout_1_1.addLayout(layout_1_1_2)
        layout_1_1_2.addWidget(self.keyword_edit,1,1,1,1)
        layout_1_1_2.addWidget(self.begin_btn,1,2,1,1)
        layout_1_1_2.addWidget(self.note_ledit,2,1,1,2)
        layout_1_1_2.addWidget(self.possible_ledit,3,1,1,2)
        layout_1_1_2.addWidget(self.save_btn,4,1,1,1)
        layout_1_1_2.addWidget(self.del_btn,4,2,1,1)

        layout_1.addWidget(self.company_desc_browser)
        layout_1.addWidget(self.job_desc_browser)
        layout_1.addWidget(self.process_bar)
        layout_1.addWidget(self.status_tag,Qt.AlignCenter)

        self.setLayout(layout_1)

    def signal_slot(self):
        self.save_btn.clicked.connect(self.save)
        self.del_btn.clicked.connect(self.delete)
        self.begin_btn.clicked.connect(self.begin)

    def begin(self):
        c = self.conn.cursor()
        # 根据输入的城市 获取对应的城市数据
        city = self.keyword_edit.text()
        if city:
            sql = "select id from areas where area='{}';".format(city)
            try:
                area_id = c.execute(sql).fetchone()[0]
            except IndexError:
                print('该城市数据不存在')
            except Exception as e:
                print(e)
            # 筛选出该区域的所有数据
            else:
                sql = "select id, company_id, job_id from raw_datas where area_id='{}' and is_read=0;".format(area_id)
                results = c.execute(sql).fetchall()
                print(results)
                total = len(results)
                self.process_bar.setMaximum(total)
                # 主要效果 阻塞for循环 通过按钮解除阻塞
                self.t = Thread(results)
                self.t.id_pipLine.connect(self.show_loop)
                self.t.valueChange.connect(self.process_bar.setValue)
                self.t.task_finished.connect(self.finished)
                self.t.start()

                self.area = city
                self.is_begined = True
                print('--')
        else:
            print('未输入城市')

    def show_loop(self, e):
        """循环显示"""
        print('show_loop', e)
        self.Id = e[0]
        company_id = e[1]
        self.jobId = e[2]
        c = self.conn.cursor()
        sql = "select company_name, company_address, company_scale, company_desc from companies where id='{}';".format(company_id)
        self.company_info = c.execute(sql).fetchone()
        print(self.company_info)
        sql = "select job_name, job_desc from jobs where id='{}';".format(self.jobId)
        self.job_info = c.execute(sql).fetchone()
        print(self.job_info)
        self.job_name.setText(self.job_info[0].strip())
        self.company_name.setText(self.company_info[0])
        self.company_scale.setText(self.company_info[2])
        self.company_area.setText(self.area)
        self.company_addr.setText(self.company_info[1])
        self.company_desc_browser.setPlainText(self.company_info[-1])
        self.job_desc_browser.setPlainText(self.job_info[1])

    def save(self):
        """
        保存该组数据到新的数据表
        并更新地图用数据
        并显示下一条"""
        possible = self.possible_ledit.text()
        note = self.note_ledit.text()

        if possible:
            c = self.conn.cursor()
            # 获取公司地址的经纬度
            addr = self.company_info[1]
            ak = 'ysZHXY6AwYQYcXLuhTCkV2a1YvOk5Dm2'
            url = 'http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}'.format(addr, ak)
            result = requests.get(url=url).json()['result']
            print('result', result)
            # 插入数据到map_datas
            sql = "insert into map_datas(lng, lat, precise, confidence, comprehension, level) " \
                  "values({}, {}, {}, {}, {}, '{}');".format(result['location']['lng'], result['location']['lat'],
                                                             result['precise'], result['confidence'],
                                                             result['comprehension'], result['level'])
            c.execute(sql)
            # 获取刚刚插入数据的map_id
            sql = "select max(id) from map_datas;"
            max_map_id = c.execute(sql).fetchone()[0]
            print('max_map_id', max_map_id)
            # 插入数据到final_datas
            sql = "insert into final_datas(possible, note, raw_id, map_id) values('{}','{}',{}, {});".format(possible, note, self.Id, max_map_id)
            c.execute(sql)
            # 更新raw_datas的is_read值 表示已经筛选过,下次不再显示
            sql = "update raw_datas set is_read=1 where id={};".format(self.Id)
            c.execute(sql)
            self.conn.commit()
            # 清除输入控件当前的数据
            self.note_ledit.clear()
            self.possible_ledit.clear()
            # 检测当前城市是否还有未筛选的数据组
            if self.is_begined and self.process_bar.value() < self.process_bar.maximum():
                self.t.next()
            else:
                print('没有next了')
        else:
            # 提醒没有填写可能性
            self.status_tag.setText('没有写可能性')
            QTimer.singleShot(2000, self.clear_statu)




    def delete(self):
        """删除该组数据 并显示下一条"""
        c = self.conn.cursor()
        sql = "delete from raw_datas where id={};".format(self.Id)
        c.execute(sql)
        sql = "delete from jobs where id={};".format(self.jobId)
        c.execute(sql)
        self.conn.commit()
        if self.is_begined and self.process_bar.value() < self.process_bar.maximum():
            self.t.next()
        else:
            print('没有next了')

    def finished(self):
        print('任务结束')

    def clear_statu(self):

        self.status_tag.setText('')


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.Q = Manager().Queue()
        self.setup_ui()
        self.signal_slots()

    def setup_ui(self):
        self.search = QLineEdit()
        self.search.setPlaceholderText('Search')
        self.crawl_btn = QPushButton('开始爬取')
        self.filter_datas_btn = QPushButton('数据筛选')
        crawl_nums_tag = QLabel('此次爬取数量')
        self.crawl_nums = QLabel('0')
        repeat_fingerprint_nums_tag = QLabel('重复指纹数量')
        self.repeat_fingerprint_numts = QLabel('0')
        error_crawl_nums_tag = QLabel('爬取出错数量')
        self.error_nums = QLabel('0')
        self.papa_map_btn = QPushButton('爸爸地图')
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout1.addStretch(0)
        layout1.addWidget(self.search)
        layout1.addWidget(self.crawl_btn)
        layout1.addStretch(1)
        layout1.addWidget(self.filter_datas_btn)
        layout.addLayout(layout1)
        layout2 = QHBoxLayout()
        layout2.addWidget(crawl_nums_tag)
        layout2.addWidget(self.crawl_nums)
        layout2.addWidget(repeat_fingerprint_nums_tag)
        layout2.addWidget(self.repeat_fingerprint_numts)
        layout2.addWidget(error_crawl_nums_tag)
        layout2.addWidget(self.error_nums)
        layout2.addStretch(1)
        layout2.addWidget(self.papa_map_btn)
        layout.addLayout(layout2)
        self.log_browser = QTextBrowser()
        self.process_bar = QProgressBar()
        layout.addWidget(self.log_browser)
        layout.addWidget(self.process_bar)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def signal_slots(self):
        self.filter_datas_btn.clicked.connect(self.open_datas_filter)
        # self.crawl_btn.clicked.connect(self.start_crawl)

    def open_datas_filter(self):
        """打开数据筛选界面"""
        self.data_filter = DatasFilterWindow()
        self.data_filter.show()



#     def start_crawl(self):
#         if self.crawl_btn.text() == '开始爬取':
#             self.crawl_btn.setText('停止爬取')
#             self.log_browser.clear()
#             self.p = Process(target=crawl, args=(self.Q, self.search.text()))
#             self.p.start()
#         else:
#             self.crawl_btn.setText('开始爬取')
#             self.p.terminate()
#             self.p.kill()
#
#
# def crawl(Q, keywords):
#     process = CrawlerProcess({
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Language': 'en',
#       'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
#       'ROBOTSTXT_OBEY' : False,
#       'LOG_LEVEL' : 'WARNING',
#       'DOWNLOAD_DELAY' : 2,
#       'HTTPPROXY_ENABLED': False})
#     process.crawl(A58Spider, Q=Q, keywords=keywords)
#     process.start()