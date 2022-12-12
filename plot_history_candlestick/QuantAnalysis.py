from Function_Set import *

def main():
    #get raw data
    [df,macd] = get_history_data();
    #draw image
    plot_image(df,macd);
    


if __name__ == '__main__':
    #get history candlestick image;
    main()
    #Stratage();
    #Test_Stratage();
