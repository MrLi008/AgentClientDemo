import sys
from typing import Self
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QComboBox,
    QTextEdit,
    QTabWidget,
)
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, pyqtSlot, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
from PyQt5.QtNetwork import QNetworkCookie
from PyQt5.QtCore import QSize
import json
import codecs
import os
import requests
import numpy as np
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

root = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.getenv("baiduce_api_key_v1", "")
SECRET_KEY = os.getenv("baiduce_api_secret_v1", "")

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY,
    }
    s = str(requests.post(url, params=params).json().get("access_token"))

    return s


class BaiduCeApi(object):
    def __init__(self):
        self.access_token = get_access_token()

    def __new__(cls) -> Self:
        if not hasattr(cls, "instance"):
            cls.instance = super(BaiduCeApi, cls).__new__(cls)
        return cls.instance

    def token(self):
        return self.access_token


access_token = BaiduCeApi().token()
modelname = "THUDM/chatglm3-6b-32k"

# from transformers import AutoTokenizer, AutoModel
# tokenizer = AutoTokenizer.from_pretrained(modelname, trust_remote_code=True, device='cuda')
# model = AutoModel.from_pretrained(modelname, trust_remote_code=True, device='cuda')
# model = model.eval()
import re
import time


def ana(
    text,
):
    pattern = r"^\d+\.\s+(.*)$"
    titles = re.findall(pattern, text, re.MULTILINE)
    # 将字符串中不符合文件名的字符替换为_
    titles = [i.replace("/", "_").replace(":", "_") for i in titles]
    return titles


import markdown


def cv_txt2html(txt):
    return markdown.markdown(txt, extensions=["tables"])


def out(txt):
    f = codecs.open("pyqt-out.txt", "a", encoding="utf-8")
    f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\n")
    f.write(txt + "\n\n")

    f.write("\n")
    f.close()


import hashlib
from datetime import datetime


def fname_format(txt):
    return hashlib.md5(txt.encode("utf-8")).hexdigest()


def chat(txt):
    fname = f"chat-{fname_format(txt)}.json"
    if os.path.exists(fname):
        return json.load(open(fname, "r", encoding="utf-8"))["result"]

    if random.random() >= 0:
        response = requests.request(
            "POST",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token="
            + access_token,
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "messages": [
                        {"role": "user", "content": txt},
                    ],
                    "disable_search": False,
                    "enable_citation": False,
                    "temperature": 0.4,
                }
            ),
        )
        if response.status_code == 200:
            # print('request-ok', response.json())

            s = response.json().get("result", "")
        else:
            print("request-error", response.json())

    # else:
    #     s = model.chat(tokenizer, txt,
    #         temperature=1,
    #         top_p=0.7,
    #         )[0]
    out(txt)
    if len(s) == 0:
        print("error: no result check")
    out(s)
    json.dump(
        {"result": s, "msg": txt, "date": datetime.now().strftime("%Y-%m-%d %H")},
        open(fname, "w", encoding="utf-8"),
        ensure_ascii=False,
    )
    # print(txt)
    # print(s)
    return s


title = "客户端demo-v0.1.0 qq952934650"
# 行业类别 子类别 细分类别 应用场景
data = dict()
if os.path.exists(f"客户端demo.txt"):
    
    for i, line in enumerate(
        codecs.open(f"客户端demo.txt", "r", encoding="utf-8").readlines()
    ):
        item = json.loads(line)
        if item["行业类别"] not in data:
            data[item["行业类别"]] = dict()
        if item["子类别"] not in data[item["行业类别"]]:
            data[item["行业类别"]][item["子类别"]] = dict()
        if item["细分类别"] not in data[item["行业类别"]][item["子类别"]]:
            data[item["行业类别"]][item["子类别"]][item["细分类别"]] = item["应用场景"]
        # if i > 100:
        #     break


# 登录地址 用于制作项目代码 后续会逐步开源哦
MYURL = "http://localhost:29001"


