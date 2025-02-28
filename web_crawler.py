import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from packaging import version  # For version comparison
import subprocess
import time
import json
import threading

from data_handler import save_data_to_file, load_json_data

# Selenium 패키지 업데이트
# def update_selenium():
#     try:
#         os.system("pip install -U selenium")
#         messagebox.showinfo("Success", "Selenium has been updated!")
#     except Exception as e:
#         messagebox.showerror("Error", f"Error updating Selenium: {e}")

# 크롬 버전 확인
# def get_installed_chrome_version():
#     """Get the installed Chrome version."""
#     try:
#         if os.name == "nt":  # Windows
#             result = subprocess.run(["reg", "query", r"HKLM\Software\Google\Chrome\BLBeacon", "/v", "version"],
#                                     capture_output=True, text=True)
#             return result.stdout.split()[-1]
#         elif os.name == "posix":  # macOS / Linux
#             # Specify the Chrome executable path for macOS
#             chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
#             result = subprocess.run([chrome_path, "--version"], capture_output=True, text=True)
#             return result.stdout.strip().split(" ")[-1]
#     except Exception as e:
#         print(f"Error fetching Chrome version: {e}")
#         return None

# 크롬과 크롬드라이버 버전 호환 체크
# 셀레니움 4.6.0 버전 이후로는 셀레니움 매니저를 통해 크롬드라이버가 자동으로 관리되므로 버전 체크가 필요 없어짐
# def version_check():
#     try:
#         # ChromeDriver를 사용하여 Chrome 브라우저 인스턴스 생성
#         options = webdriver.ChromeOptions()
#         options.add_argument("--headless=new")
#         driver = webdriver.Chrome(options=options) #headless

#         # 버전 정보 가져오기
#         chrome_version = get_installed_chrome_version()
#         driver_version = driver.capabilities['chrome']['chromedriverVersion']
#         messagebox.showinfo("Version Check",
#                             f"Chrome 버전: {chrome_version}\n"
#                             f"Chrome Driver 버전: {driver_version}")

#         chrome_version = chrome_version.split('.')[0]
#         driver_version = driver_version.split('.')[0]

#        # 버전 비교 및 메시지 출력
#         if chrome_version == driver_version:
#             message = "유효합니다: Chrome과 ChromeDriver 버전이 일치합니다."
#             print(message)
#             messagebox.showinfo("Version Check", message)
#         elif int(chrome_version) > int(driver_version):
#             message = f"ChromeDriver를 {chrome_version}.x 버전으로 업데이트해주세요."
#             print(message)
#             messagebox.showwarning("Version Mismatch", message)
#         else:
#             message = f"Chrome을 {driver_version}.x 버전으로 업데이트해주세요."
#             print(message)
#             messagebox.showwarning("Version Mismatch", message)

#         # 드라이버 종료
#         driver.quit()
        
#     except Exception as e:
#         messagebox.showerror(f"에러 발생:ChromeDriver 또는 Chrome 설치를 확인하고 다시 시도해주세요.{e}", e)

# Todo. 글로벌 변수 로컬 변수로 대체

# Global delay configuration
delay_configurations = [] # 각 delay 위젯의 참조 주소가 저장됨

def add_delay_configuration():
    """Add a new delay configuration input."""
    global delay_configurations
    frame = tk.Frame(delay_frame)
    frame.pack(pady=5)

    # Default values
    default_period = 10 ** (len(delay_configurations))
    period_label = tk.Label(frame, text="주기:")
    period_label.grid(row=0, column=0, padx=5)
    period_entry = tk.Entry(frame, width=10)
    period_entry.insert(0, str(default_period))
    period_entry.grid(row=0, column=1, padx=5)

    time_label = tk.Label(frame, text="시간:")
    time_label.grid(row=0, column=2, padx=5)
    time_entry = tk.Entry(frame, width=10)
    time_entry.insert(0, "0.5")
    time_entry.grid(row=0, column=3, padx=5)

    delay_configurations.append((period_entry, time_entry))

def validate_delays():
    """Validate user inputs for delay configurations."""
    global delay_configurations
    validated_delays = []
    for period_entry, time_entry in delay_configurations:
        try:
            period = int(period_entry.get())
            delay_time = float(time_entry.get())
            validated_delays.append((period, delay_time))
        except ValueError:
            messagebox.showerror("Error", "주기는 정수, 시간은 실수로 입력해야 합니다.")
            return None
    return validated_delays

def apply_delays(idx):
    """Apply delay based on the current index and user configurations."""
    global delay_configurations
    for period_entry, time_entry in delay_configurations:
        try:
            # Extract values from Entry widgets
            period = int(period_entry.get())
            delay_time = float(time_entry.get())

            # Apply delay
            if idx % period == 0:
                print(f"Applying delay of {delay_time} seconds at cycle {idx}")
                time.sleep(delay_time)
        except ValueError:
            # Handle invalid entries gracefully
            messagebox.showerror("Error", "주기는 정수, 시간은 실수로 입력해야 합니다.")
            return

