import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from packaging import version  # For version comparison
import subprocess
import time
import json
import threading


def select_save_path():
    """사용자가 저장할 파일 경로를 선택"""
    save_path = filedialog.asksaveasfilename(
        title="Select File to Save",
        defaultextension=".jsonl",
        filetypes=[("JSONL files", "*.jsonl"), ("All files", "*.*")]
    )
    return save_path

def save_data_to_file(data):
    """데이터를 선택한 경로에 저장"""
    save_path = select_save_path()
    if not save_path:
        messagebox.showwarning("No File Selected", "No file selected. Data was not saved.")
        return

    try:
        with open(save_path, "w", encoding="utf-8") as file:
            for record in data:
                file.write(json.dumps(record, ensure_ascii=False) + "\n")
        messagebox.showinfo("Success", f"Data successfully saved to {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")


# Selenium 패키지 업데이트
def update_selenium():
    try:
        os.system("pip install -U selenium")
        messagebox.showinfo("Success", "Selenium has been updated!")
    except Exception as e:
        messagebox.showerror("Error", f"Error updating Selenium: {e}")

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
        messagebox.showinfo("Version Check",
                            f"Chrome 버전: {chrome_version}\n"
                            f"Chrome Driver 버전: {driver_version}")

        chrome_version = chrome_version.split('.')[0]
        driver_version = driver_version.split('.')[0]

       # 버전 비교 및 메시지 출력
        if chrome_version == driver_version:
            message = "유효합니다: Chrome과 ChromeDriver 버전이 일치합니다."
            print(message)
            messagebox.showinfo("Version Check", message)
        elif int(chrome_version) > int(driver_version):
            message = f"ChromeDriver를 {chrome_version}.x 버전으로 업데이트해주세요."
            print(message)
            messagebox.showwarning("Version Mismatch", message)
        else:
            message = f"Chrome을 {driver_version}.x 버전으로 업데이트해주세요."
            print(message)
            messagebox.showwarning("Version Mismatch", message)

        # 드라이버 종료
        driver.quit()
        
    except Exception as e:
        messagebox.showerror(f"에러 발생:ChromeDriver 또는 Chrome 설치를 확인하고 다시 시도해주세요.{e}", e)



def CDfind(title,tag):
    title = driver.find_element(By.CSS_SELECTOR, tag) #태그 안 내용 저장
    return title

# Global delay configuration
delay_configurations = []

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

    # URL_TMPL의 {} 개수 확인
    placeholders = URL_TMPL.count("{}")
    if placeholders == 0:
        raise ValueError("URL_TMPL에는 최소 하나 이상의 '{}' 플레이스홀더가 필요합니다.")

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

        # Apply delay logic
        apply_delays(idx)

    driver.quit()

    # 결과를 파일에 저장
    save_data_to_file(results)

def run_crawl():
    try:
        # 입력 값 가져오기
        url_template = url_template_entry.get()
        url_input_raw = url_input_entry.get()
        title_tag_raw = title_tag_entry.get()

        # JSON 데이터로 파싱
        url_input = json.loads(url_input_raw)
        title_tag = json.loads(title_tag_raw)

        if not url_template or not url_input or not title_tag:
            messagebox.showwarning("Input Missing", "Please fill in all fields before starting.")
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
root.geometry("500x700")

# 1. Selenium Update 버튼
update_button = tk.Button(root, text="Update Selenium", command=update_selenium, width=20)
update_button.pack(pady=10)

# 2. Version Check 버튼
version_check_button = tk.Button(root, text="Check Version", command=version_check, width=20)
version_check_button.pack(pady=10)

# 3. Crawl Data 섹션
ttk.Label(root, text="URL Template:").pack(pady=5)
url_template_entry = tk.Entry(root, width=50)
url_template_entry.pack(pady=5)
url_template_entry.insert(0, "https://linkareer.com/cover-letter/{}?organizationName=삼성전자&page=1&role=DS&sort=RELEVANCE&tab=all")

ttk.Label(root, text="URL Input (list):").pack(pady=5)
url_input_entry = tk.Entry(root, width=50)
url_input_entry.pack(pady=5)
url_input_entry.insert(0, "[[33549], [33988], [33943], [33887]]")

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