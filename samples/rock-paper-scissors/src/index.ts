#!/usr/bin/env node

import { RockPaperScissors } from './game/RockPaperScissors';
import { ComputerPlayer } from './services/ComputerPlayer';
import { ConsoleUI } from './ui/ConsoleUI';
import { Choice } from './models/GameTypes';

/**
 * Main application class that orchestrates the game flow
 */
class RockPaperScissorsApp {
  private game: RockPaperScissors;
  private computerPlayer: ComputerPlayer;
  private ui: ConsoleUI;

  constructor() {
    this.game = new RockPaperScissors();
    this.computerPlayer = new ComputerPlayer();
    this.ui = new ConsoleUI();
  }

  /**
   * Run the complete game application
   */
  async run(): Promise<void> {
    try {
      this.ui.displayWelcome();

      do {
        await this.playGame();
      } while (await this.ui.askPlayAgain());

      this.ui.displayGoodbye();
    } catch (error) {
      this.ui.displayError(error instanceof Error ? error.message : 'An unknown error occurred');
    } finally {
      this.ui.close();
    }
  }

  /**
   * Play a single game (best of 3 rounds)
   */
  private async playGame(): Promise<void> {
    this.game.reset();

    while (this.game.canContinue()) {
      const gameState = this.game.getGameState();
      this.ui.displayGameStatus(gameState);

      // Get player choice
      const playerChoice = await this.ui.getUserChoice();
      if (playerChoice === null) {
        // User wants to quit
        return;
      }

      // Show computer thinking animation
      await this.ui.displayComputerThinking();

      // Get computer choice
      const computerChoice = this.computerPlayer.getChoice();

      // Play the round
      try {
        const { round, gameState: newGameState } = this.game.playRound(playerChoice, computerChoice);

        // Display round results
        this.ui.displayRoundResult(round);

        // Check if game is complete
        if (newGameState.isComplete) {
          this.ui.displayRoundSeparator();
          this.ui.displayGameResult(newGameState);
          break;
        }

        this.ui.displayRoundSeparator();
      } catch (error) {
        this.ui.displayError(error instanceof Error ? error.message : 'An error occurred during the round');
        break;
      }
    }
  }
}

/**
 * Application entry point
 */
async function main(): Promise<void> {
  const app = new RockPaperScissorsApp();
  await app.run();
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error);
  process.exit(1);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n👋 Game interrupted. Thanks for playing!');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n\n👋 Game terminated. Thanks for playing!');
  process.exit(0);
});

// Run the application
if (require.main === module) {
  main().catch((error) => {
    console.error('Failed to start application:', error);
    process.exit(1);
  });
}