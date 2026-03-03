---
stepsCompleted: [step-01-init, step-02-discovery, step-02b-vision, step-02c-executive-summary, step-03-success, step-04-journeys, step-05-domain, step-06-innovation, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish, step-12-complete, step-e-01-discovery, step-e-02-review, step-e-03-edit]
workflowStatus: complete
inputDocuments:
  - docs/planning-artifacts/product-brief-cobol-blackjack-2026-02-26.md
documentCounts:
  briefs: 1
  research: 0
  brainstorming: 0
  projectDocs: 0
workflowType: 'prd'
classification:
  projectType: cli_tool
  domain: general
  complexity: low
  projectContext: greenfield
  notes: Mainframe terminal simulation running on GnuCOBOL/Ubuntu. Terminal experience must feel authentically mainframe to non-technical leaders who have never seen a mainframe.
lastEdited: '2026-02-28'
editHistory:
  - date: '2026-02-27'
    changes: 'Added betting system, natural blackjack, double down FRs; 3 new deliberate defects; updated journeys, scope, success criteria for richer business logic'
  - date: '2026-02-28'
    changes: 'Added FR47-FR52 (Accumulated Debt Patterns): orphaned feature code, ghost copybook fields, ghost local variables, no-op operations, contradictory version headers, foreign-language comments. Added NFR9 (Accumulated Debt Patterns). Sprint Change Proposal 2026-02-28 approved by Kamal.'
---

# Product Requirements Document - cobol-blackjack

**Author:** Kamal
**Date:** 2026-02-26

## Executive Summary

cobol-blackjack is a legacy demo asset — a deliberately imperfect, multi-file COBOL Blackjack application running on a GnuCOBOL/Ubuntu mainframe sandbox. It is the "before" in a live before-and-after modernization showcase, built for a single user: Kamal, as demo presenter. The target audience is tech leaders and decision-makers who have never seen a mainframe — people who cannot connect with slide decks but need to viscerally understand what legacy systems look like, feel like, and why they need to change.

The problem is not technical — it is a sales and perception gap. Decision-makers delay or avoid modernization commitments because they cannot picture what is actually at stake. Abstract pitches do not create urgency. A live, running Blackjack game on a mainframe terminal — complete with betting, chip management, and payout logic tangled in GOTO spaghetti — does.

### What Makes This Special

Blackjack is a universal shortcut. Every leader in the room already knows the rules — they don't need to understand COBOL to follow the game. That familiarity eliminates the cognitive barrier between the audience and the demo. What they see is a terminal-based game running on what looks and feels like a real mainframe. What they are actually seeing is authentic 1980s-era code: cryptic naming, spaghetti logic, no structure, deliberate bugs, and decades of accumulated debt. The moment the modernized version is shown alongside it, the transformation is self-evident — no explanation required.

The core insight: **you can't sell what people can't picture.** This demo makes legacy reality tangible for any audience in minutes. The betting system adds the critical layer decision-makers recognize instantly: business rules buried in unmaintainable code — the exact pattern that blocks every real-world modernization.

**Project Type:** CLI / Mainframe Terminal Application | **Domain:** Tech Demo / Sales Enablement | **Complexity:** Low | **Context:** Greenfield

## Success Criteria

### User Success

Kamal can walk into a client meeting, launch the application with a single command, and run a complete Blackjack game — place bets, hit, stand, double down, see payouts — from start to finish without crashes, errors, or unexpected behavior. The terminal layout reads as authentically 1980s-era mainframe to an audience that has never seen one — the visual presentation alone signals "this is old." During the demo, Kamal can point to 6–8 distinct, visible examples of messiness in the codebase (cryptic names, spaghetti logic, dead code, deliberate bugs, tangled business rules) without preparation.

### Business Success

Decision-makers who watch the demo leave the room understanding — viscerally, not abstractly — what a legacy mainframe system looks like and why modernization matters. The application anchors the modernization pitch as the credible "before," enabling the contrast with the modernized version to land without explanation.

### Technical Success

- Application compiles with zero errors on GnuCOBOL 3.1+ on Ubuntu
- Full game round (bet, deal, hit/stand/double-down, dealer turn, payout, outcome, play-again) completes without abnormal termination under all normal input paths
- All 9 deliberate bugs implemented and independently verifiable through targeted testing
- Launch-to-first-prompt under 5 seconds from single command
- Every source file contains authentic, identifiable technical debt
- Terminal visual presentation reads as 1980s mainframe to an untrained eye
- Minimum 6 distinct code messiness examples demonstrable without COBOL expertise
- Betting and payout business logic is demonstrably entangled with game flow — not cleanly separated

## Product Scope

### MVP — Minimum Viable Product

