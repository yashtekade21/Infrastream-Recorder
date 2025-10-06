# 🎥 Raspberry Pi Video Recording Scheduler (IP Camera + Audio)

This project allows you to **schedule multiple video recordings** from an IP camera connected to a Raspberry Pi (or any Linux machine). Each recording is saved locally in `.mp4` format with audio support. You can queue multiple recordings — all run automatically in the background.

---

## 🧩 Features

* Record IP camera stream using **FFmpeg**
* Schedule multiple recordings one after another
* Automatic file naming with timestamps
* Background scheduling using Python threads
* Records both **video + audio** (AAC codec)
* Stores recordings locally under `/home/pi2b/videos`

---

## ⚙️ Requirements

### Hardware

* Raspberry Pi 2B / 3B / 4 (CLI or desktop)
* IP Camera with RTSP support
* Optional: USB Microphone (if camera doesn’t have one)

### Software

Install the following dependencies on Raspberry Pi:

```bash
sudo apt update
sudo apt install ffmpeg python3 -y
```

---

## 📁 Directory Setup

By default, videos are stored at:

```
/home/pi2b/videos
```

You can change this path in the script:

```python
localDir = "/home/pi2b/videos"
```

---

## 🔧 Configuration

Update the IP camera RTSP address in the script:

```python
ipCameraAddress = "username:password123@XXX.XXX.X.XXX"
```

**Example RTSP format:**

```
rtsp://admin:12345@192.168.1.105:554/stream1
```

---

## 🚀 Running the Scheduler

1. Save the script as `scheduler.py`
2. Run it on the Raspberry Pi:

```bash
python3 scheduler.py
```

3. Enter details when prompted:

```
Enter recording date (YYYY-MM-DD): 2025-04-10
Enter recording time (HH:MM, 24-hr format): 17:30
Enter recording duration in seconds: 30
```

The recording will be automatically started at the scheduled time and saved to the local directory.

You can schedule multiple recordings — each runs independently in the background.

---

## 💾 Downloading Videos to Your Local Machine

### Option 1: Using SCP (Linux/macOS/WSL)

```bash
scp pi2b@<raspberry_pi_ip>:/home/pi2b/videos/*.mp4 .
```

### Option 2: Using WinSCP (Windows GUI)

1. Open WinSCP and connect using SFTP

   * Host: Raspberry Pi IP
   * Username: `pi2b`
   * Password: your password
2. Navigate to `/home/pi2b/videos`
3. Drag and drop recordings to your PC

---

## 🧠 Notes

* Ensure **SSH** is enabled on the Raspberry Pi:

  ```bash
  sudo raspi-config
  ```

  → Interface Options → SSH → Enable

* Use **24-hour format** when entering time.

* Keep the terminal running — background threads will continue recording.

---

## 🧹 Optional Enhancements

* Auto-upload recordings to a server or cloud storage
* Email/SMS alert once a recording finishes
* Web interface for schedule management
* Integration with cron for permanent scheduling

---

## 📄 License

MIT License – You’re free to use and modify this project for personal or academic purposes.
