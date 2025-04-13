Class: DS 5100
Author Name: Manav Sheth
Language: Python 3
Dependencies: numpy, pandas

URL: https://github.com/m112-s/DS5100_FinalProject/tree/main
  
Overview

This Python module provides a simulation framework for rolling weighted dice, running games with multiple dice, and analyzing the results. It consists of three classes:

Die: Represents a single die with customizable faces and weights.

Game: Simulates rolling one or more dice together for a number of times.

Analyzer: Provides statistical analysis on the results of a game.

Purpose
Simulate rolling created weighted dice and analyzing results

Synopsis 

Die Class - Create and roll a weighted die

import numpy as np

from montecarlo import Die

faces = np.array([1, 2, 3, 4, 5, 6])

die = Die(faces)

die.change_weight_one_side(6, 5.0)

print(die.roll_die(10))

print(die.current_state())

Methods

init(faces:np.array) : Create a die with specified face values and equal weights

change_weight_one_side(face, new_weight) : Change weight for one specific face

roll_die(num_rolls=1) : Roll the die a specified number of times

current_state() : Return a copy of the internal face-weight DataFrame

__repr__() : 	Text representation of the die’s current state 


Game Class - Roll multiple dice together

from montecarlo import Game

dice = [Die(faces) for _ in range(3)]

game = Game(dice)

game.play(num_rolls=100)

print(game.show_results('wide'))

Methods 
init(dice: List[Die]) : Create a game from a list of Die objects. All dice must have identical faces.

play(num_rolls)	 : Roll all dice num_rolls times and store the results.

show_results(form='wide') :	Return results in 'wide' or 'narrow' DataFrame format.



Analyzer - Analyze the game results

from montecarlo import Analyzer

analyzer = Analyzer(game)

print(analyzer.jackpot())

print(analyzer.face_counts_per_roll())

print(analyzer.combo_count())

print(analyzer.permutation_count())


Methods

__init__(game: Game) : Initialize analyzer with a played game

jackpot()	: Count number of jackpots (all dice same value in a roll)

face_counts_per_roll() : Count face occurrences per roll across dice

combo_count()	: Count distinct combinations (order doesn't matter)

permutation_count()	: Count distinct permutations (order matters)
