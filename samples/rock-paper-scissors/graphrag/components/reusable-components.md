# Reusable Components Library

## 📚 컴포넌트 라이브러리 개요

이 문서는 Rock-Paper-Scissors 프로젝트에서 구현된 재사용 가능한 컴포넌트들을 정리하여, 향후 프로젝트에서 활용할 수 있도록 구성되었습니다.

## 🎮 게임 로직 컴포넌트

### 1. Choice Management System

#### 컴포넌트 개요
게임 선택지를 관리하고 검증하는 시스템

#### 핵심 코드
```typescript
// 기본 열거형 정의
enum Choice {
  ROCK = 'rock',
  PAPER = 'paper',
  SCISSORS = 'scissors'
}

// 타입 가드 함수
function isValidChoice(choice: string): choice is Choice {
  return Object.values(Choice).includes(choice as Choice);
}

// 유연한 입력 파서
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

// 디스플레이 유틸리티
const CHOICE_DISPLAY_NAMES: Record<Choice, string> = {
  [Choice.ROCK]: '🪨 Rock',
  [Choice.PAPER]: '📄 Paper',
  [Choice.SCISSORS]: '✂️ Scissors'
} as const;

function getChoiceDisplayName(choice: Choice): string {
  return CHOICE_DISPLAY_NAMES[choice];
}
```

#### 재사용 방법
1. Choice enum을 프로젝트 선택지로 확장
2. parseChoice 함수를 입력 형식에 맞게 수정
3. 디스플레이 이름을 프로젝트 테마에 맞게 조정

#### 적용 가능한 프로젝트
- 퀴즈 애플리케이션 (A/B/C/D 선택)
- 설문조사 시스템 (Yes/No/Maybe)
- 메뉴 시스템 (여러 옵션 선택)
- 게임 내 액션 선택

### 2. Round-Based Game Engine

#### 컴포넌트 개요
라운드 기반 게임의 상태를 관리하는 엔진

