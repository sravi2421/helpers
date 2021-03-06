import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import pydotplus


    
def plt_histn(*argv, bins = 25):
    '''
    plots histograms of however many series you provide
    arguments must be provided of the form: series, title, series, title.....
    
    args:
        series(pandas series):     Pandas series to be graphed in a histogram
        title(str):                Title of the associated series        
    '''
    if len(argv)%2!=0:
        assert False, "Must provide an even number of arguments of the form: series1, title1, series2, title2.....etc"
    series_title_pairs = [(arg, argv[2*i+1]) for i, arg in enumerate(argv[::2])]
    fig = plt.gcf()
    num_rows = len(series_title_pairs)//2 + len(series_title_pairs)%2#2 per row
    fig.set_size_inches(18,4*num_rows)
    for i, pair in enumerate(series_title_pairs, 1):
        plt.subplot(num_rows, 2, i)
        plt.hist(pair[0], bins = bins)
        plt.title(pair[1])
    plt.tight_layout()
    plt.show()
    
def plt_metric_by_date(metric_by_date, dates, title, metric_name):
    '''
    plots a metric over a time series
    args:
        metric_by_date(pandas series, or  
                       list of pandas series):     metric of interest, list of metrics of interest
        dates(pandas series):                      dates to plot over
        title(str):                                title
        metric_name(str or list of strs):          name of metric, used for y-axis
                                                   or list of metrics, used by legend
    '''
    formatter = DateFormatter('%m/%d/%y')
    fig, ax = plt.subplots()
    fig.set_size_inches(18,4)

    if type(metric_by_date)==list:
        for metric in metric_by_date:
            plt.plot(dates, metric)
        plt.legend(metric_name, loc=2)
    else:
        plt.plot(dates, metric_by_date)
        plt.ylabel(metric_name)

    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.xlabel('Date')

    plt.title(title)
    plt.show()

    
def plt_categ_cols(categ_counts, categ_cols):
    '''
    plots proportion of categorical values
    
    args:
        categ_counts(pandas df):       a dataframe with the columns, categ_val, categ_prop
        categ_cols(list):              list of columns to plot
    '''
    categ_cols=['device','sex']
    num_rows = len(categ_cols)//2 + len(categ_cols)%2#2 per row
    fig = plt.gcf()
    fig.set_size_inches(18,4*num_rows)

    for i, categ in enumerate(categ_cols, 1):
        plt.subplot(num_rows, 2, i)
        plt.barh(categ_counts[categ+'_val'][::-1],categ_counts[categ+'_prop'][::-1])
        plt.title('{} Column: Proportion of Total'.format(categ))

    plt.show()
    
def visualize_tree(dt, X, warning=True):
    '''
    Takes a decision tree object and generates a visualization
    Args:
        dt (sklearn decision tree):     The subject sklearn decision tree object
        X (pandas df):                  A pandas dataframe containing the X columns used to train 
                                        the decision tree object
        warning (bool):                 Boolean representing whether or not the function asserts an error
                                        on a depth of more than four 
        
    Returns:
        graph (pydotplus.graphviz.Dot): In order to display inline, Image(graph), using the Image function from below
                                        from IPython.display import Image                                  
        
    '''
    if ((dt.max_depth>4)&(warning==True)):
        assert False, 'Decision Tree Depth is {} are you sure you want to visualize?\n If so, set warning argument to False'
    else:
        dot_data = StringIO()
        export_graphviz(dt, out_file=dot_data, 
                        feature_names = list(X.columns),
                        filled=True, rounded=True,
                        special_characters=True)

        graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        return graph
    
    
def plt_coeffs(lr, X):
    '''
    Plot all coefficients of a logistic regression model

    Args:
        lr (sklearn object):  The sklearn logistic regression estimator
        X (pandas dataframe): Pandas dataframe containing the X features for the lr estimator

    Returns:
        None: This function only plots a graph, no return value is provided

    '''
    lr_coeffs = sorted([(column, coef) for column, coef in zip(X.columns, lr.coef_[0])], 
                       key = lambda x: x[1], 
                       reverse = True)

    fig = plt.gcf()
    num_feats = len(lr_coeffs)
    fig.set_size_inches(12, num_feats/2)

    label = [coeff[0] for coeff in lr_coeffs]
    width = [coeff[1] for coeff in lr_coeffs]
    plt.barh(label, width)
    plt.title('Logistic Regression Coefficients')
    plt.xlabel('Coeff. Value')
    plt.ylabel('Feature')
    plt.show()    