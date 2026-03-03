# COBOL Blackjack — A Legacy Modernization Playground

Ever wanted to practice modernizing a legacy system but had no legacy system to work with? This is that project.

COBOL Blackjack is a small, deliberately imperfect, multi-file COBOL application — a fully playable Blackjack game written in authentic 1980s mainframe style. It's got everything a real legacy codebase has: cryptic variable names, GOTO-driven control flow, dead code, orphaned features, foreign-language comments from contract teams long gone, and nine embedded bugs that have survived undetected across decades of fictional maintenance cycles.

The scope is intentionally small. You can read the entire codebase in an afternoon, understand what it does, and start modernizing it without a team or a budget or six months of onboarding. It's a safe, contained environment to try out modernization approaches — whether that's refactoring in place, rewriting in a modern language, applying AI-assisted code transformation, or just practicing the discipline of understanding code you didn't write.

Blackjack is the right domain for this. The rules are universal, so you can verify correctness without being a COBOL expert. If the game plays right after your changes, you're probably on track.

> **Note:** This code contains intentional defects and anti-patterns. They are listed in full below. A developer who "fixes" them without meaning to is breaking a feature — read the bug list before you start.

---

## Demo

<video src="https://github.com/user-attachments/assets/d6d193c8-a927-4b40-9c35-f2664fa2709a" controls title="COBOL Blackjack gameplay demo"></video>

---

## Running the Game

**Requirements:** GnuCOBOL 3.1+ and GCC on Ubuntu 20.04 or later.

```bash
# Check prerequisites
cobc --version   # GnuCOBOL 3.1+ required
gcc --version

# Clone and run — one command builds and launches
./build.sh
```

The build script compiles all modules and launches the game automatically. There is no separate run step. Compile warnings from `FORTIFY_SOURCE` are expected — the build is clean on exit code 0.

**Gameplay:** You start with 100 chips. Place a bet, then choose:
- `H` — Hit (take a card)
- `S` — Stand (end your turn)
- `D` — Double down (double your bet, take one card, auto-stand)

The dealer plays by standard casino rules. Win pays 1:1, natural blackjack pays 3:2, push returns your bet. The session ends when you run out of chips or choose to quit.

---

## Deliberate Bugs

These 9 defects are **intentional**. Each is independently verifiable and designed to be pointable during a live demo. They represent the kind of embedded business logic errors that survive for decades in real legacy systems.

| # | Bug | File | Paragraph | What it does |
|---|-----|------|-----------|--------------|
| 1 | **Biased shuffle** | `src/BJACK-DECK.COB` | `LOOP-B` | Calls `LEGACY-RANDOM-GEN` each iteration, which always returns 7. Every card in the deck gets swapped with position 7. The deck order is identical every run. |
| 2 | **Dead code paragraph** | `src/BJACK-DECK.COB` | `DEAD-1` | A paragraph named "DECK REBALANCE SUBROUTINE" sits immediately after a `GOBACK` statement. It has never executed. It rebalances nothing. |
| 3 | **Off-by-one in deal array** | `src/BJACK-DEAL.COB` | `CALC-3` | A hit card is stored at position `WS-PC` before the count increments. The correct slot is `WS-PC + 1`. The hit card silently overwrites the last dealt card in memory. |
| 4 | **Ace recalculation failure** | `src/BJACK-SCORE.COB` | `CALC-2` | When two Aces are held, the adjust loop reduces only the first Ace from 11 to 1. The second stays at 11. A two-Ace hand scores 12 instead of 2. |
| 5 | **Soft 17 rule violation** | `src/BJACK-DEALER.COB` | `LOOP-A` | The dealer hit/stand logic does not correctly handle a soft 17 (Ace counted as 11 plus six). Standard casino rules require the dealer to hit on soft 17. This deviates. |
| 6 | **No input validation** | `src/BJACK-MAIN.COB` | `LOOP-A` | The hit/stand prompt checks only `S` and `D`. Everything else — including garbage input — triggers a hit. Entering `X`, a space, or nothing at all takes a card. |
| 7 | **Payout rounding error** | `src/BJACK-MAIN.COB` | `PROC-NB` | Natural blackjack pays 3:2 using integer division. A bet of 5 returns 7 instead of 7.5. Players are silently shortchanged half a chip on every odd-bet blackjack. |
| 8 | **Double-down anytime** | `src/BJACK-MAIN.COB` | `LOOP-A` | The double-down option is offered at every action prompt, not just on the initial two-card hand. There is no check for card count before allowing `D`. |
| 9 | **Bet over balance** | `src/BJACK-MAIN.COB` | `BET-1` | Bet validation checks `WS-BL`, a variable frozen at session start and never updated after payouts. After losing chips, the player can still bet up to the original starting amount. |

