# -*- coding: utf-8 -*

from kivy.config import Config
# ウィンドウサイズの設定
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '720')
import kivy
kivy.require('1.9.1')

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.utils import get_color_from_hex
from kivy.resources import resource_add_path
from kivy.factory import Factory
from kivy.properties import StringProperty, ListProperty, ObjectProperty

import os
import csv
import codecs

# ファイルのパス(unit conversionフォルダの中にあるファイルの絶対パス)
file_path = os.path.dirname(os.path.abspath(__file__))

# フォントの設定
resource_add_path('fonts')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')


class PopupWindow(Popup):
    text_input = ObjectProperty(None)
    delete = ObjectProperty(None)
    regist = ObjectProperty(None)
    

    
# 数値や入力内容を記録するためのクラス
# @classmethodをつけるとコンテキストを生成しなくても他クラスから参照できるようになる
class Holder():
    # ボタンのインデックス
    ids = 0
    # 7つのボタン*3シート(+末尾の配列に"が何故か追記されていく現象の回避用に)+1して計22個の要素を用意
    memos = [''] * 22
    # ページ番号
    page = 1
    # ページ番号に対応したボタンのインデックスの範囲を指定するための配列
    button_index = range(7)
    
    # 指定した場所の内容を返す
    @classmethod
    def setLabel(self, id_num):
        return(str(self.memos[id_num]))
    
    # csvファイルが存在すれば内容をmemosに読み出す。
    # csvファイルが無ければ作成する
    @classmethod
    def setFile(self):
        try:
            file = open("task_data.csv","r")
            self.memos = file.readline().split(',')
            # 配列の末尾の先頭に"が追加されていく現象回避のために空の文字列をセット
            self.memos[21] = ''
            file.close()
        except:
            file = open("task_data.csv","w")
            writer = csv.writer(file)
            writer.writerow(self.memos)
            file.close()
            
    # 押されたボタンの番号を記録
    @classmethod
    def setIds(self, id_num):
        self.ids = id_num
    
    # 入力された内容をcsvファイルに記録
    @classmethod
    def setText(self, txt):
        self.memos[self.ids] = txt
        file = open("task_data.csv","w")
        writer = csv.writer(file)
        writer.writerow(self.memos)
        file.close()
        
    # 指定場所の内容を削除
    @classmethod
    def deleteText(self):
        self.memos[self.ids] = ''
        file = open("task_data.csv","w")
        writer = csv.writer(file)
        writer.writerow(self.memos)
        file.close()
        
    # 何ページの内容を表示するかを記録
    @classmethod
    def page_set(self, index):
        if index == 1:
            self.page = 1
            self.button_index = range(7)
        elif index == 2:
            self.page = 2
            self.button_index = range(7,14)
        else:
            self.page = 3
            self.button_index = range(14,21)
        
    # 現在開いているページ番号を返す
    @classmethod
    def page_num(self):
        return(int(self.page))
    
    # 現在開いているページのボタンのインデックスの範囲を返す
    @classmethod
    def page_range(self):
        return(self.button_index)
        
    # memosの内容を表示(使わないかも)
    @classmethod
    def printMemos(self):
        print(self.memos)


class Task(BoxLayout):
    # とりあえずボタンの数を7つとする
    text1 = StringProperty()
    text2 = StringProperty()
    text3 = StringProperty()
    text4 = StringProperty()
    text5 = StringProperty()
    text6 = StringProperty()
    text7 = StringProperty()
    
    # アプリ実行時の初期化の処理
    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)
        # ファイルの読み込みとページ番号(1とする)及びボタンのラベルのセット
        Holder.setFile()
        Holder.page_set(1)
        self.setButtonLabel()

    # ボタンのラベルにテキストをセット
    def setButtonLabel(self):
        for i in Holder.page_range():
            if i%7 == 0: self.ids.button1.text = Holder.setLabel(i)
            elif i%7 == 1: self.ids.button2.text = Holder.setLabel(i)
            elif i%7 == 2: self.ids.button3.text = Holder.setLabel(i)
            elif i%7 == 3: self.ids.button4.text = Holder.setLabel(i)
            elif i%7 == 4: self.ids.button5.text = Holder.setLabel(i)
            elif i%7 == 5: self.ids.button6.text = Holder.setLabel(i)
            else: self.ids.button7.text = Holder.setLabel(i)
    
    # ボタンが押された場合の処理
    def buttonClicked(self, id_num):
        # 開いているページに対応したラベルを表示する
        # page1なら0~6、page2なら7~13、page3なら14~20
        number = id_num
        if Holder.page_num() == 2: number += 7
        elif Holder.page_num() == 3: number += 14
        
        # どのボタンがクリックされたかを記録
        Holder.setIds(number)
        # ポップアップウィンドウの表示
        content = PopupWindow(title=Holder.setLabel(number), delete=self.delete, regist=self.regist)
        self.popup = Popup(title="登録/削除", content=content, size_hint=(.6, .5))
        self.popup.open()
            
    # deleteを押した時の処理
    def delete(self):
        # 指定した場所を削除
        Holder.deleteText()
        # ボタンのラベルを更新
        self.setButtonLabel()
        # ポップアプウィンドウを閉じる
        self.popup.dismiss()

    # registを押した時の処理
    def regist(self,txt):
        # 入力内容をcsvファイルに記録
        Holder.setText(txt)
        # ボタンのラベルを更新
        self.setButtonLabel()
        # ポップアップウィンドウを閉じる
        self.popup.dismiss()
        
    # 選んだページ番号を記録しボタンのラベルを更新
    def page(self,index):
        Holder.page_set(index)
        self.setButtonLabel()
        

class TaskApp(App):
    # kivy launcherでのリスト表示時におけるタイトルとアイコンの設定
    title = 'task'
    icon = 'icon.png'

    def build(self):
        return Task()

    # アプリをポーズした時
    def on_pause(self):
        return True
    
    # アプリ終了時
    #def on_stop(self):

if __name__ == '__main__':
    TaskApp().run()
    