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
    exp_mony_list = []
    count = 1
    while True:
        # 検索結果の一番上の会社名を取得
        name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
        mony_list = driver.find_elements_by_class_name("tableCondition__body")

        # 1ページ分繰り返し
        for name,mony in zip(name_list,mony_list):
            try:
                name1 = name.text.split(' ')[0]
                #name1 = name.text
                #X = name.text.find(' ')
                mony1 = mony.text
                #print(count,name1[0:X],mony1)
                print(count,name1,mony1)
            except Exception as e:
                print(e)
            finally:   
                count += 1
    
        # 次のページボタンがあればクリックなければ終了
        #button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div/nav[1]/ul/li[8]/a")
        button = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div/nav[1]/ul/li[7]/a")
        button = driver.find_element_by_xpath("iconFont--arrowLeft")
        try:
            button.click()
            time.sleep(3)
        except NoSuchElementException:
            break



# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
