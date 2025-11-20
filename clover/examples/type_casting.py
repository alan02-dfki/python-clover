import logging
from typing import List

from ..decorator import clover

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


@clover
def type_casting(
    i,
    l,
    s,
    ani: int,
    anl: List[int],
    andct: List[int],
):
    log.info(f"No annotation - no inference: i + i = {i + i}")
    log.info(f"Regardless of the implied type: l + l = {l + l}")
    log.info(f"No need to annotate strings: s + s = {s + s}")
    log.info(f"Yes annotation - yes inference: ani + ani = {ani + ani}")
    log.info(f"Can even infer some more complex types: anl + anl = {anl + anl}")
    log.info(
        f"Correctness annotations is not checked, yet: type(andct) = {type(andct)}"
    )


if __name__ == "__main__":
    type_casting(0)
