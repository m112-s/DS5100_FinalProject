import numpy as np
import pandas as pd

class Die:
    '''
    Class for creating a Die object with N sides and W weights, default weights = 1 
    '''
    def __init__(self, faces: np.ndarray):
        '''
        input: numpy array of face values 
        Method to initialize the Die, checking for incorrect inputs and giving initial weights
        output: faces and initial weight in a private dataframe, faces in the index 
        '''
        
        # Check Numpy array
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces not a NumPy array")
        
        # Check faces for duplicate values 
        if len(np.unique(faces)) != len(faces):
            raise ValueError("Die faces not distinct")
        
        # Initialize faces with weights = 1 
        self._df = pd.DataFrame({
            'weight': np.ones(len(faces))
        }, index=faces)
        
    def change_weight_one_side(self, face, new_weight):
        '''
        input: face value and new weight (must be numeric) 
        Method for chaning an individual face to a new weight. Checks if face is valid and weight is number 
        output: a dataframe with a replaced weight for specified face 
        '''
        # Check if face is valid
        if face not in self._df.index:
            raise IndexError("Face value not valid")
        
        # Check if new_weight is numeric
        try:
            new_weight = float(new_weight)
        except (TypeError, ValueError):
            raise TypeError("Weight must be a numeric type")
        
        # Set weights as called in method
        self._df.at[face, 'weight'] = new_weight
        
    def roll_die(self, num_rolls=1):
        '''
        input: number of rolls (not required) 
        Method for rolling a die an x number of times
        output: copy of private die dataframe 
        '''
        #Create random choice of faces based on weight 
        outcomes = np.random.choice(
            self._df.index,
            size=num_rolls,
            replace=True, #Allow for dupllicates 
            p=self._df['weight'] / self._df['weight'].sum() 
        )
        return outcomes.tolist()

    def current_state(self):
        '''
        Method for providing the current state of a die's weights 
        '''
        return self._df.copy()

    def __repr__(self):
        '''
        Method to help build function by providing printed outputs 
        '''
        return self._df.to_string()

    
class Game:
    '''
    Class for creating a game object with 1 or more dice used  
    '''
    def __init__(self, dice):
        '''
        input: List of dice objects 
        Method to initialize game with dice, also check for any incorrect inputs   
    
        '''
        
        # Make sure all dice used are the correct object type 
        for i in dice:
            if not isinstance(i, Die):
                raise ValueError("Input contains at least 1 non Die object")
        
        #Make sure all faces of each die are the exact same 
        first_die = set(dice[0].current_state().index)
        for i in dice:
            if set(i.current_state().index) != first_die:
                raise ValueError("All dice must have the same set of faces")

        self._dice = dice
        self._play_results = None

    def play(self, num_rolls):
        '''
        input: number for number of rolls 
        
        Method for playing all dice an x number of rolls and creating a dataframe of results 
        
        output: "wide" data frame of play results. 
        '''
        results = {}

        for i, die in enumerate(self._dice):
            results[i] = die.roll_die(num_rolls)

        self._play_results = pd.DataFrame(results)
        self._play_results.index.name = "Roll Number" 

    def show_results(self, form='wide'):
        '''
        input: form type (wide or narrow) 
        
        Method for choosing how to show results and showing the results
        
        output: results in specified format 
        '''
        if self._play_results is None:
            return None
        
        if form == 'wide':
            return self._play_results.copy()
        elif form == 'narrow':
            return self._play_results.stack().to_frame('Outcome')
        else:
            raise ValueError("Not expected either of expected values, 'wide' or 'narrow'.")

class Analyzer:
    '''
    Class for deriving analytics on each game object run 
    '''
    def __init__(self, game):
        '''
        input: game object 
        Initializing the analysis for a specific game type created
        Checks if input is a game and if the game has been played 

        '''
        if not isinstance(game, Game):
            raise ValueError("Input must be Game")
        
        self._game = game
        self._results = game.show_results(form='wide')
        
        if self._results is None:
            raise ValueError("The Game has no results")

    def jackpot(self):
        '''
        Method for checking for a jackpot
        output: returns an integer for number of "jackpots" 
        '''
        return (self._results.nunique(axis=1) == 1).sum()

    def face_counts_per_roll(self):
        '''
        Method for checking counts of a number per roll
        output: Data frame with an index of roll number and face values as columns and count values in cells 
        '''
        all_faces = pd.unique(self._results.values.ravel()) 
        counts = self._results.apply(lambda row: row.value_counts(), axis=1).fillna(0)
        return counts.reindex(columns=sorted(all_faces)).astype(int)

    def combo_count(self):
        '''
        Method for listing out all combinations of numbers (order does not matter) 
        output: a MultiIndex of distinct combinations and a column for the associated counts
        '''
        combos = self._results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combos.value_counts()
        return combo_counts.to_frame(name='Count')

    def permutation_count(self):
        '''
        Method for listing out all combinations of numbers (order matters) 
        output: data frame wiht a MultiIndex of distinct permutations and a column for the associated counts
        '''
        perms = self._results.apply(lambda row: tuple(row), axis=1)
        perm_counts = perms.value_counts()
        return perm_counts.to_frame(name='Count')


 