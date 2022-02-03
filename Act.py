import pandas as pd
import datetime as dt
import os
import matplotlib.pyplot as plt

# Activate class that hold all data and algorithms for our experiment:
class Act:
    path = "/Users/kvl/sciebo/Activate_Studie_2/"  # path to data files

    # List of participants and day-long recordings:
    ids = [str(item).zfill(3) for item in range(1,33)] # 27 persons, 33 days

    # allow constructor to specify path
    def __init__(self, path):
        self.path = path

    # read all CSV data for one participant
    def read(self, name):
        # read Bangle data:
        d1 = pd.read_csv(name + '_Bangle.csv', names=['time', 'acc_x', 'acc_y', 'acc_z', 'g'], sep="\s+|;|,",
                         engine='python')
        del d1["g"]
        # read GT3X data:
        d2 = pd.read_csv(name + '_GT3X.csv', names=['time', 'acc_x', 'acc_y', 'acc_z'], header=10)
        # read ActiLife output:
        try:
            # d11 = pd.read_csv(name + '_steps.csv', names=['time', 's1', 's2'], header=1)
            d11 = pd.read_csv(name + '_steps_GT3X.csv', names=['time', 's'], header=1)
        except:
            d11 = []
        # convert timestamps:
        d1["time"] = [dt.datetime.strptime(d1_t, "%H:%M:%S.%f") for d1_t in d1["time"]]
        if name[-3:] == 'Wit':
            d2["time"] = [dt.datetime.strptime(d2_t, "%m/%d/%Y %H:%M:%S.%f") for d2_t in
                          d2["time"]]  # Wit has other format
        else:
            d2["time"] = [dt.datetime.strptime(d2_t, "%d-%b-%y %H:%M:%S.%f") for d2_t in d2["time"]]
        d1["time"] = [d1_t.replace(month=d2["time"][0].month, year=d2["time"][0].year, day=d2["time"][0].day) for d1_t
                      in
                      d1["time"]]
        if len(d11) > 0:
            d11["time"] = [dt.datetime.strptime(d11_t, "%H:%M:%S") for d11_t in d11["time"]]
            d11["time"] = [d11_t.replace(month=d2["time"][0].month, year=d2["time"][0].year, day=d2["time"][0].day) for
                           d11_t in d11["time"]]
        # obtain first and last timestamps of Bangle raw data:
        t1 = d1["time"].iloc[0]
        t2 = d1["time"].iloc[-1]
        # cut off anythong before and after these timestamps in the ActiGraph data:
        d2 = d2[t1 <= d2["time"]]
        d2 = d2[d2["time"] <= t2]
        d2 = d2.reset_index(drop=True)  # make sure index starts at 0
        d11 = d11[t1 <= d11["time"]]
        d11 = d11[d11["time"] <= t2]
        d11 = d11.reset_index(drop=True)  # make sure index starts at 0
        # return dataframes:
        return d1, d2, d11

    ## Open source step detector oxford step detector
    ## PDF: https://www.diva-portal.org/smash/get/diva2:1474455/FULLTEXT01.pdf
    ## https://github.com/Oxford-step-counter/C-Step-Counter
    #def step_oxford(self, ???):

    # Activate's step detector, using dataframe d, and parameters (consec, intv, th)
    def step(self, d, consec=6, intv=80, th=0.6):
        consecSteps = 0
        stepsInt = 0
        stepTimeDiff = 0
        mag = ((d["acc_x"] ** 2 + d["acc_y"] ** 2 + d["acc_z"] ** 2) ** .5) / 2  # get magnitudes
        for i in range(1, len(mag) - 1, 1):  # get peaks as candidate steps
            if (mag[i] > th) and (mag[i] > mag[i - 1]) and (mag[i] > mag[i + 1]):
                mag[i] = 10
        for i in range(1, len(mag) - 1, 1):  # track time distances
            stepsInt += 80
            if (mag[i] == 10):
                stepTimeDiff = stepsInt
                stepsInt = 0
                if (stepTimeDiff >= 1100) or (stepTimeDiff <= 240):  # milliseconds
                    consecSteps = 0
                else:
                    consecSteps = consecSteps + 1
                    if (consecSteps >= consec):
                        if (consecSteps == consec):
                            steps = consec
                            j = 0
                            while steps > 0:  # mark all <consec> previous as steps
                                if (mag[i - j] == 10):
                                    mag[i] = 100  # step!
                                    steps = steps - 1
                                j = j + 1
                        else:
                            mag[i] = 100  # step!
        d["s"] = [m == 100 for m in mag]
        return d

    ## Detect walking segments from a dataset, using the above step detector, and
    ## return a pandas dataframe with the following columns:
    ##    - start and stop timestamps of the walking segment (datetime)
    ##    - the number of steps of the walking segment
    ##    - the variability of steps in the walking segment (similar to heartrate variability)
    ##    - the average amplitude of the peak that caused the steps
    #def walk_detect(self, d1):


    # read and plot the data for one participant
    def plot(self, d1, d2, d11=[]):
        # plot:
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(sharex=True, nrows=4, figsize=(27, 4))
        ax1.plot(d1["time"], d1[["acc_x", "acc_y", "acc_z"]], lw=0.2)
        ax1.set_xlim(d1["time"][0], d1["time"][len(d1) - 1])
        ax1.set_ylim(-2, 2)
        ax1.set_yticks([-2, 0, 2])
        ax1.set_yticklabels([-2, 0, 2])
        ax1.set_ylabel('Bangle')
        ax2.plot(d2["time"], d2[["acc_x", "acc_y", "acc_z"]], lw=0.2)
        ax2.set_ylim(-2, 2)
        ax2.set_yticks([-2, 0, 2])
        ax2.set_yticklabels([-2, 0, 2])
        ax2.set_ylabel('GT3X')
        if len(d11) > 0:
            #ax3.bar(d11["time"], d11["s1"] / d11["s1"].max(), width=0.0007)  # for minute-aggregated values
            #ax3.bar(d11["time"], d11["s2"] / d11["s2"].max(), bottom=1, width=0.0007)  # for minute-aggregated values
            ax3.plot(d11["time"], d11["s"]>0, 'm', lw=0.1)
        if 's' in d1.columns:
            ax3.plot(d1["time"], d1["s"] - 1, 'r', lw=0.1)
        if 's' in d2.columns:
            ax3.plot(d2["time"], d2["s"] - 2, 'k', lw=0.1)
        ax3.set_ylabel('Steps')
        ax3.set_ylim(-2, 1)
        ax3.set_yticks([-1.5, -0.5, 0.5])
        ax3.set_yticklabels(['G', 'B', 'A'])
        ax4.set_ylabel('Steps/min')
        ax4.set_ylim(0, 240)
        ax4.set_yticks([0, 120])
        ax4.set_yticklabels(['B', 'A'])
        plt.tight_layout()
        plt.subplots_adjust(hspace=0, wspace=0)
        return plt

    # take a Bangle csv file and remove the headers
    def cleanBangleCSV(self, name):
        os.system("sed -i '' '/^t/d' " + name + "_Bangle.csv")  # remove headers (that start with t)

    def parse(self, read_from_csv=True, write_to_pickle=True, write_to_fig=True, param_search=False):
        # helper function that does a brute-force search for a best parameters,
        # returns best threshold _th, best consecutive steps _consecs, and number of found _steps:
        def find_step_p(d, consec, intv, target_steps):
            _th = _best_th = 0.65
            jump = 0.01
            _steps = _minsteps = 0
            _consecs = _best_consecs = 6
            prev_diff = len(d)  # something ridiculously high
            while _th > 0.49:
                _consecs = 6
                while _consecs > 0:
                    _steps = sum(self.step(d, _consecs, intv, th=_th)["s"])
                    if abs(target_steps - _steps) < abs(target_steps - _minsteps):
                        _best_th = _th
                        _minsteps = _steps
                        _best_consecs = _consecs
                    _consecs = _consecs - 1
                _th = _th - jump
            return _best_th, _best_consecs, _minsteps
        # the main experiment routine starts here:
        ret = []
        for id in self.ids:
            if read_from_csv:
                print("Reading data from " + self.path + "_CSV/" + id)
                d1, d2, d11 = self.read(self.path + "_CSV/" + id)
                print("  - time span:", d1["time"].iloc[0], "-", d1["time"].iloc[-1], " = ",
                      (d1["time"].iloc[-1]-d1["time"].iloc[0]).total_seconds() / 3600, "hrs.")
            else:
                print("Reading data from " + self.path + "_Pkl/" + id)
                d1 = pd.read_pickle(self.path + "_Pkl/" + id + '_Bangle.pkl')
                d2 = pd.read_pickle(self.path + "_Pkl/" + id + '_GT3X.pkl')
                d11 = pd.read_pickle(self.path + "_Pkl/" + id + '_steps_GT3X.pkl')
            ## calculate steps parameters:
            target_steps = sum(d11["s"])
            if param_search:
                bangle_th, bangle_c, bangle_steps = find_step_p(d1, 6, 80, target_steps)
                gt3x_th, gt3x_c, gt3x_steps = find_step_p(d2, 1, 33, target_steps)
                d1 = self.step(d1, bangle_c, 80, bangle_th)
                d2 = self.step(d2, gt3x_c, 33, gt3x_th)
            else:
                bangle_c, bangle_th = [4, 0.54]
                d1 = self.step(d1, bangle_c, 80, bangle_th)
                bangle_steps = sum(d1["s"])
                gt3x_c, gt3x_th = [4, 0.54]
                d2 = self.step(d2, gt3x_c, 33, gt3x_th)
                gt3x_steps = sum(d2["s"])

            print("  - calculated steps: (Bangle:", bangle_steps,
                  ", GT3X:", gt3x_steps, ", ActiLife:", target_steps, ")")
            ## sum all steps per minute bin:
            d1_agg = d1.resample('Min', on='time')["s"].sum()
            d2_agg = d2.resample('Min', on='time')["s"].sum()
            d11_agg = d11.resample('Min', on='time')["s"].sum()
            bangle_corr = d11_agg.corr(d1_agg, method='pearson')
            gt3x_corr   = d11_agg.corr(d2_agg, method='pearson')
            ## write pickle files:
            if write_to_pickle:
                d1.to_pickle(self.path + "_Pkl/" + id + '_Bangle.pkl')
                d2.to_pickle(self.path + "_Pkl/" + id + '_GT3X.pkl')
                d11.to_pickle(self.path + "_Pkl/" + id + '_steps_GT3X.pkl')
                d1_agg.to_pickle(self.path + "_Pkl/" + id + '_Bangle_steps1m.pkl')
                d2_agg.to_pickle(self.path + "_Pkl/" + id + '_GT3X_steps1m.pkl')
                d11_agg.to_pickle(self.path + "_Pkl/" + id + '_steps_GT3X_1m.pkl')
                print("  - written to pickle format")
            ## plot and add histograms:
            f = self.plot(d1, d2, d11)  # use participant code
            f.gca().plot(d1_agg.index, 120*(d1_agg/max(d1_agg)), 'r')
            f.gca().fill_between(d1_agg.index, 120*(d1_agg/max(d1_agg)), color='r')
            f.gca().plot(d11_agg.index, 120*(d11_agg/max(d11_agg))+120, 'm')
            f.gca().fill_between(d11_agg.index, 120*(d11_agg/max(d11_agg)) + 120, 120, color='m')
            if write_to_fig:
                f.savefig(self.path + "_Fig/" + id + '.png')
                print("  - written to png figure")
            f.close()
            ret.append([id, d1["time"].iloc[0], d1["time"].iloc[-1],
                         (d1["time"].iloc[-1] - d1["time"].iloc[0]).total_seconds() / 3600,
                        target_steps, bangle_steps, bangle_th, bangle_c,
                        gt3x_steps, gt3x_th, gt3x_c, bangle_corr, gt3x_corr])
        return ret
