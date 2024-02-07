from tools.paddle_update import Updater
import cv2

image_path = "docs/input/invoices/processed/images"
json_path = "docs/input/invoices/processed/output"
new_json_path = "docs/input/invoices/processed/processed_output"

paddle_ocr_updater = Updater()
paddle_ocr_updater.update(image_path, json_path, new_json_path)