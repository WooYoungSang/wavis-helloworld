# TypeScript Best Practices and Patterns

## 📚 TypeScript 패턴 라이브러리

이 문서는 Rock-Paper-Scissors 프로젝트에서 적용된 TypeScript 베스트 프랙티스와 패턴들을 정리합니다.

## 🎯 핵심 TypeScript 패턴

### 1. Strict Type Safety Pattern (엄격한 타입 안전성 패턴)

#### 패턴 정의
TypeScript의 엄격 모드를 활용하여 컴파일 타임에 최대한 많은 오류를 잡는 패턴

#### tsconfig.json 설정
```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

#### 구현 예시
```typescript
// 명시적 타입 정의
interface GameState {
  readonly rounds: ReadonlyArray<Round>;
  readonly score: Score;
  readonly result: GameResult;
  readonly isComplete: boolean;
}

// null/undefined 안전성
function parseChoice(input: string): Choice | null {
  // 명시적 null 반환으로 타입 안전성 확보
  if (!input || typeof input !== 'string') {
    return null;
  }
  // ... 구현
}

// 배열 접근 안전성
function getRandomChoice(choices: Choice[]): Choice {
  if (choices.length === 0) {
    throw new Error('Choices array cannot be empty');
  }
  const index = Math.floor(Math.random() * choices.length);
  const choice = choices[index];
  if (choice === undefined) {
    throw new Error('Invalid choice selected');
  }
  return choice;
}
```

#### 장점
- 런타임 오류 사전 방지
- 리팩토링 안전성
- IDE 지원 향상
- 팀 협업 시 계약 명확성

### 2. Immutable Data Pattern (불변 데이터 패턴)

#### 패턴 정의
readonly 키워드와 방어적 복사를 활용한 불변성 보장 패턴

#### 구현 예시
```typescript
// 읽기 전용 인터페이스
interface Score {
  readonly playerWins: number;
  readonly computerWins: number;
  readonly ties: number;
}

interface Round {
  readonly roundNumber: number;
  readonly playerChoice: Choice;
  readonly computerChoice: Choice;
  readonly result: RoundResult;
}

// 읽기 전용 배열
interface GameState {
  readonly rounds: ReadonlyArray<Round>;
  readonly score: Score;
}

// 방어적 복사 패턴
class RockPaperScissors {
  private rounds: Round[] = [];
  private score: Score = { playerWins: 0, computerWins: 0, ties: 0 };

  getGameState(): GameState {
    return {
      rounds: [...this.rounds],        // 배열 복사
      score: { ...this.score }         // 객체 복사
    };
  }

  private updateScore(result: RoundResult): void {
    switch (result) {
      case RoundResult.PLAYER_WIN:
        this.score = { ...this.score, playerWins: this.score.playerWins + 1 };
        break;
      case RoundResult.COMPUTER_WIN:
        this.score = { ...this.score, computerWins: this.score.computerWins + 1 };
        break;
      case RoundResult.TIE:
        this.score = { ...this.score, ties: this.score.ties + 1 };
        break;
    }
  }
}
```

#### 장점
- 상태 변경 버그 방지
- 동시성 안전성
- 디버깅 용이성
- 상태 히스토리 추적 가능

### 3. Type Guard Pattern (타입 가드 패턴)

#### 패턴 정의
런타임에서 타입을 안전하게 검증하는 패턴

#### 구현 예시
```typescript
// 기본 타입 가드
function isValidChoice(choice: string): choice is Choice {
  return Object.values(Choice).includes(choice as Choice);
}

// 복합 타입 가드
function isValidGameState(obj: any): obj is GameState {
  return obj &&
    typeof obj === 'object' &&
    Array.isArray(obj.rounds) &&
    typeof obj.score === 'object' &&
    typeof obj.result === 'string' &&
    typeof obj.isComplete === 'boolean';
}

// 사용 예시
function processUserInput(input: string): Choice {
  if (!isValidChoice(input)) {
    throw new Error(`Invalid choice: ${input}`);
  }
  return input; // TypeScript가 이제 input을 Choice로 인식
}

