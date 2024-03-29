import numpy as np
import pandas as pd
import pytest

from clairvoyance2.data import TimeSeriesSamples
from clairvoyance2.metrics import mse_t


class TestIntegration:
    class TestMSE:
        @pytest.mark.parametrize(
            "dfs_true, dfs_pred, expected_value",
            [
                # > Check zero case.
                # >> 2 samples.
                (
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}),
                        pd.DataFrame({"a": [2, 0, 4], "b": [0, 0, 0]}),
                    ],
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}),
                        pd.DataFrame({"a": [2, 0, 4], "b": [0, 0, 0]}),
                    ],
                    0.0,
                ),
                # >> 1 sample.
                (
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}),
                    ],
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}),
                    ],
                    0.0,
                ),
                # > Check non-zero case.
                # >> 2 samples.
                (
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}),
                        pd.DataFrame({"a": [2, 0, 4], "b": [0, 0, 0]}),
                    ],
                    [
                        pd.DataFrame({"a": [-2, 0, -4, 0], "b": [1, 0, 1, 0]}),
                        pd.DataFrame({"a": [0, 1, 0], "b": [0, 2, 0]}),
                    ],
                    5.642857142857142,
                ),
                # >> 1 sample.
                (
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}),
                    ],
                    [
                        pd.DataFrame({"a": [-2, 0, -4, 0], "b": [1, 0, 1, 0]}),
                    ],
                    6.75,
                ),
            ],
        )
        def test_time_series_samples_aligned(self, dfs_true, dfs_pred, expected_value):
            data_true = TimeSeriesSamples(dfs_true)
            data_pred = TimeSeriesSamples(dfs_pred)

            metric = mse_t(data_true, data_pred)

            assert np.isclose(metric, expected_value)

        @pytest.mark.parametrize(
            "dfs_true, dfs_pred, expected_value",
            [
                # > Check zero case.
                # >> 2 samples.
                (
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}, index=[0, 1, 2, 3]),
                        pd.DataFrame({"a": [2, 0, 4], "b": [0, 0, 0]}, index=[0, 1, 2]),
                    ],
                    [
                        pd.DataFrame({"a": [0, 0, 0], "b": [0, -4, 0]}, index=[1, 2, 3]),
                        pd.DataFrame({"a": [0, 4, 99, 99], "b": [0, 0, 99, 999]}, index=[1, 2, 3, 4]),
                    ],
                    0.0,
                ),
                # >> 1 sample.
                (
                    [
                        pd.DataFrame({"a": [2, 0, 4], "b": [0, 0, 0]}, index=[0, 1, 2]),
                    ],
                    [
                        pd.DataFrame({"a": [0, 4, 99, 99], "b": [0, 0, 99, 999]}, index=[1, 2, 3, 4]),
                    ],
                    0.0,
                ),
                # > Check non-zero case.
                # >> 2 samples.
                (
                    [
                        pd.DataFrame({"a": [0, 0, 0, 0], "b": [-2, 0, -4, 0]}, index=[0, 1, 2, 3]),
                        pd.DataFrame({"a": [2, 0, 4], "b": [0, 0, 0]}, index=[0, 1, 2]),
                    ],
                    [
                        pd.DataFrame({"a": [5, 0, 5], "b": [0, 3, 1]}, index=[1, 2, 3]),
                        pd.DataFrame({"a": [1, 3, 99, 99], "b": [1, 1, 99, 999]}, index=[1, 2, 3, 4]),
                    ],
                    10.4,
                ),
                # >> 1 sample.
                (
                    [
                        pd.DataFrame({"a": [2, 0, 4], "b": [0, 0, 0]}, index=[0, 1, 2]),
                    ],
                    [
                        pd.DataFrame({"a": [1, 3, 99, 99], "b": [1, 1, 99, 999]}, index=[1, 2, 3, 4]),
                    ],
                    1.0,
                ),
            ],
        )
        def test_time_series_samples_not_aligned(self, dfs_true, dfs_pred, expected_value):
            data_true = TimeSeriesSamples(dfs_true)
            data_pred = TimeSeriesSamples(dfs_pred)

            metric = mse_t(data_true, data_pred)

            assert np.isclose(metric, expected_value)
