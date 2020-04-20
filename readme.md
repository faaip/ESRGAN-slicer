# ESRGAN Slicer
A tiny wrapper for [ESRGAN](https://github.com/xinntao/ESRGAN). ESRGAN has a limit to the size of pictures you can upscale. This script takes larger images, slices, upscales and then stitches back together. 

## TODO:
- [x] CLI
- [ ] Take directories as input
- [ ] GUI
- [ ] Distribute

### Installing and running the CLI:
Install dependencies from *requirements.txt* using **pip**.
```
pip3 install -r requirements.txt

```

Run the script as so:

```
python3 upscaler.py -i input.png -o output.png

```

When the scripts run for the first time, it will download the **RRDB_ESRGAN_x4.pth**-model from [Google Drive](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY) and place the model in `./models`.
