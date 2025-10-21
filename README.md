# Ving - Terminal-Based Visual Ping with Latency Chart

The Ving (Visual Ping) application plots a chart of the latency times during sent pings.

You can use the same parameters as with the standard `ping` command.

### Screenshot

<img width="668" height="575" alt="CleanShot 2025-10-21 at 18 45 51" src="https://github.com/user-attachments/assets/3633f982-87fd-4888-a74b-931263514314" />



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
chmod +x ving.py
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
