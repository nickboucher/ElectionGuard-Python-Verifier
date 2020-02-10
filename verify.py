#!/usr/bin/env python3
# ElectionGuard Verifier
# Nicholas Boucher 2020
import argparse


def main():
    parser = argparse.ArgumentParser(
            description='Verify ElectionGuard Elections Results.')
    parser.add_argument('election-data',
                        help='ElectionGuard results JSON file.')
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main()