def crawl_data(URL_TMPL, URL_INPUT, TITLE_TAG):
    driver = webdriver.Chrome()
    # URL_INPUT : 리스트를 리스트가 감싼 형태 [[1,20240102,3],[1,20240103,4]...]
    # TITLE_TAG : 딕셔너리를 리스트가 감싼 형태 [{title : tag}, {spec, h3.MuiTypography-root}, ...]

    # URL_TMPL의 {} 개수
    placeholders = URL_TMPL.count("{}")

    # URL_INPUT이 None, 빈 리스트([]), [[]] 중 하나이면 처리
    if not URL_INPUT or URL_INPUT == [[]]:
        if placeholders == 0:
            # URL에 `{}`가 없으면 그대로 크롤링
            url = URL_TMPL
            driver.get(url=url)
            driver.implicitly_wait(3)  # 페이지 로드 대기

            extracted_data = {}
            for tag_info in TITLE_TAG:
                for key, tag in tag_info.items():
                    try:
                        element = driver.find_element(By.CSS_SELECTOR, tag)
                        extracted_data[key] = element.text
                    except Exception as e:
                        print(f"태그 {tag}에 대한 데이터 수집 중 오류 발생: {e}")
                        extracted_data[key] = None

            # 결과를 리스트에 추가
            results = [{"url": url, **extracted_data}]
            print(f"단일 URL 크롤링 완료: {url}")
            driver.quit()
            save_data_to_file(results)
            return
        else:
            messagebox.showerror("Error", "URL_TEMPLATE에 {}가 포함되어 있지만, URL_INPUT이 비어 있습니다.")
            driver.quit()
            return
    
    results = []  # 결과를 저장할 리스트

    # URL_INPUT이 정상적인 리스트인 경우 기존 방식대로 실행
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

        # Apply delay logic
        apply_delays(idx)

    driver.quit()

    # 결과를 파일에 저장
    save_data_to_file(results)

def run_crawl():
    try:
        # 입력 값 가져오기
        url_template = url_template_entry.get().strip()
        url_input_raw = url_input_entry.get().strip()
        title_tag_raw = title_tag_entry.get().strip()

        # 빈 입력값 처리
        if not url_template:
            messagebox.showwarning("Input Error", "URL Template을 입력하세요.")
            return
        
        if not title_tag_raw:
            messagebox.showwarning("Input Error", "Title Tags 필드를 입력하세요.")
            return
        
        # JSON 데이터로 파싱
        if not url_input_raw:
            url_input = None
        else:
            try:
                url_input = json.loads(url_input_raw)  # JSON 파싱
                if not isinstance(url_input, list):  # 리스트 형식이 아니면 오류 처리
                    messagebox.showwarning("Input Error", "URL Input은 리스트 형식이어야 합니다.")
                    return
            except json.JSONDecodeError as e:
                messagebox.showerror("Error", f"URL Input JSON 형식이 올바르지 않습니다: {e}")
                return
        
        # Title Tags JSON 파싱
        try:
            title_tag = json.loads(title_tag_raw)
            if not isinstance(title_tag, list):  # 리스트 형식이 아니면 오류 처리
                messagebox.showwarning("Input Error", "Title Tags는 리스트 형식이어야 합니다.")
                return
        except json.JSONDecodeError as e:
            messagebox.showerror("Error", f"Title Tags JSON 형식이 올바르지 않습니다: {e}")
            return

        # Validate delay configurations
        validated_delays = validate_delays()
        if validated_delays is None:
            return

        # 크롤링 실행
        crawl_data(url_template, url_input, title_tag)
        messagebox.showinfo("Success", "Crawling completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error during crawling: {e}")
    finally:
        root.after(0, lambda: crawl_button.config(state=tk.NORMAL))


def crawl_data_gui():
    try:
        # 버튼 비활성화
        crawl_button.config(state=tk.DISABLED)
        # 스레드 실행
        threading.Thread(target=run_crawl, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Error", f"Unexpected Error: {e}")
        crawl_button.config(state=tk.NORMAL)


# Tkinter GUI 설정
root = tk.Tk()
root.title("Dynamic Web Crawler")
root.geometry("500x500")

# 1. Selenium Update 버튼
# update_button = tk.Button(root, text="Update Selenium", command=update_selenium, width=20)
# update_button.pack(pady=10)

# 2. Version Check 버튼
# version_check_button = tk.Button(root, text="Check Version", command=version_check, width=20)
# version_check_button.pack(pady=10)

# 3. Crawl Data 섹션
ttk.Label(root, text="URL Template:").pack(pady=5)
url_template_entry = tk.Entry(root, width=50)
url_template_entry.pack(pady=5)
url_template_entry.insert(0, "https://linkareer.com/cover-letter/{}?organizationName=삼성전자&page=1&role=DS&sort=RELEVANCE&tab=all")

ttk.Label(root, text="URL Input (list):").pack(pady=5)
url_input_entry = tk.Entry(root, width=50)
url_input_entry.pack(pady=5)
url_input_entry.insert(0, "[[33549], [33988], [33943], [33887]]")
url_load_button = tk.Button(root, text="Load JSON/JSONL File", command=lambda: load_json_data(url_input_entry))
url_load_button.pack(pady=5)

ttk.Label(root, text="Title Tags (list of dict):").pack(pady=5)
title_tag_entry = tk.Entry(root, width=50)
title_tag_entry.pack(pady=5)
title_tag_entry.insert(0, '[{"title": "h1.MuiTypography-root"}, {"spec": "h3.MuiTypography-root"}]')

# Delay Configuration Section
ttk.Label(root, text="시간 지연 추가:").pack(pady=5)
delay_frame = tk.Frame(root)
delay_frame.pack(pady=5)
add_delay_button = tk.Button(root, text="+", command=add_delay_configuration)
add_delay_button.pack(pady=10)


crawl_button = tk.Button(root, text="Start Crawling", command=crawl_data_gui, width=20)
crawl_button.pack(pady=20)

# Tkinter 실행 루프
root.mainloop()