# 用于登录和验证
def set_csrf_cookie(cookie_store, url, csrf_token):
    """
    设置cookie，用于登录和验证
    :param cookie_store: QNetworkCookieJar对象，用于存储cookie
    :param url: 用于登录和验证的URL
    :param csrf_token: 登录和验证所需的CSRF令牌
    :return: None
    """
    cookie = QNetworkCookie()
    cookie.setName(b"csrftoken")
    cookie.setValue(csrf_token.encode())
    cookie_store.setCookie(cookie, QUrl(url))

'''

{
    "代码示例": [
        "根据{v0}所列出的名称，给出一段详细的解释和python代码示例，字数控制在1000字左右，并包含注释，要求看不出来是AI生成的内容"
    ]
}
'''
tagnamepaire = json.load(open(f"agent.json", "r", encoding="utf-8"))


CSS_COMBOBOX = """  
            QComboBox {  
                border: 1px solid #73AD21; /* 边框颜色和宽度 */  
                border-radius: 5px; /* 圆角 */  
                padding: 3px; /* 内边距 */  
                min-width: 120px; /* 最小宽度 */  
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #F0F0F0, stop:1 #C5C5C5); /* 背景渐变 */  
                color: #333; /* 文本颜色 */  
            }  
  
            QComboBox::drop-down {  
                subcontrol-origin: padding;  
                subcontrol-position: top right;  
                width: 25px;  
                border-left-width: 1px;  
                border-left-color: darkgray;  
                border-left-style: solid; /* 下拉箭头旁边的边框 */  
                border-top-right-radius: 3px; /* 下拉箭头区域的圆角 */  
                border-bottom-right-radius: 3px;  
                background-color: #E5E5E5; /* 下拉箭头背景色 */  
            }  
  
            QComboBox QAbstractItemView {  
                border: 2px solid #73AD21; /* 下拉列表边框 */  
                selection-background-color: #CCE5CC; /* 选中项背景色 */  
                color: #333; /* 文本颜色 */  
                outline: 0; /* 移除轮廓 */  
            }  

        """
height_combobox = 900


