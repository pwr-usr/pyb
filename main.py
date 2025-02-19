# main.py
import argparse
import subprocess
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Lixinger Data Downloader")
    parser.add_argument("--stock-info", action="store_true", help="Download stock information")
    parser.add_argument("--fundamental", action="store_true", help="Download fundamental data")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.stock_info:
        print("Running stock information downloader...")
        subprocess.run([sys.executable, os.path.join(base_dir, "scripts", "download_stock_info.py")])

    if args.fundamental:
        print("Running fundamental data downloader...")
        subprocess.run([sys.executable, os.path.join(base_dir, "scripts", "download_fundamental.py")])

    if not args.stock_info and not args.fundamental:
        print("No action specified. Use --stock-info and/or --fundamental.")


if __name__ == "__main__":
    main()