// 고급 타입 가드 (제네릭)
function isArrayOf<T>(
  arr: any,
  typeGuard: (item: any) => item is T
): arr is T[] {
  return Array.isArray(arr) && arr.every(typeGuard);
}

function isRound(obj: any): obj is Round {
  return obj &&
    typeof obj.roundNumber === 'number' &&
    isValidChoice(obj.playerChoice) &&
    isValidChoice(obj.computerChoice) &&
    Object.values(RoundResult).includes(obj.result);
}

// 사용
const rounds: any[] = getSomeData();
if (isArrayOf(rounds, isRound)) {
  // rounds는 이제 Round[] 타입
  rounds.forEach(round => console.log(round.roundNumber));
}
```

#### 장점
- 런타임 타입 안전성
- 외부 데이터 검증
- API 응답 검증
- 마이그레이션 안전성

### 4. String Enum Pattern (문자열 열거형 패턴)

#### 패턴 정의
숫자 대신 문자열을 사용하는 열거형으로 디버깅과 직렬화 개선

#### 구현 예시
```typescript
// 문자열 열거형
enum Choice {
  ROCK = 'rock',
  PAPER = 'paper',
  SCISSORS = 'scissors'
}

enum RoundResult {
  PLAYER_WIN = 'player_win',
  COMPUTER_WIN = 'computer_win',
  TIE = 'tie'
}

enum GameResult {
  PLAYER_VICTORY = 'player_victory',
  COMPUTER_VICTORY = 'computer_victory',
  IN_PROGRESS = 'in_progress'
}

// 유틸리티 함수
function getChoiceDisplayName(choice: Choice): string {
  const displayNames: Record<Choice, string> = {
    [Choice.ROCK]: '🪨 Rock',
    [Choice.PAPER]: '📄 Paper',
    [Choice.SCISSORS]: '✂️ Scissors'
  };
  return displayNames[choice];
}

// 열거형 순회
function getAllChoices(): Choice[] {
  return Object.values(Choice);
}

// 열거형 검증
function isChoice(value: string): value is Choice {
  return Object.values(Choice).includes(value as Choice);
}
```

#### 장점
- 디버깅 친화적
- JSON 직렬화/역직렬화 안전
- 런타임 값 명확성
- 리팩토링 안전성

### 5. Interface Segregation Pattern (인터페이스 분리 패턴)

#### 패턴 정의
작고 집중된 인터페이스를 통한 의존성 분리

#### 구현 예시
```typescript
// 작고 집중된 인터페이스
interface Player {
  getChoice(): Promise<Choice> | Choice;
}

interface GameRules {
  determineWinner(choice1: Choice, choice2: Choice): RoundResult;
}

interface ScoreTracker {
  updateScore(result: RoundResult): void;
  getScore(): Score;
  reset(): void;
}

interface GameStateManager {
  getCurrentState(): GameState;
  isGameComplete(): boolean;
  canContinue(): boolean;
}

// 구현 클래스
class ComputerPlayer implements Player {
  getChoice(): Choice {
    // 구현
  }
}

class StandardGameRules implements GameRules {
  determineWinner(choice1: Choice, choice2: Choice): RoundResult {
    // 구현
  }
}

// 조합 사용
class RockPaperScissors implements ScoreTracker, GameStateManager {
  constructor(
    private rules: GameRules,
    private config: GameConfig
  ) {}

  // ScoreTracker 구현
  updateScore(result: RoundResult): void { /* 구현 */ }
  getScore(): Score { /* 구현 */ }
  reset(): void { /* 구현 */ }

  // GameStateManager 구현
  getCurrentState(): GameState { /* 구현 */ }
  isGameComplete(): boolean { /* 구현 */ }
  canContinue(): boolean { /* 구현 */ }
}
```

#### 장점
- 테스트 용이성
- 코드 재사용성
- 의존성 분리
- 확장성

### 6. Configuration Pattern (설정 패턴)

#### 패턴 정의
타입 안전한 설정 객체 패턴

#### 구현 예시
```typescript
// 기본 설정 인터페이스
interface GameConfig {
  readonly maxRounds: number;
  readonly winsNeeded: number;
  readonly allowTies: boolean;
  readonly timeout?: number;
}

