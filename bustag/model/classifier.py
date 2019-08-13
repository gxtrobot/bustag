'''
create classifier model and predict
'''
from sklearn.metrics import f1_score, recall_score, accuracy_score, precision_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from bustag.model.prepare import prepare_data, prepare_predict_data
from bustag.model.persist import load_model, dump_model
from bustag.spider.db import RATE_TYPE, ItemRate
from bustag.util import logger

model_path = './data/model/model.pkl'


def create_model():
    knn = KNeighborsClassifier(n_neighbors=11)
    return knn


def predict(X_test):
    model = load_model(model_path)
    y_pred = model.predict(X_test)
    return y_pred


def train():
    model = create_model()
    X_train, X_test, y_train, y_test = prepare_data()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    confusion_mtx = confusion_matrix(y_test, y_pred)
    evaluate(confusion_mtx, y_test, y_pred)
    dump_model(model_path, model)
    logger.info('new model trained')
    return model


def evaluate(confusion_mtx, y_test, y_pred):
    tn, fp, fn, tp = confusion_mtx.ravel()
    logger.info(f'tp: {tp}, fp: {fp}')
    logger.info(f'fn: {fn}, tn: {tn}')
    logger.info(f'accuracy_score: {accuracy_score(y_test, y_pred)}')
    logger.info(f'precision_score: {precision_score(y_test, y_pred)}')
    logger.info(f'recall_score: {recall_score(y_test, y_pred)}')
    logger.info(f'f1_score: {f1_score(y_test, y_pred)}')


def recommend():
    '''
    use trained model to recommend items
    '''
    ids, X = prepare_predict_data()
    count = 0
    total = len(ids)
    y_pred = predict(X)
    for id, y in zip(ids, y_pred):
        if y == 1:
            count += 1
            # print(id, y)
        rate_type = RATE_TYPE.SYSTEM_RATE
        rate_value = y
        item_id = id
        item_rate = ItemRate(rate_type=rate_type,
                             rate_value=rate_value, item_id=item_id)
        item_rate.save()
    return total, count


if __name__ == "__main__":
    total, count = recommend()
    print('total:', total)
    print('recommended:', count)
