# 무작위 아이디어 단어

한국어 뉴스 말뭉치에서 단어를 무작위로 뽑아 새로운 아이디어의 출발점을 만드는 정적 웹페이지입니다.

사용자가 원하는 단어 수를 입력하면 서로 다른 단어를 한 줄에 하나씩 보여 줍니다. 별도의 서버나 외부 라이브러리 없이 GitHub Pages에서 실행할 수 있습니다.

## 주요 기능

- Okt가 명사·동사·형용사로 판정한 실질 형태소 47,203개 중 균등 확률로 추첨
- 한 번의 추첨 안에서는 같은 단어가 나오지 않음
- 1개부터 100개까지 추첨 가능
- 데이터 로딩 상태와 오류 메시지 표시
- 검은 배경과 흰색 텍스트의 중앙 집중형 화면
- 모바일 화면과 긴 단어를 위한 줄바꿈 및 스크롤 지원

## 사용 방법

1. 단어 목록이 로딩될 때까지 기다립니다.
2. `단어 수`에 1부터 100 사이의 정수를 입력합니다.
3. `추첨` 버튼을 누릅니다.
4. 나온 단어들을 연결하거나 충돌시켜 아이디어를 만들어 봅니다.

## 로컬 실행

브라우저의 로컬 파일 보안 정책 때문에 `index.html`을 직접 열면 JSON 로딩이 차단될 수 있습니다. 저장소 루트에서 정적 HTTP 서버를 실행해 확인합니다.

```powershell
python -m http.server 8000
```

그다음 브라우저에서 `http://localhost:8000`을 엽니다.

## GitHub Pages 배포

1. 저장소의 **Settings → Pages**로 이동합니다.
2. 배포 소스를 **Deploy from a branch**로 선택합니다.
3. 공개할 브랜치와 루트 디렉터리 `/ (root)`를 선택합니다.
4. 저장 후 GitHub가 제공하는 Pages 주소에 접속합니다.

## 단어 데이터 재생성

재생성에는 Python 3, Java 8 이상, KoNLPy의 Okt 분석기가 필요합니다. 기존 환경에 의존성을 설치한 뒤 생성 스크립트를 실행합니다.

```powershell
python -m pip install -r requirements.txt
python scripts/build_words.py
```

스크립트는 `kor_news_2022_100K-sentences.txt`의 문장 문맥을 Okt로 분석합니다. `norm=True`, `stem=True`를 적용해 명사(`Noun`), 동사(`Verb`), 형용사(`Adjective`)만 기본형으로 추출하고, 한글 포함 여부를 확인한 뒤 첫 등장 순서로 중복을 제거해 `data/words.json`에 저장합니다. 원본 파일은 수정하지 않습니다.

웹페이지 실행 자체에는 Python, Java, KoNLPy가 필요하지 않습니다. 이들은 JSON을 다시 만들 때만 사용합니다.

## 프로젝트 구조

```text
.
├── index.html              # 화면 구조
├── styles.css              # 흑백 레이아웃과 반응형 스타일
├── app.js                  # 데이터 로딩, 입력 검증, 무작위 추첨
├── data/words.json         # 웹페이지에서 사용하는 단어 목록
├── scripts/build_words.py  # Okt로 실질 형태소 JSON 생성
├── requirements.txt        # 데이터 재생성용 Python 의존성
└── ABSORB/                 # 코드 이해를 위한 학습 교재와 해설
```

구현 흐름을 자세히 학습하려면 [ABSORB/README.md](ABSORB/README.md)를 참고하세요.

## 데이터 출처와 라이선스

단어 목록은 Wortschatz Leipzig에서 다운로드한 한국어 뉴스 텍스트 코퍼스에서 추출했습니다. 공식 이용 조건에 따라 다운로드 코퍼스에는 [CC BY](https://wortschatz-leipzig.de/en/usage)가 적용됩니다.

이 고지는 단어 데이터에 관한 것이며 프로젝트 코드의 라이선스와는 별개입니다.



