import argparse
from enum import Enum
import subprocess
import ipaddress
import validators
import logging


class MTUFinder:
    class PingResult(Enum):
        SIZE_TOO_LARGE = 1
        EXCEPTION = 2
        OK = 3

    MAX_SIZE = 8973
    MIN_SIZE = 0

    def __init__(self, host):
        self.host = host
        if not self.validate_host():
            logging.error("host is not valid")
            exit(1)

    def is_icmp_enable(self):
        process = subprocess.run(
            ['cat', '/proc/sys/net/ipv4/icmp_echo_ignore_all'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if process.stdout == 1:
            return False

        return True
    
    def validate_host(self):
        if validators.domain(self.host):
            return True

        try:
            ipaddress.ip_address(self.host)
        except Exception:
            return False

        return True

    def ping_host(self, size):
        try:
            command = ["ping", self.host, '-M', 'do', '-s', str(size), '-c', '1']
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            if result.returncode == 0:
                return self.PingResult.OK
            elif result.returncode == 1:
                return self.PingResult.SIZE_TOO_LARGE
            else:
                return self.PingResult.EXCEPTION

        except Exception:
            return self.PingResult.EXCEPTION

    def find_mtu(self):
        if not self.is_icmp_enable():
            logging.error("icmp is not available")
            exit(1)

        print(self.ping_host(0))
        if self.ping_host(0) != self.PingResult.OK:
            logging.error("host is silent")
            exit(1)

        l = self.MIN_SIZE
        r = self.MAX_SIZE

        while l <= r:
            mid = (l + r) // 2
            res = self.ping_host(mid)
            if res == self.PingResult.OK:
                l = mid + 1
            elif res == self.PingResult.SIZE_TOO_LARGE:
                r = mid - 1
            else:
                logging.error("error in ping host")
                exit(1)
        return r


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    args = parser.parse_args()
    mtu_finder = MTUFinder(args.host)
    print(f"MTU is {mtu_finder.find_mtu()}")

if __name__ == '__main__':
    main()
