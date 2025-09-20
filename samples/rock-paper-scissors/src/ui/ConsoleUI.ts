import * as readline from 'readline';
import {
  Choice,
  Round,
  GameState,
  parseChoice,
  getChoiceDisplayName,
  getRoundResultMessage,
  GameResult
} from '../models/GameTypes';

/**
 * Console-based user interface for the Rock-Paper-Scissors game
 */
export class ConsoleUI {
  private rl: readline.Interface;

  constructor() {
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  }

  /**
   * Display the game title and instructions
   */
  displayWelcome(): void {
    console.log('\n🎮 Rock-Paper-Scissors Game 🎮');
    console.log('===============================');
    console.log('Best of 3 rounds - First to 2 wins!');
    console.log('\nHow to play:');
    console.log('• Enter "rock" (or "r" or "1") for Rock 🪨');
    console.log('• Enter "paper" (or "p" or "2") for Paper 📄');
    console.log('• Enter "scissors" (or "s" or "3") for Scissors ✂️');
    console.log('• Enter "quit" to exit the game');
    console.log('\n═══════════════════════════════════════\n');
  }

  /**
   * Display current game status
   * @param gameState Current game state
   */
  displayGameStatus(gameState: GameState): void {
    console.log(`\n📊 Score: Player ${gameState.score.playerWins} - ${gameState.score.computerWins} Computer`);
    if (gameState.score.ties > 0) {
      console.log(`   Ties: ${gameState.score.ties}`);
    }
    console.log(`   Round: ${gameState.rounds.length + 1}`);
    console.log('─'.repeat(40));
  }

  /**
   * Get user choice for the current round
   * @returns Promise that resolves to user's choice or null if quit
   */
  async getUserChoice(): Promise<Choice | null> {
    while (true) {
      const input = await this.question('\n🤔 Enter your choice (rock/paper/scissors): ');

      if (input.toLowerCase().trim() === 'quit') {
        return null;
      }

      const choice = parseChoice(input);
      if (choice !== null) {
        return choice;
      }

      console.log('❌ Invalid choice! Please enter rock, paper, scissors, or quit.');
    }
  }

  /**
   * Display the result of a round
   * @param round The completed round
   */
  displayRoundResult(round: Round): void {
    console.log('\n🎯 Round Results:');
    console.log(`   You chose: ${getChoiceDisplayName(round.playerChoice)}`);
    console.log(`   Computer chose: ${getChoiceDisplayName(round.computerChoice)}`);
    console.log(`   ${getRoundResultMessage(round.result)}`);
  }

  /**
   * Display the final game results
   * @param gameState Final game state
   */
  displayGameResult(gameState: GameState): void {
    console.log('\n🏆 GAME OVER! 🏆');
    console.log('═'.repeat(40));

    const summary = this.getGameSummary(gameState);
    console.log(`Final Score: Player ${gameState.score.playerWins} - ${gameState.score.computerWins} Computer`);

    if (gameState.result === GameResult.PLAYER_VICTORY) {
      console.log('🎉 Congratulations! You won the game! 🎉');
    } else if (gameState.result === GameResult.COMPUTER_VICTORY) {
      console.log('💻 Computer wins! Better luck next time! 💻');
    }

    console.log(`\nGame Statistics:`);
    console.log(`• Total Rounds: ${summary.totalRounds}`);
    console.log(`• Player Win Rate: ${summary.playerWinRate.toFixed(1)}%`);
    console.log(`• Computer Win Rate: ${summary.computerWinRate.toFixed(1)}%`);
    if (gameState.score.ties > 0) {
      console.log(`• Tie Rate: ${summary.tieRate.toFixed(1)}%`);
    }
  }

  /**
   * Ask if user wants to play again
   * @returns Promise that resolves to true if user wants to play again
   */
  async askPlayAgain(): Promise<boolean> {
    while (true) {
      const input = await this.question('\n🔄 Do you want to play again? (y/n): ');
      const normalized = input.toLowerCase().trim();

      if (normalized === 'y' || normalized === 'yes') {
        return true;
      } else if (normalized === 'n' || normalized === 'no') {
        return false;
      }

      console.log('❌ Please enter "y" for yes or "n" for no.');
    }
  }

  /**
   * Display goodbye message
   */
  displayGoodbye(): void {
    console.log('\n👋 Thanks for playing Rock-Paper-Scissors!');
    console.log('See you next time! 🎮\n');
  }

  /**
   * Display round separator
   */
  displayRoundSeparator(): void {
    console.log('\n' + '═'.repeat(40));
  }

  /**
   * Display error message
   * @param message Error message to display
   */
  displayError(message: string): void {
    console.log(`\n❌ Error: ${message}`);
  }

  /**
   * Display thinking animation for computer choice
   */
  async displayComputerThinking(): Promise<void> {
    process.stdout.write('\n🤖 Computer is thinking');
    for (let i = 0; i < 3; i++) {
      await this.delay(300);
      process.stdout.write('.');
    }
    console.log(' 💭');
  }

  /**
   * Close the readline interface
   */
  close(): void {
    this.rl.close();
  }

  /**
   * Helper method to ask a question and get user input
   * @param questionText The question to ask
   * @returns Promise that resolves to user input
   */
  private question(questionText: string): Promise<string> {
    return new Promise((resolve) => {
      this.rl.question(questionText, resolve);
    });
  }

  /**
   * Helper method to add delay
   * @param ms Milliseconds to delay
   * @returns Promise that resolves after delay
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Calculate game summary statistics
   * @param gameState Current game state
   * @returns Game summary object
   */
  private getGameSummary(gameState: GameState): {
    totalRounds: number;
    playerWinRate: number;
    computerWinRate: number;
    tieRate: number;
  } {
    const totalRounds = gameState.rounds.length;
    const playerWinRate = totalRounds > 0 ? (gameState.score.playerWins / totalRounds) * 100 : 0;
    const computerWinRate = totalRounds > 0 ? (gameState.score.computerWins / totalRounds) * 100 : 0;
    const tieRate = totalRounds > 0 ? (gameState.score.ties / totalRounds) * 100 : 0;

    return {
      totalRounds,
      playerWinRate,
      computerWinRate,
      tieRate
    };
  }
}