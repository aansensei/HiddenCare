# Preprocessing, tuning, and training workflows using scikit-learn.

from typing import Tuple, List, Dict, Any
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, GridSearchCV


# Verify feature matrix contains only permitted predictors.
def assert_predictor_allowlist(df: pd.DataFrame, predictors: List[str]) -> None:
    forbidden = ["a1c", "dx", "seqn", "weight", "psu", "strata", "hiq", "pir", "label_dx", "label_full"]
    for col in forbidden:
        if col in df.columns:
            raise ValueError(f"Target or survey leakage variable found in feature set: {col}")
    missing = [p for p in predictors if p not in df.columns]
    if missing:
        raise ValueError(f"Missing required predictors in feature matrix: {missing}")


# Build preprocessing pipeline with median imputation and scaling.
def build_pipeline(c_value: float = 1.0, seed: int = 42) -> Pipeline:
    num_features = ["age", "bmi", "waist"]
    cat_features = ["sex"]

    num_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    cat_transformer = Pipeline(
        steps=[
            ("encoder", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, num_features),
            ("cat", cat_transformer, cat_features),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "clf",
                LogisticRegression(
                    penalty="l2",
                    C=c_value,
                    solver="lbfgs",
                    max_iter=1000,
                    random_state=seed,
                ),
            ),
        ]
    )
    return pipeline


# Tune regularized logistic regression on training release using stratified cross-validation.
def tune_and_fit_model(
    train_df: pd.DataFrame,
    target_col: str,
    predictors: List[str],
    c_grid: List[float],
    cv_folds: int = 5,
    seed: int = 42,
) -> Tuple[Pipeline, Dict[str, Any]]:
    # Extract predictor matrix and assert no leakage variables are present.
    x_train = train_df[predictors].copy()
    assert_predictor_allowlist(x_train, predictors)
    y_train = train_df[target_col].values.astype(int)

    base_pipe = build_pipeline(seed=seed)
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=seed)

    param_grid = {"clf__C": c_grid}
    grid_search = GridSearchCV(
        estimator=base_pipe,
        param_grid=param_grid,
        scoring="roc_auc",
        cv=cv,
        refit=True,
        n_jobs=-1,
    )
    grid_search.fit(x_train, y_train)

    best_pipeline = grid_search.best_estimator_
    best_c = grid_search.best_params_["clf__C"]
    best_score = grid_search.best_score_

    tuning_summary = {
        "target": target_col,
        "best_C": best_c,
        "best_cv_roc_auc": best_score,
        "cv_results": pd.DataFrame(grid_search.cv_results_),
    }
    return best_pipeline, tuning_summary


# Predict risk probabilities for the positive class.
def predict_positive_risk(
    pipeline: Pipeline,
    df: pd.DataFrame,
    predictors: List[str],
) -> np.ndarray:
    x_eval = df[predictors].copy()
    assert_predictor_allowlist(x_eval, predictors)

    classifier = pipeline.named_steps["clf"]
    pos_idx = list(classifier.classes_).index(1)

    probabilities = pipeline.predict_proba(x_eval)[:, pos_idx]
    return probabilities
