projeect folder/
│
├── app.py                    # Flask 애플리케이션의 엔트리 포인트
├── config.py                 # 설정 파일 (선택 사항)
├── static/                   # 정적 파일 (CSS, JavaScript, 이미지, svg 등)
│   ├── css/
│   ├── js/
│   └── images/
│   └── svg/                
├── templates/                # HTML 파일
│   └── index.html              
│   └── slider.html
├── myapp/                    # 다른 기능을 포함한 Python 모듈들
│   ├── __init__.py           # 패키지 초기화 파일
│   ├── routes.py             # Flask 라우트 설정 파일
│   ├── models.py             # 데이터베이스 모델 파일 (ORM 등)
│   └── services.py           # 서비스 로직 파일 (비즈니스 로직 처리)
│   └── crawler.py            # 서비스 로직 파일 (비즈니스 로직 처리)
│   └── crawler_parallel.py   # 서비스 로직 파일 (비즈니스 로직 처리)
│   └── db_helper.py          # 서비스 로직 파일 (비즈니스 로직 처리)
│   └── openai_helper.py      # 서비스 로직 파일 (비즈니스 로직 처리)
└── venv/                     # (가상 환경) 선택 사항