# 本代码是为了查询历史价格并写入文档（爬取5年内的所有数据并保存，从2021年5月的数据开始）
import csv
from Config import *
import os
import gate_api
#from Function import *
from gate_api.exceptions import ApiException, GateApiException
#获取数据--》存储数据
import gate_api
from gate_api.exceptions import ApiException, GateApiException
from Get_Data_Function import *


# print(contracts_list)
# if ("MASK_USDT" in contracts_list):
#     print("Yes")
#['KNC_USDT', 'OOKI_USDT', 'BIT_USDT', 'ZEC_USDT', 'SC_USDT', 'RVN_USDT', 'ICX_USDT', '
# DUSK_USDT', 'BEL_USDT', 'REEF_USDT', 'ALCX_USDT', 'ASTR_USDT', 'INJ_USDT', 'CAKE_USDT', 
# 'LAZIO_USDT', 'ONE_USDT', 'CEL_USDT', 'ETH_USDT', 'KLAY_USDT', 'COTI_USDT', 'MKISHU_USDT', 
# 'MANA_USDT', 'MOVR_USDT', 'OMG_USDT', 'UNI_USDT', 'LTC_USDT', 'AAVE_USDT', 'DENT_USDT', 
# 'QRDO_USDT', 'BNB_USDT', 'ALPHA_USDT', 'RAY_USDT', 'APE_USDT', 'CERE_USDT', 'STMX_USDT', 
# 'XCN_USDT', 'OGN_USDT', 'OKB_USDT', 'DOT_USDT', 'TLM_USDT', 'BTM_USDT', 'ADA_USDT', 'ANKR_USDT', 
# 'ANT_USDT', 'TRX_USDT', 'MTL_USDT', 'YFII_USDT', 'SUN_USDT', 'SAND_USDT', 'MBABYDOGE_USDT', 
# 'WIN_USDT', 'LUNC_USDT', 'SRM_USDT', 'STG_USDT', 'BAT_USDT', 'AXS_USDT', 'SOL_USDT', 'MAKITA_USDT', 
# 'BNT_USDT', 'BLZ_USDT', 'PSG_USDT', 'IOTA_USDT', 'RSR_USDT', 'PYR_USDT', 'FITFI_USDT', 'MKR_USDT', 
# 'PERP_USDT', 'COMP_USDT', 'LINK_USDT', 'CHR_USDT', 'CFX_USDT', 'GARI_USDT', 'DGB_USDT', 'MBOX_USDT', 
# 'WEMIX_USDT', 'DYDX_USDT', 'LUNA_USDT', 'HT_USDT', 'TRB_USDT', 'CTK_USDT', 'ACA_USDT', 'TFUEL_USDT', 
# 'OCEAN_USDT', 'XLM_USDT', 'HOT_USDT', 'FTM_USDT', 'LPT_USDT', 'SOS_USDT', 'ALGO_USDT', 'SHIB_USDT', 
# 'BSV_USDT', 'PORTO_USDT', 'SFP_USDT', 'SANTOS_USDT', 'BADGER_USDT', 'DAR_USDT', 'DEFI_USDT', 
# 'XEM_USDT', 'ALICE_USDT', 'ICP_USDT', 'RARE_USDT', 'LRC_USDT', 'BAKE_USDT', 'FLUX_USDT', 
# 'CRO_USDT', 'CVC_USDT', 'MINA_USDT', 'LIT_USDT', 'AST_USDT', 'AUDIO_USDT', 'ZIL_USDT', 
# 'XMR_USDT', 'FRONT_USDT', 'CTSI_USDT', 'AGLD_USDT', 'YGG_USDT', 'OP_USDT', 'ZRX_USDT', 
# 'GT_USDT', 'XCH_USDT', 'VET_USDT', 'MOB_USDT', 'BICO_USDT', 'SLP_USDT', 'ACH_USDT', 'AR_USDT', 
# 'CLV_USDT', 'IMX_USDT', 'SPELL_USDT', 'UNFI_USDT', 'SUSHI_USDT', 'FTT_USDT', 'HIGH_USDT', 
# 'HNT_USDT', 'ALT_USDT', 'YFI_USDT', 'NEAR_USDT', 'NKN_USDT', 'XVS_USDT', 'BAND_USDT', 'LOKA_USDT', 
# 'BCH_USDT', 'TOMO_USDT', 'WAVES_USDT', 'FIDA_USDT', 'DIA_USDT', 'ANC_USDT', 'CELO_USDT', 'CRV_USDT', 
# 'FLM_USDT', 'GLMR_USDT', 'FIL_USDT', 'PEOPLE_USDT', 'WAXP_USDT', 'IOTX_USDT', 'ATOM_USDT', 
# 'RLC_USDT', 'HBAR_USDT', 'REN_USDT', 'GMT_USDT', 'KAVA_USDT', 'KDA_USDT', 'GALA_USDT', 'STORJ_USDT', 
# 'PUNDIX_USDT', 'BAL_USDT', 'XAUG_USDT', 'GRIN_USDT', 'SXP_USDT', 'AKRO_USDT', 'NEXO_USDT', 'CKB_USDT', 
# 'API3_USDT', 'NEST_USDT', 'POLY_USDT', 'ETHW_USDT', 'TONCOIN_USDT', 'THETA_USDT', 'CREAM_USDT', 
# 'BTC_USDT', 'GST_USDT', 'BEAM_USDT', 'HFT_USDT', 'KSM_USDT', 'RAD_USDT', 'QTUM_USDT', 'WOO_USDT', 
# 'ATA_USDT', 'AVAX_USDT', 'EOS_USDT', 'SNX_USDT', 'AUCTION_USDT', 'XRP_USDT', 'GITCOIN_USDT', 
# 'MATIC_USDT', 'ONT_USDT', 'LINA_USDT', 'DASH_USDT', 'MASK_USDT', 'ETC_USDT', 'JST_USDT', 
# 'BSW_USDT', 'CONV_USDT', 'SKL_USDT', 'GAL_USDT', 'DODO_USDT', 'GRT_USDT', 'TRU_USDT', 'STX_USDT', 
# 'CVX_USDT', 'JASMY_USDT', 'HIVE_USDT', 'EXCH_USDT', 'ROSE_USDT', 'SUPER_USDT', 'SCRT_USDT', 
# 'USTC_USDT', 'ENJ_USDT', 'BTS_USDT', 'LOOKS_USDT', 'QNT_USDT', 'HOOK_USDT', 'FLOW_USDT', 
# 'RUNE_USDT', 'APT_USDT', 'CHZ_USDT', 'DOGE_USDT', '1INCH_USDT', 'PRIV_USDT', 'CSPR_USDT', 
# 'C98_USDT', 'RACA_USDT', 'CELR_USDT', 'XEC_USDT', 'ENS_USDT', 'POND_USDT', 'NYM_USDT', 
# 'PROM_USDT', 'IOST_USDT', 'ZEN_USDT', 'LDO_USDT', 'RNDR_USDT', 'REQ_USDT', 'DEGO_USDT', 
# 'VRA_USDT', 'QUICK_USDT', 'VGX_USDT', 'XTZ_USDT', 'EGLD_USDT', 'POLS_USDT', 'ARPA_USDT', 
# 'NFT_USDT']
settle = 'usdt' # str | Settle currency
contract = 'MATIC_USDT' # str | Futures contract
final_time = int(time.time())
bar_interval = ["1m","5m","1h","4h","1d","1w"]
# print(os.listdir("./plot_history_candlestick/Historical_Data/Data/BTC"))
# 2015.1.1 --------2020.3.1
# 1420606800      1583038800
for i in range(0, len(bar_interval)):
    print("准备写入第%d个文件..." %i)
    print("准备读取数据")
    data = get_history_data(1420606800,final_time,contract,settle,bar_interval[i])
    # print(os.listdir("./plot_history_candlestick/ETH_Historical_Data"))
    path = ("./Data/%s/" %contract)
    folder = os.path.exists(path);
    if not folder:
        os.makedirs(path)
    filename = contract +"_" + str(bar_interval[i]) + ".csv" ;
    path = path + filename;
    print("准备写入文件")
    data.to_csv(path,index_label=("Date"))
    print("写入文件成功！！")