Complete delivery. No viable partial version exists — a game that crashes or looks polished defeats the purpose.

**Must-Have Capabilities:**
- Multi-file COBOL Blackjack application (8–14 source files) compiling on GnuCOBOL 3.1+/Ubuntu
- Full game loop: bet, deal, hit/stand/double-down, dealer turn, payout, outcome, play-again
- Betting system: chip balance (starting at 100), bet placement with min/max, payout calculations (1:1 win, 3:2 natural blackjack, push returns bet)
- Natural blackjack detection: Ace + 10-value card on initial deal pays 3:2
- Double down: player doubles bet and receives exactly one card, then auto-stands
- Session persistence: chip balance carries across rounds, session ends at zero chips or player quit
- Authentic 1980s-era code style distributed across all files (cryptic naming, GOTO statements, no EVALUATE, sparse/incorrect comments, dead code)
- All 9 deliberate bugs implemented and verifiable
- Two proprietary middleware stubs (CASINO-AUDIT-LOG, LEGACY-RANDOM-GEN) compiling cleanly
- ASCII card display with chip balance and bet amount rendering in 80-column standard terminal
- Single `build.sh` script compiling and launching in one command
- README with compile/run instructions and known bugs list

**Resource Requirements:** Single developer with COBOL knowledge and GnuCOBOL/Ubuntu environment access.

### Phase 2 — Post-MVP

- Demo walkthrough guide (which bugs to highlight, which code sections to show, suggested narration)
- Side-by-side presentation materials pairing legacy with modernized version

### Phase 3 — Future Vision

- Modernized Java "after" application (separate project)
- Additional legacy application examples beyond Blackjack
- Documented modernization methodology

**Risk:** Terminal rendering consistency across machines — mitigated by targeting 80-column standard terminal only, no color dependency. Fallback: single-file COBOL Blackjack with basic tech debt is minimally viable for demo purposes.

## User Journeys

### Journey 1: Build and Verify (Kamal — Setup)

Kamal clones the repository onto a fresh Ubuntu machine. He runs the single build command. GnuCOBOL compiles all source files without errors. He launches the game, places a bet, plays a full round — deal, hit, stand, double down, dealer turn, payout, play again — and everything runs cleanly. He verifies chip balance updates correctly across rounds. He walks the codebase, confirming all 9 deliberate bugs are present and locatable, including the payout calculation error and the double-down rule violation. The terminal layout looks right: the card display, chip count, and bet prompts feel period-accurate, and nothing in the visual presentation breaks the 1980s mainframe illusion. The environment is ready to demo.

### Journey 2: Demo Day — Happy Path (Kamal — Presenting)

Kamal opens a terminal in front of a room of tech leaders. He types the launch command. The game appears in under 5 seconds — a text-based card table with chip balance, bet prompts, and ASCII card art, exactly what a mainframe terminal looked like in 1983. He places a bet, plays a round, doubles down on a good hand, watches the payout calculate. Then he pivots to the code: he pulls up 6–8 moments of deliberate messiness — a paragraph named PROC-A, a variable called WS-X1, a GOTO jump that goes nowhere obvious, a payout calculation buried in nested IFs three levels deep, a stub that silently does nothing. He points to the betting logic: "This is how business rules get trapped in legacy code. This is what your team is trying to extract." The room doesn't need to understand COBOL. They see chaos and they get it. The contrast with the modernized version, shown next, lands without a word of explanation.

### Journey 3: Demo Day — Edge Case (Kamal — Recovery)

Mid-demo, a leader asks Kamal to try something unexpected — enter a non-standard value at the hit/stand prompt, bet more chips than he has, or double down after already hitting. The no-input-validation bug means the game may behave oddly; the bet-over-balance bug lets the wager through; the double-down-anytime bug accepts it. Kamal uses each deliberately to demonstrate embedded defects. If the game reaches a broken state, he restarts with the single launch command in under 10 seconds. The demo continues without embarrassment.

### Journey 4: Audience Experience (Tech Leaders — Passive)

A CTO who has never touched a mainframe watches the demo. The terminal fills the screen. The text layout, chip balance, bet prompts, and card rendering all read as old. She doesn't know what COBOL is, but she can follow the game — she understands betting, payouts, and going bust. When Kamal points to the code and says "this variable is called WS-X1 and nobody on earth knows what it does," she laughs. When he shows the payout calculation — three nested IFs, a hardcoded multiplier, and a truncation bug — she stops laughing because she's seen this pattern in her own organization. Business rules trapped in code nobody can read. The problem becomes human. The modernization pitch clicks.

## Innovation & Novel Patterns

### Intentional Imperfection as a Design Principle