// 기본값 정의
const DEFAULT_CONFIG: GameConfig = {
  maxRounds: 5,
  winsNeeded: 2,
  allowTies: true,
  timeout: undefined
} as const;

// 설정 병합 함수
function mergeConfig(config: Partial<GameConfig> = {}): GameConfig {
  return {
    ...DEFAULT_CONFIG,
    ...config
  };
}

// 설정 검증 함수
function validateConfig(config: GameConfig): void {
  if (config.maxRounds <= 0) {
    throw new Error('maxRounds must be positive');
  }
  if (config.winsNeeded <= 0) {
    throw new Error('winsNeeded must be positive');
  }
  if (config.winsNeeded > config.maxRounds) {
    throw new Error('winsNeeded cannot exceed maxRounds');
  }
}

// 사용 예시
class RockPaperScissors {
  private readonly config: GameConfig;

  constructor(userConfig: Partial<GameConfig> = {}) {
    this.config = mergeConfig(userConfig);
    validateConfig(this.config);
  }
}

// 타입 안전한 설정 빌더
class GameConfigBuilder {
  private config: Partial<GameConfig> = {};

  setMaxRounds(rounds: number): this {
    this.config.maxRounds = rounds;
    return this;
  }

  setWinsNeeded(wins: number): this {
    this.config.winsNeeded = wins;
    return this;
  }

  build(): GameConfig {
    const finalConfig = mergeConfig(this.config);
    validateConfig(finalConfig);
    return finalConfig;
  }
}

// 사용
const config = new GameConfigBuilder()
  .setMaxRounds(7)
  .setWinsNeeded(4)
  .build();
```

#### 장점
- 타입 안전성
- 기본값 관리
- 설정 검증
- 빌더 패턴 지원

### 7. Error Handling Pattern (에러 처리 패턴)

#### 패턴 정의
타입 안전한 에러 처리와 결과 타입 패턴

#### 구현 예시
```typescript
// 사용자 정의 에러 클래스
class GameError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly context?: any
  ) {
    super(message);
    this.name = 'GameError';
  }
}

class InvalidChoiceError extends GameError {
  constructor(choice: string) {
    super(
      `Invalid choice: ${choice}`,
      'INVALID_CHOICE',
      { choice }
    );
  }
}

class GameCompleteError extends GameError {
  constructor() {
    super(
      'Game is already complete',
      'GAME_COMPLETE'
    );
  }
}

// Result 타입 패턴
type Result<T, E = Error> = {
  success: true;
  data: T;
} | {
  success: false;
  error: E;
};

function safeParseChoice(input: string): Result<Choice, InvalidChoiceError> {
  const choice = parseChoice(input);
  if (choice === null) {
    return {
      success: false,
      error: new InvalidChoiceError(input)
    };
  }
  return {
    success: true,
    data: choice
  };
}

// 사용 예시
function handleUserInput(input: string): void {
  const result = safeParseChoice(input);

  if (!result.success) {
    console.error(`Error: ${result.error.message}`);
    return;
  }

  // result.data는 이제 Choice 타입
  processChoice(result.data);
}

// Optional 타입 패턴
type Optional<T> = T | null | undefined;

function findRoundByNumber(rounds: Round[], number: number): Optional<Round> {
  return rounds.find(round => round.roundNumber === number) ?? null;
}

// 에러 가드 함수
function isGameError(error: unknown): error is GameError {
  return error instanceof GameError;
}
```

#### 장점
- 명시적 에러 처리
- 타입 안전한 에러 정보
- 컨텍스트 정보 포함
- 함수형 에러 처리

### 8. Utility Types Pattern (유틸리티 타입 패턴)

#### 패턴 정의
TypeScript 내장 유틸리티 타입을 활용한 타입 변환

#### 구현 예시
```typescript
// 기본 타입
interface GameState {
  rounds: Round[];
  score: Score;
  result: GameResult;
  isComplete: boolean;
}

// Partial - 부분 업데이트용
type GameStateUpdate = Partial<GameState>;

function updateGameState(
  current: GameState,
  update: GameStateUpdate
): GameState {
  return { ...current, ...update };
}

// Pick - 특정 필드만 선택
type GameSummary = Pick<GameState, 'score' | 'result' | 'isComplete'>;

