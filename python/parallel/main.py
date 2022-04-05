#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ray


@ray.remote
def func1():
    from datetime import datetime
    import time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("func 1 Start Time =", current_time)
    time.sleep(2)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("func 1 End Time =", current_time)


@ray.remote
def func2():
    from datetime import datetime
    import time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("func 2 Start Time =", current_time)
    time.sleep(2)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("func 2 End Time =", current_time)


def main():
    """
    Main function
    """
    ray.init()
    ray.get([func1.remote(), func2.remote()])


if __name__ == '__main__':
    main()
