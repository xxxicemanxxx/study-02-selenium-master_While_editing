import os
#from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# Chromeを起動する関数
def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

def file_write(str):
    #with openにすれば自動でファイルが閉じる　　引数　、mode='w'書き込み用、encoding = utf-8-sig：デフォルト状態
    #mode='a'追記
    with open("{}_log.txt".format(df_data_name),mode='a',encoding = "utf-8-sig") as log_file:
        log_file.write(str+"\n")
        print(str)

# main処理
def main():
    #同じファイルが存在するかを確認。同じものがあった場合に名前を変更
    global df_data_name
    df_data_name = input("保存ファイル名を入力してください\r\n")
    if os.path.exists('{}_log.txt'.format(df_data_name)):
        Judgment = input("同じファイル名が存在します上書きしますか？　yes/no\r\n現在はファイル名『{}』です\r\n".format(df_data_name))
        if Judgment =="yes":
            print("『{}』で保存します".format(df_data_name))
        else:
            df_data_name = input("保存ファイル名を再入力してください\r\n")
            print("『{}』で保存します".format(df_data_name))
    else:
        print("『{}』で保存します".format(df_data_name))

    #search_keyword = "高収入"
    search_keyword = input("検索ワードを入力してください：例 [ 社名、土日休み、未経験など ]\r\n")
    # driverを起動
    driver = webdriver.Chrome(ChromeDriverManager().install())
     # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name("topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_add_list = []
    exp_mony_list = []
    count = 1
    file_write("検索ワード：{}\ncount,会社名,勤務地,初年度年収".format(search_keyword))
    
    while True:
    #for num in range(1):   #testに使用
        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        #tableのclassを選択 → 下層にある tbody → さらに下層の3つ目のTrを選択　これが勤務地 →　tdに抜きたい値   
        add_list = driver.find_elements_by_xpath("//table[@class='tableCondition']/tbody/tr[3]/td")
        #tableのclassを選択 → 下層にある tbody → さらに下層の5つ目のTrを選択　これが初年度年収 →　tdに抜きたい値           
        mony_list = driver.find_elements_by_xpath("//table[@class='tableCondition']/tbody/tr[5]/td")

        # 1ページ分繰り返し
        for name,add,mony in zip(name_list,add_list,mony_list):
            try:
                #余分な情報を消す
                name1 = name.text.split(' ')[0]
                #X = name.text.find(' ')                   #こっちでもOK
                #print(count,name.text[0:X],mony1)         #こっちでもOK
                
                #出力
                file_write("{},{},{},{}".format(count,name1,add.text,mony.text))

                #Data list生成
                exp_name_list.append(name1)
                exp_add_list.append(add.text)
                exp_mony_list.append(mony.text)
            
            #エラーの回避策
            except Exception as e:
                file_write("{},{},{},{}\n{}".format(count,name1,add.text,mony.text,e))

            #最後に必ず実行される
            finally:   
                count += 1
    
        # 次のページボタンがあればクリックなければ終了
        #button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div/nav[1]/ul/li[8]/a")   #<a>タグは.click()ではなく、.get_attribute(“href”)でリンクURLを抜く
        #button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div/nav[1]/ul/li[7]/a")   #<a>タグは.click()ではなく、.get_attribute(“href”)でリンクURLを抜く
        button = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(button) > 0 :    #elementsで取得すると、listとして認識されるindexの指定をする必要あり
            #button[0].click()  #<a>タグは.click()できない
            button1 = button[0].get_attribute("href")
            driver.get(button1)
            time.sleep(1)
        else:
            break

    #取得したDataをpandasモジュールを使ってCSVファイルに出力
    df_data= pd.DataFrame({'会社名':exp_name_list,'勤務地':exp_add_list,'初年度年収':exp_mony_list})

    #to_csv関数を使って、csvファイルを書き出す。 encodingの引数で、utf-8-sig：デフォルト状態でcsvファイルに書き込む
    df_data.to_csv("{}.csv".format(df_data_name),encoding = "utf-8-sig")
    #encodingの引数で、shift-jisでcsvファイルに書き込んだときに文字化けを防ぐ
    #df_data.to_csv(df_data_name,encoding = 'shift-jis') #エラー発生


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
