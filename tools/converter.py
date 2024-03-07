import os
import re

# このコードが配置されているフォルダのパス
FOLDER_PATH = os.path.dirname(__file__)

# 入力フォルダのパス
INPUT_PATH = os.path.join(FOLDER_PATH, "input")
# 出力フォルダのパス
OUTPUT_PATH = os.path.join(FOLDER_PATH, "output")



# INPUT_PATH + filename のパスのファイルを変換し、OUTPUT_PATH + filenameに保存する。
def convert(filename:str) -> None:
    with open(os.path.join(INPUT_PATH, filename), "r", encoding="utf-8") as f:
        content = f.read()

    classname = re.search("public class (.+) extends", content).group(1)

    arr = content.split("\n")

    # 後ろの空白行を削除
    for i in range(len(arr)-1,0,-1):
        if arr[i] != "":
            break
        arr.pop(i)
    
    
    conv_types = [1 for i in range(len(arr))]
    func_start_flag = False
    func_begin_pos = -1
    trycatch_flag = False # trycatch構文が関数内に含まれるか

    # conv_types[n]: ファイルn行目の「変換タイプ」
    # 「変換タイプ」: その行にどういう変換を施すか
    
    # 0 => 変換しない。
    # 1 => _mydebug_.Set()を前に差し込む。
    # 2 => _mydebug_の定義とtryを後に差し込む。
    # 3 => catchを前に差し込む。
    # 4 => 変換しない。(functionの位置を表す)
    # 100 => MyDebug.Mainの定義を後に差し込む。

    for i in range(len(arr)):
        if func_start_flag == False:
            conv_types[i] = 0
        if "catch" in arr[i]:
            trycatch_flag = True
        if "function" in arr[i]:
            if func_start_flag:
                conv_types[i-2] = 3

                
            if trycatch_flag:
                for j in range(func_begin_pos, i):
                    conv_types[j] = 0
            trycatch_flag = False
            func_begin_pos = i+1


            func_start_flag = True
            conv_types[i-1] = 0
            conv_types[i] = 4
            conv_types[i+1] = 2


        if "public function Main()" in arr[i]:
            conv_types[i+1] = 100

            
    conv_types[-3] = 3
    conv_types[-2] = 0
    conv_types[-1] = 0

    # 変換する。
    for i in range(len(arr)):
        a = arr[i]
        if conv_types[i] == 2:
            arr[i] = a+"_mydebug_ = new MyDebug(); try{"
        if conv_types[i] == 3:
            arr[i] = '}catch(e:Error){_mydebug_.ShowStacks(e); }'+a
        if conv_types[i] == 100:
            arr[i] = a+"MyDebug.Main = this; _mydebug_ = new MyDebug(); try{"
        

        if "{" in a:
            continue
        if "}" in a:
            continue
        if "if(" in a:
            continue
        if "else" in a:
            continue
        if conv_types[i] == 1:
            # arr[i] = "_debug_ = "+str(i)+"; "+a
            arr[i] = '_mydebug_.Set("'+classname+'",'+str(i)+"); "+a
        
        

    content = "\n".join(arr)

    with open(os.path.join(OUTPUT_PATH, filename), "w", encoding="utf-8") as f:
        f.write(content)


# INPUT_PATH 内の全てのファイルを変換。
for filename in os.listdir(INPUT_PATH):
    convert(filename)
