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
5)  Which in=turn is overlayed upon the front and side on videos#
6)  Temp files are deleted
