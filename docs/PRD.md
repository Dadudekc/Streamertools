# Streamertools Product Requirements Document

## Overview
Streamertools is an open-source toolkit focused on helping streamers enhance live content. The current core component is the MeTuber library, which applies real-time filters and overlays to webcam feeds for seamless OBS integration.

## Current Status
- MeTuber prototype offers basic filters and a PyQt5 GUI.
- Documentation and testing infrastructure are in early stages.

## Goals
- Deliver customizable image filters and overlays for live streams.
- Provide a GUI application for real-time preview and device management.
- Enable developers to add new style modules through a modular architecture.

## User Stories
- As a streamer, I can apply artistic filters to my webcam feed to enhance my stream.
- As a developer, I can create new style modules without modifying core code.
- As a user, I can manage webcam devices and select filters from a graphical interface.

## Functional Requirements
- Load webcam feeds and apply selected style transformations.
- Offer a PyQt5-based GUI for choosing devices and styles.
- Persist user configuration through a settings manager.
- Maintain unit tests for styles, services, and GUI interactions.

## Non-Functional Requirements
- High test coverage (>80%).
- Cross-platform support for Windows and Linux.
- Clear documentation for installation, usage, and contribution.

## Out of Scope
- Cloud-based video processing.
- Proprietary or licensed effects.

## Success Metrics
- Growth in available styles and overlays.
- Community contributions and issue resolution time.
- Stable releases with passing test suites.
