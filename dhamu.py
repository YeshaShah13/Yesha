def divide(x,y):
    try:
        result = x/y
    except ZeroDivisionError:
        print('sorry')
    else:
        print(result)
    finally:
        print('congo')

divide(3,2)
divide(3,0)
