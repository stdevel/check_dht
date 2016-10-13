# check_dht
A Nagios / Icinga plugin written in Python (*based on the [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) library*) for checking humidity and temperature of DHT sensors via GPIO. The plugin also offers performance data for extensions such as PNP4Nagios.

# Requirements
For this plugin you need:
- a GPIO capable device
- the Python module [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT)
- a DHT11, DHT22 or AM2302 sensor (*check [eBay](http://www.ebay.com) for this*)
- a breadboard

![Example layout](https://raw.githubusercontent.com/stdevel/check_dht/master/example_layout.jpg "Example layout")

## Build Adafruit_Python_DHT
To build the Python library, check-out the [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT) repository. Also, make sure that the ``make`` and ``gcc`` binaries and Python development files are available on your Linux system. Run the ``setup.py`` installation script with root privileges:

```
# python setup.py install
...
Installed /usr/lib/python2.7/site-packages/Adafruit_DHT-1.1.0-py2.7-linux-armv7l.egg
Processing dependencies for Adafruit-DHT==1.1.0
Finished processing dependencies for Adafruit-DHT==1.1.0
```

Afterwards, the ``check_dht.py`` script should work as expected - make sure to set valid parameters for your test (*see below*):
```
# 
```

ds