#### 핵심 코드
```typescript
// 라운드 정의
interface Round<TChoice, TResult> {
  readonly roundNumber: number;
  readonly playerChoice: TChoice;
  readonly opponentChoice: TChoice;
  readonly result: TResult;
  readonly timestamp?: Date;
}

// 점수 추적
interface Score {
  readonly playerWins: number;
  readonly opponentWins: number;
  readonly ties: number;
}

// 게임 상태
interface GameState<TChoice, TResult> {
  readonly rounds: ReadonlyArray<Round<TChoice, TResult>>;
  readonly score: Score;
  readonly result: GameResult;
  readonly isComplete: boolean;
}

// 게임 설정
interface GameConfig {
  readonly maxRounds: number;
  readonly winsNeeded: number;
  readonly allowTies: boolean;
}

// 제네릭 게임 엔진
abstract class RoundBasedGameEngine<TChoice, TResult> {
  protected rounds: Round<TChoice, TResult>[] = [];
  protected score: Score = { playerWins: 0, opponentWins: 0, ties: 0 };

  constructor(protected readonly config: GameConfig) {}

  abstract determineRoundWinner(
    playerChoice: TChoice,
    opponentChoice: TChoice
  ): TResult;

  abstract isPlayerWin(result: TResult): boolean;
  abstract isOpponentWin(result: TResult): boolean;
  abstract isTie(result: TResult): boolean;

  playRound(
    playerChoice: TChoice,
    opponentChoice: TChoice
  ): { round: Round<TChoice, TResult>; gameState: GameState<TChoice, TResult> } {
    if (this.isGameComplete()) {
      throw new Error('Game is already complete');
    }

    const roundNumber = this.rounds.length + 1;
    const result = this.determineRoundWinner(playerChoice, opponentChoice);

    const round: Round<TChoice, TResult> = {
      roundNumber,
      playerChoice,
      opponentChoice,
      result,
      timestamp: new Date()
    };

    this.rounds.push(round);
    this.updateScore(result);

    return {
      round,
      gameState: this.getGameState()
    };
  }

  getGameState(): GameState<TChoice, TResult> {
    return {
      rounds: [...this.rounds],
      score: { ...this.score },
      result: this.getGameResult(),
      isComplete: this.isGameComplete()
    };
  }

  reset(): void {
    this.rounds = [];
    this.score = { playerWins: 0, opponentWins: 0, ties: 0 };
  }

  private updateScore(result: TResult): void {
    if (this.isPlayerWin(result)) {
      this.score = { ...this.score, playerWins: this.score.playerWins + 1 };
    } else if (this.isOpponentWin(result)) {
      this.score = { ...this.score, opponentWins: this.score.opponentWins + 1 };
    } else if (this.isTie(result)) {
      this.score = { ...this.score, ties: this.score.ties + 1 };
    }
  }

  private isGameComplete(): boolean {
    return (
      this.rounds.length >= this.config.maxRounds ||
      this.score.playerWins >= this.config.winsNeeded ||
      this.score.opponentWins >= this.config.winsNeeded
    );
  }

  private getGameResult(): GameResult {
    if (!this.isGameComplete()) {
      return GameResult.IN_PROGRESS;
    }

    if (this.score.playerWins > this.score.opponentWins) {
      return GameResult.PLAYER_VICTORY;
    } else if (this.score.opponentWins > this.score.playerWins) {
      return GameResult.OPPONENT_VICTORY;
    } else {
      return GameResult.TIE;
    }
  }
}

// 사용 예시: Rock-Paper-Scissors 구현
class RockPaperScissorsEngine extends RoundBasedGameEngine<Choice, RoundResult> {
  determineRoundWinner(playerChoice: Choice, opponentChoice: Choice): RoundResult {
    if (playerChoice === opponentChoice) {
      return RoundResult.TIE;
    }

    const playerWins =
      (playerChoice === Choice.ROCK && opponentChoice === Choice.SCISSORS) ||
      (playerChoice === Choice.PAPER && opponentChoice === Choice.ROCK) ||
      (playerChoice === Choice.SCISSORS && opponentChoice === Choice.PAPER);

    return playerWins ? RoundResult.PLAYER_WIN : RoundResult.COMPUTER_WIN;
  }

  isPlayerWin(result: RoundResult): boolean {
    return result === RoundResult.PLAYER_WIN;
  }

  isOpponentWin(result: RoundResult): boolean {
    return result === RoundResult.COMPUTER_WIN;
  }

  isTie(result: RoundResult): boolean {
    return result === RoundResult.TIE;
  }
}
```

#### 재사용 방법
1. 게임별 Choice와 Result 타입 정의
2. RoundBasedGameEngine 상속
3. 추상 메서드 구현 (게임 규칙)
4. 게임 설정 조정

#### 적용 가능한 프로젝트
- 틱택토 게임
- 카드 게임 (포커, 블랙잭)
- 턴 기반 전략 게임
- 퀴즈 대전 게임

### 3. Player Strategy System

#### 컴포넌트 개요
다양한 플레이어 타입을 통합적으로 관리하는 시스템

