from typing import Type

from toil.batchSystems.registry import add_batch_system_factory
from toil.batchSystems.abstractBatchSystem import AbstractBatchSystem

def tes_batch_system_factory() -> Type[AbstractBatchSystem]:
    """
    Import and return the TES batch system implementation class.
    """
    from toil_batch_system_tes.tes_batch_stytem import TESBatchSystem
    return TESBatchSystem

# Register on import
add_batch_system_factory("tes", tes_batch_system_factory)
