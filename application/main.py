from application import *

def runApp():
    #checking to see if main was ran
    if __name__ == "__main__":
        #instantiates the app
        app = MarketUpdateApp()
        #runs the app until window is closed
        app.mainloop()

runApp()