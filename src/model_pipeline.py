# http://scikit-learn.org/stable/auto_examples/covariance/plot_outlier_detection.html#sphx-glr-auto-examples-covariance-plot-outlier-detection-py
# GOOD DISCUSSION OF ONE CLASS SVMs: http://rvlasveld.github.io/blog/2013/07/12/introduction-to-one-class-support-vector-machines/
# ISOLATION FOREST:
# http://stackoverflow.com/questions/43063031/how-to-use-isolation-forest
# https://perso.telecom-paristech.fr/~goix/nicolas_goix_osi_presentation.pdf
#
'''
ADD IN KNN
'''
# import cPickle as pickle
from sklearn.covariance import EllipticEnvelope
from sklearn import ensemble
from sklearn.ensemble import IsolationForest
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn import svm


class ModelPipeline(object):

    def __init__(self, X=None, y=None):
        self.X = X
        self.y = y

    def run_unary_classifiers(self):
        '''Run data through pipeline of classifier models.

        INPUT: numpy array of RGB values from jpgs
        OUTPUT: not sure what yet from models
        '''
        # set models to run in pipeline...use default params first
        neigh = NearestNeighbors(n_neighbors=1)
        oneclasssvm = svm.OneClassSVM()
        isolationforest = IsolationForest()
        robust_covar = EllipticEnvelope()

        # save down sequence of models to run for future reference
        model_sequence = ['nn', 'oneclasssvm', 'isolationforest', 'robust_covar']
        # define a pipeline
        pipe = Pipeline([('oneclasssvm', oneclasssvm),
                        ('isolationforest', isolationforest),
                        ('robust_covar', robust_covar)])
        # fit models with train set
        pipe.fit(self.X)
        pipe.transform(self.X)
        f1scores = cross_val_score(pipe, self.X, self.y,
                                   cv=3, scoring='f1_weighted')
        f1results = zip(model_sequence, f1scores)
        recallscores = cross_val_score(pipe, self.X, self.y,
                                       cv=3, scoring='recall_weighted')
        recallresults = zip(model_sequence, recallscores)
        precisionscores = cross_val_score(pipe, self.X, self.y,
                                          cv=3, scoring='precision_weighted')
        precisionresults = zip(model_sequence, precisionscores)
        return f1results, recallresults, precisionresults

    def predict(self, X_test, y_test):
        X_all_training = self.X.append(X_test, ignore_index=True)
        y_all_training = self.y.append(y_test, ignore_index=True)
        randomforest = ensemble.RandomForestClassifier(max_depth=1,
                                                       max_features='auto',
                                                       n_estimators=150)
        randomforest.fit(X_all_training, y_all_training)
        f1scores = cross_val_score(randomforest,
                                   X_all_training, y_all_training,
                                   cv=5, scoring='f1_weighted')
        recallscores = cross_val_score(randomforest,
                                       X_all_training, y_all_training,
                                       cv=5, scoring='f1_weighted')
        precisionscores = cross_val_score(randomforest, X_all_training,
                                          y_all_training, cv=5,
                                          scoring='f1_weighted')
        print("f1:", f1scores,
              "recall:", recallscores,
              "precision:", precisionscores)

        # pickle randomforest fitted model and return that
        with open('data/final_model.pkl', 'w') as f:
            pickle.dump(randomforest, f)
        return "pickled model saved in data/final_model.pkl"

    def parameter_tuning(self, pipeline, params):
        # set models to run in pipeline
        sgd = linear_model.SGDClassifier(loss='log',
                                         learning_rate='optimal', penalty='l1')
        svc = LinearSVC()
        randomforest = ensemble.RandomForestClassifier()
        adaboost = ensemble.AdaBoostClassifier()
        pipeline = Pipeline([('sgd', sgd),
                            ('svc', svc),
                            ('randomforest', randomforest),
                            ('adaboost', adaboost)])
        params = dict(sgd__alpha=[0.0001, 0.001, 0.01],
                      svc__C=[1, 10],
                      randomforest__n_estimators=[150, 300, 450],
                      randomforest__max_depth=[1, 3, None],
                      randomforest__max_features=['auto', 'sqrt', 'log2'],
                      adaboost__n_estimators=[50, 100, 150],
                      adaboost__learning_rate=[0.5, 0.75, 1.0])
        gscv = GridSearchCV(pipeline,
                            params,
                            n_jobs=-1,
                            verbose=True,
                            cv=3,
                            scoring='recall_weighted')
        gscv.fit(self.X, self.y)
        best_model = gscv.best_estimator_
        best_params = gscv.best_params_
        best_recall_score = gscv.best_score_
        return best_model, best_params, best_recall_score

    def get_baseline_scores(self):
        '''Calculate baseline scores.

        inputs: cleaned/engineered df and ylabel name
        outputs: list of baseline scores (precision, recall, f1)
        '''
        y_true = self.y
        self.X['yhat_baseline'] = 1
        y_pred = self.X['yhat_baseline']
        baseline_precision = metrics.precision_score(y_true, y_pred)
        baseline_recall = metrics.recall_score(y_true, y_pred)
        baseline_f1 = metrics.f1_score(y_true, y_pred)
        return([('baseline_precision', baseline_precision),
               ('baseline_recall', baseline_recall),
               ('baseline_f1', baseline_f1)])
