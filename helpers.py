from pathlib import Path


def list_dir(self, pattern="*"):
    import glob

    return [Path(x) for x in glob.glob(str(self / pattern))]


Path.ls = list_dir


def _copy(self, target):
    import shutil

    if self.is_dir():
        shutil.copytree(str(self), str(target))
    else:
        assert self.is_file()
        shutil.copy(str(self), str(target))  # str() only there for Python < (3, 6)


Path.copy = _copy

DATA_DIR = Path("data") / "RGB and VIS-NIR HSI Data for 90 Rice Seed Varieties"


import spectral
import numpy as np
import pandas as pd
from PIL import Image


class ImageWrapper:
    """Wraps a row of the index to provide convenient access to the HSI image, RGB, white background and black background."""

    def __init__(self, row):
        self.metadata = row
        self.hsi_image_path = (DATA_DIR / row.Folder / row["File Name"]).with_suffix(
            ".hdr"
        )
        self.black_image_path = (DATA_DIR / row.Folder / "black").with_suffix(".hdr")
        self.rgb_image_path = (DATA_DIR / row.Folder / row["File Name"]).with_suffix(
            ".jpg"
        )
        self.white_rows = (625, 675)

    def _load_hsi(self):
        """Loads the HSI image."""
        if not hasattr(self, "hsi_img"):
            spectral.settings.envi_support_nonlowercase_params = True
            self.hsi_img = spectral.io.envi.open(self.hsi_image_path)
        return self.hsi_img

    def _load_black_background(self):
        """Loads the black HSI image."""
        if not hasattr(self, "black_img"):
            spectral.settings.envi_support_nonlowercase_params = True
            self.black_img = spectral.io.envi.open(self.black_image_path)
        return self.black_img

    def _load_rgb(self):
        """Loads the RGB image."""
        if not hasattr(self, "rgb_img"):
            self.rgb_img = Image.open(self.rgb_image_path)
        return self.rgb_img

    def _load_wavelengths(self):
        self.wavelengths_df = pd.read_csv(DATA_DIR / "wavelengths.csv", index_col=0)
        return self.wavelengths_df

    @property
    def hsi(self):
        return self._load_hsi()

    @property
    def hsi_calibrated(self):
        white_ref = self.white_reference[None, :, :]
        black_ref = self.black_reference[None, :, :]
        # Prevent division by zero by adding a small epsilon
        eps = np.finfo(np.float32).eps
        denominator = np.maximum(white_ref - black_ref, eps)
        # Apply normalisation
        return (self.hsi.asarray() - black_ref) / denominator

    @property
    def black_background(self):
        return self._load_black_background()

    @property
    def rgb(self):
        return self._load_rgb()

    @property
    def white_reference(self):
        self._load_hsi()

        return np.mean(self.hsi[self.white_rows[0] : self.white_rows[1], :, :], axis=0)

    @property
    def black_reference(self):
        self._load_black_background()
        return np.mean(self.black_background.asarray(), axis=0)

    @property
    def wavelengths(self):
        if not hasattr(self, "wavelengths_df"):
            self._load_wavelengths()
        return self.wavelengths_df.iloc[:, 0].values


class ImageSampleAccessor:
    def __init__(self, df):
        self.df = df

    def __getitem__(self, row_number):
        """Loads the image once and returns an ImageWrapper for chaining."""
        return ImageWrapper(self.df.iloc[row_number])


class HSIDataSetDataFrame(pd.DataFrame):
    @property
    def images(self):
        return ImageSampleAccessor(self)