This project inverts the standard quality model: bugs are requirements, tech debt is a deliverable, and unmaintainability is a success criterion. Every design decision that would normally be a defect — cryptic naming, GOTO-driven flow, dead code, no input validation, biased algorithms — is a specified, verifiable feature. A developer who tried to "fix" this code would be breaking it.

Requirements are written to the anti-pattern, not away from it. Where conventional PRDs say "the system shall be maintainable," this PRD says "the system shall be demonstrably unmaintainable in specific, targeted ways."

### Validation Approach

The authenticity test is human, not automated. A non-technical observer should look at the running terminal and the code and immediately read "old, messy, hard to understand." If the messiness requires explanation to be visible, it has failed.

### Risk Mitigation

The primary risk is over-engineering the imperfection — bugs so subtle they're invisible, or code so cryptic it's unrunnable. Countermeasure: every bug must be independently verifiable, and the game loop must complete under normal input regardless of how messy the underlying code is.

## Terminal Application — Technical Context

cobol-blackjack is an interactive terminal application with a single entry point. Not scriptable, not configurable, not designed for automation. Its entire interface is the terminal session: text in, text out.

- **Command structure:** `build.sh` compiles and launches in sequence — one command, no manual steps between. Re-running recompiles from source each time for predictability.
- **Output:** All stdout via COBOL DISPLAY statements. ASCII card art with Unicode suit symbols, ANSI color (red/white suits, yellow borders), 80-column layout, readable on monochrome terminals (color is enhancement, not dependency). Chip balance and current bet displayed alongside game state.
- **Interaction:** Player responds to bet prompts (numeric input), action prompts (H=hit, S=stand, D=double down) via keyboard. Input via COBOL ACCEPT. No mouse, no arrow keys.
- **Dependencies:** GnuCOBOL 3.1+ standard libraries only. No external rendering libraries. Build script uses standard bash.

## Functional Requirements

### Game Engine

- **FR1:** The system can shuffle and deal from a standard 52-card deck
- **FR2:** The system can deal an initial two-card hand to the player and the dealer
- **FR3:** The player can choose to hit (receive an additional card), stand (end their turn), or double down (on initial two-card hand only)
- **FR4:** The system can execute the dealer turn according to standard casino rules
- **FR5:** The system can calculate hand values with Ace counted as 1 or 11
- **FR6:** The system can determine and display the round outcome (player win, dealer win, push)
- **FR7:** The player can choose to play another round without restarting the application (session continues with current chip balance)

### Betting System

- **FR33:** The player starts each session with a chip balance of 100
- **FR34:** The player can place a bet (minimum 1 chip, maximum equal to current balance) before each round
- **FR35:** The system detects a natural blackjack (Ace + 10-value card on initial two-card deal) and resolves the round immediately
- **FR36:** The player can double down: bet is doubled, player receives exactly one additional card, then auto-stands
- **FR37:** The system calculates payouts after each round: win pays 1:1, natural blackjack pays 3:2, push returns the bet, loss forfeits the bet
- **FR38:** The chip balance persists across rounds within a session
- **FR39:** The session ends when the chip balance reaches zero (player is broke) or the player chooses to quit

### Build & Deployment

- **FR8:** Kamal can compile all source files with a single command on GnuCOBOL 3.1+/Ubuntu
- **FR9:** Kamal can launch the game immediately after compilation via the same single command
- **FR10:** The build process completes and the game reaches first player prompt within 5 seconds of command entry
- **FR11:** The build script runs without modification on a fresh Ubuntu installation with GnuCOBOL 3.1+ installed

### Terminal Display

- **FR12:** The system can display playing cards as ASCII card boxes with Unicode suit symbols in an 80-column terminal
- **FR13:** The system can display both player and dealer hands simultaneously during a round
- **FR14:** The system can display current hand values for player and dealer
- **FR15:** The system can display round outcome messages legible to a non-COBOL audience
- **FR16:** The system can prompt the player for hit/stand/double-down input in a manner consistent with 1980s terminal conventions
- **FR40:** The system can display the player's current chip balance during gameplay
- **FR41:** The system can display the current bet amount during a round
- **FR42:** The system can prompt the player to enter a bet amount before each round, displaying min/max constraints

### Legacy Code Authenticity

- **FR17:** Each source file contains identifiable examples of 1980s-era code style (cryptic naming, GOTO statements, dead code, sparse/incorrect comments)
- **FR18:** The codebase contains a minimum of 6 distinct, pointable examples of messiness demonstrable during a live demo without COBOL expertise
- **FR19:** The overall project structure, file naming, and build process reflect 1980s mainframe development anti-patterns
- **FR20:** The running terminal output visually reads as an authentic 1980s mainframe application to a non-technical observer

### Deliberate Defects

