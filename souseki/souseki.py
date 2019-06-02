# coding:utf-8
import os
os.environ ['KIVY_GL_BACKEND'] = 'angle_sdl2'
os.environ['KIVY_IMAGE'] = 'pil,sdl2'
import webbrowser as wb

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('kivy', 'exit_on_escape', '0')

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton

import pyperclip

LabelBase.register(DEFAULT_FONT, "misc/Koruri-Regular.ttf")

Builder.load_string('''
<MainScreen>:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: 0.6, 0.8, 0.6, 1
    BoxLayout:
        TextInput:
            size_hint_x: 0.7
            id: INPUT
        BoxLayout:
            orientation: "vertical"
            size_hint_x: 0.2
            BoxLayout:
                size_hint_y: 0.1
                Label:
                    text: "aaa"
                    size_hint_x: 0.4
                Switch:
                    size_hint_x: 0.6
            BoxLayout:
                size_hint_y: 0.1
                Label:
                    text: "aaa"
                    size_hint_x: 0.4
                Switch:
                    size_hint_x: 0.6
            BoxLayout:
                size_hint_y: 0.1
                Label:
                    text: "aaa"
                    size_hint_x: 0.4
                Switch:
                    size_hint_x: 0.6
            BoxLayout:
                size_hint_y: 0.1
                Label:
                    text: "aaa"
                    size_hint_x: 0.4
                Switch:
                    size_hint_x: 0.6
            Button:
                size_hint_y: 0.15
                text: "clear"
                on_press: root.clearText()
            Button:
                size_hint_y: 0.15
                text: "convert"
                on_press: root.convertText()
            Button:
                size_hint_y: 0.15
                text: "copy"
                on_press: root.copyToClipBoard()
            Button:
                size_hint_y: 0.15
                text: "Paste & Convert & Copy"
                on_press: root.pasteConvertCopyText()
            Button:
                size_hint_y: 0.15
                text: "open google"
                color: [237/255, 234/255, 163/255, 1]
                on_press: root.openGoogleTransfer()
''')

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.F_kaigyou = True
        self.F_innyou  = True
        self.F_ryakugo = True
        self.F_seperate_each_sentence = True

    def clearText(self):
        self.ids.INPUT.text = ""

    def pasteText(self):
        text = pyperclip.paste()
        self.ids.INPUT.text = text

    def convertText(self):
        text = self.ids.INPUT.text
        if self.F_kaigyou:
            text = self._convertKaigyo(text)
        if self.F_innyou:
            text = self._convertInnyou(text)
        if self.F_ryakugo:
            text = self._convertRyakugo(text)
        if self.F_seperate_each_sentence:
            text = self._seperateEachSentence(text)
        self.ids.INPUT.text = text

    def copyToClipBoard(self):
        pyperclip.copy(self.ids.INPUT.text)

    def pasteConvertCopyText(self):
        self.pasteText()
        self.convertText()
        self.copyToClipBoard()

    def openGoogleTransfer(self):
        url_org = "https://translate.google.co.jp/?hl=ja&tab=rT"

        search_text = self.ids.INPUT.text.replace("%","％")
        url = "https://translate.google.co.jp/?hl=ja&tab=TT#view=home&op=translate&sl=en&tl=ja&text="+search_text

        try:
            wb.open_new_tab(url)
        except:
            wb.open_net_tab(url_org)

        # url = "https://translate.google.co.jp/?hl=ja&tab=rT"
        # # url = "translate.google.co.jp/?hl=ja&tab=rT"
        # browser = webbrowser.get('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        # browser.open(url)


    def _convertKaigyo(self, text):
        text = text.replace("\n", " ")
        return text

    def _convertInnyou(self, text):
        for i in range(100):
            text = text.replace("[{}]".format(i), "")
        return text

    def _convertRyakugo(self, text):
        text = text.replace("Fig. ",  "Fig")
        text = text.replace("Fig.",   "Fig")
        text = text.replace("eq.",    "eq ")
        text = text.replace("Eq.",    "Eq ")
        text = text.replace("Sec.",   "Section ")
        text = text.replace("et al.", "et al")
        text = text.replace("i.e.,",  "that is,")
        text = text.replace("i.e.",   "that is,")
        text = text.replace("e.g.,",  "for example,")
        text = text.replace("e.g.",   "for example,")
        text = text.replace("cf.",    "cf")
        text = text.replace("s.t.",   "such that")
        text = text.replace("resp.",  "respectively")
        text = text.replace("w.r.t.", "with relation to")
        text = text.replace("esp.",   "especially")
        return text

    def _seperateEachSentence(self, text):
        text = text.replace(". ", ".\n")
        return text

class MainApp(App):
    def build(self):
        self.icon = "misc/souseki.jpg"
        self.title = "souseki"
        return MainScreen()

if __name__ == "__main__":
    MainApp().run()
