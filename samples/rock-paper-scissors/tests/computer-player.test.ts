import { ComputerPlayer } from '../src/services/ComputerPlayer';
import { Choice } from '../src/models/GameTypes';

describe('ComputerPlayer', () => {
  let computerPlayer: ComputerPlayer;

  beforeEach(() => {
    computerPlayer = new ComputerPlayer();
  });

  describe('Choice Generation', () => {
    test('getChoice returns a valid choice', () => {
      const choice = computerPlayer.getChoice();
      expect(Object.values(Choice)).toContain(choice);
    });

    test('getChoice returns different values over multiple calls', () => {
      const choices = new Set<Choice>();

      // Generate 100 choices to increase probability of getting all three options
      for (let i = 0; i < 100; i++) {
        choices.add(computerPlayer.getChoice());
      }

      // We should get at least 2 different choices in 100 attempts
      expect(choices.size).toBeGreaterThanOrEqual(2);
    });

    test('getPossibleChoices returns all valid choices', () => {
      const possibleChoices = computerPlayer.getPossibleChoices();
      const expectedChoices = Object.values(Choice);

      expect(possibleChoices).toHaveLength(expectedChoices.length);
      expectedChoices.forEach(choice => {
        expect(possibleChoices).toContain(choice);
      });
    });
  });

  describe('Multiple Choice Generation', () => {
    test('generateChoices returns correct number of choices', () => {
      const count = 10;
      const choices = computerPlayer.generateChoices(count);

      expect(choices).toHaveLength(count);
      choices.forEach(choice => {
        expect(Object.values(Choice)).toContain(choice);
      });
    });

    test('generateChoices with zero count returns empty array', () => {
      const choices = computerPlayer.generateChoices(0);
      expect(choices).toHaveLength(0);
    });

    test('generateChoices with large count works correctly', () => {
      const count = 1000;
      const choices = computerPlayer.generateChoices(count);

      expect(choices).toHaveLength(count);

      // Check that all choices are valid
      choices.forEach(choice => {
        expect(Object.values(Choice)).toContain(choice);
      });
    });
  });

  describe('Distribution Analysis', () => {
    test('analyzeDistribution calculates correct counts', () => {
      const choices = [
        Choice.ROCK, Choice.ROCK,
        Choice.PAPER, Choice.PAPER, Choice.PAPER,
        Choice.SCISSORS
      ];

      const analysis = ComputerPlayer.analyzeDistribution(choices);

      expect(analysis.total).toBe(6);
      expect(analysis.counts[Choice.ROCK]).toBe(2);
      expect(analysis.counts[Choice.PAPER]).toBe(3);
      expect(analysis.counts[Choice.SCISSORS]).toBe(1);
    });

    test('analyzeDistribution calculates correct percentages', () => {
      const choices = [
        Choice.ROCK, Choice.ROCK, Choice.ROCK, Choice.ROCK, // 4 rocks
        Choice.PAPER, Choice.PAPER,                         // 2 papers
        Choice.SCISSORS, Choice.SCISSORS, Choice.SCISSORS, Choice.SCISSORS // 4 scissors
      ]; // Total: 10

      const analysis = ComputerPlayer.analyzeDistribution(choices);

      expect(analysis.percentages[Choice.ROCK]).toBe(40);
      expect(analysis.percentages[Choice.PAPER]).toBe(20);
      expect(analysis.percentages[Choice.SCISSORS]).toBe(40);
    });

    test('analyzeDistribution handles empty array', () => {
      const choices: Choice[] = [];
      const analysis = ComputerPlayer.analyzeDistribution(choices);

      expect(analysis.total).toBe(0);
      expect(analysis.counts[Choice.ROCK]).toBe(0);
      expect(analysis.counts[Choice.PAPER]).toBe(0);
      expect(analysis.counts[Choice.SCISSORS]).toBe(0);
      expect(analysis.percentages[Choice.ROCK]).toBe(0);
      expect(analysis.percentages[Choice.PAPER]).toBe(0);
      expect(analysis.percentages[Choice.SCISSORS]).toBe(0);
    });

    test('analyzeDistribution with single choice', () => {
      const choices = [Choice.ROCK];
      const analysis = ComputerPlayer.analyzeDistribution(choices);

      expect(analysis.total).toBe(1);
      expect(analysis.counts[Choice.ROCK]).toBe(1);
      expect(analysis.counts[Choice.PAPER]).toBe(0);
      expect(analysis.counts[Choice.SCISSORS]).toBe(0);
      expect(analysis.percentages[Choice.ROCK]).toBe(100);
      expect(analysis.percentages[Choice.PAPER]).toBe(0);
      expect(analysis.percentages[Choice.SCISSORS]).toBe(0);
    });
  });

  describe('Randomness Quality', () => {
    test('distribution is reasonably fair over many choices', () => {
      const sampleSize = 3000; // Large sample for statistical significance
      const choices = computerPlayer.generateChoices(sampleSize);
      const analysis = ComputerPlayer.analyzeDistribution(choices);

      // Each choice should appear roughly 33.33% of the time
      // Allow for 5% deviation (28.33% - 38.33% range)
      const expectedPercentage = 100 / 3; // 33.33%
      const tolerance = 5; // 5% tolerance

      Object.values(Choice).forEach(choice => {
        const percentage = analysis.percentages[choice];
        expect(percentage).toBeGreaterThan(expectedPercentage - tolerance);
        expect(percentage).toBeLessThan(expectedPercentage + tolerance);
      });

      // Total should add up to sample size
      expect(analysis.total).toBe(sampleSize);

      // All counts should add up to total
      const totalCounts = analysis.counts[Choice.ROCK] +
                         analysis.counts[Choice.PAPER] +
                         analysis.counts[Choice.SCISSORS];
      expect(totalCounts).toBe(sampleSize);
    });

    test('consecutive choices can be different', () => {
      // This tests that the RNG can produce different consecutive values
      // It's not a guarantee, but over multiple attempts it should happen
      let foundDifferentConsecutive = false;

      for (let attempt = 0; attempt < 50; attempt++) {
        const choice1 = computerPlayer.getChoice();
        const choice2 = computerPlayer.getChoice();

        if (choice1 !== choice2) {
          foundDifferentConsecutive = true;
          break;
        }
      }

      expect(foundDifferentConsecutive).toBe(true);
    });

    test('choices show reasonable variability', () => {
      const choices = computerPlayer.generateChoices(100);
      const uniqueChoices = new Set(choices);

      // Over 100 choices, we should see all 3 options
      // This test might rarely fail due to randomness, but it's statistically very unlikely
      expect(uniqueChoices.size).toBe(3);
    });
  });

  describe('Interface Compliance', () => {
    test('implements Player interface correctly', () => {
      // This test ensures the computer player can be used as a Player
      const choice = computerPlayer.getChoice();
      expect(typeof choice).toBe('string');
      expect(Object.values(Choice)).toContain(choice);
    });

    test('getChoice method is synchronous', () => {
      const choice = computerPlayer.getChoice();
      expect(choice).toBeDefined();
      expect(typeof choice).toBe('string');
    });
  });
});