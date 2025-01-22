# prog-barcodes

Programming's checkout system for devices we use.

### Details
- Raspberry PI
- Barcode Scanner

### PI Config
0. Download Raspberry Pi OS Lite and flash onto pi.
1. Use `raspi-config` to configure console autologin, hostname, etc.
2. From your computer, clone the repository, then type `scp -r <this repo> username@hostname:/home/username/prog-checkout` to send it to the pi.
3. Set execute repo script on the PI in `~/.bash_profile`
```bash
source ~/.profile
if [ -z $DISPLAY ] && [ $(tty) = /dev/tty1 ]
then
  cd ~/prog-checkout
  python3 barcode.py
fi
```
