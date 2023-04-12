# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
# with the License. A copy of the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "LICENSE.txt" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions and
# limitations under the License.
import pytest

from pcluster.config.cluster_config import Tag
from pcluster.validators.tags_validators import ComputeResourceTagsValidator
from tests.pcluster.validators.utils import assert_failure_messages


@pytest.mark.parametrize(
    "cluster_tags, queue_tags, expected_message",
    [
        (
            [Tag("key1", "value1"), Tag("key2", "value2"), Tag("key3", "value3")],
            [Tag("key1", "value1"), Tag("key2", "value2"), Tag("key3", "value3")],
            "The following Tag keys are defined in both under `Tags` and `SlurmQueue/Tags`: ['key1', 'key2', 'key3'] "
            "and will be overridden by the value set in `SlurmQueue/Tags` for ComputeResource 'dummy_compute_resource' "
            "in queue 'dummy_queue'.",
        ),
        (
            [Tag("key1", "value1"), Tag("key2", "value2"), Tag("key3", "value3")],
            [Tag("key4", "value1"), Tag("key5", "value2"), Tag("key6", "value3")],
            None,
        ),
        (
            [Tag("key1", "value1"), Tag("key2", "value2")],
            [Tag("key1", "value2"), Tag("key3", "value2")],
            "The following Tag keys are defined in both under `Tags` and `SlurmQueue/Tags`: ['key1'] and will be "
            "overridden by the value set in `SlurmQueue/Tags` for ComputeResource 'dummy_compute_resource' in queue "
            "'dummy_queue'.",
        ),
        (
            [Tag("key1", "value1"), Tag("key2", "value2"), Tag("key3", "value3")],
            None,
            None,
        ),
        (
            None,
            [Tag("key1", "value1"), Tag("key2", "value2"), Tag("key3", "value3")],
            None,
        ),
        (
            None,
            None,
            None,
        ),
    ],
)
def test_compute_console_logging_validator(cluster_tags, queue_tags, expected_message):
    actual_failures = ComputeResourceTagsValidator().execute(
        "dummy_queue", "dummy_compute_resource", cluster_tags, queue_tags
    )
    assert_failure_messages(actual_failures, expected_message)