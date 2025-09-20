/**
 * Game choice options for Rock-Paper-Scissors
 */
export enum Choice {
  ROCK = 'rock',
  PAPER = 'paper',
  SCISSORS = 'scissors'
}

/**
 * Result of a single round
 */
export enum RoundResult {
  PLAYER_WIN = 'player_win',
  COMPUTER_WIN = 'computer_win',
  TIE = 'tie'
}

/**
 * Overall game result
 */
export enum GameResult {
  PLAYER_VICTORY = 'player_victory',
  COMPUTER_VICTORY = 'computer_victory',
  IN_PROGRESS = 'in_progress'
}

/**
 * Represents a single round of the game
 */
export interface Round {
  readonly roundNumber: number;
  readonly playerChoice: Choice;
  readonly computerChoice: Choice;
  readonly result: RoundResult;
}

/**
 * Current score state
 */
export interface Score {
  readonly playerWins: number;
  readonly computerWins: number;
  readonly ties: number;
}

/**
 * Complete game state
 */
export interface GameState {
  readonly rounds: ReadonlyArray<Round>;
  readonly score: Score;
  readonly result: GameResult;
  readonly isComplete: boolean;
}

/**
 * Player interface for different types of players
 */
export interface Player {
  /**
   * Get the player's choice for the current round
   */
  getChoice(): Promise<Choice> | Choice;
}

/**
 * Game configuration options
 */
export interface GameConfig {
  readonly maxRounds: number;
  readonly winsNeeded: number;
}

/**
 * Type guard to check if a string is a valid Choice
 */
export function isValidChoice(choice: string): choice is Choice {
  return Object.values(Choice).includes(choice as Choice);
}

/**
 * Type guard to check if a choice input is valid
 */
export function parseChoice(input: string): Choice | null {
  const normalized = input.toLowerCase().trim();

  // Allow common variations
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

/**
 * Get display name for a choice
 */
export function getChoiceDisplayName(choice: Choice): string {
  switch (choice) {
    case Choice.ROCK:
      return '🪨 Rock';
    case Choice.PAPER:
      return '📄 Paper';
    case Choice.SCISSORS:
      return '✂️ Scissors';
  }
}

/**
 * Get display message for round result
 */
export function getRoundResultMessage(result: RoundResult): string {
  switch (result) {
    case RoundResult.PLAYER_WIN:
      return '🎉 You win this round!';
    case RoundResult.COMPUTER_WIN:
      return '💻 Computer wins this round!';
    case RoundResult.TIE:
      return '🤝 It\'s a tie!';
  }
}