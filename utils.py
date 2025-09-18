def normalize_title(value: str) -> str:
	value = value.strip().lower()
	# collapse inner whitespace
	return " ".join(part for part in value.split())

