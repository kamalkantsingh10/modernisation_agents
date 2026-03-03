---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - docs/planning-artifacts/wrieup.md
date: 2026-02-26
author: Kamal
---

# Product Brief: cobol-blackjack

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary

A baseline COBOL Blackjack card game built to authentically represent a 1980s-era mainframe application, along with a mainframe sandbox environment on Ubuntu for live demonstration. This is a demo asset — the "before" in a before-and-after modernization showcase targeting tech leaders and decision-makers evaluating legacy modernization services. The application must be fully functional, runnable on GnuCOBOL, and carry all the hallmarks of real legacy code: poor structure, cryptic naming, outdated patterns, deliberate bugs, and accumulated tech debt. Blackjack was chosen for its simplicity, universal familiarity, and visual appeal — enabling non-technical audiences to immediately grasp the contrast when shown alongside a modernized version.

---

## Core Vision

### Problem Statement

Organizations with legacy mainframe applications have been attempting modernization for years, often without progress. Decision-makers — typically tech leaders who are not deeply technical — lack confidence in modernization processes because they have no tangible way to see what the journey from legacy to modern actually looks like.

### Problem Impact

Without a compelling, visual demonstration, modernization pitches remain abstract. Slide decks and whitepapers fail to convey the reality of legacy code or the transformative impact of modernization. Decision-makers delay or avoid modernization commitments, leaving critical business systems trapped on aging platforms.

### Why Existing Solutions Fall Short

Most modernization sales efforts rely on technical documentation, architecture diagrams, or case studies that non-technical leaders struggle to connect with. There is a gap in the market for a live, working demonstration that makes the before-and-after transformation immediately visible and understandable to any audience.

### Proposed Solution

Build an authentically legacy-styled COBOL Blackjack application — a multi-file, runnable card game that embodies real 1980s mainframe development practices. The codebase includes spaghetti code, cryptic variable names, incorrect comments, dead code, GOTO statements, deliberate bugs, and proprietary middleware calls. The project also includes setting up a mainframe sandbox environment on Ubuntu with GnuCOBOL, providing a ready-to-demo platform where the legacy application can be compiled, run, and showcased live. This project delivers only the legacy baseline and its runtime environment — the modernization process and modernized application are separate efforts.

### Key Differentiators

- **Authentic legacy feel:** Not a toy example but a multi-file COBOL application structured like real enterprise mainframe software — copybooks, subprograms, shared data structures
- **Deliberately imperfect:** Includes 6 specific, subtle bugs and pervasive tech debt that represent real-world legacy challenges
- **Visually accessible:** Blackjack is universally understood — non-technical audiences can watch the game being played without needing to understand the code
- **Live demo-ready:** Includes a mainframe sandbox on Ubuntu with GnuCOBOL installed and configured, enabling live compilation and execution during presentations
- **Runnable demo:** Compiles and runs on GnuCOBOL with a build script that works out of the box
- **Scoped for impact:** Focused solely on the legacy baseline and its runtime environment, keeping the project tight and deliverable

## Target Users

### Primary Users

**Kamal (Developer / Demo Presenter)**
The sole user of this application. Builds the legacy COBOL Blackjack app, modernizes it separately, and presents the before-and-after comparison to prospective clients. Needs the legacy codebase to be authentically messy, compilable, and runnable so it can be demonstrated live.

### Target Audience

This is a demo asset, not a product with end-users. The target audience is **tech leaders and decision-makers** evaluating legacy modernization services. They watch the demo but do not interact with the application directly. They are not deeply technical but need to visually grasp the difference between legacy and modernized code.

### User Journey

1. **Build:** Kamal compiles and runs the legacy COBOL app on the Ubuntu mainframe sandbox
2. **Demo:** Kamal presents the working legacy app to the audience -- showing the terminal-based Blackjack game in action
3. **Contrast:** The legacy app is shown alongside the modernized version (out of scope for this project) to demonstrate the transformation
4. **Impact:** Decision-makers see the tangible before-and-after, building confidence in the modernization process

## Success Metrics

### Acceptance Criteria

