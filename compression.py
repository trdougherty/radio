import pandas as pd

def compress(sweep):
    # This first segment is attempting to compress all of the objects into categorical variables
    cat_columns = sweep.select_dtypes(['object']).columns
    sweep[cat_columns] = sweep[cat_columns].apply(lambda x: x.astype('category'))

    # Weird case of dealing with this
    sweep = sweep.astype({"hz_bin":"int32"})

    # Manage all of the float values
    float_cols = sweep.select_dtypes(['float64']).columns
    sweep[float_cols] = sweep[float_cols].apply(lambda x: x.astype('float16'))

    # Manage all of the int values
    int_cols = sweep.select_dtypes(['int64']).columns
    sweep[int_cols] = sweep[int_cols].apply(lambda x: x.astype('int32'))
    return sweep