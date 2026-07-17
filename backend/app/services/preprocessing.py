from pathlib import Path


class ImagePreprocessor:
    def preprocess(self, path: Path) -> Path:
        try:
            import cv2

            image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
            if image is None:
                return path
            image = cv2.fastNlMeansDenoising(image)
            image = cv2.equalizeHist(image)
            _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            output = path.with_name(f"{path.stem}.preprocessed{path.suffix}")
            cv2.imwrite(str(output), image)
            return output
        except Exception:
            return path

