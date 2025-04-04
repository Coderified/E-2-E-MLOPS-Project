from scipy.stats import randint, uniform

LGB_PARAMS ={
    'n_estimators': randint(700,900),
    'max_depth' : randint(5,40),
    'learning_rate': uniform(0.01,0.1),
    'num_leaves': randint(20,80),
    
} 

RANDOMSEARCH_PARAMS = {"n_iter":3,
                     "n_jobs":-1,
                     "cv":3,
                     "verbose":2,
                     "scoring":'accuracy'
                     }