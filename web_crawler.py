import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from packaging import version  # For version comparison
import subprocess
import re # 정규식
import time
import json


# Selenium 패키지 업데이트
def update_selenium():
    os.system("pip install -U selenium")
    return

# 크롬 버전 확인
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

# 크롬과 크롬드라이버 버전 호환 체크
def version_check():
    try:
        # ChromeDriver를 사용하여 Chrome 브라우저 인스턴스 생성
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options) #headless

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
def crawl_data(URL_TMPL, URL_INPUT, TITLE_TAG, mode="w", path="result.jsonl"):
    driver = webdriver.Chrome()
    # URL_INPUT : 리스트를 리스트가 감싼 형태 [[1,20240102,3],[1,20240103,4]...]
    # TITLE_TAG : 딕셔너리를 리스트가 감싼 형태 [{title : tag}, {spec, h3.MuiTypography-root}, ...]

    # URL_TMPL의 {} 개수 확인
    placeholders = URL_TMPL.count("{}")
    if placeholders == 0:
        raise ValueError("URL_TMPL에는 최소 하나 이상의 '{}' 플레이스홀더가 필요합니다.")

    with open(path, mode, encoding="UTF-8") as output_file: #기존 파일 수정
        results = []  # 결과를 저장할 리스트

        for idx, data in enumerate(URL_INPUT):
            if len(data) != placeholders:
                raise ValueError(f"URL_INPUT의 요소 길이가 URL_TMPL의 {{}} 개수와 일치하지 않습니다: {data}")
            
            # 템플릿에 데이터를 삽입하여 URL 생성
            url = URL_TMPL.format(*data)
            driver.get(url=url)

            # 로드 대기 (필요에 따라 조정)
            driver.implicitly_wait(3)

            # 태그 데이터를 수집하여 딕셔너리로 저장
            extracted_data = {}
            for tag_info in TITLE_TAG:
                for key, tag in tag_info.items():
                    try:
                        element = driver.find_element(By.CSS_SELECTOR, tag)
                        extracted_data[key] = element.text
                    except Exception as e:
                        print(f"태그 {tag}에 대한 데이터 수집 중 오류 발생: {e}")
                        extracted_data[key] = None

            # 결과를 results에 추가
            results.append({
                "url": url,
                **extracted_data  # TITLE_TAG로부터 추출된 데이터를 동적으로 추가
            })

            print(f"[{idx + 1}/{len(URL_INPUT)}] 크롤링 완료: {url}")

        # 결과를 JSONL 형식으로 저장
        for result in results:
            output_file.write(json.dumps(result, ensure_ascii=False) + "\n")

    driver.quit()

# 실행 셀

version_check()
URL_TMPL ="https://linkareer.com/cover-letter/{}?organizationName=삼성전자&page=1&role=DS&sort=RELEVANCE&tab=all"
URL_INPUT = [[33549],[33988],[33943],[33887]]
TITLE_TAG = [{"title":"h1.MuiTypography-root"},{"spec":"h3.MuiTypography-root"}]
crawl_data(URL_TMPL,URL_INPUT,TITLE_TAG)