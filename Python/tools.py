import matplotlib, pandas, datetime, numpy, os, sys

class GMAPlot:

    f = matplotlib.figure.Figure
    a = matplotlib.figure.Axes

    @staticmethod
    def custom_axes(datetimes: list, n: int = 30) -> (f, a):
        _, Axes = matplotlib.pyplot.subplots(figsize = (20, 6))
        labels = [x.strftime(format = "%d, %H:%M") for x in datetimes]
        n_ticks, step = len(labels), len(labels)//(n - 1)
        Axes.set_xticks(ticks = range(0, n_ticks, step))
        Axes.set_xticklabels(labels[: : step], rotation = 90)
        Axes.tick_params(labelsize = 12)
        return Axes

    @staticmethod
    def candle_plot(ohlc: pandas.DataFrame, ax: a = None) -> (f, a):
        try: o, h, l, c = ohlc[["Open", "High", "Low", "Close"]].values.T
        except: o, h, l, c = ohlc[["O", "H", "L", "C"]].values.T
        n, bu, be = len(ohlc), (o <= c), (c < o)
        t, x, cw = ohlc.index, numpy.arange(n), 1/(n**(1/2))
        if (ax == None): ax = GMAPlot.custom_axes(datetimes = t)
        ax.bar(x[bu], h[bu] - l[bu], 1*cw, l[bu], fc = "w", ec = "w", lw = 1)
        ax.bar(x[bu], c[bu] - o[bu], 5*cw, o[bu], fc = "w", ec = "w", lw = 1)
        ax.bar(x[be], h[be] - l[be], 1*cw, l[be], fc = "w", ec = "w", lw = 1)
        ax.bar(x[be], o[be] - c[be], 5*cw, c[be], fc = "k", ec = "w", lw = 1)
        return ax.figure, ax

