# prog-barcodes

Programming's checkout system for devices we use.

### Details
- Raspberry PI
- Barcode Scanner

### PI Config
1. Configure console autologin, hostname, etc.
2. `scp -r <this repo> username@pi:/home/username/prog-checkout`
3. Set execute repo script in `~/.bash_profile`
```bash
source ~/.profile
if [ -z $DISPLAY ] && [ $(tty) = /dev/tty1 ]
then
  cd ~/prog-checkout
  python3 barcode.py
fi
```
