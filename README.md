# Vision algorithms with GUI
My own implementations of several basic vision algorithms with varius strategies and GUI implemented in python 3.8.8 and libraries specified in requirements.txt

## GUI
GUI isn't the most handsome, and still has some crisp edges. But here is the rundown of functionalities.

![Base app view](https://github.com/DanielKarasek/vision_project/blob/main/doc_images/base_view_screenshot.png)

In this image we can see base view. On the left is frame with result either picture or webcam video feed with applied vision algorithm(here hough lines).
U can take its snapshot (and then use for example in README :D) On the right side there are settings for current method.
New settings are applied only after apply button is pressed (not on change of scale, this was too performance costly since TK has some questionable settings for callbacks).
You can choose other algorithm by pressing operation in top menu and then choosing new algorithm.
If algorithm e.g. canny is used as part of other algorithm e.g. hough lines, settings used for first algorithm standing alone is used in case first algorithm is used as part of the second algorithm. In this example if I set gaussian filter param sigma to 5 in canny method it will then be used in hough lines with this exact setting. Only difference is hough lines and hough segments. These 2 use lot of same parameters but still are 2 different algorithms therefor above doesn't apply. Current workaround is to use COPY button in hough lines - this might be solved with template pattern/other stuff later, but I am not sure if having same common parameters is always desirible so TBD.

There are 2 mods in this app. First one applies algorithm to static image. Second one works on webcam live feed. These mods can be altered in target menu at top of the screen. You can also choose another static image in this menu. Static image must be in ./test_images folder.

Some algorithms can employ different strategies to achieve same thing. For example hough lines can employ different sample strategies to sample some(all) of the edge points(sample all, every nth point or percentage of points randomly chosen). This can lead to speed up/slow down and increase/decrease/change in quality of results.

These strategies can be changed after "change strategies" button is pressed. Strategies for each method are explained further.

 
## Nothing
Nothing only copies image (from video feed or static image) to output. Also "Nothing" allows to use gaussian filter with variable sigma, so we can see how much image will be blurred when same sigma is used in Canny/Corners etc. In future blurring settings might carry forward to them. However seing blurry image doesn't give that much of insight on how the effect on further algorithms. Therefore this path isn't decided yet.

## Canny
Canny is the bread and butter algorithm used when finding lines, segments and other interest points. It can be used for many other additional processing methods such as cartoonying image. Basic algorithm uses 2/3 parameters. Low and high threshold used in double thresholding and sigma (which might be used before canny but here it is part of canny). Currently thresholds are decided automatically via simple approximation. In future versions I hope to add strategies here, so user can choose whether to use auto/manual tuning. Therefor only parameter is sigma.

## Hough Lines
Traditional hough lines algorithm. Hough transform -> peaks -> ??? -> profit! You can alter the dimensionality of hough transform with angle count and rho dim parameters. Threshold then is minimal value of peak in normalized hough transform. Min angle and min rho then sets size MxN matrix window size in which only 1 peak might be found.
Strategies:
1. Sample strategy - downsampling of edge points to increase speed of algorithm:
    * Sample all - samples all edges
    * Sample Nth - samples every n-th edge point, fast downsample. But sometimes some line have most of it points on n-th positions
    * Sample percentage randomly - A bit slower than Sample Nth, but lowers a bit danger of surrpessing some lines
2. Hough peaks - finding peaks in hough transform:
    * My hough peaks - my algorithm to find peaks, if min angle is N and min rho is M every line has to be either N degrees or M rhos from every other. Rhos and angles are in regular non-matrixed hough space(not in hough discrete image kinda spacey). These params are invariant to Rho dim and Angle count.
    * Scipy Peaks - Scipys algorithm. Min angle and min rho are same as above but in hough discrete image spacey. That means if angle is N then 2 peaks have to be N pixels away from each other in hough discrete image matrix. (this means that these params aren't invariant to Angle count and Rho dim params)
3. Retrieve lines - how are lines retrieved (tuple points representing x,y position of input image)
    * Exact lines - retrieves lines which are cropped at end of the image. This might be required for some special occasions, however this is costly.
    * Longer lines - moves along the line much further beyond the image borders to acquiare 2 points. This is much faster.

## Hough segments
Uses Hough space and point sampled from every line found (lines don't have to be calculated explicitly though), to then find segments along these lines. For every line we take all edge points (and also close additional close ones) that contributed to that line and then try to connect them. Hough segments takes same params as hough lines plus extra params. Those are max space between points. That is how much space can be between 2 points to still be consideres part of the same segment. Another one is rho off line tolerance which means how big of a corridor is considere around the line for points to be considered to atribute to that line (visually kinda how big would division space be in SVM). And lastly min segment lenght. Uses same strategies as hough lines except for line retrievel strategies.

## Corners
Traditional corner detector using quadratical approxim. to function of most change in 8 dirs. Params are sigma for gaussian filter applied before derivs calculation. Filter size tells us in how big area around maxima to suppress other smaller maximas. Lastly threshold tells us how big maxima has to be to be considered an interest point.
R score strategy - how to calculate R score from quadtratical approxim matrix
* Harris - calculates trace and det and uses its connection to eigenvalues to calculate r score
* Shi-tomasi - calculates actual eigen values and then calculates r score as the smaller one of them at given point

## Rhombuses
This algorithm uses lines found by hough lines (or any other algorithm) in the form of angle and rho. Finds all pairs of parallel lines and then all pairs that are perpendicular to each others(pair of pairs/quadruple of potential rhombus). If any of these quadruplets have all edges of cca same length then its a rhombus. First param is maximum parallel angle difference (from perfect parallelity) between lines in pairs. And second is maximum perpendicular (from perfect perpendecularity) angle difference between pairs in quadruplets
