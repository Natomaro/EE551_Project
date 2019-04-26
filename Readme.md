# EE551_Project - Python Educational Game
## Before you run the game
Before you run, make sure you read the readme on how to ensure the game is loaded correctly. I've provided a save file that I've been using for testing because it is a little better than the starting profile. If you want to start completely over, delete the save_file.csv from your local directory.
 
## Introduction
Adventure video games have been popular since their inception 30 years ago! Although in this day and age, these games have remarkable graphics and enormous worlds. But in their humble beginnings, adventure games were text-based.

## Proposal
In this project I seek to build a game that provides a basic platform for a text-based adventure game. The game will consist of 4 main menu options - Battle, Change loadout, go to the shop, and use an item. As you battle enemies, you will collect new gear, gold, and experience points so you can become stronger. The game will have a save feature by using the python csv package - all the player's stats will get converted to a list and stored in a locally saved csv.

## Features
#### Battle
- Randomly generate an enemy.
- Player can attack with sword or with various spells that have extra effects!
- Low on health or mana mid battle - use a potion! Otherwise, run away because if you die, you lose your progress.
#### Change Loadout
- After collecting various gear and spells from battle or shopping, you can swap out your loadout!
- Kill more monsters to get better gear to become even stronger!
#### Shop
- Present items in a shop menu the player can use gold to buy.
- Also, the player can sell excess items to earn a little more gold. Otherwise, the inventory is full and they can't add new things!
#### Using Items
- The only way to replenish health and mana is to use potions! Make sure you earn gold and buy enough equipment or you might lose the game completely!
#### Saving
- When you properly exit, your player's stats get saved locally to your machine. This allows you to pick up where you left off.
- In case you want to start over, you just need to delete your local copy of save_game.csv!
## To-Do
Translate all the lessons from class into one text-based adventure game
Use classes and inheritance to make player and enemy instances
Build functions that take a user's inputs to execute battle, loadout, item, and shop sequences.
Import csv package for python to enable a save game feature.
Play test the game and build a pytest file to test a lot of the game in a single script.
Author
Nick Tomaro