#### 핵심 코드
```typescript
// 플레이어 인터페이스
interface Player<TChoice> {
  getId(): string;
  getName(): string;
  getChoice(): Promise<TChoice> | TChoice;
}

// 랜덤 플레이어 (컴퓨터)
class RandomPlayer<TChoice> implements Player<TChoice> {
  constructor(
    private readonly id: string,
    private readonly name: string,
    private readonly choices: readonly TChoice[]
  ) {}

  getId(): string {
    return this.id;
  }

  getName(): string {
    return this.name;
  }

  getChoice(): TChoice {
    const randomIndex = Math.floor(Math.random() * this.choices.length);
    return this.choices[randomIndex]!;
  }

  // 통계 분석을 위한 헬퍼 메서드
  generateChoices(count: number): TChoice[] {
    return Array.from({ length: count }, () => this.getChoice());
  }

  static analyzeDistribution<T>(choices: T[]): {
    counts: Map<T, number>;
    percentages: Map<T, number>;
    total: number;
  } {
    const counts = new Map<T, number>();
    choices.forEach(choice => {
      counts.set(choice, (counts.get(choice) || 0) + 1);
    });

    const total = choices.length;
    const percentages = new Map<T, number>();
    for (const [choice, count] of counts) {
      percentages.set(choice, total > 0 ? (count / total) * 100 : 0);
    }

    return { counts, percentages, total };
  }
}

// 인간 플레이어 (입력 기반)
class HumanPlayer<TChoice> implements Player<TChoice> {
  constructor(
    private readonly id: string,
    private readonly name: string,
    private readonly inputProvider: InputProvider<TChoice>
  ) {}

  getId(): string {
    return this.id;
  }

  getName(): string {
    return this.name;
  }

  async getChoice(): Promise<TChoice> {
    return await this.inputProvider.getInput();
  }
}

// 입력 제공자 인터페이스
interface InputProvider<TChoice> {
  getInput(): Promise<TChoice>;
}

// 콘솔 입력 제공자
class ConsoleInputProvider implements InputProvider<Choice> {
  constructor(private readonly ui: ConsoleUI) {}

  async getInput(): Promise<Choice> {
    while (true) {
      const choice = await this.ui.getUserChoice();
      if (choice !== null) {
        return choice;
      }
      console.log('Invalid input. Please try again.');
    }
  }
}

// AI 플레이어 (학습 기반)
class AIPlayer<TChoice> implements Player<TChoice> {
  private history: TChoice[] = [];

  constructor(
    private readonly id: string,
    private readonly name: string,
    private readonly choices: readonly TChoice[],
    private readonly strategy: AIStrategy<TChoice>
  ) {}

  getId(): string {
    return this.id;
  }

  getName(): string {
    return this.name;
  }

  getChoice(): TChoice {
    const choice = this.strategy.selectChoice(this.choices, this.history);
    this.history.push(choice);
    return choice;
  }

  updateHistory(opponentChoice: TChoice): void {
    // AI가 상대방의 선택을 학습할 수 있도록 업데이트
  }
}

// AI 전략 인터페이스
interface AIStrategy<TChoice> {
  selectChoice(
    availableChoices: readonly TChoice[],
    history: readonly TChoice[]
  ): TChoice;
}

// 간단한 AI 전략들
class RandomStrategy<TChoice> implements AIStrategy<TChoice> {
  selectChoice(availableChoices: readonly TChoice[]): TChoice {
    const randomIndex = Math.floor(Math.random() * availableChoices.length);
    return availableChoices[randomIndex]!;
  }
}

class CounterStrategy implements AIStrategy<Choice> {
  selectChoice(
    availableChoices: readonly Choice[],
    history: readonly Choice[]
  ): Choice {
    if (history.length === 0) {
      return Choice.ROCK; // 기본값
    }

    const lastOpponentChoice = history[history.length - 1];

    // 상대방의 마지막 선택을 이기는 선택
    switch (lastOpponentChoice) {
      case Choice.ROCK:
        return Choice.PAPER;
      case Choice.PAPER:
        return Choice.SCISSORS;
      case Choice.SCISSORS:
        return Choice.ROCK;
      default:
        return Choice.ROCK;
    }
  }
}
```

#### 재사용 방법
1. 게임별 Player 인터페이스 확장
2. 프로젝트에 맞는 InputProvider 구현
3. 게임별 AI 전략 개발
4. 플레이어 팩토리 구현

#### 적용 가능한 프로젝트
- 멀티플레이어 게임
- AI 대전 게임
- 학습 기반 게임
- 네트워크 게임

