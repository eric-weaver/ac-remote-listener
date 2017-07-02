from vendored.lirc import Lirc


lirc = Lirc()

print ", ".join(lirc_obj.devices())

lirc_obj.send_once('frigidaireAC', 'KEY_DOWN')
