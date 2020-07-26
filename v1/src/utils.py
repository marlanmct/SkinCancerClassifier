# utility functions
def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def addClassNames(classes, results):
    classPercent = {} # dict to store full class names and match percentage
    for key in results.keys():
        classPercent[key] = (classes[key], results[key])
    
    return classPercent