## 🖥️ UI 컴포넌트

### 1. Console Interface System

#### 컴포넌트 개요
대화형 콘솔 인터페이스를 구현하는 시스템

#### 핵심 코드
```typescript
// 콘솔 UI 기본 클래스
abstract class ConsoleInterface {
  protected rl: readline.Interface;

  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  // 기본 질문 메서드
  protected question(questionText: string): Promise<string> {
    return new Promise((resolve) => {
      this.rl.question(questionText, resolve);
    });
  }

  // 지연 메서드
  protected delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // 애니메이션 메서드
  protected async showProgress(
    message: string,
    duration: number = 1000,
    steps: number = 3
  ): Promise<void> {
    process.stdout.write(`\n${message}`);
    const stepDuration = duration / steps;

    for (let i = 0; i < steps; i++) {
      await this.delay(stepDuration);
      process.stdout.write('.');
    }
    console.log(' ✓');
  }

  // 선택지 메뉴
  protected async showMenu<T>(
    title: string,
    options: Array<{ key: string; label: string; value: T }>
  ): Promise<T> {
    console.log(`\n${title}`);
    console.log('─'.repeat(title.length));

    options.forEach(option => {
      console.log(`${option.key}. ${option.label}`);
    });

    while (true) {
      const input = await this.question('\nSelect an option: ');
      const option = options.find(opt => opt.key === input.trim());

      if (option) {
        return option.value;
      }

      console.log('❌ Invalid option. Please try again.');
    }
  }

  // 확인 대화상자
  protected async confirm(message: string): Promise<boolean> {
    while (true) {
      const input = await this.question(`${message} (y/n): `);
      const normalized = input.toLowerCase().trim();

      if (normalized === 'y' || normalized === 'yes') {
        return true;
      } else if (normalized === 'n' || normalized === 'no') {
        return false;
      }

      console.log('❌ Please enter "y" for yes or "n" for no.');
    }
  }

  // 숫자 입력
  protected async getNumber(
    prompt: string,
    min?: number,
    max?: number
  ): Promise<number> {
    while (true) {
      const input = await this.question(prompt);
      const number = parseInt(input.trim());

      if (isNaN(number)) {
        console.log('❌ Please enter a valid number.');
        continue;
      }

      if (min !== undefined && number < min) {
        console.log(`❌ Number must be at least ${min}.`);
        continue;
      }

      if (max !== undefined && number > max) {
        console.log(`❌ Number must be no more than ${max}.`);
        continue;
      }

      return number;
    }
  }

  // 리소스 정리
  close(): void {
    this.rl.close();
  }

  // 화면 지우기
  protected clearScreen(): void {
    console.clear();
  }

  // 헤더 표시
  protected showHeader(title: string, subtitle?: string): void {
    const width = Math.max(title.length, subtitle?.length || 0) + 4;
    const border = '═'.repeat(width);

    console.log(`\n┌${border}┐`);
    console.log(`│ ${title.padEnd(width - 2)} │`);
    if (subtitle) {
      console.log(`│ ${subtitle.padEnd(width - 2)} │`);
    }
    console.log(`└${border}┘\n`);
  }

  // 상태 표시
  protected showStatus(items: Array<{ label: string; value: string }>): void {
    const maxLabelLength = Math.max(...items.map(item => item.label.length));

    items.forEach(item => {
      const paddedLabel = item.label.padEnd(maxLabelLength);
      console.log(`${paddedLabel}: ${item.value}`);
    });
  }

  // 에러 표시
  protected showError(message: string): void {
    console.log(`\n❌ Error: ${message}\n`);
  }

  // 성공 표시
  protected showSuccess(message: string): void {
    console.log(`\n✅ ${message}\n`);
  }

  // 경고 표시
  protected showWarning(message: string): void {
    console.log(`\n⚠️  Warning: ${message}\n`);
  }
}

// 게임별 UI 구현 예시
class GameConsoleUI extends ConsoleInterface {
  showWelcome(gameName: string): void {
    this.showHeader(
      `🎮 ${gameName}`,
      'Welcome to the game!'
    );
  }

  async getPlayerName(): Promise<string> {
    while (true) {
      const name = await this.question('Enter your name: ');
      const trimmed = name.trim();

      if (trimmed.length === 0) {
        this.showError('Name cannot be empty');
        continue;
      }

      if (trimmed.length > 20) {
        this.showError('Name must be 20 characters or less');
        continue;
      }

      return trimmed;
    }
  }

  showGameState(state: any): void {
    this.showStatus([
      { label: 'Round', value: state.currentRound.toString() },
      { label: 'Player Score', value: state.playerScore.toString() },
      { label: 'Computer Score', value: state.computerScore.toString() }
    ]);
  }

  async askPlayAgain(): Promise<boolean> {
    return await this.confirm('🔄 Do you want to play again?');
  }

  showGoodbye(): void {
    this.showHeader('👋 Thanks for playing!');
  }
}
```

