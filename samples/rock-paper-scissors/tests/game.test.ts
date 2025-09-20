import { RockPaperScissors } from '../src/game/RockPaperScissors';
import { Choice, RoundResult, GameResult } from '../src/models/GameTypes';

describe('RockPaperScissors', () => {
  let game: RockPaperScissors;

  beforeEach(() => {
    game = new RockPaperScissors();
  });

  describe('Game Rules', () => {
    test('Rock beats Scissors', () => {
      const { round } = game.playRound(Choice.ROCK, Choice.SCISSORS);
      expect(round.result).toBe(RoundResult.PLAYER_WIN);
    });

    test('Scissors beats Paper', () => {
      const { round } = game.playRound(Choice.SCISSORS, Choice.PAPER);
      expect(round.result).toBe(RoundResult.PLAYER_WIN);
    });

    test('Paper beats Rock', () => {
      const { round } = game.playRound(Choice.PAPER, Choice.ROCK);
      expect(round.result).toBe(RoundResult.PLAYER_WIN);
    });

    test('Scissors loses to Rock', () => {
      const { round } = game.playRound(Choice.SCISSORS, Choice.ROCK);
      expect(round.result).toBe(RoundResult.COMPUTER_WIN);
    });

    test('Paper loses to Scissors', () => {
      const { round } = game.playRound(Choice.PAPER, Choice.SCISSORS);
      expect(round.result).toBe(RoundResult.COMPUTER_WIN);
    });

    test('Rock loses to Paper', () => {
      const { round } = game.playRound(Choice.ROCK, Choice.PAPER);
      expect(round.result).toBe(RoundResult.COMPUTER_WIN);
    });

    test('Same choices result in tie', () => {
      const choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSORS];

      choices.forEach(choice => {
        const testGame = new RockPaperScissors();
        const { round } = testGame.playRound(choice, choice);
        expect(round.result).toBe(RoundResult.TIE);
      });
    });
  });

  describe('Game State Management', () => {
    test('Initial game state is correct', () => {
      const gameState = game.getGameState();

      expect(gameState.rounds).toHaveLength(0);
      expect(gameState.score.playerWins).toBe(0);
      expect(gameState.score.computerWins).toBe(0);
      expect(gameState.score.ties).toBe(0);
      expect(gameState.result).toBe(GameResult.IN_PROGRESS);
      expect(gameState.isComplete).toBe(false);
    });

    test('Score updates correctly after player win', () => {
      const { gameState } = game.playRound(Choice.ROCK, Choice.SCISSORS);

      expect(gameState.score.playerWins).toBe(1);
      expect(gameState.score.computerWins).toBe(0);
      expect(gameState.score.ties).toBe(0);
    });

    test('Score updates correctly after computer win', () => {
      const { gameState } = game.playRound(Choice.SCISSORS, Choice.ROCK);

      expect(gameState.score.playerWins).toBe(0);
      expect(gameState.score.computerWins).toBe(1);
      expect(gameState.score.ties).toBe(0);
    });

    test('Score updates correctly after tie', () => {
      const { gameState } = game.playRound(Choice.ROCK, Choice.ROCK);

      expect(gameState.score.playerWins).toBe(0);
      expect(gameState.score.computerWins).toBe(0);
      expect(gameState.score.ties).toBe(1);
    });

    test('Round number increments correctly', () => {
      expect(game.getCurrentRoundNumber()).toBe(1);

      game.playRound(Choice.ROCK, Choice.SCISSORS);
      expect(game.getCurrentRoundNumber()).toBe(2);

      game.playRound(Choice.PAPER, Choice.ROCK);
      expect(game.getCurrentRoundNumber()).toBe(3);
    });
  });

  describe('Best of Three Logic', () => {
    test('Player wins after 2 victories', () => {
      // Player wins first round
      let result = game.playRound(Choice.ROCK, Choice.SCISSORS);
      expect(result.gameState.isComplete).toBe(false);
      expect(result.gameState.result).toBe(GameResult.IN_PROGRESS);

      // Player wins second round - game should be complete
      result = game.playRound(Choice.PAPER, Choice.ROCK);
      expect(result.gameState.isComplete).toBe(true);
      expect(result.gameState.result).toBe(GameResult.PLAYER_VICTORY);
    });

    test('Computer wins after 2 victories', () => {
      // Computer wins first round
      let result = game.playRound(Choice.SCISSORS, Choice.ROCK);
      expect(result.gameState.isComplete).toBe(false);
      expect(result.gameState.result).toBe(GameResult.IN_PROGRESS);

      // Computer wins second round - game should be complete
      result = game.playRound(Choice.PAPER, Choice.SCISSORS);
      expect(result.gameState.isComplete).toBe(true);
      expect(result.gameState.result).toBe(GameResult.COMPUTER_VICTORY);
    });

    test('Game continues through ties', () => {
      // Multiple ties shouldn't end the game
      game.playRound(Choice.ROCK, Choice.ROCK);
      game.playRound(Choice.PAPER, Choice.PAPER);
      game.playRound(Choice.SCISSORS, Choice.SCISSORS);

      const gameState = game.getGameState();
      expect(gameState.isComplete).toBe(false);
      expect(gameState.result).toBe(GameResult.IN_PROGRESS);
      expect(gameState.score.ties).toBe(3);
    });

    test('Cannot play rounds after game completion', () => {
      // End the game
      game.playRound(Choice.ROCK, Choice.SCISSORS); // Player wins
      game.playRound(Choice.PAPER, Choice.ROCK);    // Player wins - game ends

      // Trying to play another round should throw error
      expect(() => {
        game.playRound(Choice.SCISSORS, Choice.PAPER);
      }).toThrow('Game is already complete');
    });
  });

  describe('Game Reset', () => {
    test('Reset clears all game state', () => {
      // Play some rounds
      game.playRound(Choice.ROCK, Choice.SCISSORS);
      game.playRound(Choice.PAPER, Choice.ROCK);

      // Reset the game
      game.reset();

      const gameState = game.getGameState();
      expect(gameState.rounds).toHaveLength(0);
      expect(gameState.score.playerWins).toBe(0);
      expect(gameState.score.computerWins).toBe(0);
      expect(gameState.score.ties).toBe(0);
      expect(gameState.result).toBe(GameResult.IN_PROGRESS);
      expect(gameState.isComplete).toBe(false);
    });

    test('Can play new game after reset', () => {
      // Complete a game
      game.playRound(Choice.ROCK, Choice.SCISSORS);
      game.playRound(Choice.PAPER, Choice.ROCK);
      expect(game.getGameState().isComplete).toBe(true);

      // Reset and play new game
      game.reset();
      expect(game.canContinue()).toBe(true);

      const { gameState } = game.playRound(Choice.SCISSORS, Choice.PAPER);
      expect(gameState.score.playerWins).toBe(1);
      expect(gameState.rounds).toHaveLength(1);
    });
  });

  describe('Game Configuration', () => {
    test('Default configuration is correct', () => {
      const config = game.getConfig();
      expect(config.maxRounds).toBe(5);
      expect(config.winsNeeded).toBe(2);
    });

    test('Custom configuration works', () => {
      const customGame = new RockPaperScissors({
        maxRounds: 10,
        winsNeeded: 3
      });

      const config = customGame.getConfig();
      expect(config.maxRounds).toBe(10);
      expect(config.winsNeeded).toBe(3);
    });

    test('Game ends at max rounds even without clear winner', () => {
      const shortGame = new RockPaperScissors({
        maxRounds: 2,
        winsNeeded: 2
      });

      // Play 2 rounds with different winners
      shortGame.playRound(Choice.ROCK, Choice.SCISSORS); // Player wins
      const result = shortGame.playRound(Choice.SCISSORS, Choice.ROCK); // Computer wins

      expect(result.gameState.isComplete).toBe(true);
      expect(result.gameState.rounds).toHaveLength(2);
    });
  });

  describe('Game Summary', () => {
    test('Game summary calculates statistics correctly', () => {
      // Play a complete game: Player wins 2, Computer wins 1, 1 tie
      game.playRound(Choice.ROCK, Choice.SCISSORS); // Player win
      game.playRound(Choice.SCISSORS, Choice.ROCK); // Computer win
      game.playRound(Choice.PAPER, Choice.PAPER);   // Tie
      game.playRound(Choice.PAPER, Choice.ROCK);    // Player win - game ends

      const summary = game.getGameSummary();
      expect(summary.totalRounds).toBe(4);
      expect(summary.playerWinRate).toBe(50); // 2/4 = 50%
      expect(summary.computerWinRate).toBe(25); // 1/4 = 25%
      expect(summary.tieRate).toBe(25); // 1/4 = 25%
      expect(summary.winner).toBe('Player');
    });

    test('Empty game summary', () => {
      const summary = game.getGameSummary();
      expect(summary.totalRounds).toBe(0);
      expect(summary.playerWinRate).toBe(0);
      expect(summary.computerWinRate).toBe(0);
      expect(summary.tieRate).toBe(0);
      expect(summary.winner).toBe('Game in progress');
    });
  });
});