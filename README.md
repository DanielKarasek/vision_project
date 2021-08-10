# vision_project
My own implementations of several basic vision algorithms with varius strategies and GUI implemented in python 3.8.8 and libraries specified in requirements.txt

## GUI
GUI isn't the most handsome, and still has some crisp edges. But here is the rundown of functionalities.

![Base app view](https://github.com/DanielKarasek/vision_project/blob/main/doc_images/base_view_screenshot.png)

In this image we can see base view. On the left is frame with result either picture or webcam video feed with applied vision algorithm(here hough lines).
U can take its snapshot (and then use for example in README :D) On the right side there are settings for current method.
New settings are applied only after apply button is pressed (not on change of scale, this was too performance costly since TK has some questionable settings for callbacks).
You can set other algorithm by pressing operation in top menu and then choosing new algorithm.
If algorithm e.g. canny is used as part of other algorithm e.g. hough lines, settings from canny method are then also supplied to canny used in hough lines. In this example if I set gaussian filter param. sigma to 5 in canny method it will then be used in hough lines with this exact setting. Only difference is hough lines and hough segments, which are 2 algorithms using lot of same parameters but still are 2 different algorithms. Current workaround is to use COPY button in hough lines - this might be solved with template pattern later, but I am not sure if having same common parameters is always desirible so TBD.

There are 2 mods in this app. First one works on static image. Second one works on webcam live capturing. These mods can be altered in target menu at top of screen. U can also choose another static image in this menu. Static image must be in ./test_images folder.

Some algorithms can employ different strategies to achieve same thing. For example hough lines can employ different sample strategies to sample some(all) of the edge points(sample all, every nth point or percentage of points randomly chosen). This can lead to speed up/slow down and increase/decrease/change in quality of results.

These strategies can be changed after "change strategies" button is pressed. Strategies for each method are explained further.
