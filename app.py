import streamlit as st
from pykakasi import kakasi
import unicodedata
import re


st.title('暗号化システム')

def moji_list(*args):
            moji = []
            for i in range(len(args)):
                moji.extend([chr(j) for j in range(args[i][0], args[i][1])])
            return moji
moji_lists = moji_list((97, 123),  (48, 58), (12353, 12436), ) # ずらすための文字リストを作成
        
menu = st.selectbox('メニュー',['ホーム','暗号化','復号化'])

if menu == 'ホーム':
    st.write('この暗号化システムの利用については、当方一切の責任を負いません。')
elif menu == '暗号化':
    box=st.text_input('テキストを入力', '')
    key=int(st.selectbox('暗号化キー','12345'))

    if st.button('暗号化開始'):
           
        box = ''.join(box) #リストエラー対策
        box = re.findall("[^。]+。?", box.replace('\n', ''))
        box = ''.join(box) #リストエラー対策
        box = box.replace('　','') #リストエラー対策
        box = box.lower()
        box = ''.join(box) #リストエラー対策

        kakasi = kakasi()
        kakasi.setMode('J', 'H') #漢字からひらがなに変換
        kakasi.setMode("K", "H") #カタカナからひらがなに変換
        conv = kakasi.getConverter()

        box = conv.do(box)

        en_list = [] # 文字をずらす処理
        for text in box: #一文字ずつ取り出す
            if text in moji_lists: #文字照合リストに暗号したい文字があれば
                i = moji_lists.index(text) #インデックスを探す
                if len(moji_lists) <= (i + key): #文字照合リストよりインデックス＋keyが大きければ
                    s = (key + i) % len(moji_lists) #繰り越したインデックスで追加
                    en_list.append(moji_lists[s])
                else: #文字照合リストよりインデックス＋keyが小さければ
                    en_list.append(moji_lists[i + key]) #そのまま追加
            else: #文字照合リストに暗号したい文字がなければそのまま追加
                en_list.append(text)
            
        texts =  unicodedata.normalize('NFKC', box)
        en = ''.join(en_list)

        st.write(en)
elif menu == '復号化':
    box=st.text_input('テキストを入力', '')
    key=int(st.selectbox('復号化キー','12345'))
    
    if st.button('復号化開始'):
        
        de_list = [] # 文字をずらす処理
        
        box = ''.join(box) #リストエラー対策
        box = re.findall("[^。]+。?", box.replace('\n', ''))
        box = ''.join(box) #リストエラー対策
        box = box.replace('　','') #リストエラー対策
        box = box.lower()
        box = ''.join(box) #リストエラー対策
        
        for text in box: #一文字ずつ取り出す
            if text in moji_lists: #文字照合リストに複合したい文字があれば
                i = moji_lists.index(text) #インデックスを探す
                if i + 1 - key < 0: #インデックスからkeyを引いた値が0より小さければ
                
                    s = len(moji_lists) - (key - i) # 文字照合リストからkeyからインデックスを引いた値をsとする。
                    if abs(s) >= len(moji_lists): # 絶対値でリスト数から確認
                        s = s % len(moji_lists) # 余りを算定

                    de_list.append(moji_lists[s]) #余り復号化。
                else: #文字照合リストよりインデックス＋keyが小さければ
                    de_list.append(moji_lists[i - key]) #keyを引いたインデックスで複合化
            else: #文字照合リストに複合したい文字がなければそのまま追加
                de_list.append(text)

                box =  unicodedata.normalize('NFKC', box)
        de = ''.join(de_list)
            
        st.write(de)