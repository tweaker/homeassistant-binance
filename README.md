# Binance Exchange sensors component

### Installation

- Copy directory `binance` to your `<config dir>/custom_components` directory.
- Configure with config below.
- Restart Home-Assistant.

### Usage
To use this component in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry

sensor:
- platform: binance
  pairs:
  - BTCUSDT
  - ETHUSDT
  - LTCUSDT
  - EOSBTC
  - ADABTC
```

Configuration variables:

- **name** (*Optional*): Name of the device. (default = 'Binance')
- **api_key** (*Optional*): API key. You can specify any.
- **api_secret** (*Optional*): API secret. You can specify any.
- **pairs** (*Required*): Pairs of cryptocurrencies

### Screenshot

![alt text](https://raw.githubusercontent.com/tweaker/homeassistant-binance/master/screenshots/binance.png "Screenshot")