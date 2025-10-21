#!/usr/bin/env python3
"""
Terminal-based ping application with real-time latency chart
"""

import sys
import io
import time
import argparse
import statistics
from ping3 import ping
import plotext as plt
from collections import deque


class Ving:
    def __init__(self, host, count=None, interval=1, timeout=4, max_points=50):
        """
        Initialize the Ving application.
        
        Args:
            host: Target host to ping
            count: Number of pings to send (None for infinite)
            interval: Time between pings in seconds
            timeout: Ping timeout in seconds
            max_points: Maximum number of points to display on chart
        """
        self.host = host
        self.count = count
        self.interval = interval
        self.timeout = timeout
        self.max_points = max_points
        
        self.latencies = deque(maxlen=max_points)
        self.seq_numbers = deque(maxlen=max_points)
        self.all_latencies = []
        
        self.sent = 0
        self.received = 0
        self.lost = 0
        
        # For clean refresh without flickering
        self.lines_drawn = 0
        
    def format_stats(self):
        """Format statistics similar to ping command."""
        if not self.all_latencies:
            return ""
        
        min_latency = min(self.all_latencies)
        max_latency = max(self.all_latencies)
        avg_latency = statistics.mean(self.all_latencies)
        
        if len(self.all_latencies) > 1:
            stddev = statistics.stdev(self.all_latencies)
        else:
            stddev = 0
        
        loss_percent = (self.lost / self.sent * 100) if self.sent > 0 else 0
        
        stats = f"\n--- {self.host} ping statistics ---\n"
        stats += f"{self.sent} packets transmitted, {self.received} received, "
        stats += f"{loss_percent:.1f}% packet loss\n"
        stats += f"rtt min/avg/max/stddev = {min_latency:.3f}/{avg_latency:.3f}/"
        stats += f"{max_latency:.3f}/{stddev:.3f} ms"
        
        return stats
    
    def clear_previous_output(self):
        """Clear previous output lines cleanly."""
        if self.lines_drawn > 0:
            # Move cursor up and clear each line
            for _ in range(self.lines_drawn):
                print("\033[F\033[2K", end="")  # Move up and clear line
    
    def draw_chart(self, current_latency=None, timeout_occurred=False):
        """Draw the latency chart in terminal."""
        # Clear previous output
        self.clear_previous_output()
        
        # Capture the output to count lines
        output_buffer = io.StringIO()
        
        plt.clear_figure()
        
        if len(self.latencies) > 0:
            # Prepare data for chart
            x_vals = list(self.seq_numbers)
            y_vals = list(self.latencies)
            
            # Set compact plot size (width, height)
            plt.plot_size(80, 15)
            
            # Set dark theme for better aesthetics
            plt.theme('dark')
            
            # Create the plot with smooth line and points
            plt.plot(x_vals, y_vals, marker="braille", color="green+", fillx=False)
            plt.scatter(x_vals, y_vals, marker="dot", color="cyan")
            
            # Set labels and title with colors
            plt.title(f"📡 Latency Chart - {self.host}")
            plt.xlabel("Sequence")
            plt.ylabel("Latency (ms)")
            
            # Enable grid for better readability
            plt.grid(True, True)
            
            # Redirect stdout to capture output
            old_stdout = sys.stdout
            sys.stdout = output_buffer
            plt.show()
            sys.stdout = old_stdout
            
            # Get the chart output
            chart_output = output_buffer.getvalue()
            
            # Add current stats below the chart with colors
            if self.all_latencies:
                min_lat = min(self.all_latencies)
                max_lat = max(self.all_latencies)
                avg_lat = statistics.mean(self.all_latencies)
                loss_percent = (self.lost / self.sent * 100) if self.sent > 0 else 0
                
                # Color codes for terminal
                GREEN = '\033[92m'
                CYAN = '\033[96m'
                YELLOW = '\033[93m'
                RED = '\033[91m'
                RESET = '\033[0m'
                BOLD = '\033[1m'
                
                stats_line = f"\n  {BOLD}Current:{RESET} {CYAN}{current_latency:.1f}ms{RESET} │ "
                stats_line += f"Min: {GREEN}{min_lat:.1f}{RESET} │ Max: {YELLOW}{max_lat:.1f}{RESET} │ "
                stats_line += f"Avg: {CYAN}{avg_lat:.1f}{RESET} │ "
                
                if loss_percent > 0:
                    stats_line += f"Loss: {RED}{loss_percent:.1f}%{RESET}"
                else:
                    stats_line += f"Loss: {GREEN}{loss_percent:.1f}%{RESET}"
                
                if timeout_occurred:
                    stats_line += f" │ {RED}✗ TIMEOUT{RESET}"
                
                chart_output += stats_line
            
            # Print everything at once
            print(chart_output, end='')
            
            # Count lines for next clear
            self.lines_drawn = chart_output.count('\n')
            
        else:
            waiting_msg = f"Pinging {self.host}... waiting for data..."
            print(waiting_msg, end='')
            self.lines_drawn = 1
    
    def run(self):
        """Run the ping chart application."""
        CYAN = '\033[96m'
        GRAY = '\033[90m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        print(f"\n{BOLD}{CYAN}🌐 PING {self.host}{RESET} {GRAY}(Press Ctrl+C to stop){RESET}\n")
        
        try:
            seq = 0
            while self.count is None or seq < self.count:
                seq += 1
                self.sent += 1
                
                try:
                    # Perform ping
                    latency = ping(self.host, timeout=self.timeout, unit='ms')
                    
                    if latency is not None and latency is not False:
                        # Successful ping
                        self.received += 1
                        self.latencies.append(latency)
                        self.seq_numbers.append(seq)
                        self.all_latencies.append(latency)
                        
                        # Draw chart (it handles clearing previous output)
                        self.draw_chart(current_latency=latency)
                        
                        # Print ping result with color
                        GREEN = '\033[92m'
                        RESET = '\033[0m'
                        ping_result = f"\n  {GREEN}✓{RESET} {len(self.latencies)} bytes from {self.host}: "
                        ping_result += f"icmp_seq={seq} time={latency:.2f} ms"
                        print(ping_result)
                        
                        # Update lines count to include ping result
                        self.lines_drawn += 2
                    else:
                        # Timeout
                        self.lost += 1
                        
                        # Draw chart (it handles clearing previous output)
                        self.draw_chart(timeout_occurred=True)
                        
                        # Print timeout with color
                        RED = '\033[91m'
                        RESET = '\033[0m'
                        timeout_msg = f"\n  {RED}✗{RESET} Request timeout for icmp_seq {seq}"
                        print(timeout_msg)
                        
                        # Update lines count to include timeout message
                        self.lines_drawn += 2
                
                except Exception as e:
                    self.lost += 1
                    print(f"\nError: {e}")
                
                # Wait before next ping
                if self.count is None or seq < self.count:
                    time.sleep(self.interval)
        
        except KeyboardInterrupt:
            # Clear the chart before showing final stats
            self.clear_previous_output()
            print("\n\nInterrupted by user")
        
        finally:
            # Print final statistics
            print(self.format_stats())


