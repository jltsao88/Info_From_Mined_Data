#! python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 16:00:17 2019

@author: jltsa
"""
import sys
import pandas as pd

def main():
    """
    Calulates the precision, recall, accuracy and f1 scores for
    the predictions of a model against its validator.
    
    Prints out results to console.  Does not return any values.
    
    pred_file: .csv of the predication results
    val_file: .csv of the validation results
    
    To run this file path into the directory containing this script
    metrics.py, APPAREL_ids_1_2019.csv, and APPAREL_ODOM_1_2019.csv
    
    type python metrics.py APPAREL_ids_1_2019.csv APPAREL_ODOM_1_2019.csv
    into command prompt
    """
    script = sys.argv[0]
    #csv file containing model predictions
    pred_file = sys.argv[1]
    #csv file containing validation results
    val_file = sys.argv[2]

    #Prediction Set
    model_df = pd.read_csv(pred_file)
    #Human Validator Set
    human_df = pd.read_csv(val_file)
            
    #Remove Rows from model_df not in human_df
    model_df = model_df[model_df._id.isin(list(human_df._id))]
    #Reset index of model
    model_df.reset_index(inplace=True)
    
    #Get confusion matrices for theme_exists
    fit_exists_mat = confuse_mat_exists(model_df, human_df, 'fit_theme_exists')
    quality_exists_mat = confuse_mat_exists(model_df, human_df, 'quality_theme_exists')
    style_exists_mat = confuse_mat_exists(model_df, human_df, 'style_theme_exists')
    use_exists_mat = confuse_mat_exists(model_df, human_df, 'use_theme_exists')
    value_exists_mat = confuse_mat_exists(model_df, human_df, 'value_theme_exists')
    
    #Store matrices in a list
    exists_mats = [fit_exists_mat, quality_exists_mat, style_exists_mat,
                   use_exists_mat, value_exists_mat]
    
    #Get confusion matrices for theme_sentiment_label
    fit_sentiment_mat = confuse_mat_label(model_df, human_df, 'fit_sentiment_label')
    quality_sentiment_mat = confuse_mat_label(model_df, human_df, 'quality_sentiment_label')
    style_sentiment_mat = confuse_mat_label(model_df, human_df, 'style_sentiment_label')
    use_sentiment_mat = confuse_mat_label(model_df, human_df, 'use_sentiment_label')
    value_sentiment_mat = confuse_mat_label(model_df, human_df, 'value_sentiment_label')
    
    #Store matrices in a list
    sent_mats = [fit_sentiment_mat, quality_sentiment_mat, style_sentiment_mat,
                 use_sentiment_mat, value_sentiment_mat]
    
    #list of theme labels
    #padding soem whitespace to format print out better
    theme_labels = ['fit    ', 'quality', 'style  ', 'use    ', 'value  ']
    
    #Print heading with padding
    print("                  Theme_Exists Theme_Sentiment")
    
    #Loop over matrices and theme labels to calculate and print accuracy scores
    for exists_mat, sent_mat, lab in list(zip(exists_mats, sent_mats, theme_labels)):
        exists_acc = accuracy_score(exists_mat)
        sent_acc = accuracy_score(sent_mat)
        print(f'Accuracy {lab} : {exists_acc:.6f}    {sent_acc:.6f}')
    
    #Loop over matrices and theme labels to calculate and print f1 scores
    for exists_mat, sent_mat, lab in list(zip(exists_mats, sent_mats, theme_labels)):
        exists_recall = recall_score(exists_mat)
        sent_recall = recall_score(sent_mat)
        exists_prec = precision_score(exists_mat)
        sent_prec = precision_score(sent_mat)
        exists_f1 = f1_score(exists_prec, exists_recall)
        sent_f1 = f1_score(sent_prec, sent_recall)
        print(f'F-Measure {lab}: {exists_f1:.6f}    {sent_f1:.6f}')
    
    #Loop over matrices and theme labels to calculate and print precision scores
    for exists_mat, sent_mat, lab in list(zip(exists_mats, sent_mats, theme_labels)):
        exists_prec = precision_score(exists_mat)
        sent_prec = precision_score(sent_mat)
        print(f'Precision {lab}: {exists_prec:.6f}    {sent_prec:.6f}')
    
    #Loop over matrices and theme labels to calculate and print recall scores
    for exists_mat, sent_mat, lab in list(zip(exists_mats, sent_mats, theme_labels)):
        exists_recall = recall_score(exists_mat)
        sent_recall = recall_score(sent_mat)
        print(f'Recall {lab}   : {exists_recall:.6f}    {sent_recall:.6f}')
    

    
def make_confuse_mat(tp, tn, fp, fn):
    #Returns a 2x2 matrix
    #[[true positve, false positive], [false negative, true negative]]
    return [[tp, fp],
            [fn, tn]]
    
def confuse_mat_label(df_pred, df_val, label):
    """
    Creates a confusion 2x2 matrix
    [[true positve, false positive], [false negative, true negative]]
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    
    for pred, val in list(zip(df_pred[label], df_val[label])):
        if pred == 'pos' and val == 'pos':
            tp += 1
        elif pred == 'neg' and val == 'neg':
            tn += 1
        elif pred == 'pos' and val == 'neg':
            fp += 1
        elif pred == 'neg' and val =='pos':
            fn += 1
    return make_confuse_mat(tp, tn, fp, fn)

def confuse_mat_exists(df_pred, df_val, label):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    
    for pred, val in list(zip(df_pred[label], df_val[label])):
        if pred == 1 and val == 1:
            tp += 1
        elif pd.isnull(pred) == True and val == 0:
            tn += 1
        elif pred == 1 and val == 0:
            fp += 1
        elif pd.isnull(pred) == True and val == 1:
            fn += 1
    return make_confuse_mat(tp, tn, fp, fn)

def accuracy_score(mat):
    #takes in argument as a 2x2 confonsion matrix per Task3 request
    #[[true positve, false positive], [false negative, true negative]]
    #accurancy = (TP + TN) / (TP + TN + FP + FN)
    
    return (mat[0][0] + mat[1][1]) / (mat[0][0] + mat[1][1] + mat[0][1] + mat[1][0])

def precision_score(mat):
    #takes in argument as a 2x2 confonsion matrix per Task3 request
    #[[true positve, false positive], [false negative, true negative]]
    #precision = (TP) / (TP + FP)
    #Answers what proportion of positive identifications were actually correct
    
    return (mat[0][0]) / (mat[0][0] + mat[0][1])

def recall_score(mat):
    #takes in argument as a 2x2 confonsion matrix per Task3 request
    #[[true positve, false positive], [false negative, true negative]]
    #recall = (TP) / (TP + FN)
    #Answers what proportion of actual positives was identified correctly
    
    return (mat[0][0]) / (mat[0][0] + mat[1][0])

def f1_score(precision, recall):
    #takes in argument as a 2x2 confonsion matrix per Task3 request
    #[[true positve, false positive], [false negative, true negative]]
    #recall = 2 x ((precision x recall)/(precision + recall))
    #harmonic mean of precision and recall
    
    return 2*((precision*recall)/(precision+recall))

if __name__ == '__main__':
    main()