# Game Development Patterns

## 📚 패턴 라이브러리 개요

이 문서는 Rock-Paper-Scissors 프로젝트에서 적용된 게임 개발 패턴들을 정리하고, 향후 게임 개발 프로젝트에서 재사용할 수 있도록 구성되었습니다.

## 🎮 핵심 게임 개발 패턴

### 1. State Machine Pattern (상태 기계 패턴)

#### 패턴 정의
게임의 각 상태를 명확히 정의하고, 상태 간 전환을 관리하는 패턴

#### 구현 예시
```typescript
enum GameResult {
  IN_PROGRESS = 'in_progress',
  PLAYER_VICTORY = 'player_victory',
  COMPUTER_VICTORY = 'computer_victory'
}

interface GameState {
  readonly rounds: ReadonlyArray<Round>;
  readonly score: Score;
  readonly result: GameResult;
  readonly isComplete: boolean;
}

class RockPaperScissors {
  private getGameResult(): GameResult {
    if (!this.isGameComplete()) {
      return GameResult.IN_PROGRESS;
    }

    if (this.score.playerWins > this.score.computerWins) {
      return GameResult.PLAYER_VICTORY;
    } else {
      return GameResult.COMPUTER_VICTORY;
    }
  }
}
```

#### 적용 시나리오
- 턴 기반 게임
- 퍼즐 게임의 진행 상태
- 메뉴 시스템 네비게이션
- 게임 세션 라이프사이클

#### 장점
- 게임 상태 명확성
- 버그 감소 (불가능한 상태 전환 방지)
- 테스트 용이성
- 확장성

### 2. Round-Based Processing Pattern (라운드 기반 처리 패턴)

#### 패턴 정의
게임을 개별 라운드로 나누어 각 라운드를 독립적으로 처리하는 패턴

#### 구현 예시
```typescript
interface Round {
  readonly roundNumber: number;
  readonly playerChoice: Choice;
  readonly computerChoice: Choice;
  readonly result: RoundResult;
}

class RockPaperScissors {
  playRound(playerChoice: Choice, computerChoice: Choice): {
    round: Round;
    gameState: GameState;
  } {
    const roundNumber = this.rounds.length + 1;
    const result = this.determineRoundWinner(playerChoice, computerChoice);

    const round: Round = {
      roundNumber,
      playerChoice,
      computerChoice,
      result
    };

    this.rounds.push(round);
    this.updateScore(result);

    return { round, gameState: this.getGameState() };
  }
}
```

#### 적용 시나리오
- 턴 기반 전략 게임
- 카드 게임
- 보드 게임
- 퀴즈 게임

#### 장점
- 게임 로직 단순화
- 상태 관리 용이성
- 재시작/재개 기능 구현 용이
- 통계 수집 편의성

### 3. Player Strategy Pattern (플레이어 전략 패턴)

#### 패턴 정의
다양한 플레이어 타입을 동일한 인터페이스로 처리하는 패턴

#### 구현 예시
```typescript
interface Player {
  getChoice(): Promise<Choice> | Choice;
}

class ComputerPlayer implements Player {
  getChoice(): Choice {
    const choices = Object.values(Choice);
    const randomIndex = Math.floor(Math.random() * choices.length);
    return choices[randomIndex]!;
  }
}

class HumanPlayer implements Player {
  constructor(private ui: ConsoleUI) {}

  async getChoice(): Promise<Choice> {
    return await this.ui.getUserChoice();
  }
}
```

#### 적용 시나리오
- 멀티플레이어 게임
- AI vs 인간 게임
- 다양한 난이도 AI
- 네트워크 플레이어

#### 장점
- 코드 재사용성
- 새로운 플레이어 타입 추가 용이
- 테스트 가능성 (Mock Player)
- 확장성

### 4. Game Configuration Pattern (게임 설정 패턴)

#### 패턴 정의
게임 규칙과 설정을 외부에서 설정 가능하도록 하는 패턴

#### 구현 예시
```typescript
interface GameConfig {
  readonly maxRounds: number;
  readonly winsNeeded: number;
}

class RockPaperScissors {
  private readonly config: GameConfig;

  constructor(config: Partial<GameConfig> = {}) {
    this.config = {
      maxRounds: config.maxRounds ?? 5,
      winsNeeded: config.winsNeeded ?? 2
    };
  }
}

// 사용 예시
const standardGame = new RockPaperScissors();                    // 기본 설정
const customGame = new RockPaperScissors({ winsNeeded: 3 });     // 커스텀 설정
```

#### 적용 시나리오
- 다양한 게임 모드
- 난이도 조절
- 토너먼트 설정
- A/B 테스트

#### 장점
- 유연성
- 재사용성
- 테스트 용이성
- 확장성

### 5. Immutable Game State Pattern (불변 게임 상태 패턴)

#### 패턴 정의
게임 상태를 불변 객체로 관리하여 상태 변경의 안전성을 보장하는 패턴

#### 구현 예시
```typescript
interface GameState {
  readonly rounds: ReadonlyArray<Round>;
  readonly score: Score;
  readonly result: GameResult;
  readonly isComplete: boolean;
}

class RockPaperScissors {
  getGameState(): GameState {
    return {
      rounds: [...this.rounds],           // 방어적 복사
      score: { ...this.score },           // 얕은 복사
      result: this.getGameResult(),
      isComplete: this.isGameComplete()
    };
  }
}
```

