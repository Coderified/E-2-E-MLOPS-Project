from scipy.stats import randint

RF_PARAMS ={
    'n_estimators': randint(100,500), 
    'max_depth': randint(10,50), 
    'min_samples_split': randint(2,10), 
    'min_samples_leaf': randint(1,5), 
    'bootstrap': [True,False] 
} 

RANDOMSEARCH_PARAMS = {"n_iter":5,
                     "n_jobs":-1,
                     "cv":3,
                     "verbose":2,
                     "scoring":'accuracy'
                     }