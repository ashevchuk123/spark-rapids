# Copyright (c) 2020-2021, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from asserts import assert_gpu_and_cpu_are_equal_collect, assert_gpu_fallback_collect
from spark_session import is_before_spark_311
from data_gen import *
from marks import ignore_order, allow_non_gpu
import pyspark.sql.functions as f


@pytest.mark.parametrize('data_gen', all_basic_gens + decimal_128_gens + array_gens_sample + map_gens_sample + struct_gens_sample, ids=idfn)
def test_simple_limit(data_gen):
    assert_gpu_and_cpu_are_equal_collect(
            # We need some processing after the limit to avoid a CollectLimitExec
            lambda spark : unary_op_df(spark, data_gen, num_slices=1).limit(10).repartition(1),
            conf = copy_and_update(allow_negative_scale_of_decimal_conf, 
                {'spark.sql.execution.sortBeforeRepartition': 'false'}))
