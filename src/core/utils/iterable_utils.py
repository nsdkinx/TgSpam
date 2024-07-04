# -*- coding: utf-8 -*-

def remove_duplicates_from_list(lst: list) -> list:
    """Supports unhashable (immutable) types unlike set()."""
    new_list = []
    for element in lst:
        if element in new_list:
            continue
        new_list.append(element)

    return new_list


def split_list(lst: list, chunk_size: int):
    if chunk_size <= 1 or len(lst) <= chunk_size:
        return [lst]

    chunks = [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
    if len(chunks[-1]) < chunk_size:
        last_chunk = chunks.pop()
        chunks.extend([last_chunk] + [[]] * (chunk_size - len(last_chunk)))
    return chunks
