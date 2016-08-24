import time

'''
    #COLOUR DEBUG# ********Some colours appear different depending on OS*******
    #cPrint('warning','This is a warning message')
    #cPrint('prompt','This is a prompt message')
    #cPrint('failure','This is a failure message')
    #cPrint('success','This is a success message')
    #cPrint('critical','This is a critial message')
'''

def cPrint(msType, message,method='print'):

    try:
        mType = {'w':('WARNING','\033[33m'),'s':('SUCCESS','\033[32m'),\
        'f':('FAILED','\033[36m'),'p':('PROMPT','\033[35m'),'c':('CRITICAL','\033[31m')}

        color, header = mType[msType][1], mType[msType][0]
        currentTime = time.strftime('%X')
        colorReset = '\033[0m'
        newLine = '\n'
        carriageReturn = '\r'

	if method == 'print':
            print "{0}{1}[{2}] [{3}] {4}{5}".format \
                  (newLine, color, currentTime, header, message, colorReset)
        else:
            #return "{0}{1}[{2}] [{3}] {4}{5}{6}".format \
            #(newLine, color, currentTime, header, message, colorReset, carriageReturn)

            return "\n{0}[{1}] [{2}] {3}{4}".format \
                   (color, currentTime, header, message, carriageReturn)

    

    except Exception as e:
        print e
        exit(1)


def Intro():
    print "\n"
    cPrint('w','This is a warning message')
    cPrint('p','This is a prompt message')
    cPrint('f','This is a failure message')
    cPrint('s','This is a success message')
    cPrint('c','This is a critial message')

if __name__ == "__main__":
    Intro()
