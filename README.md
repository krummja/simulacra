# Simulacra

Simulacra is a roguelike game written in Python. It uses the TCOD library and NumPy for a lot of its heavy lifting.

## Running the Game

On Linux, simply open a shell and run `bash run.sh`.

Otherwise, navigate to `simulacra` and run `python3 main.py`.

## Project Organization

The project it organized into several packages. Here I provide a brief overview of the overall structure of the project and a description of its component packages.

### Content
#### Actions
#### Architect
#### Areas
#### Factories
#### Items
#### Tiles

### Engine
The Engine package contains all of the packages and modules that make up the central logic of the game.

#### model.py
Carries references to all of the data that should be persistent
    for a given session.

The Model is also responsible for initializing the `EventQueue` and
    starting the scheduling loop. Finally, it is the mediator for
    communication between the game logic and log reporting.

#### state.py
Base class for all game states.

#### Apparata
The Apparata package is really a program within a program, and it consists of two main parts.

The first is the Graph Engine - as its name implies, it represents graph structures for use in a variety of game engine contexts.

The second is the Parser - it is responsible for defining, parsing, and interpreting grammars that make use of the Graph Engine.

#### Areas
The Areas package contains the logic for representing game locations. It provides models for entity, actor, and item state for individual areas.

#### Components
While Simulacra is not built around an ECS, I have borrowed some of the concepts of an ECS architecture. Entities are essentially clusters of Components, where Components provide the core functionality of different Entity types.

#### Entities
Entities are containers for Components.

#### Events
The Events package is the true beating heart of the entire program. Its primary class is the EventQueue, which handles the scheduling and unscheduling of actors, execution of action logic, and mediation of actions and results.

#### Geometry
The Geometry package is a utility package that contains several very useful classes for... well, geometry.

#### Particles
The Particles package is an implementation of particle emitters and effects. This is still quite experimental.

#### Rendering
The Rendering package contains all of the core functions and classes responsible for presenting the game's internal states and processes to the Interface.

#### States
This package contains all of the concrete State objects that make up the game's central logic.

### Interface
#### Elements
#### Views