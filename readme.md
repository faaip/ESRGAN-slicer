# ESRGAN Slicer
A tiny wrapper for [ESRGAN](https://github.com/xinntao/ESRGAN). Takes larger images, slices, upscales and then stitches back together.

## TODO:
- [x] CLI
- [ ] GUI
- [ ] Distribute

### Download the model
Download the 'RRDB_ESRGAN_x4.pth'-model from [Google Drive](https://drive.google.com/drive/u/0/folders/17VYV_SoZZesU6mbxz2dMAIccSSlqLecY) or [Baidu Drive](https://pan.baidu.com/s/1-Lh6ma-wXzfH8NqeBtPaFQ). Place the model in `./models`. 

### Installing and running the CLI:
Install dependencies from *requirements.txt* using **pip**. 

Run the script as so:

```
python3 upscaler -i input.png -o output.png

```