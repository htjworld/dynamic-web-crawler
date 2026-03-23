# Dynamic Web Crawler

> CSS 선택자 기반 GUI 웹 크롤러 — 코딩 없이 웹 데이터를 수집합니다

## Background

팀 내 비개발자 팀원들이 매일 같은 웹 페이지를 열어 데이터를 수동으로 복사·붙여넣기하는 반복 작업을 하고 있었습니다.
Python을 모르거나 코딩에 익숙하지 않아 크롤러를 직접 작성하기 어려운 상황이었습니다.

HTML의 CSS 선택자만 알면 누구나 조작할 수 있는 GUI 기반 크롤러를 만들어 팀의 반복 수작업을 제거했습니다.

## Features

- 단일 URL 크롤링 — URL 템플릿 없이 특정 페이지 하나를 바로 크롤링
- 다중 URL 크롤링 — `{}` 플레이스홀더와 URL Input 데이터를 조합해 여러 페이지 일괄 수집
- CSS 선택자 기반 추출 — 텍스트(`text`), 링크(`href`), 이미지(`src`), 대체 텍스트(`alt`) 속성 지원
- 딜레이 설정 — 요청 주기와 대기 시간을 설정해 서버 부하 조절
- 다양한 저장 형식 — JSON, JSONL, CSV로 저장
- JSON/JSONL 불러오기 — 기존 파일을 URL Input으로 바로 활용

## Preview

https://github.com/user-attachments/assets/4cc25a18-0e21-4ea1-ad98-708747dce335

## Tech Stack

[![Skills](https://skillicons.dev/icons?i=py)](https://skillicons.dev)

## Getting Started

**Requirements**
- Python 3.8+
- Google Chrome

**macOS / Linux**
```bash
git clone https://github.com/htjworld/dynamic-web-crawler.git
cd dynamic-web-crawler
pip install -r requirements.txt
python web_crawler.py
```

**Windows**
```bash
git clone https://github.com/htjworld/dynamic-web-crawler.git
cd dynamic-web-crawler
pip install -r requirements.txt
python web_crawler.py
```

## Build

PyInstaller를 사용하면 Python 환경 없이 실행 가능한 단일 파일로 빌드할 수 있습니다.

**Requirements**
```bash
pip install pyinstaller
```

**Windows (.exe)**
```bash
pyinstaller --onefile --windowed web_crawler.py
```

빌드 완료 후 `dist/web_crawler.exe`를 실행합니다.

**macOS (.app)**
```bash
pyinstaller --onefile --windowed web_crawler.py
```

빌드 완료 후 `dist/web_crawler`를 실행합니다.

---

*last updated: 2026.03*
