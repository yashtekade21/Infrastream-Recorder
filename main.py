import os
import subprocess
import threading
import time
from datetime import datetime

# Camera & storage configuration
                    # username:password@IPv4
ipCameraAddress = "username:password123@XXX.XXX.X.XXX"
localDir = "/home/pi2b/videos" # On device storage

# Ensure localDir exists
os.makedirs(localDir, exist_ok=True)

# Record video using ffmpeg with TCP transport and safe audio codec
def record_video(duration):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"recording_{timestamp}.mp4"
    filepath = os.path.join(localDir, filename)

    try:
        ffmpeg_command = [
            "ffmpeg",
            "-rtsp_transport", "tcp",
            "-i", f"rtsp://{ipCameraAddress}",
            "-t", str(duration),
            "-c:v", "copy",
            "-c:a", "aac",          # can change to supported codec for respective device (rasp supports aac)
            "-b:a", "128k",
            filepath
        ]
        print(f"Recording for {duration} seconds... Saving to: {filepath}")
        subprocess.run(ffmpeg_command, check=True)
        print(f"Recording completed and saved: {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Fmpeg error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Background thread to wait and trigger recording
def schedule_thread(schedule_time, duration):
    now = datetime.now()
    delay = (schedule_time - now).total_seconds()

    if delay > 0:
        print(f"aiting {int(delay)} seconds until scheduled time...")
        time.sleep(delay)
        record_video(duration)
    else:
        print("Scheduled time is in the past. Skipping.")

# Main interactive loop
def main():
    print("=== Recording Scheduler ===")
    while True:
        try:
            date_str = input("\nEnter recording date (YYYY-MM-DD): ").strip()
            time_str = input("Enter recording time (HH:MM, 24-hr format): ").strip()
            duration = int(input("Enter recording duration in seconds: ").strip())

            # Combine and parse datetime
            schedule_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            now = datetime.now()

            if schedule_time <= now:
                print("[!] Time must be in the future.")
                continue

            # Start scheduling in background
            thread = threading.Thread(target=schedule_thread, args=(schedule_time, duration))
            thread.daemon = True
            thread.start()
            print(f"Scheduled recording at {schedule_time.strftime('%Y-%m-%d %H:%M')} for {duration} seconds.")

            # Ask to schedule more
            cont = input("Do you want to schedule another? (y/n): ").strip().lower()
            if cont != "y":
                print("Exiting scheduler. Waiting for scheduled recordings to finish...")
                break

        except ValueError:
            print("Invalid date/time format. Please try again.")
        except KeyboardInterrupt:
            print("\nScheduler interrupted.")
            break

    # main thread alive while background threads run
    while threading.active_count() > 1:
        time.sleep(1)

if __name__ == "__main__":
    main()
