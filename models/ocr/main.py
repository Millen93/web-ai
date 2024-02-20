from fastapi import FastAPI, File, UploadFile 
from paddleocr import PaddleOCR,draw_ocr
from PIL import Image

app= FastAPI()

def ocr(img_path):
	ocr = PaddleOCR(use_angle_cls=True, lang='en')
	result = ocr.ocr(img_path, cls=True)
	for idx in range(len(result)):
		res = result[idx]
	result = result[0]
	image  = Image.open(img_path).convert('RGB')
	txts   = [line[1][0] for line in result]
	return txts

@app.post("/image")
async def ImageUpload(file: bytes = File(...)):
	result = ''
	img_path = './image.jpg'
	with open(img_path , "wb") as image:
		image.write(file)
	list = ocr(img_path)
	for word in list:
		result += word
		result += " " 
	return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=6000,
        log_level="debug",
        reload=True,
    )
