# Radio
This project defines the hardware protocols for a project to study the raw usage of EMFS in urban spaces. It scans for signals between ~100MHz and 6GHz around every 15 seconds, returning the power transmitted at each frequency at an interval of about 1MHz. To get more information, refer to the specifications of the [hackrf](https://greatscottgadgets.com/hackrf/).

### Hardware Overview
I also use a [realtime clock from Adafruit](https://www.adafruit.com/product/3295) and a [GPS](https://www.adafruit.com/product/746). That's basically it!

### Usage
This system is set up to transmit encrypted messages to a remote server - it uses a two layer encryption. From your end, you'll want to generate asymetric keys for the sender and recieve, and give one to the raspberrypi while the recieving key lives in the server. This can of course be turned off if you're feeling spicy.

Likewise, the system is currently set up to transmit the data when it detects internet connection. This can also be turned off, in which case the device more or less turns into a chest of information you'll need to retrive manually.

LEDs have been installed for conveinece of interpretation of what's happening inside the machine. You can follow the porting on the`.gpio.env` file to see how to wire it up.
