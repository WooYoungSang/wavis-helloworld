# Go Reference Templates

Go 언어 기반 프로젝트 구현을 위한 참조 템플릿입니다.

## 구조

```
go/
├── templates/
│   ├── ci/                     # CI/CD 설정
│   ├── tests/                  # 테스트 템플릿
│   ├── go.mod.template         # Go 모듈 정의
│   ├── main.go.template        # 메인 애플리케이션
│   ├── config.go.template      # 설정 관리
│   └── Dockerfile.template     # 컨테이너화
├── config.yaml                 # Go 언어 설정
└── README.md                   # 이 파일
```

## 사용 방법

1. **프로젝트 구조 설정**: 표준 Go 프로젝트 레이아웃 사용
   ```
   cmd/          # 애플리케이션 엔트리포인트
   internal/     # 내부 패키지
   pkg/          # 외부에서 사용 가능한 패키지
   configs/      # 설정 파일
   docs/         # 문서
   tests/        # 테스트
   ```

2. **의존성 관리**: Go modules 사용
   - `go.mod` 파일로 의존성 정의
   - 버전 고정으로 재현 가능한 빌드

3. **테스트**: 표준 Go 테스트 프레임워크
   - 단위 테스트: `*_test.go`
   - 벤치마크: `Benchmark*` 함수
   - 예제: `Example*` 함수

4. **빌드 및 배포**: 정적 바이너리 생성
   - 크로스 컴파일 지원
   - Docker 멀티스테이지 빌드

## 특징

- **성능**: 컴파일된 바이너리, 낮은 메모리 사용량
- **동시성**: 고루틴과 채널을 통한 우아한 동시성 처리
- **타입 안전성**: 강타입 언어의 장점
- **표준 라이브러리**: 풍부한 표준 라이브러리

## 권장 라이브러리

- **HTTP 프레임워크**: gin, echo, fiber
- **데이터베이스**: GORM, sqlx
- **테스트**: testify
- **설정**: viper
- **로깅**: logrus, zap