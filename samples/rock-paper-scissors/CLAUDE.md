# CLAUDE.md - AI Development Guidelines

## Project Overview

This is a TypeScript implementation of a Rock-Paper-Scissors game following the Demeter WAVIS Framework v1.3. The project demonstrates modern TypeScript development practices with comprehensive testing, type safety, and clean architecture.

## 🎯 Project Context

**Game Description**: Console-based Rock-Paper-Scissors game with best-of-three rounds
**Technology Stack**: TypeScript, Node.js, Jest
**Architecture Pattern**: Layered architecture with clear separation of concerns
**Framework**: Demeter WAVIS v1.3

## 🏗️ Architecture Overview

### Layer Structure
```
Presentation Layer:    ConsoleUI
Application Layer:     RockPaperScissorsApp (index.ts)
Business Logic Layer:  RockPaperScissors, ComputerPlayer
Domain Model Layer:    GameTypes (interfaces, enums, utilities)
```

### Key Design Patterns
- **Interface Segregation**: Player interface for different player types
- **Immutable State**: Readonly interfaces and defensive copying
- **Command Pattern**: Round-based game progression
- **Strategy Pattern**: Different player implementations (Human, Computer)

## 📁 Code Organization

### Directory Structure
- `src/models/`: Type definitions, interfaces, enums
- `src/game/`: Core game logic and state management
- `src/services/`: Business services (Computer player)
- `src/ui/`: User interface implementations
- `tests/`: Comprehensive test suites

### Naming Conventions
- **Classes**: PascalCase (e.g., `RockPaperScissors`, `ComputerPlayer`)
- **Interfaces**: PascalCase (e.g., `Player`, `GameState`)
- **Enums**: PascalCase with UPPER_CASE values (e.g., `Choice.ROCK`)
- **Methods**: camelCase (e.g., `playRound`, `getGameState`)
- **Files**: kebab-case for multi-word files (e.g., `computer-player.test.ts`)

## 🔧 Development Guidelines

### TypeScript Best Practices

1. **Strict Type Safety**
   ```typescript
   // Use strict TypeScript configuration
   "strict": true,
   "noImplicitAny": true,
   "noImplicitReturns": true
   ```

2. **Immutable Data Structures**
   ```typescript
   // Use readonly for interface properties
   interface GameState {
     readonly rounds: ReadonlyArray<Round>;
     readonly score: Score;
   }
   ```

3. **Type Guards and Validation**
   ```typescript
   // Implement type guards for runtime validation
   export function isValidChoice(choice: string): choice is Choice {
     return Object.values(Choice).includes(choice as Choice);
   }
   ```

4. **Enum Usage**
   ```typescript
   // Use string enums for better debugging
   export enum Choice {
     ROCK = 'rock',
     PAPER = 'paper',
     SCISSORS = 'scissors'
   }
   ```

### Code Quality Standards

1. **Single Responsibility**: Each class has one clear purpose
2. **Open/Closed Principle**: Extensible without modification
3. **Dependency Inversion**: Depend on abstractions (Player interface)
4. **Error Handling**: Comprehensive error handling with meaningful messages

### Testing Strategy

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **Coverage Requirements**: Maintain >90% test coverage
4. **Test Organization**: Mirror source directory structure in tests

## 🚀 Development Workflow

### Adding New Features

1. **Define Types First**
   ```typescript
   // Add new interfaces/enums to GameTypes.ts
   export interface NewFeature {
     readonly property: string;
   }
   ```

2. **Implement Core Logic**
   ```typescript
   // Add business logic with proper error handling
   public newMethod(): Result {
     if (!this.isValid()) {
       throw new Error('Invalid state for operation');
     }
     return this.processLogic();
   }
   ```

3. **Write Tests**
   ```typescript
   // Comprehensive test coverage
   describe('NewFeature', () => {
     test('handles normal case', () => {
       // Test implementation
     });

     test('handles edge cases', () => {
       // Test edge cases
     });
   });
   ```

4. **Update Documentation**
   - Update SSOT.md if requirements change
   - Update README.md for user-facing changes
   - Add inline documentation for complex logic

### Code Review Checklist

- [ ] Type safety: No `any` types without justification
- [ ] Error handling: All error paths covered
- [ ] Testing: New code has corresponding tests
- [ ] Performance: No obvious performance issues
- [ ] Immutability: State changes are handled correctly
- [ ] Documentation: Complex logic is documented

## 🧪 Testing Guidelines

### Test Structure
```typescript
describe('ComponentName', () => {
  describe('FeatureGroup', () => {
    test('specific behavior description', () => {
      // Arrange
      const input = setupTestData();

      // Act
      const result = componentUnderTest.method(input);

      // Assert
      expect(result).toBe(expectedValue);
    });
  });
});
```

### Test Categories
1. **Happy Path Tests**: Normal operation scenarios
2. **Edge Case Tests**: Boundary conditions and limits
3. **Error Handling Tests**: Invalid inputs and error states
4. **Integration Tests**: Component interactions

### Mock Usage
- Mock external dependencies (filesystem, network)
- Use real implementations for domain logic
- Mock UI interactions for automated testing

## 📊 Performance Considerations

### Memory Management
- Use readonly arrays to prevent accidental mutations
- Implement defensive copying for state changes
- Clear resources in UI components

### Scalability
- Game logic supports configurable rules
- Interface-based design allows for different implementations
- Modular architecture supports feature additions

## 🔒 Security Considerations

### Input Validation
```typescript
// Always validate user input
const choice = parseChoice(userInput);
if (choice === null) {
  throw new Error('Invalid choice provided');
}
```

### Error Information
- Don't expose internal state in error messages
- Provide helpful user-facing error messages
- Log technical details separately from user messages

## 🐛 Debugging Guidelines

### Common Issues
1. **Type Errors**: Check interface implementations
2. **State Mutations**: Verify immutability patterns
3. **Test Failures**: Check for async/await issues
4. **Build Errors**: Verify import/export statements

### Debugging Tools
- Use TypeScript strict mode for compile-time checks
- Leverage Jest's debugging features for tests
- Use console.log strategically (remove before commit)

## 🔄 Maintenance

### Dependency Management
- Keep dependencies up to date
- Regular security audits with `npm audit`
- Pin major versions for stability

### Code Refactoring
- Refactor when adding three similar features
- Extract common patterns into utilities
- Maintain backward compatibility for public APIs

## 📈 Future Enhancements

### Potential Features
1. **Multiple Game Modes**: Rock-Paper-Scissors-Lizard-Spock
2. **AI Players**: Different difficulty levels
3. **Game History**: Persistent game statistics
4. **Multiplayer**: Network-based multiplayer support
5. **Web Interface**: Browser-based UI

### Architecture Extensions
- Plugin system for game rules
- Event-driven architecture for game events
- Configuration management for different game modes

## 🤖 AI Assistant Guidelines

When working with this codebase:

1. **Maintain Type Safety**: Always use proper TypeScript types
2. **Follow Patterns**: Use existing architectural patterns
3. **Test Coverage**: Add tests for new functionality
4. **Documentation**: Update relevant documentation
5. **Error Handling**: Handle edge cases appropriately

### Common Tasks
- Adding new game rules: Extend Choice enum and update logic
- New player types: Implement Player interface
- UI improvements: Modify ConsoleUI class methods
- Testing: Follow existing test patterns and coverage requirements

---

This document serves as a comprehensive guide for AI assistants and developers working on this Rock-Paper-Scissors project within the Demeter WAVIS Framework v1.3.