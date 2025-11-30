# DRS
A cricket Decision-Review-System for cricket. I began developing this in Sixth-Form first as personal project to settle arguments that my brother and I would have playing backgarden cricket, then I did it as my A-Level Computer Science NEA project. After completing, Sixth Forum I got busy and this project was shelved for university work and other personal projects. Recently, since moving back home I have rediscovered the merits for this project so I have began updating and reworking it to improve accuracy.

My initial plans were to take 2 mobile phones filming the ball from 2 different angles (straight on and from the side) as stereo inputs. The square leg camera would also have a microphone (with a long AUX lead plugged in), this microphone would then be taped to  the stumps. This would serve for edge detection (UltraEdge/Snickometer style reviews). A webserver would be used to sync the trigger for filming across the two phones, taking in the footage and processing the videos and for tracking the type of review and how many reviews each person/team has taken. The ball prediction would be done by fitting the balls path post-bounce to a quadratic function for height and fitting lateral movement to a linear regression. I would deal with instances where the ball hasn't bounced by using a estimate coefficeint of restitution. If you're intrested more about the initial plans and structure I have included my NEA report in this repo. The edge reviews would be handled by FFMPEG.

After restarting this project, I reworked this orignal plan. This paper by Kamble et al [https://doi.org/10.1007/s10462-017-9582-2] served a large part of my inspiration when researching how I would improve my ball tracker. I began by searching for conoturs using the YCrCb colourspace not HSV. Using, what I have learned in the last few years in Computer Vision I realised this will be better for outdoor applications as it seperates luminence. I aslo ANDed this mask with a background subtractor to isolate only frames that are moving. I then used a Kalman Filter to handle cases of occlusion and to improve my prediction after it hits the pad. For more details on the Kalman Filter I used see the plan inside the Ball Tracking folder. 

### Technologies/Libraries used
<ul>
  <li>Python</li>
  <li>OpenCV</li>
  <li>numpy (for custom Kalman Filter code)</li>
  <li>FFMPEG</li>
  <li>MatPlotLib for 3D views</li>
</ul>

### This program can do:
<ul>
<li>  
  LBW appeals
  <ol>
        <li>Ultra-edge/Snicko</li>
        <li>Ball tracking</li>
        <li>Ball Prediction</li>
  </ol>
</li>
  <li>
Edge detection (Ultra-Edge/Snicko)
    <ol>
          <li>Use mic data to form waveform</li>
          <li>Display on slo-mo overlay</li>
    </ol>
  </li>
</ul>

### How it will work:
#### Edge detection
A microphone will be connected to the mobile that provides the sideo on view (as this will be the closest to the pitch) via an AUX cable. Below are the steps to how the footage captured will be transformed into a edge detector (like Ultra-edge/Snicko).
<ol type="1">
<li>Footage is slowed down</li>
<li>Slower audio is  isolated, amplified and outputted</li>
<li>Waveform is generated from outpuuted audio</li>
<li>This waveform is overlayed over a "Ultra-edge" image background.</li>
<li>Which inturn is overlayed upon the front and side on videos</li>
<li>Temp files are deleted</li>
</ol>

#### Ball tracking
<ol type="1">
<li>Prior to play, the bounds of the ball in YCrCb are detected and inputted(using inbuilt utility). Additionaly, a brief period of footage (around 5s) is fed into the background remover so it can learn what the background is (must be done for both cameras)</li>
<li>Synchronised footage of both angles is fed in (Edge detection if required has already been done)</li>
<li>Track ball position - Run independetly on both angles (first on side-on camera then front-on camera)</li>
  <ol>
        <li>First user draws boundng box over stumps using mouse (so the software can work out pixels per m and where the stumps are)</li>
        <li>Then Kalman filter based tracker runs handiling cases of occclusion</li>
          <ol>
            <li>Initial trust is low (highly relies on sensor data) - Especially for ax as this is definitely non-linear despite our modelling. But slowly grows in confidence</li>
            <li>Tries to find closest contour to predicted value to feed in as sensor data (Nearest Neighbour Data Association)</li>
            <li>Normalised Innovation Squared is constantly monitored. A simple hypothesis test is run with Chi-Sqaured sitribution to determine if we are 99% certain on ball has deviated from model</li>
            <li>If ball has deviated (most likely it has bounced) then reset Kalman Filter back to initial state and reobserve and learn patterns</li>
          </ol>
        <li>User hits 'h' on keyboard when bat hits pad so Kalman filter ignores sensor inputs and just predicts based on previous observed path + physics model</li>
  </ol>
<li>Primative 3D Triangulation</li>
  <ul>
      <li>Side-on plane (observed in m): becomes Depth/How far down pitch(x) against height(z)</li>
      <li>Front-on plane (observed in m): becomes Lateral Position(y) against height (z)</li>
  </ul>
  <li>After theese 3D values are sythesised using inputed stump bounding boxes it is determined if the ball has: pitched in-line/outside off (at the moment doesn't taken into account outside leg is allowed if no shot offfered),impacted in line and if it will go on to       hit the stumps</li>
 <li>3D views are drawn in MatPlotLib and outputted with outcome for us to see</li>
</ol>

### Results:
I ran 2 tests of throwing the ball when there was no batsman (so I could compare the end result to where I predicted. The table below shows the euclidean distance (sqrt(dx^2 + dy^2 + dz^2)) of the ball from the actual observed position in that test. This shows my triangulation methods although primative are largely accurate as well as testing the kalman filter and prediction logic. The frame where I set the ball hit the pad (so to ignore all observed values and only predict from) is in bold. 
| Euclidean distance -   test 1 	| Euclidean distance- test 2 	|
|---	|---	|
| 0.0628614 	| 0.06221 	|
| 0.0601523 	| 0.059538 	|
| 0.0577105 	| 0.057128 	|
| 0.0551992 	| 0.054651 	|
| 0.0528156 	| 0.052301 	|
| 0.0505478 	| 0.050067 	|
| 0.0483191 	| 0.047873 	|
| 0.04615 	| 0.045737 	|
| 0.0444602 	| 0.044067 	|
| 0.0448984 	| 0.044504 	|
| 0.0444334 	| 0.044046 	|
| 0.0440767 	| 0.043695 	|
| 0.043685 	| 0.043309 	|
| 0.0432568 	| 0.042887 	|
| 0.0427859 	| 0.042423 	|
| 0.0423278 	| 0.041972 	|
| 0.0418399 	| 0.041491 	|
| 0.0414297 	| **0.041088** 	|
| 0.0409831 	| 0.040648 	|
| 0.0405218 	| 0.040194 	|
| 0.0400163 	| 0.039696 	|
| 0.0394851 	| 0.039173 	|
| **0.0389269** 	| 0.038624 	|
| 0.0383515 	| 0.038058 	|
| 0.0378079 	| 0.037523 	|
| 0.0372174 	| 0.036942 	|
| 0.0365733 	| 0.036309 	|
| 0.0359177 	| 0.035664 	|
| 0.0352579 	| 0.035016 	|

In test 1 the mean distance from the observed values was: 0.044414093m with a standard deviation of 0.007150342. \
In test 2 the mean distance from the observed values was: 0.044028741m with a standard deviation of 0.007043823. \
\
**The final distance from the observed value at the back of the net was around 0.035m or around 3.5cm (which is about half the width of a cricket ball).**

### Conclusion/Improvements:
Whilst this system does effectively track the ball and predict where it will end up it does have several shortcomings and thus has a lot of room for further improvements but unfortunately due to reasons specified below there is likely to be slow progress. At the moement, this system uses manually synced low-resolution high noise cameras from old mobile phones. This means they can only track to this level of detail when the velocity of the ball is quite low (throwdowns for the testing data). Additionally, the manual syncing process is a nightmare to do as I must manually go through frame by frame and sync based on two frames that match up from a queue like a hand clapping. I could develop the webserver based sync I orignally planned but upon further research now I realise the latency of wireless communication over the internet would mean that they are not properly synchronised. I think the best solution would be to employ to microcontroller based cameras that can fire off of a GPIO pin. That way I could connect the two up with a long cable and have a much more accurate sync. Additionaly, if those microcontrollers were to run a high-speed global shutter camera module this would fix my velocity cap problem. However, I can not put this system in place due to budget constraints. All of this hardware would likely cost in excess of £150-200 (this doesn't even include the money for a processing server) which is alot of money to put into a backgarden DRS project. Additionaly, the netting we used to stop balls flying over fences or into the house if a batter misses a ball has now been destroyed by the wind so using it and gathering new test data is a bit more difficult. Additionaly if I had known about proper matrix based chess board style triangulation when initially creating this project this would greatly aid in improving accuracy in more conditions but as I previosuly mentioned the lack of ability to gather new step more difficult.

Other limitations, like the system not responding well if the ball bounces just before/is due to bounce after the ball hits the pad can be addressed however. I would likely address them in a similair way to how I had orignally planned (see NEA report document for details). 

Having said all of that, I'm still quite happy as to how well the system works now and it is a shame it is unlikely to be used much now as me and my brother are much more mature and do not argue as much about if its out or not in backgarden cricket. If you want to see a workthrough of the program then look inside of the Ball Tracking folder.

### NOTE: 
Development has temporarily halted as I need reference footage from front on to continue and I can currently not go and generate this. Will restart as soon as possible
