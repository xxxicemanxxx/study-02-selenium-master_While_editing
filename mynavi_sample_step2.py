import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd

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

# main処理


def main():
    search_keyword = "高収入"
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
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
    
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
    #tableのclassを選択 → 下層にある tbody → さらに下層の3つ目のTrを選択　これが初年度年収 →　tdに抜きたい値   
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
            print(count,name1,add.text,mony.text)

        #エラーの回避策
        except Exception as e:
            print(e)
        #最後に必ず実行される
        finally:   
            count += 1


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
