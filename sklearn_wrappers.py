import pandas as pd

def rank_models(GCV):
    '''
    for a sklearn gridsearch cv object, returns an ordered dataframe of models, ordered by CV test score
    
    args:
        GCV (sklearn grisearch object)
    
    returns:
        ordered_cv (pandas DataFrame):       a dataframe with columns containing different model parameters
                                             and the model test scores
    '''
    params = {param:[] for param in GCV.cv_results_['params'][0].keys()} #parameters of interest

    for param_set in GCV.cv_results_['params']:
        for curr_param in params.keys():
            params[curr_param].append(param_set[curr_param])

    ordered_cv = (
        pd.DataFrame(data = {**params,'test_score':GCV.cv_results_['mean_test_score']})
        .sort_values('test_score',ascending=False))
    return ordered_cv