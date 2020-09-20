#this is the backend and parts of the front end of the app
#contains many of the aspects inclusing the charts and data
import tkinter as tk
from tkinter import *
from tkcalendar import *
from date import dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.pyplot as plt
from webscrape import getTextfornews
style.use('dark_background')

# fonts to be used by the labels
Large_Font= ("Impact", 30)
Small_Font= ("Arial", 20)
Text_Font= ("Arial", 16)
Header_Font= ("Impact", 23)
#current siginifies the current selection of the ticker to be passed through backend
current = ""
class MarketUpdateApp(tk.Tk):
    def __init__(self, *args,**kwargs):
        #creating the window that will hold all the frames
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"MarketUpdateApp")
        self.container = tk.Frame(self)
        self.container.pack(side="top",fill="both",expand = True)
        self.container.grid_rowconfigure(0,weight = 1)
        self.container.grid_columnconfigure(0,weight = 1)
        #creating the frames and bringing the startpage to the top
        self.frames = {}
        for page in (StartPage,UpdatePage):
            frame = page(self.container, self)
            self.frames[page] = frame
            frame.grid(row=0,column = 0, sticky = "nsew")
        self.show_frame(StartPage)
    # lift up different pages to the top of the window
    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
    # update backend with any changes to the selection by the user.
    def Update(self):
        frame = UpdatePage(self.container, self)
        self.frames[UpdatePage] = frame
        frame.grid(row=0,column = 0, sticky = "nsew")
        self.show_frame(StartPage)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        global current
        # used to change the current selection of the dropdown menu
        variable = StringVar()
        if current=="":
            variable.set("Ticker")
        else:
            variable.set(current)
        # different choices for the tickers
        options = ["^GSPC","AAPL","AMZN","MSFT","GOOG","FB","TSLA","V","JNJ","WMT"]

        tk.Frame.__init__(self,parent)
        # header
        label = tk.Label(self, text = "MarketUpdate", font = Large_Font)
        label.grid(pady=10,padx = 10, row = 0, column = 1)
        # instructions to the user/welcome
        welcomestatement = "Hello! Welcome to the MarketUpdate App."
        welcomestatement+=" Thank you for choosing this platform.\n "
        welcomestatement+="Choose a Ticker and a start date to begin."
        welcome = tk.Label(self, text = welcomestatement, font = Small_Font)
        welcome.grid(pady =10, padx = 10,row =1, column = 1)
        # calendar
        global cal
        cal = Calendar(self, selectmode = "day", year = 2020, month = 5, day = 15)
        cal.grid(pady = 10,padx = 10, row = 2, column =1)
        cal.configure(background = "red", foreground = "black")

        # button for choosing ticker (drop down menu)
        menubutton = OptionMenu(self, variable, *options, command = self.func)
        menubutton.grid(pady=10,padx = 10, row = 2, column =0)
        
        # button for getting an update
        updatebutton = tk.Button(self, text= "Get Update",bg = "red", fg = "red", 
                                 command =lambda:[controller.Update(),controller.show_frame(UpdatePage)])
        updatebutton.grid(padx = 10,pady = 10, row = 2, column = 2)

        newsheadertext = "Most recent news on the general market from Yahoo Finance"
        newsheader = tk.Label(self, text = newsheadertext, font = Header_Font, fg = "red")
        newsheader.grid(pady=10,padx=10, row =3, column = 1)
        # general news for the market
        newsimported = getTextfornews('https://finance.yahoo.com/')
        
        news = tk.Label(self, text = newsimported, font = Text_Font, fg = "blue")
        news.grid(pady=10,padx=10, row =4, column = 1)

    #Used to save the selected ticker from the dropdown menue and also to pass the selection
    #selection into the 
    def func(self,value):
        global current
        current = value

class UpdatePage(tk.Frame):
    def __init__(self, parent, controller):
        global current
        global cal

        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "MarketUpdate for "+current+" Since "+cal.get_date(), font = Large_Font)
        label.pack(pady=10,padx = 10)
        returnbutton = tk.Button(self, text= "Return",bg = "red", fg = "red",
                           command = lambda: controller.show_frame(StartPage))
        returnbutton.pack(padx = 10,pady = 10, side = "bottom")
        # determining if selection has been made yet
        if current!="Ticker" and current!="":
            # gets the selected date from calendar by user using global var
            a = cal.get_date().split("/")
            month = int(a[0])
            day = int(a[1])
            if int(a[2])>30:
                year = int("19"+a[2])
            else:
                year = int("20"+a[2])
            # getting start and end dates, end date being the current date
            d = dt(month, day,year)
            
            #creating Figure for data
            fig = Figure(figsize=(5,5),dpi = 100)
            sub = fig.add_subplot(111)

            # using pandas dataframe and gathering data
            df = web.DataReader(current,'yahoo',d.getProperDate(),d.getToday())
            # plotting the dataframe
            sub.plot(df['Adj Close'])
            data = FigureCanvasTkAgg(fig,self)
            data.draw()
            # adding the usual toolbar that comes with plt
            data.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = TRUE)
            toolbar = NavigationToolbar2Tk(data, self)
            toolbar.update()
            data._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = TRUE)
            # adding the type of news.
            newsforticker1 = "Most recent news for "+current+" on Yahoo Finance"
            newslabel1 = Label(self, text = newsforticker1, font = Text_Font, fg = "red")
            newslabel1.pack(padx = 10, pady = 10, side = "top")
            # adding the news as a label.
            newsforticker2 = "\n"+getTextfornews('https://finance.yahoo.com/quote/{}?p={}'.format(current,current))
            newslabel2 = Label(self, text = newsforticker2, font = Text_Font)
            newslabel2.pack(padx = 10, pady = 10, side = "bottom")
        else:
            error = Label(self, text = "Please click return and select a ticker.", font = Small_Font, fg = "red")
            error.pack(pady=10, padx = 10)


# making sure that the app isnt being passed through
# can be ran through here or on main.py
if __name__ == "__main__":
    app = MarketUpdateApp()
    app.mainloop()