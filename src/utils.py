# utility functions
def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def addClassNames(classes, results):
    classPercent = {} # dict to store full class names and match percentage
    for i, result in enumerate(results):
        if i == 0:
            classPercent['akiec'] = (classes['akiec'], result)
        elif i == 1:
            classPercent['bcc'] = (classes['bcc'], result)
        elif i == 2:
            classPercent['bkl'] = (classes['bkl'], result)
        elif i == 3:
            classPercent['df'] = (classes['df'], result)
        elif i == 4:
            classPercent['mel'] = (classes['mel'], result)
        elif i == 5:
            classPercent['nv'] = (classes['nv'], result)
        else:
            classPercent['vasc'] = (classes['vasc'], result)
    return classPercent
