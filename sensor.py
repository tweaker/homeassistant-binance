"""
Binance exchange sensor
"""

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_SCAN_INTERVAL)
from homeassistant.util import Throttle

import voluptuous as vol

import datetime
import logging
from decimal import Decimal

from .const import (
    DEFAULT_NAME, ICON, CONF_API_KEY,
    CONF_API_SECRET, CONF_PAIRS, ALL_PAIRS
)

__version__ = '1.0.2'
REQUIREMENTS = ['python-binance==0.7.1']

_LOGGER = logging.getLogger(__name__)
DOMAIN = 'sensor'

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(seconds=10)
SCAN_INTERVAL = datetime.timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_API_KEY, default=CONF_API_KEY): cv.string,
    vol.Optional(CONF_API_SECRET, default=CONF_API_SECRET): cv.string,
    vol.Required(CONF_PAIRS, default=[]): vol.All(cv.ensure_list, [vol.In(ALL_PAIRS)])
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup thr Binance sensors."""

    api_key = config.get(CONF_API_KEY)
    api_secret = config.get(CONF_API_SECRET)
    name = config.get(CONF_NAME)
    pairs = config.get(CONF_PAIRS)

    try:
        data = BinanceData(api_key, api_secret)
        data.update()
    except:
        _LOGGER.error("Error setting up Binance sensor")
        return False

    entities = []
    for pair in pairs:
        entities.append(BinanceSensor(data, name, pair))

    async_add_entities(entities, True)


class BinanceData(object):

    def __init__(self, api_key, api_secret):
        """Initialize."""
        self._api_key = api_key
        self._api_secret = api_secret
        self.data = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        from binance.client import Client

        _LOGGER.debug('Fetching data from binance.com')
        try:
            client = Client(self._api_key, self._api_secret)
            prices = client.get_all_tickers()
            for i in prices:
                self.data[i['symbol']] = i['price']
            _LOGGER.debug("Rates updated to %s", self.data)
        except:
            _LOGGER.error('Error fetching data from binance.com')
            self.data = {}
            return False


class BinanceSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, data, name, pair):
        """Initialize the sensor."""
        self.data = data
        self._pair = pair
        self._name = name + " " + ALL_PAIRS[pair][0]
        self._icon = ALL_PAIRS[pair][1]
        self._state = None
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    def update(self):
        """Update current values."""
        self.data.update()
        data = self.data.data
        if str(ALL_PAIRS[self._pair][0]).split('/')[1] in ['USDT', 'TUSD', 'USDC', 'USDS']:
            self._state = "%.2f" % Decimal(data[self._pair])
        else:
            self._state = data[self._pair]
