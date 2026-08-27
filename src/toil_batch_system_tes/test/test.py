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

from types import SimpleNamespace
import unittest

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


class TESBatchSystemDiagnosticsTest(unittest.TestCase):
    """Unit tests for failure diagnostics formatting."""

    def test_failure_diagnostics_present_without_executor_stdout_stderr(self):
        from toil_batch_system_tes.tes_batch_system import TESBatchSystem

        executor_log = SimpleNamespace(
            exit_code=None,
            stderr=None,
            stdout=None,
            reason='OOMKilled',
            message='Container terminated by platform',
        )
        task_log = SimpleNamespace(logs=[executor_log], system_logs=['init container failed'])
        task = SimpleNamespace(id='tes-task-123', state='EXECUTOR_ERROR', logs=[task_log])

        diagnostics = TESBatchSystem._format_failure_diagnostics('tes-task-123', task)

        self.assertTrue(diagnostics)
        self.assertIn('task_id=tes-task-123', diagnostics)
        self.assertIn('final_state=EXECUTOR_ERROR', diagnostics)
        self.assertIn('executor_reason=OOMKilled', diagnostics)
        self.assertIn('next_steps=', diagnostics)

    def test_failure_diagnostics_present_when_executor_log_missing(self):
        from toil_batch_system_tes.tes_batch_system import TESBatchSystem

        task = SimpleNamespace(id='tes-task-456', state='SYSTEM_ERROR', logs=[])

        diagnostics = TESBatchSystem._format_failure_diagnostics('tes-task-456', task)

        self.assertTrue(diagnostics)
        self.assertIn('task_id=tes-task-456', diagnostics)
        self.assertIn('final_state=SYSTEM_ERROR', diagnostics)
        self.assertIn('executor_log=missing', diagnostics)
        self.assertIn('next_steps=', diagnostics)
