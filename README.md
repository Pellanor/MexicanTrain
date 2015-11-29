# MexicanTrain
Bots play Mexican Train against each other!

This is a little project that I've been working on to get some practise with Python, and to try to apply some new design patterns I haven't used much before.

What Is Mexican Train?
=======
[Mexican Train](https://en.wikipedia.org/wiki/Mexican_Train) is a dominoes game where players try to be the first to play all dominoes from their hand onto one or more "trains" in the centre of the table.

The game is coded agains the rules that I played the game with. These may or may not contain some house rules.

Summary of rules:
* Played using double twelve dominoes
* Play starts with the double twelve. If nobody has it in their starting hand, they draw until somebody has it.
* Immedatly upon the double twelve being played the player who placed it draws a replacement tile and starts the first turn.
* In everybodys first turn they are allowed to play any number of dominoes.
  * To play a domino it must line up with the last number on the train that it is played on. All trains start at twelve,
  * Each player can play on their own train, the mexican train, or an open train.
  * If a player plays a double, they demand satisfaction.
    * When a player demands satisfaction they have the opportunity to immediatley satisfy it by playing a domino that continues the train (has a value matching the double).
    * If they cannot satisfy themself, they must draw another domino. If the new domino provides satisfaction, it can be played immediately and play continues.
    * If they still cannot play, they must end their turn and pass to the next player. If they demanded satisfaction on their own train, it is considered open and will be until they are able to play on it at a later date.
    * While a train demands satisfaction, it is the only train that can be played on. As soon as it is played on it no longer demands satisfaction.
* After the first turn players can only play a single domino per turn, with the exception being when they demand satisfaction.
* Once a player has played their last domino, that player wins the round. A new round begins starting with the double eleven domino.

Bots!
======
There are a few different bots that are currently implemented. All extend [BaseBot](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/BaseBot.py)
* [MoveBot](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/MoveBot.py) Places one move at a time, with no advanced planning.
* [LongBot](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/LongBot.py) Places the longest possible train on the first turn.
* [FatBot](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/FatBot.py) Places as many dominoe sas possible on the first turn.

All bots are implemented using the strategy patern. They can provide an implementation of [Strategy](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/strategy/strategy.py) to [BaseBot](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/BaseBot.py)'s functions to easily take advantage of various helper methods.

The [Prioirty](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/strategy/Priority.py) [Strategy](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/strategy/strategy.py) uses a priority chain to apply a sequesnce of filters to determine which play is preferable.

Bots use the [BotGameState](https://github.com/Pellanor/MexicanTrain/blob/master/src/bots/state/BotGameState.py) to read the game state without being able to write to it. It also includes a number functions to provide additional insight into the state of the game.
