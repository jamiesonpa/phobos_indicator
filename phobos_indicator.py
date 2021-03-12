#libraries and initializations
#region
import requests
import bs4
import urllib
import urllib3
from bs4 import BeautifulSoup
import time
from termcolor import colored
import colorama
from colorama import init
import datetime
import pytrends
from pytrends.request import TrendReq
from datetime import datetime
from datetime import date
pytrend = TrendReq()
#endregion
print("Calculating...")


#handling API links and stuff for glassnode
#region 
links = []
PRICE_link = 'https://api.glassnode.com/v1/metrics/market/price_usd_ohlc?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
MCTCR_link = 'https://api.glassnode.com/v1/metrics/mining/marketcap_thermocap_ratio?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
MVRVZ_link = 'https://api.glassnode.com/v1/metrics/market/mvrv_z_score?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
Puell_link = 'https://api.glassnode.com/v1/metrics/indicators/puell_multiple?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
STH_NUPL_link = 'https://api.glassnode.com/v1/metrics/indicators/nupl_less_155?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
LTH_NUPL_link = 'https://api.glassnode.com/v1/metrics/indicators/nupl_more_155?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
MFRP_link = 'https://api.glassnode.com/v1/metrics/mining/revenue_from_fees?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
PSIP_link  = 'https://api.glassnode.com/v1/metrics/supply/profit_relative?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
TSLA30to90_link = 'https://api.glassnode.com/v1/metrics/supply/active_1m_3m?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
RP_link1 = 'https://api.glassnode.com/v1/metrics/indicators/realized_profit?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
NVT_link = 'https://api.glassnode.com/v1/metrics/indicators/nvts?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
CVDD_link = 'https://api.glassnode.com/v1/metrics/indicators/cvdd?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
RC_link = 'https://api.glassnode.com/v1/metrics/market/marketcap_realized_usd?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
RHODL_link = 'https://api.glassnode.com/v1/metrics/indicators/rhodl_ratio?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
RP_link2 = 'https://api.glassnode.com/v1/metrics/indicators/realized_profit?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&&api_key='
EADF_link = 'https://api.glassnode.com/v1/metrics/indicators/dormancy_flow?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
TTVCA_link = 'https://api.glassnode.com/v1/metrics/transactions/transfers_volume_adjusted_sum?a=BTC&c=usd&e=aggregated&f=csv&i=24h&timestamp_format=humanized&api_key='
aSOPR_link = 'https://api.glassnode.com/v1/metrics/indicators/sopr_adjusted?a=BTC&c=native&e=aggregated&f=csv&i=24h&timestamp_format=humanized&u=1611705600&api_key='

links = [(aSOPR_link, "asopr"),(TTVCA_link, "ttvca"),(EADF_link, "eadf"),(RP_link2, "rp1"),(PRICE_link,"price"),(RC_link,"rc"), (CVDD_link,"cvdd"), (Puell_link,"puell"),(STH_NUPL_link,"sthnupl"),(LTH_NUPL_link,"lthnupl"),(MVRVZ_link,"mvrvz"),(MCTCR_link,"mctcr"), (NVT_link,"nvt"),(RP_link1,"rp2"),(MFRP_link,"mfrp"),(PSIP_link,"psip"), (TSLA30to90_link, "tsla"), (RHODL_link, "rhodl")]
api_appended_links = []
#This API key will have to be replaced if being used by someone else
api_key = '6293830e-a13c-42c5-853e-8e316e17731f'
for link in links:
    newlink = link[0] + api_key
    api_appended_links.append((newlink, link[1]))
#endregion

#handling API links and stuff for cryptoquant
cc_access_token = "8sVB89r4XQGTfj57Oorso31Pl8E8u1oyA4AbviJY"
btc_exchange_inflow_url = "https://api.cryptoquant.com/v1/btc/exchange-flows/inflow?exchange=all_exchange&window=day&from=20110101&limit=10000000"
btc_miner_netflow_url = "https://api.cryptoquant.com/v1/btc/miner-flows/netflow?miner=all_miner&window=day&from=20110101&limit=10000000"
btc_miner_to_exchanges_url = "https://api.cryptoquant.com/v1/btc/inter-entity-flows/miner-to-exchange?from_miner=all_miner&to_exchange=all_exchange&window=day&from=20110101&limit=10000000"
btc_miner_to_spot_exchange_url = "https://api.cryptoquant.com/v1/btc/inter-entity-flows/miner-to-exchange?from_miner=all_miner&to_exchange=spot_exchange&window=day&from=20110101&limit=10000000"
price_url = "https://api.cryptoquant.com/v1/btc/market-data/price-usd?window=day&from=20200101&limit=10000000"