def main():
    parser = argparse.ArgumentParser(
        description='Ping utility with terminal-based latency chart',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s google.com
  %(prog)s -c 10 8.8.8.8
  %(prog)s -i 0.5 -W 2 example.com
        """
    )
    
    parser.add_argument('host', help='Target host to ping')
    parser.add_argument('-c', '--count', type=int, default=None,
                        help='Number of pings to send (default: infinite)')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                        help='Wait interval seconds between pings (default: 1.0)')
    parser.add_argument('-W', '--timeout', type=float, default=4.0,
                        help='Time to wait for response in seconds (default: 4.0)')
    parser.add_argument('-m', '--max-points', type=int, default=50,
                        help='Maximum points to display on chart (default: 50)')
    
    args = parser.parse_args()
    
    # Check if running with sufficient privileges
    try:
        # Test if we can ping
        test_result = ping("127.0.0.1", timeout=1)
        if test_result is None:
            print("Warning: May need elevated privileges (sudo) to send ICMP packets", 
                  file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Note: This program may require sudo privileges to work properly", 
              file=sys.stderr)
        return 1
    
    # Create and run ping chart
    ving = Ving(
        host=args.host,
        count=args.count,
        interval=args.interval,
        timeout=args.timeout,
        max_points=args.max_points
    )
    
    ving.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())

