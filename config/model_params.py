from scipy.stats import randint, uniform

LGB_PARAMS ={
    'n_estimators':randint(100,500),
    'max_depth' : randint(5,50),
    'learning_rate': uniform(0.01,0.2),
    'num_leaves': randint(20,100),
    'force_row_wise':True,
    'boosting_type' : ['gbdt' , 'dart' , 'goss']
} 

RANDOMSEARCH_PARAMS = {"n_iter":5,
                     "n_jobs":-1,
                     "cv":3,
                     "verbose":2,
                     "scoring":'accuracy'
                     }