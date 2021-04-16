#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd

'''
Scanned tweets containing one or more of the *Keywords below will be returned
'''


elephantRhinoKeywords = ['ivory', 'horn', 'tusk', 'carved', 'mammoth', 'antique',
            'african material', 'african materials', 'trophy', 'bone', 'medicine', 
            'medicinal', 'authentic', 'skull', 'decorative', 'wild']

pangolinKeywords = ['pangolin', 'scales', 'exotic', 'trophy', 'dragon',
                    'delicacy', 'medicine', 'medicinal', 'authentic', 'antique',
                    'african material', 'yellow material', 'african materials',
                    'decorative', 'live', 'wild']

catKeywords = ['skin', 'fur', 'pelt', 'taxidermy', 'rug', 'hide',
            'bone', 'meat', 'delicacy', 'medicine', 'medicinal', 'live',
            'authentic', 'leopard', 'tiger', 'claw', 'claws', 'tooth', 'teeth',
            'skull', 'bone', 'decorative', 'trophy', 'paw', 'paws', 'wild']

bearKeywords = ['skin', 'fur', 'pelt', 'taxidermy', 'rug', 'hide',
            'bone', 'meat', 'delicacy', 'medicine', 'medicinal', 'live',
            'authentic', 'bear', 'cub', 'bearcub', 'wild', 'claw', 'claws', 'tooth', 'teeth',
            'skull', 'bone', 'decorative', 'trophy', 'paw', 'paws']

turtlesKeywords = ['turtle', 'tortoise', 'turtle eggs', 'tortoise eggs', 'eggs',
                  'shell', 'delicacy', 'medicine', 'medicinal', 'live', 'decorative',
                  'authentic', 'wild']

birdKeywords = ['bill', 'casque', 'casques', 'beak', 'feathered', 'horn', 'decorative',
                'carved', 'authentic', 'live', 'egg', 'eggs', 'wild']

generalKeywords = ['sale', 'selling', 'price']


def add_tweet(animalType):
    
    ''' 
    possible animalType values are "bears", "birds", "cats", "pangolins",
    "turtles", "elephant_rhino"
    
    This function inserts a tweet into the animalType MySQL database.
    '''
    
    return ("INSERT INTO {}"
            "(tweetID, image, followers, location,"
            "text, tweetTime, coordinates)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)").format(animalType.upper())


def create_dataframe(table,dbConnection):
    
    '''
    This function selects all data from the the designated table and stores
    the returned values into a pandas dataframe.
    '''
    
    try:
        df = pd.read_sql(("SELECT * FROM {}").format(table.upper()),dbConnection)
        dbConnection.close()
        return df
        
    except Exception as e:
        dbConnection.close()
        print(str(e))
        
        
    