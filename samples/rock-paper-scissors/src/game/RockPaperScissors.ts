import {
  Choice,
  RoundResult,
  GameResult,
  Round,
  Score,
  GameState,
  GameConfig,
  Player
} from '../models/GameTypes';

/**
 * Main Rock-Paper-Scissors game engine
 */
export class RockPaperScissors {
  private rounds: Round[] = [];
  private score: Score = { playerWins: 0, computerWins: 0, ties: 0 };
  private readonly config: GameConfig;

  constructor(config: Partial<GameConfig> = {}) {
    this.config = {
      maxRounds: config.maxRounds ?? 5, // Maximum rounds to prevent infinite ties
      winsNeeded: config.winsNeeded ?? 2 // Best of 3 (first to 2 wins)
    };
  }

  /**
   * Determine the winner of a single round
   * @param playerChoice Player's choice
   * @param computerChoice Computer's choice
   * @returns Result of the round
   */
  private determineRoundWinner(playerChoice: Choice, computerChoice: Choice): RoundResult {
    if (playerChoice === computerChoice) {
      return RoundResult.TIE;
    }

    // Check winning conditions for player
    const playerWins =
      (playerChoice === Choice.ROCK && computerChoice === Choice.SCISSORS) ||
      (playerChoice === Choice.PAPER && computerChoice === Choice.ROCK) ||
      (playerChoice === Choice.SCISSORS && computerChoice === Choice.PAPER);

    return playerWins ? RoundResult.PLAYER_WIN : RoundResult.COMPUTER_WIN;
  }

  /**
   * Update the score based on round result
   * @param result Result of the round
   */
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

  /**
   * Determine if the game is complete
   * @returns true if game is complete, false otherwise
   */
  private isGameComplete(): boolean {
    const maxRoundsReached = this.rounds.length >= this.config.maxRounds;
    const playerWon = this.score.playerWins >= this.config.winsNeeded;
    const computerWon = this.score.computerWins >= this.config.winsNeeded;

    return maxRoundsReached || playerWon || computerWon;
  }

  /**
   * Get the current game result
   * @returns Current game result
   */
  private getGameResult(): GameResult {
    if (!this.isGameComplete()) {
      return GameResult.IN_PROGRESS;
    }

    if (this.score.playerWins > this.score.computerWins) {
      return GameResult.PLAYER_VICTORY;
    } else if (this.score.computerWins > this.score.playerWins) {
      return GameResult.COMPUTER_VICTORY;
    }

    // This shouldn't happen with best-of-3 format, but handle edge case
    return this.score.playerWins >= this.config.winsNeeded ?
      GameResult.PLAYER_VICTORY : GameResult.COMPUTER_VICTORY;
  }

  /**
   * Play a single round
   * @param playerChoice Player's choice for this round
   * @param computerChoice Computer's choice for this round
   * @returns Round result and updated game state
   */
  playRound(playerChoice: Choice, computerChoice: Choice): {
    round: Round;
    gameState: GameState;
  } {
    if (this.isGameComplete()) {
      throw new Error('Game is already complete. Start a new game to continue playing.');
    }

    const roundNumber = this.rounds.length + 1;
    const result = this.determineRoundWinner(playerChoice, computerChoice);

    const round: Round = {
      roundNumber,
      playerChoice,
      computerChoice,
      result
    };

    // Update game state
    this.rounds.push(round);
    this.updateScore(result);

    const gameState: GameState = {
      rounds: [...this.rounds],
      score: { ...this.score },
      result: this.getGameResult(),
      isComplete: this.isGameComplete()
    };

    return { round, gameState };
  }

  /**
   * Get the current game state
   * @returns Current game state
   */
  getGameState(): GameState {
    return {
      rounds: [...this.rounds],
      score: { ...this.score },
      result: this.getGameResult(),
      isComplete: this.isGameComplete()
    };
  }

  /**
   * Reset the game to initial state
   */
  reset(): void {
    this.rounds = [];
    this.score = { playerWins: 0, computerWins: 0, ties: 0 };
  }

  /**
   * Get game configuration
   * @returns Current game configuration
   */
  getConfig(): GameConfig {
    return { ...this.config };
  }

  /**
   * Get the current round number (next round to be played)
   * @returns Current round number
   */
  getCurrentRoundNumber(): number {
    return this.rounds.length + 1;
  }

  /**
   * Check if game can continue (not at max rounds and no winner yet)
   * @returns true if game can continue, false otherwise
   */
  canContinue(): boolean {
    return !this.isGameComplete();
  }

  /**
   * Get game summary statistics
   * @returns Object with game statistics
   */
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

    let winner: string;
    const gameResult = this.getGameResult();
    switch (gameResult) {
      case GameResult.PLAYER_VICTORY:
        winner = 'Player';
        break;
      case GameResult.COMPUTER_VICTORY:
        winner = 'Computer';
        break;
      default:
        winner = 'Game in progress';
    }

    return {
      totalRounds,
      playerWinRate,
      computerWinRate,
      tieRate,
      winner
    };
  }
}