# Wargame Army List Builder

## Description
A simple CLI tool built in Python as a learning exercise.

The goal is for the core logic of the program to be able to:
- Create an army
- Add a unit
- Remove a unit
- Calculate total points
- Show the list

To start, the program will pull from a local database of units located in a JSON file.  Later that data can be pulled from an external source. Similarly, the program will initially be used through the CLI and later the logic can be converted into an API.

## Installation
WIP

## Usage Instructions
WIP

## Current Progress

### Project Roadmap

#### Milestone 1 - Load Data ![Static Badge](https://img.shields.io/badge/Status-Done-blue)
The program successfully reads units.json and converts it into Python objects.

The program should be able to:
- load the JSON file
- create objects for:
  - Game
  - Faction
  - Unit
  - Model
- store them in memory
- build lookup dictionaries

#### Milestone 2 - Build Lookup Systems ![Static Badge](https://img.shields.io/badge/Status-Done-blue)
The program can find objects quickly.

The data loader should create lookup dictionaries and then program should be able to do things like:
- Get faction by ID
- Get all units belonging to a faction
- Get models for a unit

#### Milestone 3 - Create the Army Object ![Static Badge](https://img.shields.io/badge/Status-Done-blue)
The program can take user data to create an Army object.

An army should store
- name
- faction_id
- units

The program should be able to:
- create army
- add unit
- remove unit
- show army

#### Milestone 4 - Points Calculation ![Static Badge](https://img.shields.io/badge/Status-Done-blue)
The program can calculate the total points for a user made army.

#### Milestone 5 - Army Validation ![Static Badge](https://img.shields.io/badge/Status-Done-blue)
The program can check the point totals against army building rules.

The program should validate things like:
- unit must belong to army faction
- points cannot exceed limit
- maximum duplicate units

#### Milestone 6 - Saving and Loading Armies ![Static Badge](https://img.shields.io/badge/Status-In_Progress-green)
The program can save and load armies from storage.

Armies will be saved as JSON files.

The program should be able to:
- save army
- load army
- list saved armies

#### Milestone 7 - CLI Interface ![Static Badge](https://img.shields.io/badge/Status-Not_Started-gray)
User should be able to ineract with program through the cli.

#### Milestone 8 - Optional Features ![Static Badge](https://img.shields.io/badge/Status-Not_Started-gray)
- Unit search
- Army role summary
- Army export

#### Milestone 9 - API ![Static Badge](https://img.shields.io/badge/Status-Not_Started-gray)
Expose functionality via an API

### Features Implemented

### Features Planned

#### Core Features
- Create an army
- Add a unit
- Remove a unit
- Calculate total points
- Show the list

#### Additional Features
- Save lists
- Load lists
- Validate lists
- Import rules/unit data
- Export lists in various formats

### Known Bugs

## Contact

esstarks.scott@gmail.com