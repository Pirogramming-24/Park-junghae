from paddleocr import PaddleOCR
import cv2

# 서버 시작 시 OCR 모델 1번만 로딩
ocr = PaddleOCR(
    lang="korean",
    use_angle_cls=False,
    rec=True,
    det=True,
    show_log=False
)

def run_ocr(image_path):
    """
    image_path: 업로드된 이미지 경로
    return: [{text, y}, ...]
    """
    try:
        img = cv2.imread(image_path)
        if img is None:
            print("❌ 이미지 로드 실패:", image_path)
            return []

        result = ocr.ocr(img, cls=False)

        texts = []
        for line in result:
            for box, (text, score) in line:
                y = box[0][1]  # 좌상단 y좌표
                texts.append({
                    "text": text,
                    "y": float(y)
                })

        return texts

    except Exception as e:
        print("OCR ERROR:", e)
        return []
