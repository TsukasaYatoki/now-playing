import random
import string
import time


def main():
    file_path = "/tmp/output.txt"
    interval = 10.0

    try:
        while True:
            rand_seq = "".join(
                random.choices(string.ascii_letters + string.digits, k=16)
            )
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(rand_seq + "\n")
            print(f"Written: {rand_seq}")

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nInterrupt signal received, exiting program.")


if __name__ == "__main__":
    main()
