# Raspberry Pi Keylogger

A simple Python-based keylogger designed for use on a Raspberry Pi. It captures keyboard input from One of the 4 usb-a porta of Raspberry pi 4, sends the keys from the usb-c porta to the computer, that Power It at the same time, and save the typed keys review.

---

## Features

- Captures all keystrokes using the [`keyboard`](https://pypi.org/project/keyboard/) Python package.
- Simple to install and run.
- Can be set to start automatically on reboot via `crontab`.

---

## Requirements

- Raspberry Pi running Linux
- Python 3.x
- Root (sudo) access
- The following Python package:
  - `keyboard`

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Filippo-Carta/raspberry-pi-keylogger.git
   cd raspberry-pi-keylogger
   ```

2. **Install dependencies:**

   ```bash
   pip install keyboard
   ```

3. **Make the main script executable (optional):**

   ```bash
   chmod +x main.py main.sh
   ```

4. **Add configs:**

   ```bash
   sudo nano /boot/firmware/cmdline.txt
   ```
   Add this after "rootwait":
   ```txt
   modules-load=dwc2,g_hid
   ```
   Should look something like this:
   ```txt
   ... fsck.repair=yes rootwait modules-load=dwc2,g_hid quiet splash p ...
   ```
   Then edit this file:
   ```bash
   sudo nano /boot/firmware/cmdline.txt
   ```
   and add:
   ```bash
   [cm5]
   dtoverlay=dwc2

   [all]
   dtoverlay=dwc2
   ```
   
   #Installation completed!

---

## Running the Keylogger

To run the logger manually:

```bash
sudo python3 main.py
```

Or using the shell script:

```bash
sudo bash main.sh
```

---

## Autostart on Boot (using crontab)

To run the keylogger automatically at startup, add the following lines to your crontab:

1. **Open the root crontab editor:**

   ```bash
   sudo crontab -e
   ```

2. **Add these lines at the bottom:**

   ```cron
   @reboot sudo bash /home/pi/raspberry-pi-keylogger/main.sh &
   @reboot sudo python3 /home/pi/raspberry-pi-keylogger/main.py &
   ```

   > ⚠️ **Important:**
   >
   > - Replace `/home/pi/raspberry-pi-keylogger/` with the actual path if different.
   > - The `&` at the end of each line runs the scripts in the background.
   > - Using `sudo` in crontab is only needed if you're **not** editing the root crontab.  
   >   When using `sudo crontab -e`, remove `sudo` from the lines:
   >
   >   ```cron
   >   @reboot bash /home/pi/raspberry-pi-keylogger/main.sh &
   >   @reboot python3 /home/pi/raspberry-pi-keylogger/main.py &
   >   ```

---

## Log Output

- The script will likely log to a file such as `key_log.txt` or similar (check the repo for exact implementation).
- Ensure the script has write permissions in its directory.

---

## Ethical Notice

> ⚠️ **This software is for educational purposes only. Do not use it to log keystrokes on devices you do not own or have explicit permission to monitor. Unauthorized keylogging is illegal and unethical.**

---



## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your proposed changes.
