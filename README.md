Dynamic Web Crawler

📌 서비스 개요

이 프로그램은 코딩을 모르지만 크롤링의 동작 원리를 이해하는 사용자가 쉽게 데이터를 수집할 수 있도록 도와주는 도구입니다. 사용자는 크롤링할 페이지의 HTML 태그의 CSS 선택자만 입력하면, 프로그램이 자동으로 데이터를 추출하여 다양한 형식(JSON, JSONL, CSV)으로 저장할 수 있습니다. GUI 기반으로 설계되어 있어 직관적인 조작이 가능하며, 원하는 데이터를 빠르게 확보할 수 있습니다.



https://github.com/user-attachments/assets/4cc25a18-0e21-4ea1-ad98-708747dce335



🔧 주요 기능

1. URL 템플릿을 통한 다중 페이지 크롤링

사용자가 입력한 URL Template과 URL Input 데이터를 조합하여 여러 페이지의 데이터를 한 번에 크롤링할 수 있습니다.

예: https://example.com/page/{} 형태의 URL에서 {} 부분을 여러 값으로 치환하여 반복 요청 수행

2. 동적 요소 크롤링 설정

HTML 태그의 CSS 선택자를 직접 입력하여 원하는 데이터를 추출할 수 있습니다.

텍스트(text), 링크(href), 이미지(src) 등 다양한 속성을 선택하여 저장 가능

3. 크롤링 속도 조절 (딜레이 설정)

크롤링 과정에서 서버 부하를 줄이기 위해 특정 주기마다 지연 시간을 설정할 수 있습니다.

주기(횟수)와 지연 시간(초) 단위로 입력 가능

4. 실시간 크롤링 진행 상태 표시

각 페이지 크롤링이 완료될 때마다 현재 진행 상황을 출력하여 사용자가 상태를 확인할 수 있습니다.

5. 다양한 파일 형식 지원

크롤링한 데이터를 JSON, JSONL, CSV 형식으로 저장 가능

JSON 및 JSONL 파일 불러오기를 지원하여 기존 데이터를 활용할 수 있음

🚀 사용 방법

프로그램 실행 후 URL Template과 URL Input을 입력합니다.

URL Template 형식: 크롤링할 URL의 기본 형태로, 가변적인 부분을 {}로 표시합니다.

예: https://example.com/page/{}

URL Input 형식: {} 부분을 채울 데이터를 리스트 형태로 입력합니다.

예: [[33549], [33988], [33943], [33887]] (각 리스트의 값이 {}에 대체됨)

⚠️ {}의 개수와 리스트 내부 요소의 개수가 일치해야 정상적으로 동작합니다.

크롤링할 HTML 요소의 CSS 선택자를 추가하여 원하는 데이터를 설정합니다.

(선택) 지연 시간을 설정하여 요청 속도를 조정합니다.

Start Crawling 버튼을 눌러 크롤링을 시작합니다.

완료 후 데이터를 JSON, JSONL, CSV 파일로 저장합니다.

🛠 Todo

하나의 사이트에서 다양한 요소들을 한 번에 긁어오는 기능 추가

크롤링 데이터의 정렬 및 필터링 기능 추가
