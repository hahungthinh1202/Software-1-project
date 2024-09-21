Pandemic game

Background
  - Four severe virus has spread out all over the world. Two players act as disease specilist 
    whose mission is to treat the hotspot while researching final vacines before the situation
    get out of control.

Game overview:
  - Two player must work together to reseaching the cure of all four virus.
  - Controling the situation by travel to hotspot and temporary treat the disease.
  - Player will lose if 8 outbreak occur (8 epidemic card drawn)
    or disease spreads too much (not enough disease marker to put on the map)
    or player run out of time (not enough player card to draw)

Game flow:
  - Game set up ->
  - Player 1 take turn ->
  - Computer spread disease ->
  - Player 2 take turn ->
  - Computer spread disease -> and so on

Game dipicts of some part
  - Game map include 48 major city in the world, partially connected.
  - Player turn: 4 actions, any combination of the actions below:
    +  Move
    +  Build research station at player location.
    +  Treat disease (remove disease marker from map)
    +  Share knowledge (exchange player card)
    +  Discover a cure
  - After 4 action: player draw 2 player card from the deck.
  - Computer turn:
    +  Spread disease with specific rule.
    +  Check if outbreak can happen, resolve.
    +  Check lose condition.
   
Database implementation
basic data of the game
  - Map database:
    + information of 48 location (fixed)
    + Connection information to other city (fixed)
    + Current virus infections (temporary)
    + if there is a reseach center here (temporary)
    
  - Player card database
    + 48 city card: has 2 main infomation:
        . city name use as a direct flight to the specify location (fixed)
        . card color (yellow/red/blue/black) depicts the knowledge about the virus. 
          use to find the cure in the future. (fixed)
    + 6 epidemic cards: When drawn, outbreak happens. (fixed)
    + 5 event cards: specific condition. (fixed)
  - Computer card database:
    + has only city name on it, use to automatically infects specific city in computer turn. (fixed)
      
  - Game play information database
    + Whose turn it is
    + Player 1 and player 2 current location + player cards
    + outbreak track
  
    
