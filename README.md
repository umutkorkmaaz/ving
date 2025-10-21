# Ving - Terminal-Based Virtual Ping with Latency Chart

The Ving (Virtual Ping) application plots a chart of the latency times during sent pings.

You can use the same parameters as with the standard `ping` command.

## Features

- Standard ping functionality (ICMP packets)
- Statistics (min, max, avg, stddev, packet loss)
- Colorful and modern UI


## Installation

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

After installation, you can use the `ving` command.

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x ping_chart.py
```

**Note:** Root privileges may be required to send ICMP packets.

### Uninstallation
To remove Ving from the system:
```bash
./scripts/uninstall.sh
```

## License

MIT License - You can use it freely.

## Contributing

Pull requests are welcome!

### Credits
> This project was created entirely using Cursor with the claude-4.5-sonnet model.