class GMAData:

    @staticmethod
    def tfconv(n_sec: int) -> str:
        tf = ""
        mults = {"S": 1, "M": 60, "H": 60, "D": 24}
        for unit, qty in mults.items():
            if n_sec/qty < 1: return tf
            n_sec = n_sec/qty
            tf = unit + str(int(n_sec))
        return tf

    @staticmethod
    def makeCSV():
        current = os.getcwd()
        sheets = os.listdir(current)
        ohlc = ["d", "t", "O", "H", "L", "C"]
        for n, sheet in enumerate(sheets):
            os.rename(sheet, "_" + sheet)
            if sheet[0].islower(): continue
            prog = 100*(n - 0.5)/(len(sheets) - 1)
            sys.stdout.write("\rProcessing %s: %.2f%%" % (sheet, prog))
            csv = pandas.read_csv("_" + sheet, names = ohlc)
            csv.index = pandas.to_datetime(csv["d"] + " " + csv["t"])
            csv.index += datetime.timedelta(hours = 2)
            csv.drop(columns = ["d", "t"], inplace = True)
            prog = 100*(n - 0.0)/(len(sheets) - 1)
            sys.stdout.write("\rProcessing %s: %.2f%%" % (sheet, prog))
            csv.to_csv(sheet, header = False, index = True)
        print("\nFinished!")
    
    @staticmethod
    def download(quote: str) -> pandas.DataFrame:
        URL = "https://drive.google.com/uc?id="
        IDs = {
            "AUDCAD": "1K_J_Ayd3ENmH33hGbIR12IXC8gs1QPMY",
            "AUDCHF": "1dpbp-7Kopnp7wiiCSLUGQ57s7zLk4lnQ",
            "AUDJPY": "1LclCvy0GFHE-xUJIhrSh4qrGQNj4Li83",
            "AUDNZD": "14C0ug6tyzMB-FQpz5O02gUuR-Ms-2VWm",
            "AUDUSD": "1p_6F9Vrn-veMoQe7Gj6gNEWwIFFLvjPZ",
            "BRENT":  "1RnPV4MFEF3n2vcMgPZI07OxBzlMHwgC5",
            "CAC40":  "1UIKsdN86IVXBopS5G-vm7trhFQT1EfT-",
            "CADCHF": "1j-yC7k5k5NAewZ0DoH0UTkZHV7ecFEPu",
            "CADJPY": "1IQbyh8bf98SOeLw9uFsUR6hI_r56q7c2",
            "CHFJPY": "12oH8zmrUTmnaAed2NCuZfHzk9NuLI3sW",
            "EURAUD": "1BxEvGSqrtkTPTfO0UbWLbs5uMdesl3bB",
            "EURCAD": "1DT1ZcRB0lIw6o4LFSL0sjV-Zju3AmBUP",
            "EURCHF": "1-TlL0gJiNDSAZYoX9hocNqPvEMbxdHIr",
            "EURGBP": "1e-S8uHFQ1Vf0WDQN-rLX9UseW-PxrvQ9",
            "EURJPY": "1w8q0aWQNg60A9IjC1m05A2A__qApwsu2",
            "EURNZD": "14VemLMFTEE25lClN8SuA7HnUZ6ccybyi",
            "EURUSD": "1puF1qbKEtqUquPms6noN1t-ECrKcdaPp",
            "GBPAUD": "1GkNolf7RqfxSmD62N1L1nqwao0OcFkbO",
            "GBPCAD": "15Oa57-It5oXguzWKyaJZKRJ2Gm-4ZZQj",
            "GBPCHF": "1QhO69dl3VIi5KGQ8Ws2v-awJFgzDNrUV",
            "GBPJPY": "1yfrdq3qftvi-okx9eLpJOFFdUf7yxm-C",
            "GBPNZD": "1sYbVfiro89WP_UZJb33A3koNoG0sY9OB",
            "GBPUSD": "1KcExK47W20e9bqpAU0UODq8KYDohROlG",
            "JPN225": "1DAdnsNCUn-mCo1Jcpr82RTHnFQywNmov",
            "NZDCAD": "1jLCaetcBxZlCP0LftRk6D4Q1P3Ozhf6v",
            "NZDCHF": "11nV490C7IPuKLB_yF6AYaBpgI8Toj40A",
            "NZDJPY": "1IwSNG5kQzn8GWCcTs2HMpEyxoJcsGv8x",
            "NZDUSD": "1sokvSTU-5sEaVIUMm4zu4VzBeQ6n5G8D",
            "UK100":  "1_rNREcCjx1WHquhzg8limY5DN5ML94RL",
            "US100":  "1uJdGLMDTVbokJnTrRyNvUw5XoAqVGElB",
            "US500":  "19amjpL-fkv5sC33QO319gcDJOfojBee2",
            "USDCAD": "1wfk7rEOHtX3vykVThqTqVmFaqGhjFr4w",
            "USDCHF": "1D-TSkvsGHimW_AWTh59RApMUtLjm4kmp",
            "USDJPY": "17RWiPvzsKjoJ7LGaYAbJSsXMYT6Ggh4m",
            "USDMXN": "1bcNB7OT_x-wxxnRI0Tw_-KmkKQgELdvD",
            "USDXY":  "1c88dVHjHHyRoE7YkuS8PfT-k87KwmiE4",
            "WTI":    "1WPjVzDN3DoYQBAqQOfToY30AAIHwAaBd",
            "XAGUSD": "1L6Re4UOrzSHu_-RFXpMwMnUdJJeUipf0",
            "XAUUSD": "1N6sm9DUf67pLbbFIgoyuFa6mqggdbkhg",
        }
        assert (quote in IDs.keys()), "Quote inexistent."
        columns = ["O", "H", "L", "C"]
        Data = pandas.read_csv(URL + IDs[quote],
                index_col = 0, names = columns)
        Data.index = pandas.to_datetime(Data.index,
                 format = "%Y-%m-%d %H:%M:%S")
        return Data