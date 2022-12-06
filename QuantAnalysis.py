from Function_Set import *

def main():
    df = get_history_data();
    #print(df.iloc[-1,0])
    plot_image(df);


if __name__ == '__main__':
    #get history candlestick image;
    main()
    #Stratage();
    #Test_Stratage();
