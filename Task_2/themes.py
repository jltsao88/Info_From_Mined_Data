#! python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 17:31:52 2019

@author: jltsa
"""
import sys
import pandas as pd

def main():
    """
    script to read in csv file and out analysis on themes
    
    To run script open commond line and path into directory containing
    this script.  Type python themes.py <csv_data>
    Ex) python themes.py APPAREL_ids_1_2019.csv
    
    First argument: path to csv file to load in
    """
    script = sys.argv[0]
    file_path = sys.argv[1]
    
    #read in csv
    df = pd.read_csv(file_path)
    
    #get totals and percentages for each theme
    use_neg, use_pos, use_total = get_theme_totals(df, themes[0][0], themes[0][1])
    use_negp, use_posp = theme_percentages(use_neg, use_pos, use_total)
    
    fit_neg, fit_pos, fit_total = get_theme_totals(df, themes[1][0], themes[1][1])
    fit_negp, fit_posp = theme_percentages(fit_neg, fit_pos, fit_total)
    
    value_neg, value_pos, value_total = get_theme_totals(df, themes[2][0], themes[2][1])
    value_negp, value_posp = theme_percentages(value_neg, value_pos, value_total)
    
    style_neg, style_pos, style_total = get_theme_totals(df, themes[3][0], themes[3][1])
    style_negp, style_posp = theme_percentages(style_neg, style_pos, style_total)
    
    quality_neg, quality_pos, quality_total = get_theme_totals(df, themes[4][0], themes[4][1])
    quality_negp, quality_posp = theme_percentages(quality_neg, quality_pos, quality_total)
    
    #print out analysis
    print(f'OUT OF {len(df)} REVIEWS\n')
    print(f'Use Theme:\n # of total occurances: {use_total},\n # of pos reviews: {use_pos}'+\
          f' | {use_posp}%\n # of neg reviews: {use_neg} | {use_negp}%\n')
    print(f'Fit Theme:\n # of total occurances: {fit_total},\n # of pos reviews: {fit_pos}'+\
          f' | {fit_posp}%\n # of neg reviews: {fit_neg} | {fit_negp}%\n')
    print(f'Value Theme:\n # of total occurances: {value_total},\n # of pos reviews: {value_pos}'+\
          f' | {value_posp}%\n # of neg reviews: {value_neg} | {value_negp}%\n')
    print(f'Style Theme:\n # of total occurances: {style_total},\n # of pos reviews: {style_pos}'+\
          f' | {style_posp}%\n # of neg reviews: {style_neg} | {style_negp}%\n')
    print(f'Quality Theme:\n # of total occurances: {quality_total},\n # of pos reviews: {quality_pos}'+\
          f' | {quality_posp}%\n # of neg reviews: {quality_neg} | {quality_negp}%\n')
    
    
#The Themes    
themes = [('use_sentiment_label', 'use_theme_exists'), ('fit_sentiment_label', 'fit_theme_exists'),
          ('value_sentiment_label', 'value_theme_exists'),('style_sentiment_label', 'style_theme_exists'),
          ('quality_sentiment_label', 'quality_theme_exists')]
    
#function to get neg and pos counts of sentiments
def get_theme_totals(df, sentiment, exists):
    df = df.groupby(sentiment)[exists].sum()
    neg , pos = df['neg'], df['pos']
    total = neg+pos
    return neg, pos, total

#function to get percentages of sentiment label in themes
def theme_percentages(neg, pos, total):
    neg_percent = round(neg/total, 2)
    pos_percent = round(pos/total, 2)
    return neg_percent, pos_percent

if __name__ == '__main__':
    main()