import pytest

from acme.refined_function import RefinedFunction


@pytest.fixture()
def parsed_docstring():
    return {'name': 'AdaBoostClassifier',
            'type': 'class',
            'short_description': 'An AdaBoost classifier.',
            'long_description': 'An AdaBoost [1] classifier is a meta-estimator that begins by fitting a\nclassifier on the original dataset and then fits '
                                'additional copies of the\nclassifier on the same dataset but where the weights of incorrectly\nclassified instances are '
                                'adjusted such that subsequent classifiers focus\nmore on difficult cases.\n\nThis class implements the algorithm known as '
                                'AdaBoost-SAMME [2].\n\nRead more in the :ref:`User Guide <adaboost>`.\n\n.. versionadded:: 0.14',
            'functions': {'__init__': {'name': '__init__',
                                       'type': 'fun',
                                       'short_description': 'An AdaBoost classifier.',
                                       'long_description': 'An AdaBoost [1] classifier is a meta-estimator that begins by fitting a\nclassifier on the '
                                                           'original dataset and then fits additional copies of the\nclassifier on the same dataset but where '
                                                           'the weights of incorrectly\nclassified instances are adjusted such that subsequent classifiers '
                                                           'focus\nmore on difficult cases.\n\nThis class implements the algorithm known as AdaBoost-SAMME ['
                                                           '2].\n\nRead more in the :ref:`User Guide <adaboost>`.\n\n.. versionadded:: 0.14',
                                       'params': [{'name': 'self', 'description': '', 'type': None},
                                                  {'name': 'base_estimator',
                                                   'description': 'The base estimator from which the boosted ensemble is built.\nSupport for sample weighting '
                                                                  'is required, as well as proper\n``classes_`` and ``n_classes_`` attributes. If ``None``, '
                                                                  'then\nthe base estimator is :class:`~sklearn.tree.DecisionTreeClassifier`\ninitialized '
                                                                  'with `max_depth=1`.',
                                                   'type': object,
                                                   'default': None},
                                                  {'name': 'n_estimators',
                                                   'description': 'The maximum number of estimators at which boosting is terminated.\nIn case of perfect fit, '
                                                                  'the learning procedure is stopped early.',
                                                   'type': object,
                                                   'default': 50},
                                                  {'name': 'learning_rate',
                                                   'description': 'Weight applied to each classifier at each boosting iteration. A higher\nlearning rate '
                                                                  'increases the contribution of each classifier. There is\na trade-off between the '
                                                                  '`learning_rate` and `n_estimators` parameters.',
                                                   'type': object,
                                                   'default': 1.0},
                                                  {'name': 'algorithm',
                                                   'description': "If 'SAMME.R' then use the SAMME.R real boosting algorithm.\n``base_estimator`` must "
                                                                  "support calculation of class probabilities.\nIf 'SAMME' then use the SAMME discrete "
                                                                  "boosting algorithm.\nThe SAMME.R algorithm typically converges faster than SAMME,"
                                                                  "\nachieving a lower test error with fewer boosting iterations.",
                                                   'type': object,
                                                   'default': 'SAMME.R'},
                                                  {'name': 'random_state',
                                                   'description': 'Controls the random seed given at each `base_estimator` at each\nboosting '
                                                                  'iteration.\nThus, it is only used when `base_estimator` exposes a `random_state`.\nPass an '
                                                                  'int for reproducible output across multiple function calls.\nSee :term:`Glossary '
                                                                  '<random_state>`.',
                                                   'type': object,
                                                   'default': None}],
                                       'returns': None},
                          'decision_function': {'name': 'decision_function',
                                                'type': 'fun',
                                                'short_description': 'Compute the decision function of ``X``.',
                                                'long_description': None,
                                                'params': [{'name': 'self', 'description': '', 'type': None},
                                                           {'name': 'X',
                                                            'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, '
                                                                           'or LIL. COO, DOK, and LIL are converted to CSR.',
                                                            'type': object}],
                                                'returns': {'name': 'score',
                                                            'description': 'The decision function of the input samples. The order of\noutputs is the same of '
                                                                           'that of the :term:`classes_` attribute.\nBinary classification is a special cases '
                                                                           'with ``k == 1``,\notherwise ``k==n_classes``. For binary classification,'
                                                                           '\nvalues closer to -1 or 1 mean more like the first or second\nclass in '
                                                                           '``classes_``, respectively.',
                                                            'type': object}},
                          'fit': {'name': 'fit',
                                  'type': 'fun',
                                  'short_description': 'Build a boosted classifier from the training set (X, y).',
                                  'long_description': None,
                                  'params': [{'name': 'self', 'description': '', 'type': None},
                                             {'name': 'X',
                                              'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, or LIL. COO, DOK, '
                                                             'and LIL are converted to CSR.',
                                              'type': object},
                                             {'name': 'y',
                                              'description': 'The target values (class labels).',
                                              'type': object},
                                             {'name': 'sample_weight',
                                              'description': 'Sample weights. If None, the sample weights are initialized to\n``1 / n_samples``.',
                                              'type': object,
                                              'default': None}],
                                  'returns': {'name': 'self',
                                              'description': 'Fitted estimator.',
                                              'type': object}},
                          'get_params': {'name': 'get_params',
                                         'type': 'fun',
                                         'short_description': 'Get parameters for this estimator.',
                                         'long_description': None,
                                         'params': [{'name': 'self', 'description': '', 'type': None},
                                                    {'name': 'deep',
                                                     'description': 'If True, will return the parameters for this estimator and\ncontained subobjects that '
                                                                    'are estimators.',
                                                     'type': object,
                                                     'default': True}],
                                         'returns': {'name': 'params',
                                                     'description': 'Parameter names mapped to their values.',
                                                     'type': object}},
                          'predict': {'name': 'predict',
                                      'type': 'fun',
                                      'short_description': 'Predict classes for X.',
                                      'long_description': 'The predicted class of an input sample is computed as the weighted mean\nprediction of the '
                                                          'classifiers in the ensemble.',
                                      'params': [{'name': 'self', 'description': '', 'type': None},
                                                 {'name': 'X',
                                                  'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, or LIL. COO, DOK, '
                                                                 'and LIL are converted to CSR.',
                                                  'type': object}],
                                      'returns': {'name': 'y',
                                                  'description': 'The predicted classes.',
                                                  'type': object}},
                          'predict_log_proba': {'name': 'predict_log_proba',
                                                'type': 'fun',
                                                'short_description': 'Predict class log-probabilities for X.',
                                                'long_description': 'The predicted class log-probabilities of an input sample is computed as\nthe weighted '
                                                                    'mean predicted class log-probabilities of the classifiers\nin the ensemble.',
                                                'params': [{'name': 'self', 'description': '', 'type': None},
                                                           {'name': 'X',
                                                            'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, '
                                                                           'or LIL. COO, DOK, and LIL are converted to CSR.',
                                                            'type': object}],
                                                'returns': {'name': 'p',
                                                            'description': 'The class probabilities of the input samples. The order of\noutputs is the same '
                                                                           'of that of the :term:`classes_` attribute.',
                                                            'type': object}},
                          'predict_proba': {'name': 'predict_proba',
                                            'type': 'fun',
                                            'short_description': 'Predict class probabilities for X.',
                                            'long_description': 'The predicted class probabilities of an input sample is computed as\nthe weighted mean '
                                                                'predicted class probabilities of the classifiers\nin the ensemble.',
                                            'params': [{'name': 'self', 'description': '', 'type': None},
                                                       {'name': 'X',
                                                        'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, or LIL. COO, '
                                                                       'DOK, and LIL are converted to CSR.',
                                                        'type': object}],
                                            'returns': {'name': 'p',
                                                        'description': 'The class probabilities of the input samples. The order of\noutputs is the same of '
                                                                       'that of the :term:`classes_` attribute.',
                                                        'type': object}},
                          'score': {'name': 'score',
                                    'type': 'fun',
                                    'short_description': 'Return the mean accuracy on the given test data and labels.',
                                    'long_description': 'In multi-label classification, this is the subset accuracy\nwhich is a harsh metric since you '
                                                        'require for each sample that\neach label set be correctly predicted.',
                                    'params': [{'name': 'self', 'description': '', 'type': None},
                                               {'name': 'X', 'description': 'Test samples.', 'type': object},
                                               {'name': 'y', 'description': 'True labels for `X`.', 'type': object},
                                               {'name': 'sample_weight',
                                                'description': 'Sample weights.',
                                                'type': object,
                                                'default': None}],
                                    'returns': {'name': 'score',
                                                'description': 'Mean accuracy of ``self.predict(X)`` wrt. `y`.',
                                                'type': object}},
                          'set_params': {'name': 'set_params',
                                         'type': 'fun',
                                         'short_description': 'Set the parameters of this estimator.',
                                         'long_description': "The method works on simple estimators as well as on nested objects\n(such as "
                                                             ":class:`~sklearn.pipeline.Pipeline`). The latter have\nparameters of the form "
                                                             "``<component>__<parameter>`` so that it's\npossible to update each component of a nested object.",
                                         'params': [{'name': 'self', 'description': '', 'type': None},
                                                    {'name': 'params', 'description': '', 'type': None}],
                                         'returns': {'name': 'self',
                                                     'description': 'Estimator instance.',
                                                     'type': object}},
                          'staged_decision_function': {'name': 'staged_decision_function',
                                                       'type': 'fun',
                                                       'short_description': 'Compute decision function of ``X`` for each boosting iteration.',
                                                       'long_description': 'This method allows monitoring (i.e. determine error on testing set)\nafter each '
                                                                           'boosting iteration.',
                                                       'params': [{'name': 'self', 'description': '', 'type': None},
                                                                  {'name': 'X',
                                                                   'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, '
                                                                                  'or LIL. COO, DOK, and LIL are converted to CSR.',
                                                                   'type': object}],
                                                       'returns': {'name': 'score',
                                                                   'description': 'The decision function of the input samples. The order of\noutputs is the '
                                                                                  'same of that of the :term:`classes_` attribute.\nBinary classification is '
                                                                                  'a special cases with ``k == 1``,\notherwise ``k==n_classes``. For binary '
                                                                                  'classification,\nvalues closer to -1 or 1 mean more like the first or '
                                                                                  'second\nclass in ``classes_``, respectively.',
                                                                   'type': object}},
                          'staged_predict': {'name': 'staged_predict',
                                             'type': 'fun',
                                             'short_description': 'Return staged predictions for X.',
                                             'long_description': 'The predicted class of an input sample is computed as the weighted mean\nprediction of the '
                                                                 'classifiers in the ensemble.\n\nThis generator method yields the ensemble prediction after '
                                                                 'each\niteration of boosting and therefore allows monitoring, such as to\ndetermine the '
                                                                 'prediction on a test set after each boost.',
                                             'params': [{'name': 'self', 'description': '', 'type': None},
                                                        {'name': 'X',
                                                         'description': 'The input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, or LIL. COO, DOK, '
                                                                        'and LIL are converted to CSR.',
                                                         'type': object}],
                                             'returns': {'name': 'y',
                                                         'description': 'The predicted classes.',
                                                         'type': object}},
                          'staged_predict_proba': {'name': 'staged_predict_proba',
                                                   'type': 'fun',
                                                   'short_description': 'Predict class probabilities for X.',
                                                   'long_description': 'The predicted class probabilities of an input sample is computed as\nthe weighted '
                                                                       'mean predicted class probabilities of the classifiers\nin the ensemble.\n\nThis '
                                                                       'generator method yields the ensemble predicted class probabilities\nafter each '
                                                                       'iteration of boosting and therefore allows monitoring, such\nas to determine the '
                                                                       'predicted class probabilities on a test set after\neach boost.',
                                                   'params': [{'name': 'self', 'description': '', 'type': None},
                                                              {'name': 'X',
                                                               'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, '
                                                                              'or LIL. COO, DOK, and LIL are converted to CSR.',
                                                               'type': object}],
                                                   'returns': None},
                          'staged_score': {'name': 'staged_score',
                                           'type': 'fun',
                                           'short_description': 'Return staged scores for X, y.',
                                           'long_description': 'This generator method yields the ensemble score after each iteration of\nboosting and '
                                                               'therefore allows monitoring, such as to determine the\nscore on a test set after each boost.',
                                           'params': [{'name': 'self', 'description': '', 'type': None},
                                                      {'name': 'X',
                                                       'description': 'The training input samples. Sparse matrix can be CSC, CSR, COO,\nDOK, or LIL. COO, '
                                                                      'DOK, and LIL are converted to CSR.',
                                                       'type': object},
                                                      {'name': 'y', 'description': 'Labels for X.', 'type': object},
                                                      {'name': 'sample_weight',
                                                       'description': 'Sample weights.',
                                                       'type': object,
                                                       'default': None}],
                                           'returns': {'name': 'z', 'description': None, 'type': object}}}}


class TestRefinedFunction:
    def test_load_docstring(self, parsed_docstring):
        refined_function = RefinedFunction("sklearn.ensemble", "BINARY_CLASSIFICATION", parsed_docstring)
        assert refined_function.module_name == "AdaBoostClassifier"
        assert refined_function.parameters[0] == {'name': 'self', 'description': '', 'type': None, 'default_value': None}