cc_urls = [(btc_exchange_inflow_url, "btc_exch_inflow"),(btc_miner_netflow_url, "btc_miner_netflow"), (btc_miner_to_exchanges_url, "btc_miners2exch"), (btc_miner_to_spot_exchange_url,"btc_miners2spot"), (price_url, "btc_price")]

#main functions
#region
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def acquire_datasets(links):
    datasets = []
    for link in links:
        html = urllib.request.urlopen(link[0])
        time.sleep(1)
        soup = BeautifulSoup(html, "html.parser")
        split_soup = str(soup).split("\n")
        datapoints = []
        ss = split_soup[1:(len(split_soup)-1)]
        for line in ss:
            split_line = line.split(",")
            datapoints.append(split_line[1])    
        datasets.append((link[1],datapoints))

    return datasets
def GetCryptoQuant_data(access_token, cc_urls):

    headers = { 'Authorization': 'Bearer ' + access_token }

    btc_miners2exch = []
    btc_miners2spot = []
    btc_miner_netflow = []
    btc_exch_inflow = []
    btc_price = []

    counter = 0
    for url in cc_urls:

        url_text = url[0]
        response = requests.get(url_text, headers=headers)
        response_text = response.text
        split_response = response_text.split("{")
        for line in split_response:
            line = line[0:len(line)-2]
            splitlines = line.split(",")
            current_datapoint = []
            for splitline in splitlines:
                if splitline.find("date") != -1:
                    split_splitline = splitline.split(":")
                    datepoint = split_splitline[1].replace('"',"")
                    datepoint = datepoint.strip()
                    current_datapoint.append(datepoint)
                if splitline.find("inflow_total") != -1:
                    split_splitline = splitline.split(":")
                    flowpoint = split_splitline[1].strip()
                    flowpoint = flowpoint.replace('"',"")
                    flowpoint = flowpoint.replace('}',"")
                    flowpoint = flowpoint.replace(']',"")
                    flowpoint = flowpoint.replace('{',"")
                    flowpoint = float(flowpoint)
                    current_datapoint.append(flowpoint)
                elif splitline.find("flow_total") != -1:
                    split_splitline = splitline.split(":")
                    flowpoint = split_splitline[1].strip()
                    flowpoint = flowpoint.replace('"',"")
                    flowpoint = flowpoint.replace('}',"")
                    flowpoint = flowpoint.replace(']',"")
                    flowpoint = flowpoint.replace('{',"")
                    flowpoint = float(flowpoint)
                    current_datapoint.append(flowpoint)
                elif splitline.find("price_usd_close") != -1:
                    split_splitline = splitline.split(":")
                    flowpoint = split_splitline[1].strip()
                    flowpoint = flowpoint.replace('"',"")
                    flowpoint = flowpoint.replace('}',"")
                    flowpoint = flowpoint.replace(']',"")
                    flowpoint = flowpoint.replace('{',"")
                    flowpoint = float(flowpoint)
                    current_datapoint.append(flowpoint)
            if counter == 0:
                btc_exch_inflow.append(current_datapoint)
            elif counter == 1:
                btc_miner_netflow.append(current_datapoint)
            elif counter == 2:
                btc_miners2exch.append(current_datapoint)
            elif counter == 3:
                btc_miners2spot.append(current_datapoint)
            elif counter == 4:
                btc_price.append(current_datapoint)
        counter = counter + 1
    

    btc_exch_inflow_fixed = []
    for point in btc_exch_inflow:
        if point != []:
            btc_exch_inflow_fixed.append(point)

    btc_miner_netflow_fixed = []
    for point in btc_miner_netflow:
        if point != []:
            btc_miner_netflow_fixed.append(point)

    btc_miners2exch_fixed = []
    for point in btc_miners2exch:
        if point != []:
            btc_miners2exch_fixed.append(point)


    btc_miners2spot_fixed = []
    for point in btc_miners2spot:
        if point != []:
            btc_miners2spot_fixed.append(point)
            
    btc_price_fixed = []
    for point in btc_price:
        if point != []:
            btc_price_fixed.append(point)

    combined_data = []
    for point in btc_exch_inflow_fixed:
        date = point[0]
        for point2 in btc_miner_netflow_fixed:
            if point2[0] == date:
                combined_data.append([point[0], point[1], point2[1]])

    combined_data2 = []
    for point in combined_data:
        date = point[0]
        for point3 in btc_miners2exch_fixed:
            if point3[0] == date:
                combined_data2.append([point[0], point[1], point[2], point3[1]])
    combined_data3 = []
    for point in combined_data2:
        date = point[0]
        for point4 in btc_miners2spot_fixed:
            if point4[0] == date:
                combined_data3.append([point[0], point[1], point[2], point[3], point4[1]])
    combined_data4 = []
    for point in combined_data3:
        date = point[0]
        for point5 in btc_price_fixed:
            if point5[0] == date:
                combined_data4.append([point[0], point[1], point[2], point[3], point[4], point5[1]])

    combined_data4.reverse()


    btc_miners2_spot_7dsum = 0
    btc_exch_inflow_7dsum = 0
    for point in combined_data4[len(combined_data4)-8:len(combined_data4)-1]:
        btc_miners2_spot_7dsum = btc_miners2_spot_7dsum + point[4]
        btc_exch_inflow_7dsum = btc_exch_inflow_7dsum + point[1]
    
    todays_btc_miner2spot = (combined_data4[len(combined_data4)-1])[4]
    todays_btc_exchinflow = (combined_data4[len(combined_data4)-1])[1]
    btc_miners2spot_7dMA = btc_miners2_spot_7dsum/7
    btc_exch_inflow_7dMA = btc_exch_inflow_7dsum/7

    if float(todays_btc_miner2spot) > float(btc_miners2spot_7dMA):
        today_m2s_greater = True
        print("Bitcoin miners to spot exchanges 7 day moving average: " + str(btc_miners2spot_7dMA) + " | Today's value: " + str(todays_btc_miner2spot) + " | Today's value is greater than the MA") 
    else:
        today_m2s_greater = False
        print("Bitcoin miners to spot exchanges 7 day moving average: " + str(btc_miners2spot_7dMA) + " | Today's value: " + str(todays_btc_miner2spot) + " | Today's value is less than the MA") 

    if todays_btc_exchinflow > btc_exch_inflow_7dMA:
        today_eif_greater = True
        print("Bitcoin exchange inflow 7 day moving average: " + str(btc_exch_inflow_7dMA) + " | Today's value: " + str(todays_btc_exchinflow)  + " | Today's value is greater than the MA")
    else:
        today_eif_greater = False
        print("Bitcoin exchange inflow 7 day moving average: " + str(btc_exch_inflow_7dMA) + " | Today's value: " + str(todays_btc_exchinflow)  + " | Today's value is less than the MA")

