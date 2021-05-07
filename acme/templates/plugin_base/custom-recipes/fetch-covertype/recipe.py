import dataiku
from dataiku.customrecipe import *
import pandas as pd, numpy as np
from sklearn.datasets import fetch_covtype


output_name = get_output_names_for_role('output')[0]
output_dataset = dataiku.Dataset(output_name)

data = fetch_covtype()
x = pd.DataFrame(data.data, columns=None)
y = pd.DataFrame(data.target, columns=['target'])

covertype_classif_df = pd.concat([x, y], axis=1)

output_dataset.write_with_schema(covertype_classif_df)
