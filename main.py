import requests
import datetime
import time 
import argparse
import random
from typing import List, Set, Dict, Tuple, Text, Optional, AnyStr


class Failure(object):
    def __init__(self, time: datetime.datetime, duration: int, url: str):
        self.time = time 
        self.duration = duration
        self.url = url

    def __str__(self):
        return f'{self.time}, {self.duration}, {self.url}'


def write_failure(file_name: str, failure: Failure) -> None:
    with open(file_name, 'a') as f:
        f.write(f"{failure}\n")


def attempt_connection(urls: List[str], duration=0) -> Failure:
    url = random.choice(urls)

    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return Failure(datetime.datetime.utcnow(), duration, url)

        return None
    except Exception as e:
        print('Failed to make request due to ', e)
        return Failure(datetime.datetime.utcnow(), duration, url)

    return None


def main():
    now = datetime.datetime.utcnow()
    today_date = now.strftime("%Y_%m_%d_%H")

    parser = argparse.ArgumentParser(description='Start a watcher for uptime')

    parser.add_argument(
        '--url',
        '-u',
        nargs='+',
        help='A url to test against. You can provide multiple',
        default=["https://www.google.com"]
    )

    args = parser.parse_args()

    failure = None

    print('Started watching the urls:', args.url)

    while True:
        previous_failure = failure

        if failure is None:        
            failure = attempt_connection(args.url, 0)
        else:
            failure = attempt_connection(args.url, failure.duration)

        if failure is None:
            if previous_failure is not None:
                print('Downtime ended!')
        else:
            if failure.duration < 2:
                print('Downtime started!')
            elif failure.duration > 1 and failure.duration % 10 == 0:
                print(f'{failure.url} still down for {failure.duration}')

            write_failure(today_date, failure)

        time.sleep(1)


if __name__ == '__main__':
    main()