def GetG_trends_data():
    pytrends = TrendReq(hl='en-US', tz=360)
    kw_list = ["bitcoin", "ethereum"]
    pytrends.build_payload(kw_list, timeframe='today 5-y', geo='US')
    df = pytrends.interest_over_time().tail(1)
    current_google_trends_datapoint = int(df.iat[0,0])
    ethereum_datapoint = str(int(df.iat[0,1]))
    print("Gtrends datapoint (ETH): " + str(ethereum_datapoint) + " (previous ATH was 9)")
    if current_google_trends_datapoint < 75:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        if current_google_trends_datapoint < 85:
            print("Gtrends datapoint (BTC): " + str(current_google_trends_datapoint) + ", indicating that we are in the " + colored("CAUTION ZONE", "yellow"))
        else:
            if current_google_trends_datapoint < 95:
                print("Gtrends datapoint (BTC): " + str(current_google_trends_datapoint) + ", indicating that we are in the " + colored("HIGH CAUTION ZONE", "orange", attrs=["blink"]))
            else:
                if current_google_trends_datapoint < 100:
                    print("Gtrends datapoint (BTC): " + str(current_google_trends_datapoint) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
    else:
        print("Gtrends datapoint (BTC): " + str(current_google_trends_datapoint) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))


def GetMCTCR_data(data):
    values = data[1]
    if float(values[-1]) < 0.0000038:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final MCTCR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]) + " NOTE: THIS IS A HIGHLY RELIABLE INDICATOR. DO NOT IGNORE THIS PIERCE")
        return (float(values[-1])/0.0000038)
    elif ((float(values[-1]))/(0.0000038)) > .9:
        print("Final MCTCR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("CAUTION ZONE", "YELLOW", attrs=["blink"]) + " NOTE: THIS IS A HIGHLY RELIABLE INDICATOR. DO NOT IGNORE THIS PIERCE")
        return (float(values[-1])/0.0000038)
    else:
        print("Final MCTCR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/0.0000038)

def GetTTVCA_data(data, price):
    values = data[1]
    last_val = float(values[-1])
    ratio = last_val/float(price)
    if ratio < 2000000:
        dangerzone = False
    else:
        dangerzone = True
    
    proportion = round(((ratio/2000000) *100),2)

    if proportion > 93:
        cautionzone = True
    else:
        cautionzone = False

    if dangerzone == True:
        print("Final TTVCA datapoint: " + str(ratio) + ", which is " + str(proportion) + "% to the threshold, indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]) + " NOTE: THIS IS A HIGHLY RELIABLE INDICATOR. DO NOT IGNORE THIS PIERCE")
        return ratio
    elif cautionzone == True:
        print("Final TTVCA datapoint: " + str(ratio) + ", which is " + str(proportion) + "% to the threshold, indicating that we are in the " + colored("CAUTION ZONE", "yellow", attrs=["blink"]) + " NOTE: THIS IS A HIGHLY RELIABLE INDICATOR. DO NOT IGNORE THIS PIERCE")
        return ratio
    else:
        print("Final TTVCA datapoint: " + str(ratio) + ", which is " + str(proportion) + "% to the threshold, indicating that we are in the " + colored("SAFE ZONE", "green"))
        return ratio

def GetRHODL_data(data):
    values = data[1]
    if float(values[-1]) < 50000:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        if  float(values[-1]) < 60000:
            print("Final RHODL datapoint: " + str( float(values[-1])) + ", indicating that we are in the " + colored("CAUTION ZONE", "yellow"))
            return (float(values[-1])/50000)
        else:
            if  float(values[-1]) < 70000:
                print("Final RHODL datapoint: " + str(float(values[-1])) + ", indicating that we are in the " + colored("HIGH CAUTION ZONE", "orange"))
                return (float(values[-1])/50000)
            else:
                if  float(values[-1]) < 100000:
                    print("Final RHODL datapoint: " + str( float(values[-1])) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
                else:
                    print(colored("WARNING: RHODL ERROR", "red"))
    else:
        print("Final RHODL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/50000)


def GetaSOPR_data(data, price):
    values = data[1]
    if float(values[-1]) < 1.2:
        cautionzone = False
        dangerzone = False
    elif float(values[-1]) < 30:
        if float(values[-1]) > 1.3:
            cautionzone = False
            dangerzone = True
        else:
            dangerzone = False
            if float(values[-1]) > 1.2:
                cautionzone = True


    if dangerzone == True:
        print("Final aSOPR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return (float(values[-1])/1.4)
    elif cautionzone == True:
        print("Final aSOPR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("CAUTION ZONE", "yellow", attrs=["blink"]) + " NOTE: THIS IS A HIGHLY RELIABLE INDICATOR. DO NOT FUCK THIS UP")
        return (float(values[-1])/1.4)
    else:
        print("Final aSOPR datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/1.4)
    

def GetMVRVZ_data(data):
    values = data[1]
    if float(values[-1]) < 7:
        dangerzone = False
    else:
        dangerzone = True

    if float(values[-1]) < 6:
        cautionzone = True
    else:
        cautionzone = False

    if dangerzone == True:
        print("Final MVRVZ datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]) + " NOTE: THIS IS A HIGHLY RELIABLE INDICATOR. DO NOT FUCK THIS UP")
        return (float(values[-1])/7)
    elif cautionzone == True:
        print("Final MVRVZ datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("CAUTION ZONE", "yellow", attrs=["blink"]) + " NOTE: THIS IS A HIGHLY RELIABLE INDICATOR. DO NOT FUCK THIS UP")
        return (float(values[-1])/7)
    else:
        print("Final MVRVZ datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/7)
    
def GetPuell_data(data):
    values = data[1]
    if float(values[-1]) < 4.2:
        dangerzone = False
    else:
        dangerzone = True

    if float(values[-1]) > 3:
        cautionzone = True
    else:
        cautionzone = False

    if dangerzone == True:
        print("Final Puell datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]) + "NOTE: THIS IS A HIGHLY RELIABLE INDICATOR: DONT FUCK THIS UP")
        return (float(values[-1])/4.2)
    elif cautionzone == True:
        print("Final Puell datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("CAUTION ZONE", "yellow", attrs=["blink"]) + "NOTE: THIS IS A HIGHLY RELIABLE INDICATOR: DONT FUCK THIS UP")
        return (float(values[-1])/4.2)
    else:
        print("Final Puell datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green")) 
        return (float(values[-1])/4.2)

def GetSTHNUPL_data(data):
    values = data[1]
    if float(values[-1]) < .48:
        dangerzone = False
    else:
        dangerzone = True

    if float(values[-1]) > .38:
        cautionzone = True
    else:
        cautionzone = False


    if dangerzone == True:
        print("Final STHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return (float(values[-1])/.48)
    elif cautionzone == True:
        print("Final STHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("CAUTION ZONE", "yellow", attrs=["blink"]))
        return (float(values[-1])/.48)
    else:
        print("Final STHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/.48)

def GetLTHNUPL_data(data):
    values = data[1]
    if float(values[-1]) < .94:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final LTHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return (float(values[-1])/.94)
    else:
        print("Final LTHNUPL datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/.94)

def GetMFRP_data(data):
    values = data[1]
    if float(values[-1]) < .35:
        dangerzone = False
    else:
        dangerzone = True

    if dangerzone == True:
        print("Final MFRP datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return (float(values[-1])/.35)
    else:
        print("Final MFRP datapoint: " + str(values[-1]) + ", indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/.35)

def GetEADF_data(data):
    values = data[1]
    if float(values[-1]) < 1500000:
        dangerzone = False
    else:
        dangerzone = True
    
    if float(values[-1]) > (1500000 * .93):
        cautionzone = True
    else:
        cautionzone = False

    if dangerzone == True:
        print("Final EADF datapoint: " + str(values[-1]) + ", which is " + str(round(((float(values[-1])/1500000)*100),2)) + "% of the threshold, indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return (float(values[-1])/1500000)
    elif cautionzone == True:
        print("Final EADF datapoint: " + str(values[-1]) + ", which is " + str(round(((float(values[-1])/1500000)*100),2)) + "% of the threshold, indicating that we are in the " + colored("CAUTION ZONE", "yellow", attrs=["blink"]))
        return (float(values[-1])/1500000)
    else:
        print("Final EADF datapoint: " + str(values[-1]) + ", which is " +  str(round(((float(values[-1])/1500000)*100),2))  + "% of the threshold, indicating that we are in the " + colored("SAFE ZONE", "green"))
        return (float(values[-1])/1500000)

def GetPSIP_data(data):
    values = data[1]

    if float(values[-1]) < .9:
        not_in_high_zone = True
    else:
        not_in_high_zone = False
    
    last10sum = 0
    for value in values[-11:-1]:
        if float(value) > .90:
            last10sum = last10sum+1
        else:
            last10sum = last10sum+0
    
    if last10sum > 8:
        been_in_high_zone = True
    else:
        been_in_high_zone = False
    
    if not_in_high_zone == True:
        if been_in_high_zone == True:
            dangerzone = True
        else:
            dangerzone = False
    else:
        dangerzone = False

    if dangerzone == True:
        print("Final PSIP datapoint: "  + str(values[-1]) + " indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return 1
    else:
        print("Final PSIP datapoint: " + str(values[-1]) + " indicating that we are in the " + colored("SAFE ZONE", "green"))
        return 0

def GetTSLA_data(data):
    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    positive_slope_sum = 0
    for slope in slopes[-11:-2]:
        if float(slope) > 0:
            positive_slope_sum = positive_slope_sum + 1
        else:
            positive_slope_sum = positive_slope_sum + 1
    
    if slopes[-1] > 0:
        dangerzone = False
    else:
        if positive_slope_sum > 9:
            dangerzone = True
        else:
            dangerzone = False

    if dangerzone == True:
        print("Final TLSA30to90 verdict-- last ten slopes postive, current slope negative, indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return 1
    else:
        print("Final TLSA30to90 verdict-- we are in the " + colored("SAFE ZONE", "green"))
        return 0

def GetCVDD_data(data):
    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    if slopes[-1] > 60:
        dangerzone = True
    else:
        dangerzone = False

    if dangerzone == True:
        print("Final CVDD verdict-- we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return 1
    else:
        print("Final CVDD verdict-- we are in the " + colored("SAFE ZONE", "green"))
        return 0
    
def GetNVT_data(data):

    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    positive_slope_sum = 0
    for slope in slopes[-11:-2]:
        if float(slope) > 0:
            positive_slope_sum = positive_slope_sum + 1
        else:
            positive_slope_sum = positive_slope_sum + 1
    
    if slopes[-1] > 0:
        dangerzone = False
    else:
        if positive_slope_sum > 9:
            dangerzone = True
        else:
            dangerzone = False

    if dangerzone == True:
        print("Final NVT verdict-- last ten slopes postive, current slope negative, indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]) + " (Note: this is a sell indicator only valid during INSANE bull runs for finding absolute price peaks)")
        print("\t\t NVT function says that the running positive slope sum is " + str(positive_slope_sum))
    else:
        print("Final NVT verdict-- we are in the " + colored("SAFE ZONE", "green"))
        print("\t\t NVT function says that the running positive slope sum is " + str(positive_slope_sum))
    
    if dangerzone == True:
        return 1
    else:
        return 0

def GetRC_data(data):
    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1

    counter = 1
    jerks = []
    for slope_point in slopes:
        if counter < (len(slopes)):
            jerk = abs((float(slopes[counter]) - float(slopes[counter-1]))/100000)
            jerks.append(jerk)
        counter = counter +1

    if jerks[-1] > 25000:
        dangerzone = True
    else:
        dangerzone = False

    if dangerzone == True:
        print("Final RCJ datapoint: " + str(jerks[-1]) + ", indicating we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
    else:
        print("Final RCJ datapoint: " + str(jerks[-1]) + ", indicating we are in the " + colored("SAFE ZONE", "green"))
    return (jerks[-1]/25000)

def GetPrice_data(data):
    values = data[1]
    return values[-2]

def GetRP_data1(data):

    values = data[1]
    slopes = []
    counter = 1
    while counter < len(values):
        if values[counter] == "":
            if values[counter-1] == "":
                slope = 0
            else:
                slope = 0 - float(values[counter-1])
        elif values[counter-1] == "":
            slope = float(values[counter]) - 0
        else:
            slope = float(values[counter]) - float(values[counter-1])
        slopes.append(slope)
        counter = counter +1
    
    positive_slope_sum = 0
    for slope in slopes[-11:-2]:
        if float(slope) > 0:
            positive_slope_sum = positive_slope_sum + 1
        else:
            positive_slope_sum = positive_slope_sum + 1
    
    if slopes[-1] > 0:
        dangerzone = False
    else:
        if positive_slope_sum > 9:
            dangerzone = True
        else:
            dangerzone = False

    if dangerzone == True:
        print("Final RP Slope verdict-- last ten slopes postive, current slope negative, indicating that we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
        return 1
    else:
        print("Final RP Slope verdict-- we are in the " + colored("SAFE ZONE", "green"))
        return 0

def GetRP_data2(data, p):
    currentprice = p
    values = data[1]
    rpdatapoint = float(values[-1])
    RPthreshold = (float(currentprice) * 200000)
    percent_to_threshold =((rpdatapoint/RPthreshold)*100)

    if percent_to_threshold >= 95:
        dangerzone = True
    else:
        dangerzone = False

    if dangerzone == True:
        print("Final RP2 datapoint: " + str(percent_to_threshold) + "%" + ", indicating we are in the " + colored("DANGER ZONE", "red", attrs=["blink"]))
    else:
        print("Final RP2 datapoint: " + str(percent_to_threshold) + "%" + ", indicating we are in the " + colored("SAFE ZONE", "green"))
    
    retstr = 1

    return retstr
    
def GetCurrentDate(data):
    datasets = []
    for link in data:
        if link[1] == "price":
            html = urllib.request.urlopen(link[0])
            time.sleep(1)
            soup = BeautifulSoup(html, "html.parser")
            split_soup = str(soup).split("\n")
            datapoints = []
            ss = split_soup[1:(len(split_soup)-1)]
            line_of_interest = ss[-2]
            split_line_of_interest = line_of_interest.split(",")
            current_date = split_line_of_interest[0]
    return current_date

#endregion

#script execution
#region
GetG_trends_data()
GetCryptoQuant_data(cc_access_token, cc_urls)
acquired_data = acquire_datasets(api_appended_links)
last_price = 0

for dataset in acquired_data:
    if str(dataset[0]) == "price":
        prices = dataset[1]
        last_price = prices[-2]

for dataset in acquired_data:
    if dataset[0] == "mctcr":
        MCTCR = GetMCTCR_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "ttvca":
        TTVCA = GetTTVCA_data(dataset, last_price)

for dataset in acquired_data:
    if dataset[0] == "mvrvz":
        MVRVZ = GetMVRVZ_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "eadf":
        EADF = GetEADF_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "puell":
        PUELL = GetPuell_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "sthnupl":
        STHNUPL = GetSTHNUPL_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "lthnupl":
        LTHNUPL = GetLTHNUPL_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "mfrp":
        MFRP = GetMFRP_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "psip":
        PSIP = GetPSIP_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "tsla":
        TSLA = GetTSLA_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "cvdd":
        CVDD = GetCVDD_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "nvt":
        NVT = GetNVT_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "rc":
        RC = GetRC_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "price":
        PRICE = GetPrice_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "rhodl":
        RHODL = GetRHODL_data(dataset)

for dataset in acquired_data:
    if dataset[0] == "rp1":
        RP1 = GetRP_data1(dataset)

for dataset in acquired_data:
    if dataset[0] == "rp2":
        RP2 = GetRP_data2(dataset, PRICE)

for dataset in acquired_data:
    if dataset[0] == "asopr":
        aSOPR = GetaSOPR_data(dataset, PRICE)

date_time = GetCurrentDate(api_appended_links)
BinaryIndicators = (CVDD + NVT + RP1 + TSLA + PSIP)/5
Non_BinaryIndicators = (RC + MCTCR + MVRVZ + PUELL + STHNUPL + LTHNUPL + MFRP + aSOPR)/8
IndicatorMetric = ((BinaryIndicators + Non_BinaryIndicators)/2) + .1


if (IndicatorMetric * 100) > 85:
    tcolor = "red"
elif (IndicatorMetric *100) >70:
    tcolor = "orange"
elif (IndicatorMetric*100) > 50:
    tcolor = "yellow"
else:
    tcolor = "green"

indicator_metric_string = str((round(IndicatorMetric*100,2))) + "%"
print("Pierce's Modulus for " +  date_time + " is " + colored(indicator_metric_string, tcolor) + ". Greater than 70% indicates highly probable sell.")
if tcolor == "red":
    print("You should fucking sell right now")
elif tcolor == "orange":
    print("probably hold, but be careful")
elif tcolor == "yellow":
    print("hodl")
elif tcolor == "green":
    print("hodlllll")

d1 = date.today()
d0 = date(2020, 3, 8)
delta = d1 - d0
days = 600
elapsed = delta.days

percentage_to_peak_chrono = round(((elapsed/days)*100),2)

if percentage_to_peak_chrono < 25:
    print("Chronologically, we are " + colored((str(percentage_to_peak_chrono) + "%"), "green", attrs=["blink"]) + " of the way to our projected market peak.")
elif percentage_to_peak_chrono < 50:
    print("Chronologically, we are " + colored((str(percentage_to_peak_chrono) + "%"), "yellow",) + " of the way to our projected market peak.")
elif percentage_to_peak_chrono < 75:
    print("Chronologically, we are " + colored((str(percentage_to_peak_chrono) + "%"), "yellow", attrs=["blink"]) + " of the way to our projected market peak.")
elif percentage_to_peak_chrono < 100:
    print("Chronologically, we are " + colored((str(percentage_to_peak_chrono) + "%"), "red") + " of the way to our projected market peak.")
elif percentage_to_peak_chrono > 100:
    print("Chronologically, we are " + colored((str(percentage_to_peak_chrono) + "%"), "red", attrs=["blink"]) + " of the way to our projected market peak.")


print("\nIf one or more of these indicators is red, there is cause for alarm")

output_string = ""
for dataset in acquired_data:
    values = dataset[1]
    if dataset[0] == "price":
        value_of_interest = values[-2]
    else:
        value_of_interest = values[-1]
    output_string = output_string+ value_of_interest + ","

print(output_string)


finish = input("Press enter to close the window...")

#endregion
