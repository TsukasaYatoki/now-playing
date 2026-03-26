import argparse
import time
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(
        description="Write current time to a text file every t seconds"
    )
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        default=1.0,
        help="Time interval in seconds (default: 1.0)",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="/tmp/output.txt",
        help="Target filename (default: /tmp/output.txt)",
    )

    args = parser.parse_args()

    print(
        f"Program started. Writing current time to {args.file} every {args.time} seconds. Press Ctrl+C to stop."
    )

    try:
        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(args.file, "a", encoding="utf-8") as file:
                file.write(now + "\n")
            print(f"Time written: {now}")

            time.sleep(args.time)

    except KeyboardInterrupt:
        print("\nInterrupt signal received, exiting program.")


if __name__ == "__main__":
    main()
