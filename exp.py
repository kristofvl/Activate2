import Act
import os 
import pandas as pd

# start by specifying your path:
path = os.path.expanduser('~')+"/Activate2/"
myExperiment = Act.Act(path)

# # ## Example for an experiment with interactive visualization:
#id = '003'  # Patient ID
# # read all relevant pkl files:
# d1 = pd.read_pickle(path + "_Pkl/" + id + '_Bangle.pkl')
# d2 = pd.read_pickle(path + "_Pkl/" + id + '_GT3X.pkl')
# d11 = pd.read_pickle(path + "_Pkl/" + id + '_steps_GT3X.pkl')
# # read all relevant csv files:
#d1, d2, d11 = myExperiment.read(id)
# # detect steps and add these as an extra  column "s" to the dataframes:
#d1 = myExperiment.step(d1, consec=2, intv=80, th=0.62)  # step detection for Bangle.js
#d2 = myExperiment.step(d2, consec=1, intv=33, th=0.56)  # step detection for GT3X
# # detects walking and add as an extra column "ws" to the dataframes:
# # For time period of 120 Seconds, where more than 2 steps are considered as walking
# # Bangle (with intv = 80), windowSize = 1500 (2000 msec / 80), threshold = 99  
# # GT3X (with intv = 33), windowSize = 2000 (2000 msec / 33), threshold = 99
#df_walking_bangle = myExperiment.walk_detect(d1, windowSize = 1500, threshold = 99) # Walking detection for Bangle
#df_walking_gt3x = myExperiment.walk_detect(d2, windowSize = 3636, threshold = 99) # Walking Detection for GT3X
# # sum all steps per minute bin:
# d1_agg = d1.resample('Min', on='time')["s"].sum()
# d2_agg = d2.resample('Min', on='time')["s"].sum()
# d11_agg = d11.resample('Min', on='time')["s"].sum()
# print("Pearson correlation between ActiLife and Bangle steps: "+str(d1_agg.corr(d11_agg, method='pearson')))
# print("Pearson correlation between ActiLife and GT3X steps:   "+str(d2_agg.corr(d11_agg, method='pearson')))
# # show in plot:
# f = myExperiment.plot(d1, d2, d11)
# f.gca().plot(d1_agg.index, 120*(d1_agg/max(d1_agg)), 'r')
# f.gca().fill_between(d1_agg.index, 120*(d1_agg/max(d1_agg)), color='r')
# f.gca().plot(d11_agg.index, 120*(d11_agg/max(d11_agg))+120, 'm')
# f.gca().fill_between(d11_agg.index, 120*(d11_agg/max(d11_agg)) + 120, 120, color='m')
# f.savefig(path + "_Fig/" + id + '_test.png')
# f.show()

# ## Example for a full experiment that takes all data files, calculates the best parameters for
# ## step detection, walking segments detection and outputs everything to a set of plots and dataframes:
#ret = myExperiment.parse(read_from_csv=False, write_to_pickle=True, write_to_fig=True, param_search=True, walking_detect = True)
# ## Example for a reduced experiment that takes all data files, takes fixed parameters that were determined beforehand for
# ## step detection, walking segment detection and outputs everything to a set of plots and dataframes:
ret = myExperiment.parse(read_from_csv=True, write_to_pickle=False, write_to_fig=True, param_search=False, walking_detect = True)
ret = pd.DataFrame(ret, columns = ["id", "t1", "t21", "dur", "steps",
                                   "bangle_s", "bangle_th", "bangle_c",
                                   "gt3x_s", "gt3x_th", "gt3x_c", "bangle_corr", "gt3x_corr"])
ret.to_csv(path + "_Pkl/" + '_res_4_053.csv')

# dta = pd.read_csv(path + '_Study_volunteers.csv')
# res = pd.read_csv(path + "_Pkl/" + '_res_4_053.csv')
# dd = {'ID': dta.ID, 'BangleID': dta.BangleID, 'steps': res.steps, 'steps_bangle': res.bangle_s,
#       'steps_dev': abs(res.steps-res.bangle_s)/res.bangle_s,
#       'bangle_corr': res.bangle_corr}
# d = pd.DataFrame(dd)
# d = d.drop(14)  # remove two error-prone datasets (due to missing data)
# d = d.drop(18)
