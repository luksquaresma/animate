

def unpack_nested_lists(lst):
    return [
        item 
        for sublist in lst 
        for item in (
            unpack_nested_lists(sublist) 
            if isinstance(sublist, list)
            else [sublist]
            )
        ]
