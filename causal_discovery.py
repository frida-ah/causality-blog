import pandas as pd

df = pd.read_excel("./data/output/data.xlsx")
df = df[
    [
        "date",
        "searches",
        "duration_sunshine",
        # "duration_rainfall",
        "daily_avg_temperature",
    ]
]
df = df.set_index("date")


def apply_directlingam(df):
    import lingam
    from lingam.utils import make_dot

    print(df.columns)
    print(df.dtypes)

    model = lingam.DirectLiNGAM()
    model.fit(df)

    print(model.causal_order_)
    print(len(model.adjacency_matrix_))
    labels = [
        "searches",
        "sun",
        # "rain",
        "temp",
    ]
    dot = make_dot(model.adjacency_matrix_, ignore_shape=True, lower_limit=0.05, labels=labels)
    dot.format = "png"
    dot.render("directlingam")
    dot


apply_directlingam(df)


def apply_varlingam(df):
    import lingam
    from lingam.utils import make_dot
    import numpy as np

    print(df.columns)
    print(df.dtypes)

    model = lingam.VARLiNGAM(lags=1)
    model.fit(df)
    labels = [
        "searches(t)",
        "sun(t)",
        "rain(t)",
        # "temp(t)",
        "searches(t-1)",
        "sun(t-1)",
        "rain(t-1)",
        # "temp(t-1)",
    ]
    print(len(model.adjacency_matrices_))

    dot = make_dot(np.hstack(model.adjacency_matrices_), ignore_shape=True, lower_limit=0.05, labels=labels)
    dot.format = "png"
    dot.render("dag")
    dot


apply_varlingam(df)


def apply_causal_learn_pc(df):
    from causallearn.search.ConstraintBased.PC import pc
    from causallearn.utils.cit import fisherz
    import numpy as np

    data_list = []

    for column in df.columns:
        data_list.append(df[column].to_numpy())

    data = np.array(data_list).T
    print(data_list)
    print(df.columns)
    cg = pc(data, 0.05, fisherz, True, 0, 0)

    cg.draw_pydot_graph()  # visualization using pydot
    # X1: searches
    # X2: temperature
    # X3: rainfall
    # X4: snowfall


apply_causal_learn_pc(df)


def apply_FCI(df):
    from causallearn.search.ConstraintBased.FCI import fci
    from causallearn.utils.GraphUtils import GraphUtils
    import numpy as np
    from causallearn.utils.cit import fisherz

    data_list = []

    for column in df.columns:
        data_list.append(df[column].to_numpy())

    data = np.array(data_list).T
    G = fci(dataset=data, independence_test_method=fisherz, alpha=0.05)
    # visualization
    pdy = GraphUtils.to_pydot(G[0])
    pdy.write_png("FCI.png")


apply_FCI(df)