---

## Anti-Patterns and Technical Debt

Beyond the bugs, every source file was written to accumulate the kind of structural debt that characterises real legacy systems — code that was once maintained by multiple teams across multiple years, with features abandoned mid-implementation, patches applied under pressure, and tribal knowledge that left with the people who wrote it.

### Orphaned Feature Code

Several features were partially implemented and then withdrawn, leaving dead paragraphs in the codebase. They compile and do nothing.

- **Split hand** (`PROC-SP` in `BJACK-MAIN.COB`, `PROC-DS` in `BJACK-DEAL.COB`, `CALC-8/8A/8X` in `BJACK-DISPL.COB`) — partially built in 1987, withdrawn before release
- **Five-card Charlie bonus** (`PROC-CB` in `BJACK-SCORE.COB`) — a Nevada rule variant disabled in 1988 per casino contract change, preserved "for potential reactivation"
- **Insurance logic** (`PROC-INS` in `BJACK-DEALER.COB`) — disabled 1988, payout table never configured
- **Original random number generator** (`PROC-R1` in `LEGACY-RANDOM-GEN.COB`) — replaced by a hardcoded return value per Defect 0042, preserved for audit trail

### Ghost Variables

Fields declared in working storage that are never read or written anywhere in the procedure division. The compiler allocates the memory. Nothing ever uses it.

- `WS-X2` in `BJACK-DEAL.COB`
- `WS-CB` in `BJACK-SCORE.COB`
- Ghost field groups in `WS-HANDS.cpy` and `WS-GAME.cpy`

### No-Op Patch Statements

Statements that execute and produce no observable effect — residue from emergency patches applied between 1988 and 1989. A comment in `BJACK-DEALER.COB` warns: "DO NOT REMOVE — REQUIRED FOR INITIALIZATION SEQUENCE STABILITY." This is incorrect. They are inert.

### Contradictory Version Headers

At least four module headers carry `WRITTEN` and `UPDATED` date comments that conflict with each other or with the actual implementation sequence — consistent with code copied from other systems and edited without updating the header.

### Foreign-Language Comments

Six comments across the codebase are written in French or German, referencing plausible-sounding internal defect reports, terminal compatibility patches, and regulatory compliance notes. These were added by contract teams between 1987 and 1989.

- **French:** `BJACK-SCORE.COB`, `BJACK-DISPL.COB`, `LEGACY-RANDOM-GEN.COB`
- **German:** `BJACK-DEAL.COB`, `BJACK-DEALER.COB`, `CASINO-AUDIT-LOG.COB`

---

## Source Files

| File | Purpose |
|------|---------|
| `src/BJACK-MAIN.COB` | Main game loop and control logic |
| `src/BJACK-DECK.COB` | Deck initialisation and shuffle |
| `src/BJACK-DEAL.COB` | Card dealing to player and dealer |
| `src/BJACK-SCORE.COB` | Hand value calculation and Ace adjustment |
| `src/BJACK-DEALER.COB` | Dealer automated turn logic |
| `src/BJACK-DISPL.COB` | Terminal display and rendering |
| `src/LEGACY-RANDOM-GEN.COB` | Random number stub (returns 7) |
| `src/CASINO-AUDIT-LOG.COB` | Audit log stub (does nothing) |
| `copy/` | Copybooks — shared data structures |
