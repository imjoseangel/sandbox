#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Based on the rolling codes/hopping codes problem:
# http://programmingpraxis.com/2014/05/16/rolling-code
#
# We simulate a parking lot with multiple fobs and receivers
# sending and receiving signals (respectively). This is also
# a demonstration of a simple use of generator-based coroutines
# in Python (although they are not necessary here).

import logging
import random
import uuid

# Set up logging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RollingCode:
    # Fakes for encryption.
    @staticmethod
    def encrypt(data, key=None):
        logger.debug("Encrypting {}, with key {}".format(data, key))
        return (data, key)

    @staticmethod
    def decrypt(encrypted, key=None):
        logger.debug("Decrypting {}, with key {}".format(encrypted, key))
        if encrypted[1] == key:
            return encrypted[0]
        else:
            logger.error("Cannot decrypt given data using given key.")
            # "Encrypted" data could have been None, so we
            # should raise an exception here, but since this
            # is just an exercise, we're not going to.
            return None

    @staticmethod
    def send(frame):
        logger.debug("Sending frame {}".format(frame))
        for receiver in RollingCode._receivers:
            receiver.send(frame)

    @staticmethod
    def close_receivers():
        logger.debug("Closing all receivers.")
        for receiver in RollingCode._receivers:
            receiver.close()
        RollingCode._receivers = []

    @staticmethod
    def _register_receiver(receiver):
        logger.debug("Registering receiver.")
        RollingCode._receivers.append(receiver)

    # Receivers are implemented as generator-based coroutines.
    _receivers = []


class Fob(RollingCode):
    def __init__(self, rng_seed, serial_num):
        logger.debug("Initializing fob {}.".format(serial_num))
        self.rng = random.Random(rng_seed)
        self.serial_num = serial_num

    def press(self, func_code):
        logger.info("{} pressed {}.".format(self.serial_num, func_code))
        rolling_code = self.rng.random()
        self.send((self.serial_num,
                   self.encrypt(func_code, rolling_code),
                   self.encrypt(rolling_code)))


class Receiver(RollingCode):
    def __init__(self, rng_seed, recognized_serial_nums):
        logger.debug("Initializing receiver accepting fobs {}.".format(
            recognized_serial_nums))

        self.rng = random.Random(rng_seed)
        self.recognized_serial_nums = recognized_serial_nums

        # Set up generator-based coroutine to receive transmissions
        # via superclass' facilities.
        receiver_coroutine = self._receive()
        receiver_coroutine.next()
        self._register_receiver(receiver_coroutine)

    def _receive(self):
        logger.debug("Initializing receiver's coroutine.")

        try:
            while True:
                frame = yield

                # Extract sections from frame.
                serial_num, enc_func_code, enc_roll_code = frame

                # Ensure fob has recognized serial number.
                if serial_num not in self.recognized_serial_nums:
                    continue

                # Decrypt the rolling code.
                rolling_code = self.decrypt(enc_roll_code)

                # Compare next 256 numbers in rng instead of just one number,
                # since signal could have been sent when fob was out of range.
                # If any match, then except signal.
                synchronized = False
                for _ in range(256):
                    if self.rng.random() == rolling_code:
                        synchronized = True
                        break
                if not synchronized:
                    continue

                # If fob sent more than 256 consecutive signals out of range,
                # the receiver has to resynchronize. In real fob/receiver
                # systems, this is generally a tedious manual procedure. The
                # exercise statement is a little ambiguous on how to deal with
                # this situation, so we don't do anything...

                # Perform requested action if everything agrees.
                func_code = self.decrypt(enc_func_code, rolling_code)
                logger.info(
                    "Receiver accepting fobs {} accepted code {} from fob {}."
                    .format(self.recognized_serial_nums,
                            func_code, serial_num))
        finally:
            logger.debug("Closing receiver.")


def main():
    # Here, we simulate a parking lot with multiple receivers and fobs,
    # some of each may be unmatched. Then, we will send random events from
    # various fobs.

    # Set up a few receivers.
    rng_seeds_and_serials = []
    for _ in range(20):
        # We generate a few accepted serial numbers (as UUIDs) and a rng seed.
        recognized_serial_nums = [uuid.uuid4() for _ in
                                  range(random.randint(2, 4))]
        rng_seed = uuid.uuid4()

        # We don't keep track of the receivers since they register themselves
        # with their superclass and we don't interact with them directly.
        Receiver(rng_seed, recognized_serial_nums)

        # We keep track of input parameters for created receivers so
        # we can create matching fobs.
        rng_seeds_and_serials.append((rng_seed, recognized_serial_nums))

    # Set up some fobs.
    fobs = []
    for rng_seed, serials in rng_seeds_and_serials:
        # We create fobs for about 80% of the receivers.
        if random.random() > 0.2:
            fobs.append(Fob(rng_seed, random.choice(serials)))

    # We also create a few fobs for non-existent receivers.
    for _ in range(3):
        # For simplicity we use the serial as the rng seed.
        serial = uuid.uuid4()
        fobs.append(Fob(serial, serial))

    # Send some signals (fob and receiver should log same signal).
    for _ in range(100):
        random.choice(fobs).press(random.randint(1, 10))

    # Clean up.
    RollingCode.close_receivers()


if __name__ == "__main__":
    main()