#### 재사용 방법
1. ConsoleInterface를 상속하여 게임별 UI 구현
2. 필요한 입력 메서드 추가
3. 게임별 화면 레이아웃 커스터마이징
4. 에러 처리 및 검증 로직 확장

#### 적용 가능한 프로젝트
- CLI 도구
- 터미널 게임
- 설정 마법사
- 대화형 스크립트

### 2. Input Validation System

#### 컴포넌트 개요
사용자 입력을 안전하게 검증하고 파싱하는 시스템

#### 핵심 코드
```typescript
// 검증 결과 타입
type ValidationResult<T> = {
  isValid: true;
  value: T;
} | {
  isValid: false;
  error: string;
};

// 검증기 인터페이스
interface Validator<T> {
  validate(input: string): ValidationResult<T>;
}

// 기본 검증기들
class StringValidator implements Validator<string> {
  constructor(
    private readonly minLength: number = 0,
    private readonly maxLength: number = Infinity,
    private readonly pattern?: RegExp
  ) {}

  validate(input: string): ValidationResult<string> {
    const trimmed = input.trim();

    if (trimmed.length < this.minLength) {
      return {
        isValid: false,
        error: `Must be at least ${this.minLength} characters long`
      };
    }

    if (trimmed.length > this.maxLength) {
      return {
        isValid: false,
        error: `Must be no more than ${this.maxLength} characters long`
      };
    }

    if (this.pattern && !this.pattern.test(trimmed)) {
      return {
        isValid: false,
        error: 'Invalid format'
      };
    }

    return {
      isValid: true,
      value: trimmed
    };
  }
}

class NumberValidator implements Validator<number> {
  constructor(
    private readonly min: number = -Infinity,
    private readonly max: number = Infinity,
    private readonly integer: boolean = false
  ) {}

  validate(input: string): ValidationResult<number> {
    const trimmed = input.trim();
    const number = parseFloat(trimmed);

    if (isNaN(number)) {
      return {
        isValid: false,
        error: 'Must be a valid number'
      };
    }

    if (this.integer && !Number.isInteger(number)) {
      return {
        isValid: false,
        error: 'Must be an integer'
      };
    }

    if (number < this.min) {
      return {
        isValid: false,
        error: `Must be at least ${this.min}`
      };
    }

    if (number > this.max) {
      return {
        isValid: false,
        error: `Must be no more than ${this.max}`
      };
    }

    return {
      isValid: true,
      value: number
    };
  }
}

class EnumValidator<T extends string> implements Validator<T> {
  constructor(
    private readonly values: readonly T[],
    private readonly caseSensitive: boolean = false
  ) {}

  validate(input: string): ValidationResult<T> {
    const processedInput = this.caseSensitive ? input.trim() : input.trim().toLowerCase();
    const processedValues = this.caseSensitive ? this.values : this.values.map(v => v.toLowerCase());

    const index = processedValues.indexOf(processedInput as T);
    if (index === -1) {
      return {
        isValid: false,
        error: `Must be one of: ${this.values.join(', ')}`
      };
    }

    return {
      isValid: true,
      value: this.values[index]
    };
  }
}

// 조합 검증기
class CompositeValidator<T> implements Validator<T> {
  constructor(private readonly validators: Validator<T>[]) {}

  validate(input: string): ValidationResult<T> {
    for (const validator of this.validators) {
      const result = validator.validate(input);
      if (!result.isValid) {
        return result;
      }
    }

    // 마지막 검증기의 결과 반환
    return this.validators[this.validators.length - 1].validate(input);
  }
}

// 커스텀 검증기
class CustomValidator<T> implements Validator<T> {
  constructor(
    private readonly validateFn: (input: string) => ValidationResult<T>
  ) {}

  validate(input: string): ValidationResult<T> {
    return this.validateFn(input);
  }
}

// 검증된 입력 헬퍼
class ValidatedInput {
  static async getString(
    ui: ConsoleInterface,
    prompt: string,
    validator: Validator<string>
  ): Promise<string> {
    while (true) {
      const input = await ui.question(prompt);
      const result = validator.validate(input);

      if (result.isValid) {
        return result.value;
      }

      console.log(`❌ ${result.error}`);
    }
  }

  static async getNumber(
    ui: ConsoleInterface,
    prompt: string,
    validator: Validator<number>
  ): Promise<number> {
    while (true) {
      const input = await ui.question(prompt);
      const result = validator.validate(input);

      if (result.isValid) {
        return result.value;
      }

      console.log(`❌ ${result.error}`);
    }
  }

  static async getEnum<T extends string>(
    ui: ConsoleInterface,
    prompt: string,
    validator: Validator<T>
  ): Promise<T> {
    while (true) {
      const input = await ui.question(prompt);
      const result = validator.validate(input);

      if (result.isValid) {
        return result.value;
      }

      console.log(`❌ ${result.error}`);
    }
  }
}

// 사용 예시
async function getUserConfiguration(ui: ConsoleInterface): Promise<{
  name: string;
  age: number;
  difficulty: 'easy' | 'medium' | 'hard';
}> {
  const nameValidator = new StringValidator(2, 20, /^[a-zA-Z\s]+$/);
  const ageValidator = new NumberValidator(1, 120, true);
  const difficultyValidator = new EnumValidator(['easy', 'medium', 'hard']);

  const name = await ValidatedInput.getString(
    ui,
    'Enter your name: ',
    nameValidator
  );

  const age = await ValidatedInput.getNumber(
    ui,
    'Enter your age: ',
    ageValidator
  );

  const difficulty = await ValidatedInput.getEnum(
    ui,
    'Select difficulty (easy/medium/hard): ',
    difficultyValidator
  );

  return { name, age, difficulty };
}
```

