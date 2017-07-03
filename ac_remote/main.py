import constants
import logging
import settings
from vendored.lirc import Lirc
import pubnub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

logger = logging.getLogger()
pubnub.set_stream_logger('pubnub', logging.WARNING)

pnconfig = PNConfiguration()
pnconfig.subscribe_key = settings.SUBSCRIBE_KEY
pnconfig.publish_key = settings.PUBLISH_KEY
pnconfig.ssl = True

pubnub = PubNub(pnconfig)


lirc = Lirc()


class KeyPressSubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            logger.info('Disconnected')
        elif status.category == PNStatusCategory.PNConnectedCategory:
            logger.info('Connected')
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            logger.info('Reconnected')

    def message(self, pubnub, message):
        key = message.message
        if valid_key_press(key):
            logging.info('Sending {} key press'.format(key))
            lirc.send_once(constants.REMOTE_NAME, key)

            # Send an acknowledgement message with the key that was pressed
            pubnub.publish().channel(constants.CHANNEL_ACK).message(key).async(publish_callback)


def valid_key_press(message):
    if message in constants.VALID_KEYS:
        return True
    else:
        return False


def publish_callback(envelope, status):
    if not status.is_error():
        logger.info('Successfully published message')
    else:
        logger.error('Error publishing message')


def main():
    keypress_listener = KeyPressSubscribeCallback()
    pubnub.add_listener(keypress_listener)
    logger.info('Subscribing to {}'.format(constants.CHANNEL_REMOTE))
    pubnub.subscribe().channels(constants.CHANNEL_REMOTE).execute()

if __name__ == '__main__':
    main()
