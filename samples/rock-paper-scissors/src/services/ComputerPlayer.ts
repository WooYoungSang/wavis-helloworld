import { Choice, Player } from '../models/GameTypes';

/**
 * Computer player implementation with random choice generation
 */
export class ComputerPlayer implements Player {
  private readonly choices: ReadonlyArray<Choice>;

  constructor() {
    this.choices = Object.values(Choice);
  }

  /**
   * Generate a random choice for the computer player
   * @returns A randomly selected Choice
   */
  getChoice(): Choice {
    const randomIndex = Math.floor(Math.random() * this.choices.length);
    return this.choices[randomIndex]!;
  }

  /**
   * Get all possible choices (mainly for testing)
   * @returns Array of all possible choices
   */
  getPossibleChoices(): ReadonlyArray<Choice> {
    return this.choices;
  }

  /**
   * Generate multiple choices for testing distribution
   * @param count Number of choices to generate
   * @returns Array of randomly generated choices
   */
  generateChoices(count: number): Choice[] {
    const results: Choice[] = [];
    for (let i = 0; i < count; i++) {
      results.push(this.getChoice());
    }
    return results;
  }

  /**
   * Calculate choice distribution from an array of choices
   * @param choices Array of choices to analyze
   * @returns Object with choice counts and percentages
   */
  static analyzeDistribution(choices: Choice[]): {
    counts: Record<Choice, number>;
    percentages: Record<Choice, number>;
    total: number;
  } {
    const counts: Record<Choice, number> = {
      [Choice.ROCK]: 0,
      [Choice.PAPER]: 0,
      [Choice.SCISSORS]: 0
    };

    // Count occurrences
    for (const choice of choices) {
      counts[choice]++;
    }

    // Calculate percentages
    const total = choices.length;
    const percentages: Record<Choice, number> = {
      [Choice.ROCK]: total > 0 ? (counts[Choice.ROCK] / total) * 100 : 0,
      [Choice.PAPER]: total > 0 ? (counts[Choice.PAPER] / total) * 100 : 0,
      [Choice.SCISSORS]: total > 0 ? (counts[Choice.SCISSORS] / total) * 100 : 0
    };

    return { counts, percentages, total };
  }
}