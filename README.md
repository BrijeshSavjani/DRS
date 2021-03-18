# DRS
A cricket Decision-Review-System(like Hawkeye) for mobile phones. Predicted equipment required includes 2 mobile phones,one microphone and potenmtially one webserver.

#### This program will (eventaully) be able to:
- Do LBW appeals
  - Ultra-edge/Snicko
  - Ball tracking
  - Ball Prediction
- Edge detection
  -Use mic data to form waveform
  -Display on slo-mo overlay
- Manage Reviews
  - Allow x reviews per innings per team (2 team)

Will include code based in : Python(Standard and OpenCV), React(App) and FFMPEG commaunds (For video processing)

### How it will work:
#### Edge detection
A microphone will be connected to the mobile that provides the sideo on view (as this will be the closest to the pitch) via an AUX cable. Below are the steps to how the footage captured will be transformed into a edge detector (like Ultra-edge/Snicko).
1)  Footage is slowed down
2)  Slower audio is  isolated, amplified and outputted
3)  Waveform is generated from outpuuted audio
4)  This waveform is overlayed over a "Ultra-edge" image background.
5)  Which inturn is overlayed upon the front and side on videos
6)  Temp files are deleted

#### Ball tracking
This is a simplified plan. I will add the full plans and flow charts that I drew out at the start for more details. This will require both camera angles and will most likely require a python webserver for Open CV and FFMPEG. Howver, the need for this may be removed in a future update.

1) User selects start of ball(Frame ball is released from the hand of the bowler)
2)(Side on camera)
  - This is so we can calculate the height of the ball (using a quadratic to model the change in height)
  - Captured 2 planar co-ordinate will be grouped into sets of 3 
  - This set of 3 will be sent to my quadratic solver program that will return the equationof a quadratic that contains those thhree points
  - All equations that are returrned will be stored
  - Stored equation dataset is cleaned then a mean average is calculated
3)(Front on camera)
  - Used for lateral movement (Assumed to be linear)
  - Horrizontal (x) co-ordinate of ball is calculated and stored
  - Regression line against time is calculated and used to see if it will hit ball
4) What if the ball will bounce after the impact whith the batsman?
  A 3D position is calculated 
  - Both cameras will need to be used for this
  - It's location in all planes can be worked out because two angles will be used
  - The height of the stumps and distance between stumps will be used as mile markers to help find the position
  - This can then be used to calculate the velocity of the ball. (This will be done after every ball)
  - The coefficent of restitution is predicted (using a graph of previously collected values of that ball type on that pitch)
  - New quadratic is calculated from root and turning point (Calculated using velocity (Max-height))
 5) Time is plugged into all equations & value is stored.
 6) Co-ordinaete of stored ball is compared to position of stumps. If it's hitting then the batsman in adjudged out.
