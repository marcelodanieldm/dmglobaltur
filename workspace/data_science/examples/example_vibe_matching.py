from vibe_matching_classifier import classify_luxury_persona

# Ejemplo de texto de reseña/post
text = "El hotel tenía un ambiente clásico y el personal hablaba varios idiomas. Compartí mi experiencia en Xiaohongshu."

result = classify_luxury_persona(text)
print('Resultado de clasificación:')
print(result)
