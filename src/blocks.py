def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in raw_blocks:
        block = block.strip()
        lines = block.split("\n")
        lines = [ln.strip() for ln in lines]
        cleaned = "\n".join(lines).strip()
        if cleaned:
            cleaned_blocks.append(cleaned)
    return cleaned_blocks