function getGameSummary(state: GameState): GameSummary {
  return {
    score: state.score,
    result: state.result,
    isComplete: state.isComplete
  };
}

// Omit - 특정 필드 제외
type GameStateWithoutRounds = Omit<GameState, 'rounds'>;

// Record - 키-값 매핑
type ChoiceCount = Record<Choice, number>;

function countChoices(rounds: Round[]): ChoiceCount {
  return rounds.reduce((count, round) => {
    count[round.playerChoice] = (count[round.playerChoice] || 0) + 1;
    return count;
  }, {} as ChoiceCount);
}

// Readonly 유틸리티
type ReadonlyGameState = Readonly<GameState>;

// 커스텀 유틸리티 타입
type NonEmptyArray<T> = [T, ...T[]];

function getRandomElement<T>(arr: NonEmptyArray<T>): T {
  const index = Math.floor(Math.random() * arr.length);
  return arr[index];
}

// 조건부 타입
type ApiResponse<T> = T extends string
  ? { message: T }
  : { data: T };

// 매핑된 타입
type Optional<T> = {
  [K in keyof T]?: T[K];
};

type Required<T> = {
  [K in keyof T]-?: T[K];
};
```

#### 장점
- 타입 재사용성
- 코드 중복 감소
- 타입 안전성 유지
- 표현력 향상

## 🔄 패턴 조합 및 실무 적용

### 패턴 조합 예시
```typescript
// 여러 패턴을 조합한 실제 구현
class GameEngine {
  // Configuration Pattern + Strict Type Safety
  constructor(private readonly config: GameConfig) {
    validateConfig(config);
  }

  // Type Guard + Error Handling Pattern
  processInput(input: string): Result<Choice, InvalidChoiceError> {
    if (!isValidChoice(input)) {
      return {
        success: false,
        error: new InvalidChoiceError(input)
      };
    }
    return {
      success: true,
      data: input
    };
  }

  // Immutable Data + Interface Segregation
  playRound(
    player1: Player,
    player2: Player
  ): Promise<GameState> {
    // 구현
  }
}
```

### 성능 최적화 팁

#### 1. 타입 체크 최적화
```typescript
// 비효율적
function processItems(items: any[]): ProcessedItem[] {
  return items
    .filter(item => isValidItem(item))
    .map(item => processItem(item as ValidItem));
}

// 효율적
function processItems(items: any[]): ProcessedItem[] {
  const result: ProcessedItem[] = [];
  for (const item of items) {
    if (isValidItem(item)) {
      result.push(processItem(item));
    }
  }
  return result;
}
```

#### 2. 메모이제이션
```typescript
// 비용이 큰 타입 변환 캐싱
const typeCache = new Map<string, Choice>();

function parseChoiceWithCache(input: string): Choice | null {
  if (typeCache.has(input)) {
    return typeCache.get(input)!;
  }

  const result = parseChoice(input);
  if (result !== null) {
    typeCache.set(input, result);
  }
  return result;
}
```

## 📋 패턴 선택 가이드

### 프로젝트 단계별 패턴 적용

#### 초기 개발 (필수)
- Strict Type Safety Pattern
- String Enum Pattern
- Interface Segregation Pattern

#### 중간 개발 (권장)
- Type Guard Pattern
- Immutable Data Pattern
- Configuration Pattern

#### 고급 개발 (선택)
- Error Handling Pattern
- Utility Types Pattern
- 성능 최적화 패턴

### 팀 크기별 패턴 전략

#### 개인/소규모 팀 (1-3명)
- 핵심 패턴 집중
- 단순함 우선
- 점진적 도입

#### 중규모 팀 (4-10명)
- 표준화된 패턴 적용
- 코드 리뷰 기준 마련
- 문서화 강화

#### 대규모 팀 (10명+)
- 모든 패턴 체계적 적용
- 린터 규칙 강화
- 자동화 도구 활용

---

**이러한 TypeScript 패턴들은 Rock-Paper-Scissors 프로젝트에서 실제로 검증되었으며, 대규모 TypeScript 프로젝트에서도 효과적으로 적용할 수 있는 입증된 방법들입니다.**