- **FR21:** The deck management module contains a biased shuffle algorithm
- **FR22:** The dealer logic module contains a soft 17 rule violation
- **FR23:** The scoring module contains an Ace value recalculation failure when two Aces are held
- **FR24:** The main game module contains no input validation on the hit/stand prompt
- **FR25:** The deal module contains an off-by-one error in the deal array
- **FR26:** The deck module contains a dead code paragraph that is never called
- **FR43:** The betting module contains a payout rounding error: natural blackjack 3:2 payout is calculated using integer division, truncating fractional chips (e.g., bet of 5 pays 7 instead of 7.5, but bet of 3 pays 4 instead of 4.5 — inconsistent truncation)
- **FR44:** The game module allows double down after the player has already hit (rule violation — double down should only be available on initial two-card hand)
- **FR45:** The betting module allows the player to bet more chips than their current balance under a specific sequence (e.g., bet validation checks stale balance variable)
- **FR46:** Each of the 9 deliberate bugs is independently verifiable through targeted testing without running the full game

### Accumulated Debt Patterns

- **FR47:** Each COBOL module contains at least one commented-out paragraph block representing a dropped feature (split hand, five-card charlie, insurance, original RNG, or audit log write) — syntactically valid COBOL in column 7 comment form, never reachable from any live execution path
- **FR48:** WS-HANDS.cpy and WS-GAME.cpy each contain at least one field group that is declared but never read or written by any module (ghost copybook fields following existing WS-XX naming convention)
- **FR49:** At least two modules declare a 77-level local variable in WORKING-STORAGE that is initialized but never referenced in PROCEDURE DIVISION (ghost local variable)
- **FR50:** At least two modules contain a COBOL statement that executes but produces no observable side effect (e.g., COMPUTE WS-X = WS-X + 0, duplicate MOVE ZERO to a field already zero at that point)
- **FR51:** At least four module headers carry WRITTEN/UPDATED date comments that conflict with each other or with the actual implementation sequence — consistent with code copied from other systems and edited without updating the header
- **FR52:** At least six comments across the codebase are written in French or German, referencing plausible-sounding internal defect reports, terminal compatibility patches, or regulatory compliance notes; all in column 7 comment form within 72-character line width

### Middleware Stubs

- **FR28:** The system calls a CASINO-AUDIT-LOG stub that accepts parameters and performs no operation
- **FR29:** The system calls a LEGACY-RANDOM-GEN stub that returns a hardcoded value
- **FR30:** Both middleware stubs compile and link without errors as part of the standard build

### Documentation

- **FR31:** Kamal can read a README that provides step-by-step compile and run instructions
- **FR32:** Kamal can read a README that lists and describes all 9 known bugs with enough detail to locate them in the code

## Non-Functional Requirements

### Performance

- Application reaches first player prompt within 5 seconds of single launch command on standard Ubuntu machine
- Card display and game state render immediately upon each player action — no perceptible delay between input and output
- Play-again loop restarts a new round without recompilation or perceptible lag

### Reliability

- Game completes a full round (bet through play-again prompt) without abnormal termination under any normal input (numeric bet, H, S, D, or equivalent)
- FR24 (no input validation), FR44 (double-down-anytime), and FR45 (bet-over-balance) define the boundary of "normal input" — undefined behavior on unexpected input and rule violations are specified defects, not reliability gaps
- Application produces consistent, repeatable behavior across multiple consecutive runs on the same machine

### Compatibility

- All source files compile without errors or warnings on GnuCOBOL 3.1+ on Ubuntu 20.04 or later
- Terminal display renders correctly in any standard 80-column terminal emulator (gnome-terminal, xterm, tmux) without special configuration
- Build script requires no additional dependencies beyond GnuCOBOL and standard GNU utilities

### Intentional Un-maintainability

- Codebase scores "unmaintainable" against any standard code quality heuristic — cryptic naming, no modularity, non-linear flow, absent documentation
- Any code analysis tool (manual or automated) surfaces multiple, distinct quality issues on first inspection
- The quality bar is explicitly inverted: a clean, well-structured implementation constitutes a failure against this requirement

### Accumulated Debt Patterns (NFR9)

- Every source module contains at least one orphaned paragraph block (FR47), and at least one of: ghost variable (FR49), no-op statement (FR50), contradictory version header (FR51), or foreign-language comment (FR52)
- Comments may be in English, French, or German — mixed-language presence is a feature, not an error
- Ghost copybook fields are legal and required: compiler allocates storage, no module references them
- No-op statements must compile and execute without side effects — they represent authentic patch residue
- Version date contradictions must be humanly plausible (copy-paste from other systems, management-driven renumbering) rather than obviously fabricated
