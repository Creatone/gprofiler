#
# Copyright (c) Granulate. All rights reserved.
# Licensed under the AGPL3 License. See LICENSE.md in the project root for license information.
#
from abc import ABC
from typing import Iterable, Tuple, Type

from gprofiler.log import get_logger_adapter
from gprofiler.utils import get_kernel_release

logger = get_logger_adapter(__name__)
kernel_release = get_kernel_release()

KernelMessage = Tuple[float, int, str]


class Provider(ABC):
    def iter_new_messages(self) -> Iterable[KernelMessage]:
        ...


class EmptyProvider(Provider):
    def __init__(self):
        print("This kernel does not support the new /dev/kmsg interface for reading messages.")
        print("Profilee error monitoring not available.")
        print()
        logger.warning("Profilee error monitoring not available.")

    def iter_new_messages(self):
        return []


DefaultMessagesProvider: Type[Provider]
if kernel_release >= (3, 5):
    from gprofiler.devkmsg import DevKmsgProvider

    DefaultMessagesProvider = DevKmsgProvider
else:
    DefaultMessagesProvider = EmptyProvider