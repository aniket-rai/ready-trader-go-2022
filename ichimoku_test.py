import csv
from multiprocessing.sharedctypes import Value

with open('goog.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #Open, High, Low, Close
    data = [[float(x.replace(',', '')) for x in row[1:-1]] for row in list(reader)[1:]]

def get_rolling_average(data, WINDOW_SIZE):
    if len(data) < WINDOW_SIZE:
        pass #IMPLEMENT A FAILSAFE FOR THIS
    
    rolling_average_data = []
    for index in range(WINDOW_SIZE, len(data)):
        rolling_max = max(x[1] for x in data[index - WINDOW_SIZE : index])
        rolling_min = min(x[2] for x in data[index - WINDOW_SIZE : index])
        rolling_avg = round((rolling_max + rolling_min) / 2)
        # rolling_average_data.append((rolling_min, rolling_max, rolling_avg))
        rolling_average_data.append(rolling_avg)
    
    return rolling_average_data


def calculate_tenkan_sen(data):
    #The Conversion Line [(9D-High + 9D-Low) //2]
    temp = get_rolling_average(data, WINDOW_SIZE=9)
    tenkan_sen_data = [None for _ in range(9)] + temp + [None for _ in range(26)]
    return tenkan_sen_data
    

def calculate_kijun_sen(data):
    #The Base Line [(26D-High + 26D-Low) //2]
    temp = get_rolling_average(data, WINDOW_SIZE=26)
    kijun_sen_data = [None for _ in range(26)] + temp + [None for _ in range(26)]
    return kijun_sen_data

def calculate_chikou_span(data):
    #Lagging Span - 26 days backwards
    chikou_span_data = [x[3] for x in data[26:]] + [None for _ in range(52)]
    return chikou_span_data

def calculate_senkou_span_a(data, tenkan, kijun):
    #Conversion and Base Midpoint, offset forwards by 26 (52 total)
    senkou_span_a_data = [None for _ in range(52)]
    
    for index in range(52, len(data) + 26):
        senkou_span_a_data.append((tenkan[index - 26] + kijun[index - 26]) // 2)
    
    return senkou_span_a_data

def calculate_senkou_span_b(data):
    #[(52D-High + 52D-Low) // 2], offset forwards by 26 (78 total)
    temp = get_rolling_average(data, WINDOW_SIZE=52)
    senkou_span_b_data = [None for _ in range(78)] + temp
    return senkou_span_b_data

tenkan = calculate_tenkan_sen(data)
kijun = calculate_kijun_sen(data)
ssa = calculate_senkou_span_a(data, tenkan, kijun)
ssb = calculate_senkou_span_b(data)
# for index, (row, a, b) in enumerate(zip(data + [[None for _ in range(4)] for _ in range(26)], ssa, ssb)):
#     print(index, row + [a] + [b])


def make_prediction():
    pass
