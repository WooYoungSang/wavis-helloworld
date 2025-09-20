# TypeScript Reference Templates

TypeScript 언어 기반 프로젝트 구현을 위한 참조 템플릿입니다.

## 구조

```
typescript/
├── templates/
│   ├── ci/                     # CI/CD 설정
│   ├── tests/                  # 테스트 템플릿
│   ├── main.ts.template        # 메인 애플리케이션
│   ├── config.ts.template      # 설정 관리
│   ├── package.json.template   # 패키지 정의
│   ├── tsconfig.json.template  # TypeScript 설정
│   └── Dockerfile.template     # 컨테이너화
├── config.yaml                 # TypeScript 언어 설정
└── README.md                   # 이 파일
```

## 사용 방법

1. **프로젝트 구조 설정**: 표준 Node.js/TypeScript 구조
   ```
   src/          # 소스 코드
   tests/        # 테스트
   dist/         # 컴파일된 JavaScript
   configs/      # 설정 파일
   docs/         # 문서
   package.json  # 패키지 정의
   tsconfig.json # TypeScript 설정
   ```

2. **의존성 관리**: npm 또는 yarn
   - `package.json`: 의존성 정의
   - `package-lock.json`: 정확한 버전 고정
   - 개발/운영 의존성 분리

3. **테스트**: Jest 또는 Vitest
   - 단위 테스트: `*.test.ts`
   - 통합 테스트: `*.integration.test.ts`
   - E2E 테스트: Playwright 또는 Cypress

4. **빌드 및 배포**:
   - TypeScript 컴파일: `tsc`
   - 번들링: esbuild, Vite, Webpack
   - Docker 컨테이너화

## 특징

- **타입 안전성**: 컴파일 타임 타입 검사
- **개발 경험**: 우수한 IDE 지원
- **생태계**: 풍부한 npm 패키지
- **현대적**: 최신 JavaScript 기능 지원

## 권장 라이브러리

- **런타임**: Node.js, Bun, Deno
- **웹 프레임워크**: Express, Fastify, Koa
- **테스트**: Jest, Vitest, Mocha
- **설정**: dotenv, config
- **로깅**: winston, pino