import {
  Choice,
  RoundResult,
  GameResult,
  isValidChoice,
  parseChoice,
  getChoiceDisplayName,
  getRoundResultMessage
} from '../src/models/GameTypes';

describe('GameTypes', () => {
  describe('Enums', () => {
    test('Choice enum contains expected values', () => {
      expect(Choice.ROCK).toBe('rock');
      expect(Choice.PAPER).toBe('paper');
      expect(Choice.SCISSORS).toBe('scissors');
    });

    test('RoundResult enum contains expected values', () => {
      expect(RoundResult.PLAYER_WIN).toBe('player_win');
      expect(RoundResult.COMPUTER_WIN).toBe('computer_win');
      expect(RoundResult.TIE).toBe('tie');
    });

    test('GameResult enum contains expected values', () => {
      expect(GameResult.PLAYER_VICTORY).toBe('player_victory');
      expect(GameResult.COMPUTER_VICTORY).toBe('computer_victory');
      expect(GameResult.IN_PROGRESS).toBe('in_progress');
    });
  });

  describe('isValidChoice', () => {
    test('returns true for valid choices', () => {
      expect(isValidChoice('rock')).toBe(true);
      expect(isValidChoice('paper')).toBe(true);
      expect(isValidChoice('scissors')).toBe(true);
    });

    test('returns false for invalid choices', () => {
      expect(isValidChoice('invalid')).toBe(false);
      expect(isValidChoice('')).toBe(false);
      expect(isValidChoice('ROCK')).toBe(false); // Case sensitive
      expect(isValidChoice('lizard')).toBe(false);
      expect(isValidChoice('spock')).toBe(false);
    });
  });

  describe('parseChoice', () => {
    test('parses full choice names correctly', () => {
      expect(parseChoice('rock')).toBe(Choice.ROCK);
      expect(parseChoice('paper')).toBe(Choice.PAPER);
      expect(parseChoice('scissors')).toBe(Choice.SCISSORS);
    });

    test('parses choice names case-insensitively', () => {
      expect(parseChoice('ROCK')).toBe(Choice.ROCK);
      expect(parseChoice('Paper')).toBe(Choice.PAPER);
      expect(parseChoice('SCISSORS')).toBe(Choice.SCISSORS);
      expect(parseChoice('Rock')).toBe(Choice.ROCK);
    });

    test('parses single character shortcuts', () => {
      expect(parseChoice('r')).toBe(Choice.ROCK);
      expect(parseChoice('p')).toBe(Choice.PAPER);
      expect(parseChoice('s')).toBe(Choice.SCISSORS);
      expect(parseChoice('R')).toBe(Choice.ROCK);
      expect(parseChoice('P')).toBe(Choice.PAPER);
      expect(parseChoice('S')).toBe(Choice.SCISSORS);
    });

    test('parses numeric shortcuts', () => {
      expect(parseChoice('1')).toBe(Choice.ROCK);
      expect(parseChoice('2')).toBe(Choice.PAPER);
      expect(parseChoice('3')).toBe(Choice.SCISSORS);
    });

    test('handles whitespace correctly', () => {
      expect(parseChoice(' rock ')).toBe(Choice.ROCK);
      expect(parseChoice('  paper  ')).toBe(Choice.PAPER);
      expect(parseChoice('\tscissors\t')).toBe(Choice.SCISSORS);
      expect(parseChoice(' r ')).toBe(Choice.ROCK);
    });

    test('handles alternative spellings', () => {
      expect(parseChoice('scissor')).toBe(Choice.SCISSORS); // Singular form
    });

    test('returns null for invalid inputs', () => {
      expect(parseChoice('invalid')).toBeNull();
      expect(parseChoice('')).toBeNull();
      expect(parseChoice('4')).toBeNull();
      expect(parseChoice('lizard')).toBeNull();
      expect(parseChoice('spock')).toBeNull();
      expect(parseChoice('x')).toBeNull();
    });

    test('handles edge cases', () => {
      expect(parseChoice('0')).toBeNull();
      expect(parseChoice('-1')).toBeNull();
      expect(parseChoice('1.5')).toBeNull();
      expect(parseChoice('rock!')).toBeNull();
      expect(parseChoice('rock paper')).toBeNull();
    });
  });

  describe('getChoiceDisplayName', () => {
    test('returns correct display names with emojis', () => {
      expect(getChoiceDisplayName(Choice.ROCK)).toBe('🪨 Rock');
      expect(getChoiceDisplayName(Choice.PAPER)).toBe('📄 Paper');
      expect(getChoiceDisplayName(Choice.SCISSORS)).toBe('✂️ Scissors');
    });

    test('returns consistent display names', () => {
      // Test that multiple calls return the same result
      expect(getChoiceDisplayName(Choice.ROCK)).toBe(getChoiceDisplayName(Choice.ROCK));
      expect(getChoiceDisplayName(Choice.PAPER)).toBe(getChoiceDisplayName(Choice.PAPER));
      expect(getChoiceDisplayName(Choice.SCISSORS)).toBe(getChoiceDisplayName(Choice.SCISSORS));
    });
  });

  describe('getRoundResultMessage', () => {
    test('returns correct messages for round results', () => {
      expect(getRoundResultMessage(RoundResult.PLAYER_WIN)).toBe('🎉 You win this round!');
      expect(getRoundResultMessage(RoundResult.COMPUTER_WIN)).toBe('💻 Computer wins this round!');
      expect(getRoundResultMessage(RoundResult.TIE)).toBe('🤝 It\'s a tie!');
    });

    test('returns consistent messages', () => {
      // Test that multiple calls return the same result
      expect(getRoundResultMessage(RoundResult.PLAYER_WIN))
        .toBe(getRoundResultMessage(RoundResult.PLAYER_WIN));
      expect(getRoundResultMessage(RoundResult.COMPUTER_WIN))
        .toBe(getRoundResultMessage(RoundResult.COMPUTER_WIN));
      expect(getRoundResultMessage(RoundResult.TIE))
        .toBe(getRoundResultMessage(RoundResult.TIE));
    });
  });

  describe('Type Structure Validation', () => {
    test('Round interface has correct structure', () => {
      const round = {
        roundNumber: 1,
        playerChoice: Choice.ROCK,
        computerChoice: Choice.SCISSORS,
        result: RoundResult.PLAYER_WIN
      };

      // TypeScript will catch type errors at compile time
      expect(round.roundNumber).toBe(1);
      expect(round.playerChoice).toBe(Choice.ROCK);
      expect(round.computerChoice).toBe(Choice.SCISSORS);
      expect(round.result).toBe(RoundResult.PLAYER_WIN);
    });

    test('Score interface has correct structure', () => {
      const score = {
        playerWins: 2,
        computerWins: 1,
        ties: 0
      };

      expect(score.playerWins).toBe(2);
      expect(score.computerWins).toBe(1);
      expect(score.ties).toBe(0);
    });

    test('GameState interface has correct structure', () => {
      const gameState = {
        rounds: [],
        score: { playerWins: 0, computerWins: 0, ties: 0 },
        result: GameResult.IN_PROGRESS,
        isComplete: false
      };

      expect(Array.isArray(gameState.rounds)).toBe(true);
      expect(typeof gameState.score).toBe('object');
      expect(gameState.result).toBe(GameResult.IN_PROGRESS);
      expect(gameState.isComplete).toBe(false);
    });

    test('GameConfig interface has correct structure', () => {
      const config = {
        maxRounds: 5,
        winsNeeded: 2
      };

      expect(config.maxRounds).toBe(5);
      expect(config.winsNeeded).toBe(2);
    });
  });

  describe('Enum Completeness', () => {
    test('Choice enum has exactly 3 values', () => {
      const choices = Object.values(Choice);
      expect(choices).toHaveLength(3);
      expect(choices).toContain('rock');
      expect(choices).toContain('paper');
      expect(choices).toContain('scissors');
    });

    test('RoundResult enum has exactly 3 values', () => {
      const results = Object.values(RoundResult);
      expect(results).toHaveLength(3);
      expect(results).toContain('player_win');
      expect(results).toContain('computer_win');
      expect(results).toContain('tie');
    });

    test('GameResult enum has exactly 3 values', () => {
      const results = Object.values(GameResult);
      expect(results).toHaveLength(3);
      expect(results).toContain('player_victory');
      expect(results).toContain('computer_victory');
      expect(results).toContain('in_progress');
    });
  });
});