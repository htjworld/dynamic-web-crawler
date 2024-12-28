import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from packaging import version  # For version comparison
import subprocess
import re # 정규식
import time


# Selenium 패키지 업데이트
def update_selenium():
    os.system("pip install -U selenium")
    return

def get_installed_chrome_version():
    """Get the installed Chrome version."""
    try:
        # Command to fetch the Chrome version
        if os.name == "nt":  # Windows
            result = subprocess.run(["reg", "query", r"HKLM\Software\Google\Chrome\BLBeacon", "/v", "version"],
                                    capture_output=True, text=True)
            return result.stdout.split()[-1]
        elif os.name == "posix":  # macOS / Linux
            # Specify the Chrome executable path for macOS
            chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            result = subprocess.run([chrome_path, "--version"], capture_output=True, text=True)
            return result.stdout.strip().split(" ")[-1]
    except Exception as e:
        print(f"Error fetching Chrome version: {e}")
        return None

def version_check():
    try:
        # ChromeDriver를 사용하여 Chrome 브라우저 인스턴스 생성
        driver = webdriver.Chrome()

        # 버전 정보 가져오기
        chrome_version = get_installed_chrome_version()
        driver_version = driver.capabilities['chrome']['chromedriverVersion']
        print("Chrome 버전:", chrome_version)
        print("Chrome Driver 버전:", driver_version)

        chrome_version = chrome_version.split('.')[0]
        driver_version = driver_version.split('.')[0]

        # 버전 비교 및 메시지 출력
        if chrome_version == driver_version:
            print("유효합니다: Chrome과 ChromeDriver 버전이 일치합니다.")
        elif int(chrome_version) > int(driver_version):
            print(f"ChromeDriver를 {chrome_version}.x 버전으로 업데이트해주세요.")
        else:
            print(f"Chrome을 {driver_version}.x 버전으로 업데이트해주세요.")


        # 드라이버 종료
        driver.quit()
        
    except Exception as e:
        print("에러 발생:", str(e))
        print("ChromeDriver 또는 Chrome 설치를 확인하고 다시 시도해주세요.")



def CDfind(title,tag):
    title = driver.find_element(By.CSS_SELECTOR, tag) #태그 안 내용 저장
    return title

# Todo. 수정
def crawl_data(URL_TMPL, mode="w", path="crawling_results/result.jsonl", element, *args):
    driver = webdriver.Chrome()
    

    with open(path, mode, encoding="UTF-8") as output_file: #기존 파일 수정
        for a,u in enumerate(cover_letter):
            driver.get(url=u["url"])
            if (a+1) %100 ==0:
                print("[{}]번째 자소서 크롤링 진행중".format(a+1))
            time.sleep(1.5)

            title = driver.find_element(By.CSS_SELECTOR, "h1.MuiTypography-root") #제목 저장
            spec = driver.find_element(By.CSS_SELECTOR, "h3.MuiTypography-root") #스펙 저장


            # 페이지 소스를 가져와서 BeautifulSoup으로 파싱
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')


            # 특정 태그를 기준으로 태그 외부의 텍스트 추출
            main_content = soup.find('article').find('main')



            # 예제에서 제외할 클래스 리스
            main_text = extract_text_excluding_target(main_content)

            cover_letter[a]['title'] = title.text
            cover_letter[a]['spec'] = spec.text
            cover_letter[a]['main_text'] = main_text



    # 웹 드라이버 종료
    driver.quit()

# 실행 셀
version_check()