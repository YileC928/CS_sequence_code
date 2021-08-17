'''
Linear regression

Yile Chen

Main file for linear regression and model selection.
'''

import numpy as np
from sklearn.model_selection import train_test_split
import util


class DataSet(object):
    '''
    Class for representing a data set.
    '''

    def __init__(self, dir_path):
        '''
        Class for representing a dataset, performs train/test
        splitting.

        Inputs:
            dir_path: (string) path to the directory that contains the
              file
        '''

        parameters_dict = util.load_json_file(dir_path, "parameters.json")
        self.pred_vars = parameters_dict["predictor_vars"]
        self.name = parameters_dict["name"]
        self.dependent_var = parameters_dict["dependent_var"]
        self.training_fraction = parameters_dict["training_fraction"]
        self.seed = parameters_dict["seed"]
        self.labels, data = util.load_numpy_array(dir_path, "data.csv")
        self.training_data, self.testing_data = train_test_split(data,
            train_size=self.training_fraction, test_size=None,
            random_state=self.seed)

class Model(object):
    '''
    Class for representing a model.
    '''

    def __init__(self, dataset, pred_vars):
        '''
        Construct a data structure to hold the model.
        Inputs:
            dataset: an dataset instance
            pred_vars: a list of the indices for the columns (of the
              original data array) used in the model.
        '''

        # REPLACE pass WITH YOUR CODE
        self.dataset = dataset
        self.pred_vars = pred_vars
        self.dep_var = dataset.dependent_var

        predictors = dataset.training_data[:, self.pred_vars]
        X = util.prepend_ones_column(predictors)
        y = dataset.training_data[:, self.dep_var]
        self.beta = util.linear_regression(X, y)
        y_pred = util.apply_beta(self.beta, X)
        self.R2 = 1 - np.sum((y-y_pred)**2)/np.sum((y-np.average(y))**2)

        predictors_test = dataset.testing_data[:, self.pred_vars]
        X_test = util.prepend_ones_column(predictors_test)
        y_test = dataset.testing_data[:, self.dep_var]
        y_pred_test = util.apply_beta(self.beta, X_test)
        self.R2_test = 1 - np.sum((y_test-y_pred_test)**2)/np.sum((y_test-np.average(y_test))**2)


    def __repr__(self):
        '''
        Format model as a string.
        '''

        # Replace this return statement with one that returns a more
        # helpful string representation
        
        formula = []
        for i in range(1, len(self.beta)):
            formula.append("+ {} * {}".format(self.beta[i], self.dataset.labels[self.pred_vars[i-1]]))
        name_dep_var = "{} ~ ".format(self.dataset.labels[self.dep_var])
        return name_dep_var + "{}".format(self.beta[0]) + " ".join(formula)
        #"{:.6f}".format(self.beta)
        #return "!!! You haven't implemented the Model __repr__ method yet !!!"

    ### Additional methods here


def compute_single_var_models(dataset):
    '''
    Computes all the single-variable models for a dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        List of Model objects, each representing a single-variable model
    '''

    # Replace [] with the list of models
    lst_models = []
    for i in dataset.pred_vars:
        lst_models.append(Model(dataset, [i]))
    return lst_models


def compute_all_vars_model(dataset):
    '''
    Computes a model that uses all the predictor variables in the dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object that uses all the predictor variables
    '''

    # Replace None with a model object
    return Model(dataset, dataset.pred_vars)


def compute_best_pair(dataset):
    '''
    Find the bivariate model with the best R2 value

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object for the best bivariate model
    '''

    # Replace None with a model object
    dict_models = {}
    R2_max = 0
    for a in dataset.pred_vars:
        for b in dataset.pred_vars:
            if a != b:
                bi_pred_vars = [a, b]
                model = Model(dataset, bi_pred_vars)
                dict_models[model.R2] = model
                if model.R2 > R2_max:
                    R2_max = model.R2

    return dict_models[R2_max]


def forward_selection(dataset):
    '''
    Given a dataset with P predictor variables, uses forward selection to
    select models for every value of K between 1 and P.

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A list (of length P) of Model objects. The first element is the
        model where K=1, the second element is the model where K=2, and so on.
    '''
    max_R2 = 0
    pred_vars_used = []
    pred_var = []
    lst_models = []
    for k in range(len(dataset.pred_vars)):
        dict_models = {}
        for var in dataset.pred_vars:
            if var not in pred_vars_used:
                pred_var = pred_vars_used.copy()
                pred_var.append(var)
                model = Model(dataset, pred_var)
                dict_models[model.R2] = model
                if model.R2 > max_R2:
                    max_R2 = model.R2

        lst_models.append(dict_models[max_R2])
        pred_vars_used = (dict_models[max_R2].pred_vars)

    return lst_models


def validate_model(dataset, model):
    '''
    Given a dataset and a model trained on the training data,
    compute the R2 of applying that model to the testing data.

    Inputs:
        dataset: (DataSet object) a dataset
        model: (Model object) A model that must have been trained
           on the dataset's training data.

    Returns:
        (float) An R2 value
    '''

    # Replace 0.0 with the correct R2 value
    return model.R2_test
