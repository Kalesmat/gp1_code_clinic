
def colour(string, colour):
    """
    input your string and desired colour to ouput a new string of 
    specified colour
    """
    if colour == "red":
        final_string = u'\u001b[31m '+string+u" \u001b[0m"
    if colour == "green":
        final_string = u'\u001b[32m '+string+u" \u001b[0m"
    if colour == "yellow":
        final_string = u'\u001b[33m '+string+u" \u001b[0m"
    if colour == "blue":
        final_string = u'\u001b[34m '+string+u" \u001b[0m"
    if colour == "purple":
        final_string = u'\u001b[35m '+string+u" \u001b[0m"
    if colour == "cyan":
        final_string = u'\u001b[36m '+string+u" \u001b[0m"
    if colour == "white":
        final_string = u'\u001b[0m '+string+u" \u001b[0m"

    return(final_string)

