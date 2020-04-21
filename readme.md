# ESRGAN Slicer
A tiny wrapper for [ESRGAN](https://github.com/xinntao/ESRGAN). ESRGAN has a limit to the size of pictures you can upscale. This script takes larger images, slices, upscales and then stitches back together. 

## TODO:
- [x] CLI
- [x] Take directories as input
- [x] Can run with CPU only
- [x] GUI
- [ ] More progress (TQDM)
- [ ] Distribute

### Installing and running the CLI:
Install dependencies from *requirements.txt* using **pip**.
```
pip3 install -r requirements.txt

```

### Run GUI
```
python3 slicer_gui.py
```

### Run CLI
Run the script as so:

```
python3 upscaler.py -i input.png -o output.png

```

it can also upscale contents of directories:
```
python3 upscaler.py -i input_dir -o output_dir
```

When the scripts run for the first time, it will download the **RRDB_ESRGAN_x4.pth**-model from [Google Drive](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY) and place the model in `./models`.
