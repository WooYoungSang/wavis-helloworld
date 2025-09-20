# Page snapshot

```yaml
- generic [ref=e1]:
  - banner [ref=e2]:
    - heading "Don't Press Button" [level=1] [ref=e3]
  - main [ref=e4]:
    - generic [ref=e5]: 돌이킬 수 없어요!
    - button "Don't Press Button - Main interaction button" [ref=e6] [cursor=pointer]: Don't Press Button
  - dialog "Would you like to proceed with payment?" [ref=e7]:
    - generic [ref=e8]:
      - heading "Would you like to proceed with payment?" [level=2] [ref=e9]
      - generic [ref=e10]:
        - button "Yes" [active] [ref=e11] [cursor=pointer]
        - button "No" [ref=e12] [cursor=pointer]
```