- **Flawless gameplay:** The Blackjack game runs smoothly from start to finish -- dealing, hitting, standing, dealer turn, outcome display, and play-again loop all work without errors or visual glitches
- **Polished ASCII display:** Card rendering and game state display must feel like a real gaming engine is behind it -- clean layout, consistent formatting, responsive to player input
- **One-command launch:** The entire application compiles and runs with a single command (e.g., `./build.sh && cobcrun BJACK-MAIN` or equivalent single statement)
- **Multi-file tech debt distribution:** Each source file contains its own authentic technical debt -- no file is "clean"
- **Project-level anti-patterns:** The overall project structure, naming conventions, build process, and documentation reflect 1980s-era practices and organizational anti-patterns
- **Deliberate bugs present:** All 6 specified bugs are implemented and subtly embedded -- detectable by analysis but not obvious during casual play

### Business Objectives

- Deliver a compelling, credible "before" asset that anchors the modernization demo
- Enable Kamal to confidently present the legacy app live without worrying about crashes or visual issues

### Key Performance Indicators

- Application compiles with zero errors on GnuCOBOL 3.1+
- Full game round completes without abnormal termination
- All 6 deliberate bugs are verifiable through targeted testing
- Launch-to-gameplay time is under 5 seconds from single command
- Non-technical audience can follow the game visually without explanation

## MVP Scope

### Core Features

**COBOL Blackjack Application**
- Single-player Blackjack against a computer dealer with standard casino rules
- Multi-file architecture: 8-14 COBOL source files (programs + copybooks), structured like real enterprise mainframe software
- ASCII art card display with polished, smooth rendering -- must feel like a real gaming engine
- Flawless game loop: deal, hit/stand, dealer turn, outcome, play again
- Terminal-based I/O using DISPLAY/ACCEPT only (no CICS, no BMS)

**Authentic 1980s Legacy Code Style**
- Cryptic variable names (WS-X1, WS-PHT, WS-FLAG-A)
- Vague paragraph names (PROC-A, CALC-1, CHECK-X)
- Sparse, incorrect, outdated comments
- GOTO statements, nested IFs, no EVALUATE
- Dead code, unused variables, mixed WORKING-STORAGE
- No structured programming patterns from COBOL 85

**Technical Debt (Distributed Across All Files)**
- Every source file carries its own authentic tech debt -- no clean files
- Project-level anti-patterns reflecting 1980s development practices
- Spaghetti code with non-linear PERFORM jumps
- Magic numbers scattered inconsistently
- No input validation, no arithmetic overflow protection

**6 Deliberate Bugs**
- Biased shuffle algorithm (BJACK-DECK)
- Soft 17 rule violation (BJACK-DEALER)
- Ace value recalculation failure with two Aces (BJACK-SCORE)
- No input validation on hit/stand prompt (BJACK-MAIN)
- Off-by-one in deal array (BJACK-DEAL)
- Dead code paragraph never called (BJACK-DECK)

**Proprietary Middleware Stubs**
- CASINO-AUDIT-LOG stub (accepts params, does nothing)
- LEGACY-RANDOM-GEN stub (returns hardcoded value)
- Both compile and link without errors

**Ubuntu Mainframe Sandbox**
- GnuCOBOL 3.1+ environment setup on Ubuntu
- One-command build and run script
- Ready for live demo with no manual configuration

**Deliverables**
- All COBOL source files (8-14 files)
- Middleware stub programs
- Build script (build.sh) -- works on Ubuntu
- README with compile/run instructions and known bugs

### Out of Scope for MVP

- Splitting pairs, doubling down, insurance, side bets
- Multiple players or multiplayer
- Betting/chips system
- Web-based UI or terminal viewer
- CICS or BMS screen maps
- The modernization process itself
- The modernized Java "after" application
- macOS support (Ubuntu only for this project)

### MVP Success Criteria

- build.sh compiles and runs with a single command on GnuCOBOL 3.1+ / Ubuntu
- Full Blackjack round plays from start to finish without errors
- All 6 deliberate bugs present and verifiable
- ASCII card display renders cleanly in standard terminal
- Every source file contains authentic technical debt
- Non-technical audience can follow gameplay visually

### Future Vision

This project is scoped as a standalone demo asset. Future efforts (separate projects) include:
- Modernized Java version of the application (the "after")
- Documented modernization process/methodology
- Side-by-side demo presentation materials
- Potential expansion to additional legacy application examples