#### 재사용 방법
1. 프로젝트별 검증기 구현
2. 복합 검증 규칙 조합
3. 커스텀 검증 로직 추가
4. 에러 메시지 현지화

#### 적용 가능한 프로젝트
- 사용자 등록 시스템
- 설정 입력 도구
- 데이터 입력 애플리케이션
- API 파라미터 검증

## 🧪 테스트 유틸리티 컴포넌트

### 1. Statistical Testing Framework

#### 컴포넌트 개요
확률적 동작을 검증하는 통계적 테스트 프레임워크

#### 핵심 코드
```typescript
// 통계 분석 유틸리티
class StatisticalAnalyzer {
  static analyzeDistribution<T>(
    samples: T[],
    expectedDistribution?: Map<T, number>
  ): {
    counts: Map<T, number>;
    percentages: Map<T, number>;
    total: number;
    isUniform: boolean;
    chiSquareTest?: number;
  } {
    const counts = new Map<T, number>();
    samples.forEach(sample => {
      counts.set(sample, (counts.get(sample) || 0) + 1);
    });

    const total = samples.length;
    const percentages = new Map<T, number>();
    for (const [key, count] of counts) {
      percentages.set(key, total > 0 ? (count / total) * 100 : 0);
    }

    // 균등 분포 검증
    const uniqueValues = Array.from(counts.keys());
    const expectedPercentage = 100 / uniqueValues.length;
    const tolerance = 5; // 5% 허용 오차

    const isUniform = Array.from(percentages.values()).every(percentage =>
      Math.abs(percentage - expectedPercentage) <= tolerance
    );

    // 카이제곱 검정 (선택적)
    let chiSquareTest: number | undefined;
    if (expectedDistribution) {
      chiSquareTest = this.calculateChiSquare(counts, expectedDistribution, total);
    }

    return {
      counts,
      percentages,
      total,
      isUniform,
      chiSquareTest
    };
  }

  private static calculateChiSquare<T>(
    observed: Map<T, number>,
    expected: Map<T, number>,
    total: number
  ): number {
    let chiSquare = 0;

    for (const [key, expectedRatio] of expected) {
      const observedCount = observed.get(key) || 0;
      const expectedCount = expectedRatio * total;

      if (expectedCount > 0) {
        chiSquare += Math.pow(observedCount - expectedCount, 2) / expectedCount;
      }
    }

    return chiSquare;
  }

  static calculateMean(numbers: number[]): number {
    return numbers.reduce((sum, num) => sum + num, 0) / numbers.length;
  }

  static calculateStandardDeviation(numbers: number[]): number {
    const mean = this.calculateMean(numbers);
    const squaredDifferences = numbers.map(num => Math.pow(num - mean, 2));
    const variance = this.calculateMean(squaredDifferences);
    return Math.sqrt(variance);
  }

  static isWithinRange(
    value: number,
    target: number,
    tolerancePercent: number
  ): boolean {
    const tolerance = target * (tolerancePercent / 100);
    return Math.abs(value - target) <= tolerance;
  }
}

// 테스트 헬퍼 함수들
class TestHelpers {
  // 랜덤 함수 테스트
  static testRandomFunction<T>(
    randomFn: () => T,
    possibleValues: T[],
    sampleSize: number = 1000,
    tolerancePercent: number = 10
  ): {
    passed: boolean;
    analysis: ReturnType<typeof StatisticalAnalyzer.analyzeDistribution>;
    message: string;
  } {
    const samples = Array.from({ length: sampleSize }, () => randomFn());
    const analysis = StatisticalAnalyzer.analyzeDistribution(samples);

    const expectedPercentage = 100 / possibleValues.length;
    const tolerance = expectedPercentage * (tolerancePercent / 100);

    let passed = true;
    let failedValues: string[] = [];

    for (const value of possibleValues) {
      const percentage = analysis.percentages.get(value) || 0;
      if (!StatisticalAnalyzer.isWithinRange(percentage, expectedPercentage, tolerancePercent)) {
        passed = false;
        failedValues.push(`${value}: ${percentage.toFixed(2)}%`);
      }
    }

    const message = passed
      ? `Distribution test passed. All values within ${tolerancePercent}% tolerance.`
      : `Distribution test failed. Values outside tolerance: ${failedValues.join(', ')}`;

    return { passed, analysis, message };
  }

  // 성능 측정
  static measurePerformance<T>(
    fn: () => T,
    iterations: number = 1000
  ): {
    averageTimeMs: number;
    minTimeMs: number;
    maxTimeMs: number;
    totalTimeMs: number;
    operationsPerSecond: number;
  } {
    const times: number[] = [];

    for (let i = 0; i < iterations; i++) {
      const start = performance.now();
      fn();
      const end = performance.now();
      times.push(end - start);
    }

    const totalTimeMs = times.reduce((sum, time) => sum + time, 0);
    const averageTimeMs = totalTimeMs / iterations;
    const minTimeMs = Math.min(...times);
    const maxTimeMs = Math.max(...times);
    const operationsPerSecond = 1000 / averageTimeMs;

    return {
      averageTimeMs,
      minTimeMs,
      maxTimeMs,
      totalTimeMs,
      operationsPerSecond
    };
  }

  // 메모리 사용량 측정 (Node.js)
  static measureMemoryUsage<T>(fn: () => T): {
    result: T;
    memoryUsed: number;
    heapUsed: number;
  } {
    if (typeof process === 'undefined') {
      throw new Error('Memory measurement only available in Node.js');
    }

    const startMemory = process.memoryUsage();
    const result = fn();
    const endMemory = process.memoryUsage();

    return {
      result,
      memoryUsed: endMemory.rss - startMemory.rss,
      heapUsed: endMemory.heapUsed - startMemory.heapUsed
    };
  }

  // 비동기 함수 타임아웃 테스트
  static async testWithTimeout<T>(
    asyncFn: () => Promise<T>,
    timeoutMs: number
  ): Promise<{ result: T; timedOut: false } | { timedOut: true }> {
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error('Timeout')), timeoutMs);
    });

    try {
      const result = await Promise.race([asyncFn(), timeoutPromise]);
      return { result, timedOut: false };
    } catch (error) {
      if (error instanceof Error && error.message === 'Timeout') {
        return { timedOut: true };
      }
      throw error;
    }
  }
}

// Jest 헬퍼 매처들
const customMatchers = {
  toBeWithinPercentage(received: number, expected: number, tolerance: number) {
    const pass = StatisticalAnalyzer.isWithinRange(received, expected, tolerance);

    if (pass) {
      return {
        message: () =>
          `expected ${received} not to be within ${tolerance}% of ${expected}`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected ${received} to be within ${tolerance}% of ${expected}`,
        pass: false,
      };
    }
  },

  toHaveUniformDistribution<T>(received: T[], tolerance: number = 10) {
    const analysis = StatisticalAnalyzer.analyzeDistribution(received);
    const pass = analysis.isUniform;

    if (pass) {
      return {
        message: () => `expected distribution not to be uniform`,
        pass: true,
      };
    } else {
      return {
        message: () =>
          `expected distribution to be uniform within ${tolerance}% tolerance`,
        pass: false,
      };
    }
  }
};

