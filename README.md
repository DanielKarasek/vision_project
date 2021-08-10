# Vision algorithms with GUI
My own implementations of several basic vision algorithms with varius strategies and GUI implemented in python 3.8.8 and libraries specified in requirements.txt

## GUI
GUI isn't the most handsome, and still has some crisp edges. But here is the rundown of functionalities.

![Base app view](https://github.com/DanielKarasek/vision_project/blob/main/doc_images/base_view_screenshot.png)

In this image we can see base view. On the left is frame with result either picture or webcam video feed with applied vision algorithm(here hough lines).
U can take its snapshot (and then use for example in README :D) On the right side there are settings for current method.
New settings are applied only after apply button is pressed (not on change of scale, this was too performance costly since TK has some questionable settings for callbacks).
You can set other algorithm by pressing operation in top menu and then choosing new algorithm.
If algorithm e.g. canny is used as part of other algorithm e.g. hough lines, settings used for first algorithm standing alone is used in case first algorithm is used as part in second algorithm. In this example if I set gaussian filter param sigma to 5 in canny method it will then be used in hough lines with this exact setting. Only difference is hough lines and hough segments. These 2 use lot of same parameters but still are 2 different algorithms therefor above doesn't apply. Current workaround is to use COPY button in hough lines - this might be solved with template pattern later, but I am not sure if having same common parameters is always desirible so TBD.

There are 2 mods in this app. First one applies algorithm to static image. Second one works on webcam live feed. These mods can be altered in target menu at top of the screen. You can also choose another static image in this menu. Static image must be in ./test_images folder.

Some algorithms can employ different strategies to achieve same thing. For example hough lines can employ different sample strategies to sample some(all) of the edge points(sample all, every nth point or percentage of points randomly chosen). This can lead to speed up/slow down and increase/decrease/change in quality of results.

These strategies can be changed after "change strategies" button is pressed. Strategies for each method are explained further.


## Nothing
Nothing only copies image (from video feed or static image) to output. Also Nothing allows to use gaussian filter with variable sigma, so we can see how much image will be blurred when same sigma is used in Canny. In future blurring settings might carry forward to canny. However in this case seing blurry image, doesn't give that much of insight on how will cannied image look. Therefor this isn't path isn't decided yet.

## Canny
Canny is the bread and butter algorithm used when processing lines, segments and other interest points. It can be used for many other additional processing methods to for example cartoony image. Basic algorithm uses 2/3 parameters. Low and high threshold used in double thresholding and sigma (which might be used before canny but here it is part of canny). Currently thresholds are decided automatically via simple approximation. In future versions I hope to add strategies here, so user can choose whether to use auto/manual tuning. Only parameter is therefor sigma.

## Hough Lines
Traditional hough lines algorithm. Hough transform -> peaks -> ??? -> profit! You can alter the dimensionality of hough transform with angle count and rho dim parameters. Threshold then is min. value of peak in hough transform. Min angle and min rho then sets size MxN matrix size in which only 1 peak might be found.
Strategies:
  1. Sample strategy - downsampling of edge points to increase speed of algorithm
    * Sample all - samples all edges
    * Sample Nth - samples every n-th edge point, fast downsample. But sometimes some line have most of it points on n-th positions
    * Sample percentage randomly - A bit slower than Sample Nth, but lowers a bit danger of surrpessing some lines
  2. Hough peaks - finding peaks in hough transform
    * My hough peaks - my algorithm to find peaks, which takes arguments of min angle and min rho as minimum rho/angle value before transformation into discrete image hough space(e.g. min rho 7 means that 2 lines have with same angle have to be at least 7 pixels apart)
    * Scipy Peaks - Scipys algorithm. Min angle and min rho means only space between points in discrete image hough space -> therefor behaviour of these params are different if angle count and rho dim are higher/lower
