# Python Reference Templates

Python 언어 기반 프로젝트 구현을 위한 참조 템플릿입니다.

## 구조

```
python/
├── templates/
│   ├── ci/                     # CI/CD 설정
│   ├── tests/                  # 테스트 템플릿
│   ├── main.py.template        # 메인 애플리케이션
│   ├── config.py.template      # 설정 관리
│   ├── requirements.txt.template # 의존성 정의
│   ├── pyproject.toml.template # 프로젝트 설정
│   └── Dockerfile.template     # 컨테이너화
├── config.yaml                 # Python 언어 설정
└── README.md                   # 이 파일
```

## 사용 방법

1. **프로젝트 구조 설정**: 표준 Python 패키지 구조
   ```
   src/{{PROJECT_NAME}}/  # 소스 코드
   tests/                 # 테스트
   configs/               # 설정 파일
   docs/                  # 문서
   requirements.txt       # 의존성
   pyproject.toml         # 프로젝트 설정
   ```

2. **의존성 관리**: pip + requirements.txt 또는 Poetry
   - `requirements.txt`: 운영 의존성
   - `requirements-dev.txt`: 개발 의존성
   - 가상환경 사용 권장

3. **테스트**: pytest 사용
   - 단위 테스트: `test_*.py`
   - 픽스처를 통한 테스트 데이터 관리
   - 코드 커버리지: pytest-cov

4. **빌드 및 배포**:
   - Docker 컨테이너화
   - pip 패키지로 배포

## 특징

- **가독성**: 명확하고 간결한 문법
- **생산성**: 빠른 개발 사이클
- **생태계**: 풍부한 라이브러리와 프레임워크
- **유연성**: 다양한 용도에 적합

## 권장 라이브러리

- **웹 프레임워크**: FastAPI, Django, Flask
- **데이터베이스**: SQLAlchemy, Django ORM
- **테스트**: pytest, unittest
- **설정**: pydantic-settings
- **로깅**: structlog, loguru