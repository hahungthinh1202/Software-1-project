Database visualized (updated 25/09)

https://lucid.app/lucidchart/8a40251e-b848-447d-8b42-5662e0650fb7/edit?invitationId=inv_51c4a464-47e2-4a5b-8e11-dea5a81ff0c6&page=0_0#

Pandemic Game

Background
  - Four severe viruses have spread across the world. Two players act as disease specialists whose mission is to treat hotspots while researching final vaccines before the situation gets out of control.
    
Game objectives:
  - Two players must work together to research the cure for all four viruses.
    Control the situation by traveling to hotspots and temporarily treating the disease.
  - Players will lose if 8 outbreaks occur (8 epidemic cards are drawn),
    the disease spreads too much (not enough disease markers to place on the map),
    or if time runs out (not enough player cards to draw).
  - Player will win immediately after discover four cures 
    
Game Flow:
  - Game setup
  - Player 1 takes a turn
  - Computer spreads disease
  - Player 2 takes a turn
  - Computer spreads disease
  - Repeat this cycle

Game Depictions of Some Parts:
  - The game map includes 48 major cities around the world, partially connected.
  - Player’s turn: 4 actions, any combination of the following actions:
    + Move
    + Build a research station at the player's location
    + Treat disease (remove disease markers from the map)
    + Share knowledge (exchange player cards)
    + Discover a cure
  - After 4 actions, the player draws 2 player cards from the deck.
  - Computer's turn:
    + Spread disease according to specific rules
    + Check if an outbreak occurs and resolve it
    + Check for lose conditions
    + 
Database Implementation:
  - Map database:
    + Information on 48 locations (fixed)
    + Connection information to other cities (fixed)
    + Current virus infections (temporary)
    + Whether there is a research center in a city (temporary)
      
  - Player card database:
    + Data types: city card, epidemic card, event card
    + 48 city cards: contain two main pieces of information:
    + City name (used for direct flights to the specified location) (fixed)
    + Card color (yellow/red/blue/black) depicting knowledge of the virus (used to find cures later) (fixed)
    + 6 epidemic cards: when drawn, outbreaks occur (fixed)
    + 5 event cards: special conditions (optional)
      
  - Computer card database:
    + Contains only city names, used to automatically infect specific cities during the computer's turn (fixed)
      
  - Gameplay information database:
    + Whose turn it is
    + Outbreak track
    + Amount of vaccine discovered
      
  - Player information database:
    + Player's current location
    + List of player cards in possession


