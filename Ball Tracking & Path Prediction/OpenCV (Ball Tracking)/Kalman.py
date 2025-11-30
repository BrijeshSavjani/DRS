'''
Kalman filtering:
Used to model and predict noisy mesaurements into usable data

Algorithm setps:

1) Prediction stage
    State Prediction      : x̂ₖ = Fₖ ⋅ x̂ₖ₋₁|ₖ₋₁ + BₖUₖ = A ⋅ (x̂ₖ₋₁|ₖ₋₁)
    Covariance prediction : Pₖ|ₖ₋₁ = Fₖ ⋅ P̂ₖ₋₁|ₖ₋₁ ⋅ Fₖᵀ + Qₖ

2) Update/Innovation Stage
    State Innovation      : ỹₖ = zₖ - (Hₖ ⋅ x̂ₖ|ₖ₋₁)
    Covariance Innovation : Sₖ = Hₖ ⋅ Pₖ|ₖ₋₁ ⋅ Hₖᵀ + Rₖ

3) Kalman Gain Calculation
    Kalman Gain : Kₖ = Pₖ|ₖ₋₁ ⋅ Hₖᵀ ⋅ Sₖ⁻¹

4) Estimation/Evaluation Stage:
    State Estimate      : x̂ₖ|ₖ = x̂ₖ|ₖ₋₁ + Kₖ ⋅ ỹₖ
    Covariance Estimate : Pₖ|ₖ = (I - Kₖ ⋅ Hₖ) ⋅ Pₖ|ₖ₋₁

'''

import numpy as np
import scipy.stats as stats

class Kalman():

    
    def __init__(self,A_matrix:np.array,x0:np.array,Q_k:np.array,H_k:np.array,R_k:np.array,p0:np.array,variance=1,B_matrix:np.array = None,U_k:np.array = None): 
        #Set F_K,Q_k,R_k,H_k,B_K & U_k to provided values
        #B_K and U_k default to None if there is no control variables, variance for Q_k defaults to 1
        self.F_k = A_matrix.copy()
        self.Q_k = Q_k.copy() * variance
        self.H_k = H_k.copy()
        self.R_k = R_k.copy()
        #Set previous prediction to init values - provide in constructor
        self.previous_estimate = [x0,p0]
        
        #Handle optional params
        self.B_k = B_matrix.copy() if B_matrix is not None else None
        self.U_k = U_k.copy() if U_k is not None else None

        #Blank for now will be set later
        self.current_prediction = [None,None]
        self.state_innovation = np.array([],float)
        self.covariance_innovation = np.array([],float)
        self.kalman_gain = np.array([],float)
    

    def Predict(self): #Do NOT use if using RunFullStep()
        #Set current_prediction to estimates based on previous estimate
        self.current_prediction[0] = self.F_k @ self.previous_estimate[0]
        self.current_prediction[1] = (self.F_k @ self.previous_estimate[1] @ self.F_k.T) + self.Q_k
        
        if self.B_k is not None: self.current_prediction[0] += (self.B_k @ self.U_k)

        return self.current_prediction[0] #Return state prediction in case needed


    def __Update(self,observed_values:np.array):
        #Set innovation(error values) from observed values
        self.state_innovation =  observed_values - (self.H_k @ self.current_prediction[0])
        self.covariance_innovation = (self.H_k @ self.current_prediction[1] @ self.H_k.T) + self.R_k
        #Then calculate Kalman Gain
        self.kalman_gain = self.current_prediction[1] @ self.H_k.T @  np.linalg.inv(self.covariance_innovation)


    def __Estimate(self):
        #Estimate state & covariance
        state_estimate = self.current_prediction[0] + (self.kalman_gain @ self.state_innovation)
        covariance_estimate = (np.identity(self.current_prediction[1].shape[0]) - (self.kalman_gain @ self.H_k)) @ self.current_prediction[1]
        #Update previous estimate
        self.previous_estimate = [state_estimate,covariance_estimate]        
        #Return state estimate
        return state_estimate
    
    def GetNIS(self):
        return self.state_innovation.T @ np.linalg.inv(self.covariance_innovation) @ self.state_innovation
    
    def ObserveNIS(self,value):
        state_inno = value - (self.H_k @ self.current_prediction[0])
        covariance_inno = (self.H_k @ self.current_prediction[1] @ self.H_k.T) + self.R_k
        return state_inno.T @ np.linalg.inv(covariance_inno ) @ state_inno

    def RunFullStep(self,observed_values:np.array = None):
        self.Predict()#Predict new state

        if observed_values is not None: #If we have values
            self.__Update(observed_values) #Update
            return self.__Estimate() #and return estimate
        else:
            self.previous_estimate = self.current_prediction #Otherwise set prediction as prevous estimate
            return self.current_prediction[0] # and return prediction


    def RunStepWithoutPredict(self,observed_values:np.array = None): #Forwhen we want to use Nearest to prediction for observation
        if observed_values is not None: #If we have values
            self.__Update(observed_values) #Update
            return self.__Estimate() #and return estimate
        else:
            self.previous_estimate = self.current_prediction #Otherwise set prediction as prevous estimate
            return self.current_prediction[0] # and return prediction


    
