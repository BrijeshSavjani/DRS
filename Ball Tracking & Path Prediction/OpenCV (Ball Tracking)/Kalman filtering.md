# Kalman filtering:

Derived using SUVAT equations (s = ut +  0.5at<sup>2</sup> & v = u + at)

Linear filter so assuming constant acceleration (not entirely accurate but have a large Q to overcome)

​	-> For better accuracy we could use a UKF or particle filter

​	-> Chose no control values because a<sub>x</sub> is not known and is quite difficult to work out as it's a combination of many forces.  


$$
Model \space state = 
\begin{bmatrix} 
x  \\
y  \\
v_x \\
v_y \\
a_x \\
a_y
\end{bmatrix}

\space\space\space  


A = 
\begin{bmatrix} 
1 & 0 & t & 0 & 0.5t^2 & 0\\
0 & 1 & 0 & t & 0 & 0.5t^2\\
0 & 0 & 1 & 0 & t & 0\\
0 & 0 & 0 & 1 & 0 & t\\
0 & 0 & 0 & 0 & 1 & 0\\
0 & 0 & 0 & 0 & 0 & 1\\
\end{bmatrix} 
\space\space\space  

B = 
\begin{bmatrix} 
 0 \\
 0
\end{bmatrix}

\space\space\space  

H = 
\begin{bmatrix} 
 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
 0 & 1 & 0 & 0 & 0 & 0 & 0
\end{bmatrix}
\newline
\newline
$$


Algorithm steps:

1. **Prediction stage**
   $$
   \hat{x}_k = F_k \cdot \hat{x}_{k-1 | k-1}+ B_kU_k= A \cdot (\hat{x}_{k-1|k-1}) \newline
   P_{k|k-1} = F_k \cdot \hat{P}_{k-1|k-1} \cdot {F_k }^T + Q_k
   $$
   Predict state and covariance using modeled equations and previous prediction, if at at start/initial frame can use identity matrix or initial guess matrix

2. **Update/Innovation stage**
   $$
   State \space innovation(\tilde{y_k}) = z_k - (H_k \cdot \hat{x}_{k | k-1}) 
   \newline
   Covariance \space innovation(S_k) = H_k \cdot P_{k|k-1} \cdot {H_k}^T + R^k
   $$
   Aim of this step is to find error(innovation) based on values we predicted in previous stage.

   

   z<sub>k</sub> is the literal measured value. Will look for contour centroid close to this value. If we can't find any near by we assume occlusion and predict without input (If too long quit out of loop as won't be accurate). 

3. **Kalman Gain**
   $$
   K_k = (P_{k|k-1} \cdot {H_k}^T) + R^k
   $$
   Measure of how certainty about an observed value. R<sup>k</sup> is a parameter for observation noise and can be tuned for best results

4. **Estimation/Evaluation stage**

$$
State \space (\hat{x}_{k|k}) = \hat{x}_{k|k-1} + K_k \cdot \tilde{y}_k
\newline
Covariance \space (P_{k|k}) = (I - K_k \cdot H_k) \cdot P_{k|k-1}
$$

Estimate state and covariance using value it guessed,Kalman gain and observed value (for state)