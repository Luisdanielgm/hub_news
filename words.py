stopwords = ['entre', 'tras', 'los', 'mías', 'lo', 'vuestros', 'vía', 'para', 'mío', 'nuestra', 'nuestros', 'nuestras', 'versus', 'la', 'bajo', 'en', 'tuyos', 'ante', 'sobre', 'suyo', 'desde', 'tuya', 'vuestra', 'hasta', 'nuestro', 'tu', 'esta', 'su', 'esos', 'aquella', 'vuestro', 'sus', 'durante', 'esas', 'del', 'un', 'mi', 'al', 'aquellos', 'aquel', 'mía', 'míos', 'suya', 'tuyas', 'ese', 'por', 'mediante', 'vuestras', 'unas', 'hacia', 'este', 'estos', 'unos', 'una', 'a', 'sin', 'esa', 'estas', 'suyas', 'de', 'tuyo', 'aquellas', 'las', 'con', 'suyos', 'según']

# Create a set to remove duplicates
unique_stopwords = set(stopwords)

# Convert back to a list if needed
stopwords = list(unique_stopwords)

print(stopwords)