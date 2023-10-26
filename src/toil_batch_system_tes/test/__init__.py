# Copyright (C) 2015-2021 Regents of the University of California
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
import os
import unittest

from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from toil.test import MT

def needs_tes(test_item: MT) -> MT:
    """Use as a decorator before test classes or methods to run only if TES is available."""

    from toil_batch_system_tes.tes_batch_system import TESBatchSystem

    tes_url = os.environ.get('TOIL_TES_ENDPOINT', TESBatchSystem.get_default_tes_endpoint())
    try:
        urlopen(tes_url, timeout=5)
    except HTTPError:
        # Funnel happens to 404 if TES is working. But any HTTPError means we
        # dialed somebody who picked up.
        pass
    except URLError:
        # Will give connection refused if we can't connect because the server's
        # not there. We can also get a "cannot assign requested address" if
        # we're on Kubernetes dialing localhost and !!creative things!! have
        # been done to the network stack.
        return unittest.skip(f"Run a TES server on {tes_url} to include this test")(test_item)
    return test_item
