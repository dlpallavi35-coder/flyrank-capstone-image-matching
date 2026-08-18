from app.services.vision_service import analyze_image

result = analyze_image("uploads/dogimage.webp")

print(result)