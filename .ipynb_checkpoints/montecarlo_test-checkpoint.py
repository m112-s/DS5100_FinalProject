import unittest
import numpy as np
import pandas as pd
from montecarlo import Die
from montecarlo import Game
from montecarlo import Analyzer

class TestMonteCarlo(unittest.TestCase):
    
    def setUp(self):
        self.faces = np.array([1,2,3,4,5,6,7,8,9,10])
        self.die1 = Die(self.faces)
        self.die2 = Die(self.faces)
        self.die3 = Die(self.faces)
        
        self.die1.change_weight_one_side(10, 10)        
        self.die2.change_weight_one_side(2, 2.0)
        self.die3.change_weight_one_side(3, 3)
        
        self.game = Game([self.die1, self.die2, self.die3])
        self.game.play(5)
        self.analyzer = Analyzer(self.game)

    def test_die_init_valid(self):
        self.assertTrue(len(self.die1.current_state()) == 10)

    def test_die_init_invalid(self):
        with self.assertRaises(TypeError):
            Die([1, 2, 3])  # not a NumPy array

    def test_die_init_duplicate_faces(self):
        with self.assertRaises(ValueError):
            Die(np.array([1, 1, 1]))  

    def test_die_change_weight_valid(self):
        self.die1.change_weight_one_side(1, 2.5)
        actual = self.die1.current_state().loc[1, 'weight']
        self.assertTrue(actual == 2.5)

    def test_die_change_weight_invalid(self):
        with self.assertRaises(TypeError):
            self.die1.change_weight_one_side(2, "high")  

    def test_die_roll_die(self):
        rolls = self.die1.roll_die(3)
        self.assertTrue(isinstance(rolls, list))
        self.assertTrue(len(rolls) == 3)

    def test_die_current_state(self):
        df = self.die1.current_state()
        self.assertTrue('weight' in df.columns)
        self.assertFalse(df.empty)
        
    def test_game_init_valid(self):
        self.assertTrue(isinstance(self.game, Game))
        self.assertTrue(hasattr(self.game, '_dice'))
        self.assertEqual(len(self.game._dice), 3)

    def test_game_init_invalid_die_type(self):
        with self.assertRaises(ValueError):
            Game([self.die1, 1001, self.die3])

    def test_game_init_invalid_face_mismatch(self):
        die_mismatch = Die(np.array(['a', 'b', 'c']))
        with self.assertRaises(ValueError):
            Game([self.die1, die_mismatch])

    def test_game_play_shape(self):
        self.game.play(4)
        df = self.game.show_results()
        self.assertTrue(df.shape == (4, 3)) 

    def test_game_show_results_wide(self):
        self.game.play(2)
        result = self.game.show_results(form='wide')
        self.assertTrue(isinstance(result, pd.DataFrame))
        self.assertEqual(result.shape, (2, 3))

    def test_game_show_results_narrow(self):
        self.game.play(2)
        result = self.game.show_results(form='narrow')
        self.assertTrue(isinstance(result.index, pd.MultiIndex))

    def test_show_results_invalid_format(self):
        self.game.play(1)
        with self.assertRaises(ValueError):
            self.game.show_results(form=1001)
            
    def test_analyzer_init_with_invalid_game(self):
        with self.assertRaises(ValueError):
            Analyzer("not_a_game")
            
    def test_analyzer_init_with_unplayed_game(self):
        game = Game([self.die1, self.die2, self.die3])
        with self.assertRaises(ValueError):
            Analyzer(game) 
            
    def test_analyzer_jackpot(self):
        jackpots = self.analyzer.jackpot()
        self.assertTrue(jackpots >= 0)

    def test_analyzer_face_counts_per_roll(self):
        df = self.analyzer.face_counts_per_roll()
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.shape[0], 5)  
        self.assertTrue((df.sum(axis=1) == 3).all()) 

    def test_analyzer_combo_count(self):
        df = self.analyzer.combo_count()
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.columns.tolist(), ['Count'])
        self.assertTrue(isinstance(df.index[0], tuple))

    def test_analyzer_permutation_count(self):
        df = self.analyzer.permutation_count()
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertEqual(df.columns.tolist(), ['Count'])
        self.assertTrue(isinstance(df.index[0], tuple))


if __name__ == '__main__':
    unittest.main()
