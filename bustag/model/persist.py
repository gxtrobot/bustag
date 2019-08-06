'''
persist model required files
'''
import pickle


def dump_model(path, models):
    '''
    Args:
        models: tuple of models to save
    '''
    with open(path, 'wb') as f:
        pickle.dump(models, f)


def load_model(path):
    with open(path, 'rb') as f:
        models = pickle.load(f)
    return models