class MultiLevelComboBox(QWidget):
    def __init__(self):
        super().__init__()
        shape_oneline = 50
        self.select_data = data
        self.select_texts = [
            "",
            "",
            "",
            "",
            "",
        ]

        # 创建布局
        layout = QVBoxLayout(self)

        layout_h = QHBoxLayout(self)

        # 创建第一个 QComboBox
        self.combo1 = QComboBox(self)
        self.combo1.addItem("")
        self.combo1.addItems(self.select_data.keys())
        self.combo1.currentIndexChanged.connect(self.on_combo1_changed)
        layout_h.addWidget(self.combo1)

        # 创建第二个 QComboBox，初始为空
        self.combo2 = QComboBox(self)
        self.combo2.currentIndexChanged.connect(self.on_combo2_changed)
        layout_h.addWidget(self.combo2)
        # 创建第3个 QComboBox，初始为空
        self.combo3 = QComboBox(self)
        layout_h.addWidget(self.combo3)

        layout.addLayout(layout_h)

        # 文本录入
        self.text_tp = QLineEdit(
            self,
        )
        self.text_tp.setPlaceholderText("关键词有哪些")
        self.text_tp.height = 10
        layout.addWidget(self.text_tp)

        # 配置提交按钮
        self.submit_button = QPushButton("推荐", self)
        self.submit_button.clicked.connect(self.on_submit_clicked)
        layout.addWidget(self.submit_button)

        # 推荐结果展示
        self.combo = QComboBox(self)
        self.combo.setStyleSheet(CSS_COMBOBOX)
        layout.addWidget(self.combo)

        # 手动输入题目
        self.title_edit = QTextEdit(
            self, 
        )
        self.title_edit.setPlaceholderText("录入解析目标")
        self.title_edit.setMaximumHeight(shape_oneline*2)
        layout.addWidget(self.title_edit)

        # 配置提交按钮
        self.submit_button_title = QPushButton("启动", self)
        self.submit_button_title.clicked.connect(self.on_submit_title_clicked)
        layout.addWidget(self.submit_button_title)

        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # 配置tab标签页
        qtab_root = QTabWidget(self)
        qtab_root.setMinimumHeight(height_combobox)

        qtab = QTabWidget(self)
        self.qltab = {}
        for index, tab_title in enumerate(tagnamepaire["tag"]):
            tab1 = QWidget()
            tab1.layout = QVBoxLayout(tab1)
            qltab1 = QWebEngineView(self)
            qltab1.setHtml("")
            qltab1.setMinimumHeight(height_combobox)
            tab1.layout.addWidget(
                qltab1,
                0,
                Qt.AlignTop,
            )
            self.qltab[index] = qltab1
            qtab.addTab(tab1, tab_title)

        qtab_root.addTab(qtab, "左侧第一个分析")

        qtab_code = QTabWidget(self)

        tab1 = QWidget()
        tab1.layout = QVBoxLayout(tab1)
        self.qltab1 = QWebEngineView(self)
        # qltab1.setHtml('构建')
        
        self.load_myurl()
        self.qltab1.setMinimumHeight(height_combobox)
        tab1.layout.addWidget(
            self.qltab1,
            0,
            Qt.AlignTop,
        )
        qtab_code.addTab(tab1, "构建")
        qtab_root.addTab(qtab_code, "构建")

        layout.addWidget(qtab_root)

        qltab2 = QWidget(self)
        qltab2.layout = QHBoxLayout(
            qltab2,
        )
        self.webview_edit2 = QWebEngineView(
            self,
        )
        self.webview_edit2.setHtml("Empty")
        self.webview_edit2.setMinimumHeight(height_combobox)

        qltab2.layout.addWidget(
            self.webview_edit2,
            1,
        )
        self.text_edit2 = QTextEdit(
            self,
        )
        self.text_edit2.setText("Empty")
        self.text_edit2.setMinimumHeight(height_combobox)
        qltab2.layout.addWidget(
            self.text_edit2,
            1,
        )
        qtab_root.addTab(qltab2, "右侧第一个汇总")

        # 创建一个 QTextEdit 控件
        self.text_edit = QTextEdit(
            self,
        )
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet(
            """
                                     QTextEdit {
                                     background-color: #f0f0f0;
                                     border: 1px solid #ccc;
                                     padding: 5px;
                                     }
        """
        )
        self.text_edit.setFont(QFont("Arial", 12))
        self.text_edit.setMaximumWidth(200)
        self.text_edit.setMaximumHeight(100)

        # 设置多行文本内容
        self.text_edit.setPlainText("分析结果")
        layout.addWidget(
            self.text_edit,
        )

        # 主界面配置
        self.setGeometry(100, 100, 2200, 800)
        self.setWindowTitle(title)

        # init variable
        self.this_token = 0
        self.step = 0

    def load_myurl(self):
        # csrftoken
        response = requests.get(f"{MYURL}/api/ucsrf")
        response.raise_for_status()  # 确保请求成功
        csrf = response.json().get("csrfToken")
        print("csrf: ", csrf)

        self.qltab1.setUrl(QUrl(MYURL))

        set_csrf_cookie(self.qltab1.page().profile().cookieStore(), MYURL, csrf)

    @pyqtSlot(int)
    def on_combo1_changed(self, index):
        # 根据第一个 QComboBox 的选择更新第二个 QComboBox 的选项
        selected_text = self.combo1.currentText()
        self.select_texts[0] = selected_text
        self.update_combo2(selected_text)

    def on_combo2_changed(self, index):
        selected_text = self.combo2.currentText()
        self.select_texts[1] = selected_text
        self.update_combo3(selected_text)

    def update_combo2(self, selected_text):
        # 清除第二个 QComboBox 的选项
        self.combo2.clear()

        # 根据第一个 QComboBox 的选择添加新的选项到第二个 QComboBox
        if selected_text in data:
            self.combo2.addItems(data[selected_text].keys())
        self.select_texts[1] = list(data[selected_text].keys())[0]

    def update_combo3(self, selected_text):
        # 清除第三个 QComboBox 的选项
        self.combo3.clear()
        self.select_texts[1] = selected_text
        # 根据第二个 QComboBox 的选择添加新的选项到第三个 QComboBox
        if self.select_texts[1] in data[self.select_texts[0]] and len(
            data[self.select_texts[0]][self.select_texts[1]]
        ):
            self.combo3.addItems(
                data[self.select_texts[0]][self.select_texts[1]].keys()
            )
            self.select_texts[2] = list(
                data[self.select_texts[0]][self.select_texts[1]].keys()
            )[0]

    def on_submit_clicked(
        self,
    ):
        print(self.select_texts)
        tp = f"""根据行业类别{self.select_texts[0]},以及子类别{self.select_texts[1]},以及细分类别{self.select_texts[2]},应用场景{self.select_texts[3]},请给出10个最相关的课题名称。
相关的关键词有：{self.text_tp.text()}，联想到相关的具体事务与系统，推荐一些常见的系统名称，要求难度符合一般本科生的毕设,一行一个，按序号给出
"""
        self.step = 0
        # 清空combo
        self.combo.clear()
        self.combo.addItems(ana(chat(tp)))

    def upgrade_step(
        self,
    ):
        v = 1 / 8
        self.step += v
        self.progressBar.setValue(int(self.step * 100))

    def on_submit_title_clicked(
        self,
    ):
        # tp = f'''根据行业类别{self.select_texts[0]},以及子类别{self.select_texts[1]},以及细分类别{self.select_texts[2]},应用场景{self.select_texts[3]},并根据选择的题目：{self.combo.currentText()},
        # 给出系统的功能点和系统涉及到的用户类型，并说明用户的用例和流程
        # '''
        req_html = dict()

        def _title_ana(tp, i):
            print("Task: ", i, " start.", datetime.now())
            self.this_token += len(tp)

            self.upgrade_step()
            markdown_text = chat(
                tp.format(
                    **{
                        "title_selected": title_selected,
                        "industry": self.select_texts[0],
                        "sub_industry": self.select_texts[1],
                        "sub_sub_industry": self.select_texts[2],
                        "application_scene": self.select_texts[3],
                    }
                )
            )
            html = cv_txt2html(markdown_text)
            req_html[i] = {"markdown_text": markdown_text, "html": html}
            return (i, html)

        self.this_token = 0

        title_selected = self.title_edit.toPlainText()
        if len(title_selected) == 0:
            title_selected = self.combo.currentText()
            self.title_edit.setText(title_selected)
        print("开始处理： ", title_selected)
        self.text_edit.setText("")
        start = time.time()

        # for index, tp in enumerate(tagnamepaire['tp']):
        #     _title_ana(tp,  index)
        with ThreadPoolExecutor(max_workers=8) as executor:
            items = [
                executor.submit(_title_ana, tp, index)
                for index, tp in enumerate(tagnamepaire["tp"])
            ]
            for item in as_completed(items):
                i, html = item.result()
                print("Task: ", i, " done.", datetime.now())

                self.qltab[i].setHtml(f"{html}<br/><br/><br/><br/>")
                self.this_token += len(html)
                self.upgrade_step()

        # 依次将文本追加到 QTextEdit 控件
        htmls = []
        mk_texts = []
        for i, item in sorted(
            req_html.items(),
            key=lambda x: x[0],
        ):
            title = tagnamepaire["tag"][i]
            htmls.append(item["html"])
            mk_texts.append(f'\n# {i+1}.{title}\n\n{item["markdown_text"]}\n\n')
        self.webview_edit2.setHtml("".join(htmls))
        self.text_edit2.setText("".join(mk_texts))

        end = time.time()
        second = round(end - start)
        minit = second // 60

        tspend = f"{second}秒 | {minit}分"

        self.text_edit.setText(
            f"""分析完成。。。。
耗时：{tspend}
消耗Token：{self.this_token}

"""
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiLevelComboBox()
    # 设置默认字体大小
    QApplication.setFont(QFont("Microsoft YaHei", 20))
    window.show()
    sys.exit(app.exec_())
