# ElectionGuard Verification Utilities
# Nicholas Boucher 2020
from constants import LOG_VERBOSE, LOG_NORMAL, BYTE_ORDER
from logging import basicConfig, getLogger

def int_to_bytes(num: int) -> bytes:
    """Converts an integer to a sequence of bytes with byte order set by
        in the program constants."""
    # Determine the number of bytes needed in the buffer
    num_bytes = 0
    temp = num
    while temp != 0:
        temp >>= 8
        num_bytes += 1
        
    # Convert the integer to bytes in the specified byte ordering
    return num.to_bytes(num_bytes, BYTE_ORDER)

def fail(message: str) -> bool:
    """Outputs a failure log message with the passed text and
        returns false."""
    # Get logging infrastructure
    basicConfig(format='%(message)s')
    log = getLogger("election_verifier")

    # Log failure in verbose mode
    log.log(LOG_VERBOSE, f"{message}\n")

    # Return false for failure
    return False