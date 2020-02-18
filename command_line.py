#!/usr/bin/env python3
# ElectionGuard Command Line Verifier Utility
# Nicholas Boucher 2020
from argparse import ArgumentParser
from logging import getLogger, WARNING
from verify import verify_election
from models import Record


def main() -> None:
    """Main point of entry for command line execution."""
    # Parse argument from command line
    # Setup logging infrastructure
    log = getLogger()
    log.setLevel(WARNING)

    # Deserialize election data JSON
    with open("env/valid_encrypted.json", 'r') as f:
        election = Record.deserialize(f.read())

    # Verify the election results
    if verify_election(election):
        log.warning("Election Valid.")
    else:
        log.warning("Election Invalid.")


if __name__ == '__main__':
    main()
