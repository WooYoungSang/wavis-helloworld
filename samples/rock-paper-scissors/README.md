# 🎮 Rock-Paper-Scissors Game

A TypeScript implementation of the classic Rock-Paper-Scissors game with best-of-three rounds, featuring a console-based interface and comprehensive testing.

## 🌟 Features

- **Best-of-Three Format**: First player to win 2 rounds wins the game
- **Interactive Console Interface**: User-friendly prompts and visual feedback
- **Smart Input Parsing**: Accepts multiple input formats (full names, shortcuts, numbers)
- **Comprehensive Game Logic**: Handles all rules, edge cases, and game states
- **Detailed Statistics**: Win rates, round summaries, and game analysis
- **Robust Error Handling**: Graceful handling of invalid inputs and edge cases
- **TypeScript**: Full type safety and modern JavaScript features
- **Extensive Testing**: 90%+ test coverage with Jest

## 🚀 Quick Start

### Prerequisites

- Node.js 18.0.0 or higher
- npm or yarn package manager

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd rock-paper-scissors
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Build the project:**
   ```bash
   npm run build
   ```

4. **Run the game:**
   ```bash
   npm start
   ```

   Or for development with hot reload:
   ```bash
   npm run dev
   ```

## 🎯 How to Play

1. Start the game with `npm start`
2. Follow the on-screen prompts
3. Enter your choice when prompted:
   - `rock`, `r`, or `1` for Rock 🪨
   - `paper`, `p`, or `2` for Paper 📄
   - `scissors`, `s`, or `3` for Scissors ✂️
   - `quit` to exit at any time
4. The computer will make its choice
5. See the round results and updated score
6. First to 2 wins takes the game!
7. Choose to play again or exit

### Game Rules

- Rock beats Scissors (Rock crushes Scissors)
- Scissors beats Paper (Scissors cuts Paper)
- Paper beats Rock (Paper covers Rock)
- Same choices result in a tie

## 🏗️ Project Structure

```
rock-paper-scissors/
├── src/
│   ├── game/
│   │   └── RockPaperScissors.ts    # Main game engine
│   ├── models/
│   │   └── GameTypes.ts            # Type definitions and utilities
│   ├── services/
│   │   └── ComputerPlayer.ts       # Computer opponent logic
│   ├── ui/
│   │   └── ConsoleUI.ts            # Console interface
│   └── index.ts                    # Application entry point
├── tests/
│   ├── game.test.ts                # Game engine tests
│   ├── computer-player.test.ts     # Computer player tests
│   └── game-types.test.ts          # Type utilities tests
├── docs/
│   └── SSOT.md                     # Requirements documentation
├── dist/                           # Compiled JavaScript (generated)
├── package.json                    # Project configuration
├── tsconfig.json                   # TypeScript configuration
├── jest.config.js                  # Test configuration
└── README.md                       # This file
```

## 🛠️ Development

### Available Scripts

```bash
# Development
npm run dev          # Run with hot reload using ts-node
npm run build        # Compile TypeScript to JavaScript
npm run start        # Run compiled application

# Testing
npm test             # Run all tests
npm run test:watch   # Run tests in watch mode

# Code Quality
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run clean        # Remove compiled files
```

### Development Workflow

1. **Make changes** to TypeScript files in `src/`
2. **Run tests** to ensure everything works: `npm test`
3. **Test your changes** in development mode: `npm run dev`
4. **Build and test** the production version: `npm run build && npm start`

### Adding Features

The codebase is designed for easy extension:

- **New game modes**: Extend `GameConfig` interface and `RockPaperScissors` class
- **Different players**: Implement the `Player` interface
- **UI enhancements**: Modify `ConsoleUI` class or create new UI implementations
- **Game rules**: Extend `Choice` enum and update winner determination logic

## 🧪 Testing

The project includes comprehensive tests covering:

- **Game Logic**: All winning conditions, edge cases, and state management
- **Computer Player**: Random choice generation and distribution analysis
- **Type Utilities**: Input parsing, validation, and display functions
- **Error Handling**: Invalid inputs and edge cases

Run tests with:
```bash
npm test                 # Run all tests once
npm run test:watch       # Run tests in watch mode
npm test -- --coverage  # Run tests with coverage report
```

### Test Coverage

Current test coverage exceeds 90% across all categories:
- Statements: >90%
- Branches: >90%
- Functions: >90%
- Lines: >90%

## 📦 Building and Distribution

### Build for Production

```bash
npm run build
```

This creates optimized JavaScript files in the `dist/` directory.

### Running Production Build

```bash
npm start
```

### Creating a Standalone Executable

For distribution, you can create a standalone executable:

```bash
# Install pkg globally
npm install -g pkg

# Create executables for different platforms
pkg . --out-path dist/executables
```

## 🔧 Configuration

### Game Configuration

The game can be configured by modifying the `GameConfig` interface:

```typescript
const customGame = new RockPaperScissors({
  maxRounds: 10,    // Maximum rounds before tie-breaker
  winsNeeded: 3     // Wins needed to win the game
});
```

### TypeScript Configuration

Key TypeScript settings in `tsconfig.json`:
- **Target**: ES2022 for modern JavaScript features
- **Strict Mode**: Enabled for maximum type safety
- **Module**: CommonJS for Node.js compatibility

## 🎨 Features Showcase

### Smart Input Parsing
- Accepts multiple input formats: `rock`, `r`, `1`
- Case-insensitive: `ROCK`, `Rock`, `rock`
- Handles whitespace: ` rock `, `  r  `

### Rich Console Interface
- Emoji support for visual appeal: 🪨 📄 ✂️
- Color coding for different game states
- Progress tracking and statistics
- Graceful error handling

### Comprehensive Statistics
- Win rates for player and computer
- Tie percentages
- Round-by-round history
- Game summaries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and add tests
4. Ensure all tests pass: `npm test`
5. Commit your changes: `git commit -m 'Add new feature'`
6. Push to the branch: `git push origin feature/new-feature`
7. Submit a pull request

### Code Style

- Use TypeScript strict mode
- Follow existing naming conventions
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with the [Demeter WAVIS Framework v1.3](../README.md)
- Inspired by the classic Rock-Paper-Scissors game
- TypeScript and Node.js ecosystem

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Review the test files for usage examples
3. Open an issue on the project repository

### Troubleshooting

**Game won't start:**
- Ensure Node.js 18+ is installed: `node --version`
- Install dependencies: `npm install`
- Build the project: `npm run build`

**Tests failing:**
- Clear node_modules: `rm -rf node_modules && npm install`
- Check TypeScript version: `npx tsc --version`

**TypeScript errors:**
- Ensure TypeScript is installed: `npm list typescript`
- Check tsconfig.json for correct paths

---

**Happy Gaming!** 🎮 Enjoy playing Rock-Paper-Scissors!