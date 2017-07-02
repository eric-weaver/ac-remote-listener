import constants
import settings
from vendored.lirc import Lirc
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.subscribe_key = settings.SUBSCRIBE_KEY
pnconfig.ssl = False

pubnub = PubNub(pnconfig)

lirc = Lirc()


class KeyPressSubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            print('Connected')
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        key = message.message
        if valid_key_press(key):
            lirc.send_once(constants.REMOTE_NAME, key)


def valid_key_press(message):
    if message in constants.VALID_KEYS:
        return True
    else:
        return False


def main():
    keypress_listener = KeyPressSubscribeCallback()
    pubnub.add_listener(keypress_listener)
    print('Subscribing to {}'.format(constants.REMOTE_NAME))
    pubnub.subscribe().channels(constants.REMOTE_NAME).execute()

if __name__ == '__main__':
    main()
