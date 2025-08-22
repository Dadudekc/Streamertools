# Streamertools Product Requirements Document

## Overview
Streamertools provides a suite of free, open-source tools for livestreamers. The initial focus is the **MeTuber** library, which applies real-time image filters and overlays to webcam feeds for use with OBS.

## Problem Statement
Streamers lack a lightweight, customizable library for applying artistic effects to live video without relying on proprietary solutions.

## Goals
- Offer a modular Python library for filters and overlays.
- Integrate easily with OBS and typical streaming setups.
- Maintain high test coverage and developer-friendly documentation.

## Target Audience
- Streamers who want creative control over their webcam feed.
- Developers interested in extending and customizing video effects.

## Key Features
- Image filters such as vibrant color, black and white, and sepia.
- Overlay effects including halftones, glitches, and light leaks.
- Bitwise operations for advanced visual effects.
- Modular style system for adding new effects quickly.

## Non-Goals
- Full video editing or streaming platform management.
- Proprietary or paid effects.

## Success Metrics
- Number of built-in styles and community contributions.
- Test coverage above 80%.
- Adoption measured by PyPI downloads and GitHub stars.