#### 적용 시나리오
- 상태 기반 게임
- 실시간 멀티플레이어
- 상태 저장/복원 기능
- 디버깅 및 로깅

#### 장점
- 상태 변경 안전성
- 디버깅 용이성
- 시간 여행 가능 (상태 히스토리)
- 동시성 안전성

### 6. Input Validation Pattern (입력 검증 패턴)

#### 패턴 정의
사용자 입력을 안전하게 검증하고 파싱하는 패턴

#### 구현 예시
```typescript
function parseChoice(input: string): Choice | null {
  const normalized = input.toLowerCase().trim();

  switch (normalized) {
    case 'r':
    case 'rock':
    case '1':
      return Choice.ROCK;
    case 'p':
    case 'paper':
    case '2':
      return Choice.PAPER;
    case 's':
    case 'scissors':
    case 'scissor':
    case '3':
      return Choice.SCISSORS;
    default:
      return null;
  }
}

function isValidChoice(choice: string): choice is Choice {
  return Object.values(Choice).includes(choice as Choice);
}
```

#### 적용 시나리오
- 사용자 입력 처리
- 네트워크 메시지 검증
- 설정 파일 파싱
- API 요청 검증

#### 장점
- 보안성 향상
- 사용자 경험 개선
- 에러 방지
- 유연한 입력 형식 지원

### 7. Game Statistics Pattern (게임 통계 패턴)

#### 패턴 정의
게임 진행 중 통계를 수집하고 분석하는 패턴

#### 구현 예시
```typescript
class RockPaperScissors {
  getGameSummary(): {
    totalRounds: number;
    playerWinRate: number;
    computerWinRate: number;
    tieRate: number;
    winner: string;
  } {
    const totalRounds = this.rounds.length;
    const playerWinRate = totalRounds > 0 ? (this.score.playerWins / totalRounds) * 100 : 0;
    const computerWinRate = totalRounds > 0 ? (this.score.computerWins / totalRounds) * 100 : 0;
    const tieRate = totalRounds > 0 ? (this.score.ties / totalRounds) * 100 : 0;

    return {
      totalRounds,
      playerWinRate,
      computerWinRate,
      tieRate,
      winner: this.getWinnerString()
    };
  }
}
```

#### 적용 시나리오
- 플레이어 성과 추적
- 게임 밸런싱
- 분석 대시보드
- 성취 시스템

#### 장점
- 데이터 기반 결정
- 플레이어 참여도 향상
- 게임 개선 인사이트
- 개인화 기능

## 🔄 패턴 조합 및 상호작용

### 패턴 조합 예시
```typescript
class GameEngine {
  // State Machine + Round-Based Processing
  private state: GameState;
  private config: GameConfig;

  // Player Strategy + Input Validation
  constructor(
    private player1: Player,
    private player2: Player,
    config: Partial<GameConfig> = {}
  ) {
    this.config = { ...defaultConfig, ...config };
    this.state = this.createInitialState();
  }

  // Immutable State + Statistics
  async playRound(): Promise<GameResult> {
    const choice1 = await this.player1.getChoice();
    const choice2 = await this.player2.getChoice();

    const newRound = this.createRound(choice1, choice2);
    this.state = this.updateState(newRound);

    return this.state.result;
  }
}
```

## 📋 패턴 선택 가이드

### 프로젝트 규모별 권장 패턴

#### 소규모 프로젝트 (< 1000 LOC)
- State Machine Pattern (필수)
- Input Validation Pattern (필수)
- Game Configuration Pattern (선택)

#### 중규모 프로젝트 (1000-5000 LOC)
- 소규모 패턴 전체
- Player Strategy Pattern (필수)
- Immutable Game State Pattern (권장)
- Game Statistics Pattern (선택)

#### 대규모 프로젝트 (> 5000 LOC)
- 모든 패턴 적용
- 추가 패턴: Observer, Command, Factory

### 게임 장르별 권장 패턴

#### 턴 기반 게임
- Round-Based Processing (필수)
- State Machine (필수)
- Player Strategy (필수)

#### 실시간 게임
- Immutable State (필수)
- Observer Pattern (권장)
- Command Pattern (권장)

#### 퍼즐 게임
- State Machine (필수)
- Input Validation (필수)
- Statistics (선택)

## 🚀 확장 및 최적화

### 성능 최적화 팁
1. **상태 복사 최소화**: 필요한 경우에만 방어적 복사
2. **메모리 풀링**: 자주 생성되는 객체 재사용
3. **지연 계산**: 필요시에만 통계 계산
4. **이벤트 배칭**: 다중 상태 변경 시 배칭

### 확장성 고려사항
1. **모듈화**: 패턴별 독립 모듈
2. **인터페이스 안정성**: 하위 호환성 유지
3. **설정 중심**: 하드코딩 최소화
4. **플러그인 아키텍처**: 동적 기능 추가

---

**이러한 게임 개발 패턴들은 Rock-Paper-Scissors 프로젝트에서 검증되었으며, 다양한 게임 프로젝트에서 재사용할 수 있는 입증된 솔루션들입니다.**