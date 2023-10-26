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

from toil.test import needs_fetchable_appliance
from toil.test.batchSystems.batchSystemTest import hidden, numCores 

from toil_batch_system_tes.test import needs_tes

@needs_tes
@needs_fetchable_appliance
class TESBatchSystemTest(hidden.AbstractBatchSystemTest):
    """
    Tests against the TES batch system
    """

    def supportsWallTime(self):
        return True

    def createBatchSystem(self):
        # Import the batch system when we know we have it.
        # Doesn't really matter for TES right now, but someday it might.
        from toil_batch_system_tes.tes_batch_system import TESBatchSystem
        return TESBatchSystem(config=self.config,
                              maxCores=numCores, maxMemory=1e9, maxDisk=2001)
