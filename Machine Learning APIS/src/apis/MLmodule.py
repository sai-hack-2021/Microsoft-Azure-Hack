import numpy as np
import pickle
import os

class Machine_learning:

    filename = os.getcwd()+"/src/apis/"+'trainedmodel.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    def __init__(self):
        self.btemp = 0.0
        self.continuous = 0
        self.Night_Rise = 0
        self.Chills = 0
        self.wf = 0 # weakness and Fatigue
        self.jp = 0 #joint pain
        self.cp = 0 #chest Pain
        self.stiffness = 0
        self.RN = 0 #Runningnose
        self.NB = 0 #Noseblockage
        self.DC = 0 #dry Cough
        self.ST = 0 #sorethroat
        self.CSP = 0 #coughwithsputum
        self.Vomitting = 0
        self.Lmotion = 0
        self.UI = 0

    def setValues(self,Temp,TOF,bpain,VOM,LM,COU,COLD,Ui):
        TOF = int(TOF)
        bpain = int(bpain)
        COU = int(COU)
        COLD = int(COLD)
        # setting the labels
        #----------setting  Type of fever
        self.btemp = float(Temp)
        if TOF == 0:
            self.continuous = 1
            self.Night_Rise = 0
            self.Chills = 0

        elif TOF == 1:
            self.continuous = 0
            self.Night_Rise = 0
            self.Chills = 1

        elif TOF == 2:
            self.continuous = 0
            self.Night_Rise = 1
            self.Chills = 0

        #----------setting Bpain

        if bpain == 0:
            self.wf = 1
            self.jp = 0
            self.cp = 0
            self.stiffness = 0

        elif bpain == 1:
            self.wf = 0
            self.jp = 1
            self.cp = 0
            self.stiffness = 0

        elif bpain == 2:
            self.wf = 0
            self.jp = 0
            self.cp = 1
            self.stiffness = 0

        elif bpain == 3:
            self.wf = 0
            self.jp = 0
            self.cp = 0
            self.stiffness = 1

        #----------setting COLD
        if COLD == 0:  #no cold
            self.RN = 0
            self.NB = 0

        elif COLD == 1:
            self.RN = 1
            self.NB = 0

        elif COLD == 2:
            self.RN = 0
            self.NB = 1

        #----------setting Cough

        if COU == 0:
            self.DC = 0
            self.ST = 0
            self.CSP = 0

        elif COU == 1:
            self.DC = 1
            self.ST = 0
            self.CSP = 0

        elif COU == 2:
            self.DC = 0
            self.ST = 1
            self.CSP = 0

        elif COU == 3:
            self.DC = 0
            self.ST = 0
            self.CSP = 1
#---------------------------------------- Others


        self.Vomitting = int(VOM)
        self.Lmotion = int(LM)
        self.UI = int(Ui)

        values = [self.btemp,self.continuous,self.Night_Rise,self.Chills,self.wf,self.jp,self.cp,self.stiffness,self.RN,self.NB,self.DC,self.ST,self.CSP,self.Vomitting,self.Lmotion,self.UI]


    def predictValues(self):
        values = [self.btemp,self.continuous,self.Night_Rise,self.Chills,self.wf,self.jp,self.cp,self.stiffness,self.RN,self.NB,self.DC,self.ST,self.CSP,self.Vomitting,self.Lmotion,self.UI]
        print(values)
        return(str(Machine_learning.loaded_model.predict(np.array(values).reshape(1,16))[0]))



