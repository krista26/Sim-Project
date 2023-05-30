# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 12:57:45 2023

@author: krist
"""
import numpy as np
import operator
import matplotlib.pyplot as plt

## Yahtzee simulator!
class Yahtzee(object):
    """This is the Yahtzee Object """
    def __init__(self, strategy='upper', every=True, verbose=False):
        #Initalize scorecard with zeros for each category. Separate into upper and lower card so
        # Strategy can be separated
        self.scorecard={"upper":{"1":0,
                   "2":0,
                   "3":0,
                   "4":0,
                   "5":0,
                   "6":0},
                   "lower":{"3x":0,
                            "4x":0,
                            "fh":0,
                            "sm_s":0,
                            "lg_s":0,
                            "yahtzee":0,
                            "chance":0,
                            "bonus":0}}
        
        self.upper_bonus=0
        self.strategy=strategy
        self.every=every
        self.verbose=verbose
    

    def roll_dice(self, dice=[]):
        #Roll x dice and store each dice in a list
        for i in range(5-len(dice)):
            dice.append(np.random.randint(1,7))
            
        return dice
    
    def keep_dice(self, dice):
        dice=sorted(dice, reverse=True)
        count_dic= self.create_count_dict(dice)
        kept=[]
        
        #Sort dictionary by descending values to get dice with highest occurance 
        sorted_d = dict( sorted(count_dic.items(), key=operator.itemgetter(1),reverse=True))
        
        
        #Iterate through values and check if we have already recorded points
        for item in sorted_d:
            if self.scorecard['upper'][str(item)]==0:
                #If points are still 0, keep all the dice for that number
                for i in range(sorted_d[item]):
                    kept.append(item)
                return kept
                
        return kept
        
    def create_count_dict(self, dice):
        
        dice=sorted(dice, reverse=True)
        count_dic={}
        for num in dice:
            if num not in count_dic:
                count_dic[num]=1
            else:
                count_dic[num]+=1
        
        return count_dic
        
    def check_for_straight(self, dice):
        dice=sorted(dice, reverse=True)
        dice_set=set(dice)
        if dice == [6,5,4,3,2] or dice== [5,4,3,2,1]:
            if self.scorecard["lower"]["lg_s"]==0:
                self.scorecard["lower"]["lg_s"]=40
                return True
        elif dice_set=={1,3,4,5,6} or dice_set=={3,4,5,6} or dice_set=={2,3,4,5} or dice_set=={1,2,3,4,6} or dice_set=={1,2,3,4}:
            if self.scorecard["lower"]['sm_s']==0:
                self.scorecard["lower"]['sm_s']=30
                return True
        return False
    
    def check_for_fh(self, dice):
        count_dic= self.create_count_dict(dice)
        #If there are only two items in the count dic and one of them has a count of two the other must have a count of three and is therefore a full house
        if len(count_dic)==2:
            for item in count_dic:
                if count_dic[item]==2:
                    if self.scorecard["lower"]['fh']==0:
                        self.scorecard["lower"]['fh']=25
                        return True
        return False
    
    def check_for_5x_4x_3x(self, dice):
        dice=sorted(dice, reverse=True)
        count_dic= self.create_count_dict(dice)
        for item in count_dic:
            if count_dic[item]==5:
                #print("Yahtzee!")
                if self.scorecard["lower"]['yahtzee']==0:
                    self.scorecard["lower"]['yahtzee']= 50
                
                elif self.scorecard["lower"]['bonus']!='X':
                    self.scorecard["lower"]['bonus']+= 50
                return True
            elif count_dic[item]==4:
                if self.scorecard["lower"]['4x']==0:
                    self.scorecard["lower"]['4x']= sum(dice)
                    return True
            elif count_dic[item]==3:
                if self.scorecard["lower"]['3x']==0:
                    self.scorecard["lower"]['3x']= sum(dice)
                    #print(dice)
                    #print(sum(dice))
                    return True
        return False
    
    def record_upper_scores(self, dice):
        dice=sorted(dice, reverse=True)
        count_dic= self.create_count_dict(dice)
        kept=[]
        
        #Sort dictionary by descending values to get dice with highest occurance 
        sorted_d = dict( sorted(count_dic.items(), key=operator.itemgetter(1),reverse=True))
        
        for item in sorted_d:
            if sorted_d[item]==5:
               #print('Yahtzee!') 
               if self.scorecard["lower"]['yahtzee']==0:
                   self.scorecard["lower"]['yahtzee']= 50
               elif self.scorecard["lower"]['bonus']!="X":
                   self.scorecard["lower"]['bonus']+=50
               return True
           
            elif self.scorecard['upper'][str(item)]==0:
                self.scorecard['upper'][str(item)]= item*sorted_d[item]
                return True
            
        #Return False if not able to record scores
        return False
    
    def record_chance(self, dice):
        if self.scorecard["lower"]['chance']==0:
            self.scorecard["lower"]['chance']= sum(dice)
            return True
        
        return False
            
    def scratch(self):
        
        #Scratch the upper scores, lower numbers first. Then lower scores
        
        for item in self.scorecard["lower"]:
            if self.scorecard["lower"][item]==0:
                self.scorecard["lower"][item]="X"
                
        for item in self.scorecard["upper"]:
            if self.scorecard["upper"][item]==0:
                self.scorecard["upper"][item]="X"
        
            
    def play_game(self):
        #14 turns in a typical yahtzee game
        
        for i in range(14):
            
            dice=[]
            score_recorded=False
            
            
            if self.verbose:
                print(f"Round {i}")
                
            #Roll twice and keep dice
            for j in range(2):
                
                dice=self.roll_dice(dice)
                
                if self.verbose:
                    print(f"For roll {j+1} the dice are {dice}")
                    
                
                #Check for special occurances between each of the rolls if variable every is True
                
                if self.every:
                    if self.check_for_fh(dice):
                        score_recorded=True
                        #print(dice)
                        #print("fh recorded")
                    elif self.check_for_straight(dice):
                        score_recorded=True
                        #print(dice)
                        #print("straight recorded")
                        
                #Choose which dice to keep between each roll    
                dice=self.keep_dice(dice)
                
                if self.verbose:
                    print(f"The dice I'm keeping are {dice}")
                    
                
            #Final dice roll
            dice= self.roll_dice(dice)
            
            #Check for points
            if self.strategy=='Upper' and not score_recorded:
                #With upper strategy, always record upper first
                if self.record_upper_scores(dice):
                    #print(dice)
                    #print("upper score recorded")
                    pass
                elif self.check_for_5x_4x_3x(dice):
                    #print(dice)
                    #print("multiple recorded 2")
                    pass
                elif self.check_for_fh(dice):
                    #print(dice)
                    #print("fh recorded")
                    pass
                elif self.check_for_straight(dice):
                    #print(dice)
                    #print("straight recorded")
                    pass
                elif self.record_chance(dice):
                    #print("chance recorded")
                    pass
                else:
                    self.scratch()
                    #print("scratch")
                    
            #In lower strategy, we check for the lower scores first
            elif self.strategy=='Lower' and not score_recorded:
                if self.check_for_5x_4x_3x(dice):
                    #print(dice)
                    #print("multiple recorded 2")
                    pass
                elif self.check_for_fh(dice):
                    #print(dice)
                    #print("fh recorded")
                    pass
                elif self.check_for_straight(dice):
                    #print(dice)
                    #print("straight recorded")
                    pass
                elif self.record_upper_scores(dice):
                    #print(dice)
                    #print("upper score recorded")
                    pass
                elif self.record_chance(dice):
                    #print("chance recorded")
                    pass
                else:
                    self.scratch()
                    #print("scratch")
                
        
        upper_scores=0
        lower_scores=0
        for item in self.scorecard["upper"]:
            if isinstance(self.scorecard["upper"][item], int):
                upper_scores+=self.scorecard["upper"][item]
                
        if upper_scores>=63:
            upper_scores+=25
            
        for item in self.scorecard["lower"]:
            if isinstance(self.scorecard["lower"][item], int):
                lower_scores+=self.scorecard["lower"][item]
                
                
        total_score=upper_scores+lower_scores
        
        # print(self.scorecard)
        
        # print(f"Upper Score: {upper_scores}")
        # print(f"Lower Score: {lower_scores}")
        
        # print(f"Total score: {lower_scores+upper_scores}")
        
        return total_score

    
def run_and_plot(strategy, games=100, every=True, ir=False):
    scores=np.zeros(games)
    for i in range(games):
        
        game=Yahtzee(strategy, every)
        
        scores[i]=game.play_game()
    
    if not ir:
        plt.hist(scores, bins=15)
        plt.xlabel("Game Score")
        plt.ylabel("# of Games")
        plt.axvline(scores.mean(), label='Average Game Score', color='black')
        plt.legend()
        if every:
            plt.title(f"Yahtzee Scores with Strategy: '{strategy}' & Check Between Rolls")
        else:
            plt.title(f"Yahtzee Scores with Strategy: '{strategy}' & Not Checking Between Rolls")
        plt.show()
        
        print(f"Average score with '{strategy}' strategy and check in between rolls= {every}: {scores.mean()}")
        print(f"Standard Deviation of Scores with '{strategy}' strategy and check in between rolls= {every}: {scores.std()}")
        
    else:
        return scores.mean()



strategies=["Upper", "Lower"]
every=[True, False]

for strat in strategies:
    for ev in every:
        run_and_plot(strat, 1000, ev)

        
## Independent Replications

for strat in strategies:
    for ev in every:
        means=np.zeros(50)
        for i in range(50):
            means[i]= run_and_plot(strat, games=200, every=ev, ir=True)
            
        plt.hist(means, bins=10)
        plt.xlabel("Game Score")
        plt.ylabel("# of Games")
        plt.axvline(means.mean(), label='Average Game Score', color='black')
        plt.legend()
        if ev:
            plt.title(f"Yahtzee Scores with Strategy: '{strat}' & Check Between Rolls")
        else:
            plt.title(f"Yahtzee Scores with Strategy: '{strat}' & Not Checking Between Rolls")
        plt.show()
        
        print(f"Average score with '{strat}' strategy and check in between rolls= {ev}: {means.mean()}")
        print(f"Standard Deviation of Scores with '{strat}' strategy and check in between rolls= {ev}: {means.std()}")

