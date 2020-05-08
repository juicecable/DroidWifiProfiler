# DroidWifiProfiler

Helps you figure out what level you need to set your wifi roaming to (for minimum connectivity)

Requirements:
- An accessable server running the udp ping server
- Qpython3 on Android running the Wifi Profiler
- Android 10 phone with Wifi-Throttling Disabled, for reliable results
- At least one wifi that you have the ability to connect to and gain at least local internet from where you can connect to the ping server

Directions:
1. Setup the Ping Server and Make it Acessable to the Wifi Profiling Android Device
2. Set the variables as needed in the code
3. If on Android 10, go into developer options and disable wifi scan throttling
4. Change the variables as needed in the Wifi Profiler Code
5. Run the Wifi Profiler Code
6. Move around where you want to profile the selected wifi
7. Press Control-C on the Wifi Profilers Keyboard to stop the program
8. The wifi metrics should be returned to you
