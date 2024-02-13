# prog-barcodes

Programming's checkout system for devices we use.

### Details
- Raspberry PI
- Barcode Scanner
- [Todo] LCD Display + Button

### PI Config
1. Configure console autologin, hostname, etc.
2. Install `python3`
3. Set execute repo script in `~/.bash_profile`
```bash
source ~/.profile
if [ -z $DISPLAY ] && [ $(tty) = /dev/tty1 ]
then
  cd ~/prog-checkout
  python3 barcode.py
fi
```