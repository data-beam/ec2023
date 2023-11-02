# This function receive an number as string and clear it removing commas and dots in 
# wrong position. After that returns an float number.
# this examples shows how the function must behave:
# Input: 1,456.80   Output: 1456.80
# Input: 5          Output: 5.00
# Input: 46,7       Output: 46.70
# Input: 215,4      Output: 215.40
# Input: 334,8      Output: 334.80
def clear_number(number):
    # If the number is empty, return 0
    if number == '':
        return 0
    
    # Remove all blank and special characters
    number = number.replace(' ', '')
    number = number.replace('\n', '')
    number = number.replace('\t', '')
    number = number.replace('\r', '')
    number = number.replace('(', '')
    number = number.replace(')', '')
    
    try:
        valor = float(number)
        return valor
    except ValueError:
        pass
    
    if number.count(',') == 1:
        number = number.replace(',', '.')

    try:
        valor = float(number)
        return valor
    except ValueError:
        pass
    

    # find position of the last dot
    pos = number.rfind('.')
    
    #remove all dots where position is before the last dot (pos)
    number = number[:pos].replace('.', '') + number[pos:]

    try:
        valor = float(number)
        return valor
    except ValueError:
        pass

    print("Error: ", number)
    return number


# Adiciona um texto ao gráfico    
def addText(chart,angle=300, dx=0, dy=0):
    combined = chart.mark_bar() + chart.mark_text(
        align='left', 
        baseline='bottom', 
        dx=dx,
        dy=dy,
        font='monospace',
        fontWeight='bold',
        fontSize=12,
        angle=angle, 
    )
    combined = combined.configure_axis(
        labelFontSize=14,
        titleFontSize=16
    ).configure_title(
        fontSize=20,
        anchor='middle',
        subtitleFontSize=14,
    )
    return combined