// TypeScript 타입 확장
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeWithinPercentage(expected: number, tolerance: number): R;
      toHaveUniformDistribution(tolerance?: number): R;
    }
  }
}

// 사용 예시
describe('Random Function Tests', () => {
  test('computer player generates uniform distribution', () => {
    const computerPlayer = new ComputerPlayer();
    const choices = computerPlayer.generateChoices(3000);

    expect(choices).toHaveUniformDistribution(5);
  });

  test('random number generator is within tolerance', () => {
    const results = Array.from({ length: 1000 }, () => Math.random());
    const average = StatisticalAnalyzer.calculateMean(results);

    expect(average).toBeWithinPercentage(0.5, 5);
  });
});
```

#### 재사용 방법
1. 확률적 동작 테스트에 StatisticalAnalyzer 활용
2. 성능 테스트에 TestHelpers 사용
3. 커스텀 Jest 매처 추가
4. 프로젝트별 통계 기준 설정

#### 적용 가능한 프로젝트
- 게임 밸런싱 테스트
- 알고리즘 성능 검증
- 랜덤 함수 품질 테스트
- 로드 밸런싱 검증

---

**이러한 재사용 가능한 컴포넌트들은 Rock-Paper-Scissors 프로젝트에서 실제로 검증된 구현체들로, 다양한 프로젝트에서 활용하여 개발 속도를 높이고 품질을 보장할 수 있습니다.**