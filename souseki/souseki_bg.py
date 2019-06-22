# coding:utf-8
import os
import webbrowser as wb
import pyperclip


"""
https://qiita.com/yukiB/items/586b20c58b16b5d3917c より引用
"""
from pyhooked import Hook, KeyboardEvent, MouseEvent

def handle_events(args):
    if isinstance(args, KeyboardEvent):
        ### TODO: なんかする
        print(args.key_code, args.current_key, args.event_type)


"""
自分で定義する部分
"""
def copyConvertCopyText(F_kaigyou = True,
                        F_innyou  = True,
                        F_ryakugo = True,
                        F_seperate_each_sentence = True):

    ### TODO: 選択部分をコピーする関数
    text = aaa()

    ### 以前のを改変して流用できる
    if F_kaigyou:
        text = convertKaigyo(text)
    if F_innyou:
        text = convertInnyou(text)
    if F_ryakugo:
        text = convertRyakugo(text)
    if F_seperate_each_sentence:
        text = seperateEachSentence(text)

    ### 以前のを改変して流用できる
    copyToClipBoard()


def convertKaigyo(text):
    text = text.replace("\n", " ")
    return text

def convertInnyou(text):
    for i in range(100):
        text = text.replace("[{}]".format(i), "")
    return text

def convertRyakugo(text):
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

def seperateEachSentence(text):
    text = text.replace(". ", ".\n")
    return text

def copyToClipBoard(text):
    pyperclip.copy(text)



if __name__ == '__main__':
    hk = Hook()
    hk.handler = handle_events
    hk.hook()






#
