*HIGH-LEVEL DESCRIPTION* **Helping you figure out how to bring natural colors into your life??** Taking the guesswork out of evaluating colors in online product images will match what consumer has at home.


*WHY?* Hard to gauge the true color of something you see online, and hard to tell whether it will match something you have in mind. This has stopped me on numerous occasions from buying things online, even if i can return it because returning is still a hassle. So, want to build something that could ID the color composition in a photo (or in a part of a photo) & predict whether it will match what user had in mind. **also, natural tones don't have to be neutrals--> colors of nature**


*Create dataset of only good color matches:*
    1. Scrub NatGeo for Nature contest pictures
        - Selenium + BeautifulSoup
        - **how many good photos need, minimum?**
        Alternatives:
            - https://github.com/carlosabalde/ngwallpaper
            - http://tofu.psych.upenn.edu/~upennidb/

    2. Translate each picture into a data point
        - grab raw color values from each picture (color values in RGB code)
            - each pixel has its own color value as a tuple
        - each picture will have a list of tuples
        **keep code somewhere of which is the "home" photo and which is the "prospie" photo**
            from PIL import Image
            import numpy as np
            image = Image.open('9192469_1600x1200.jpg', 'r')
            width, height = image.size
            pixel_values = list(image.getdata())
            if image.mode == 'RGB':
                channels = 3
            elif image.mode == 'L':
                channels = 1
            else:
                print("Unknown mode: %s" % image.mode)
            pixel_values = np.array(pixel_values).reshape(width, height, channels))

            *how to flatten lists by one level in python*
            http://lemire.me/blog/2006/05/10/flattening-lists-in-python/
            def flatten(x):
                flat = True
                ans = []
                for i in x:
                if ( i.__class__ is list):
                ans = flatten(i)
                else:
                ans.append(i)
                return ans


    3. Add in ylabels to create raw dataset below:    
            pic_id               raw_color_values                             ylabel
               1      [(255, 165, 0), (189, 183, 107), (0, 128, 0), ... ]        1
               **could i make a raw dataset without ylabels?**
               **maybe separate out each color value as own feature?**

    4. Do feature reduction on raw dataset:
        - DBSCAN! density based algorithm – it assumes clusters for dense regions, doesn’t require that every point be assigned to a cluster (so doesn’t partition the data) but instead extracts the ‘dense’ clusters and leaves sparse background classified as ‘noise’.
        cluster around 3 features: R, G, B, in 3-dimensional feature space.
            - hyperparameters: min_sample, epsilon (distance parameter)
        http://hdbscan.readthedocs.io/en/latest/comparing_clustering_algorithms.html

        a. for each picture, simplify the number of colors found in each picture and add weighting for color prominence (so can ignore minor color variations and provides a rough measure of color composition):
            - cluster the obvs & take the mode of each cluster
            - 'weight' = (#obvs originally in each cluster)/(total # in picture)
            - collapse down one obvs (mode_color_value_combo, mode_weight)

    5. Final training dataset should look like:
                      weighted_color_values                            ylabel
            [(255165000, 0.15), (189183107, 0.25), (000128000, 0.6)]      1

*do train/test/split randomly*
    - can add in a y_train, y_test for it if needed for the command.

*fit some unary classifier with train set*
    - something with silhouette analysis & k-means clustering? or KNN?
    http://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
    - look at unary classifers to try below.

*make prediction on test set*


*How evaluate predictions made on X_test?*
    - well, if i randomly split the dataset into X_test and X_train, and all my data only has one class...then, can't I evaluate predictions made on X_test by seeing how many were predicted to be outliers vs inliers? In reality, they should all be inliers. So from there, i can create my own confusion matrix?
    - more reading to do on outlier models: https://books.google.com/books?id=UNmfDgAAQBAJ&pg=PA25&lpg=PA25&dq=how+outlier+dector+models+test+train+predictions&source=bl&ots=kUt_hUlz0N&sig=l_V21p98KUbr1ID7M1L3prUY6EE&hl=en&sa=X&ved=0ahUKEwiQgMW15MrTAhUPxGMKHaFtD-EQ6AEIOTAD#v=onepage&q&f=false

*Provide a recommendation:*
    - TBD, lower prioritity.


*How it will work:*
    1. User pastes two photos, a "member" photo and a "prospie" photo, into web app
    2. Separate code transforms photos into one observation, send to model
        - **potential issue: b/c include weighting measure, need to require the photos are to the same scale...**
        - **maybe leave making/using a weight measure for now? Would it be too simple without?**
    3. Model takes new observation in and predicts whether the combination of color palettes is a good match
    4. Model will also give a recommendation on what would be a good color or colors alternative. recommendation not in rbg code, but the color itself.


*Good examples of potential pictures for training set*
http://www.creativebloq.com/photography/still-life-photography-1131688
http://www.nationalgeographic.com/photography/best-photos-2016/
http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/gallery/winners-landscape/1

http://photography.nationalgeographic.com/photography/photo-contest/2014/entries/gallery/nature-winners/
http://photography.nationalgeographic.com/photography/photo-contest/2013/entries/gallery/nature-winners/


http://photography.nationalgeographic.com/nature-photographer-of-the-year-2016/gallery/week-10-landscape/1
http://photography.nationalgeographic.com/contest-2015/gallery/week-10-nature/1
http://travel.nationalgeographic.com/travel/traveler-magazine/photo-contest/2014/entries/gallery/outdoor-scenes-week-14/#/2


maybe can pull off atlantic? but only like 18 photos at best from one site....ugh....
https://www.theatlantic.com/photo/2016/12/winners-of-the-2016-national-geographic-nature-photographer-of-the-year-contest/510350/


*unary classifiers to try*
    random one (Unary classifier to detect exploits for different hardware indicators with TensorFlow) from github: https://github.com/zblasingame/unary-classifier


    OneClassSVM in sklearn: http://scikit-learn.org/stable/modules/outlier_detection.html

    ensemble.IsolationForest in sklearn: One efficient way of performing outlier detection in high-dimensional datasets is to use random forests. http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html#sklearn.ensemble.IsolationForest

    See Outlier detection with several methods. for a comparison of ensemble.IsolationForest with svm.OneClassSVM (tuned to perform like an outlier detection method) and a covariance-based outlier detection with covariance.MinCovDet. http://scikit-learn.org/stable/auto_examples/covariance/plot_outlier_detection.html#sphx-glr-auto-examples-covariance-plot-outlier-detection-py

*python code to try all three sklearn outlier detection methods*
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.font_manager

from sklearn import svm
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest

rng = np.random.RandomState(42)

# Example settings
n_samples = 200
outliers_fraction = 0.25
clusters_separation = [0, 1, 2]

# define two outlier detection tools to be compared
classifiers = {
    "One-Class SVM": svm.OneClassSVM(nu=0.95 * outliers_fraction + 0.05,
                                     kernel="rbf", gamma=0.1),
    "Robust covariance": EllipticEnvelope(contamination=outliers_fraction),
    "Isolation Forest": IsolationForest(max_samples=n_samples,
                                        contamination=outliers_fraction,
                                        random_state=rng)}

# Compare given classifiers under given settings
xx, yy = np.meshgrid(np.linspace(-7, 7, 500), np.linspace(-7, 7, 500))
n_inliers = int((1. - outliers_fraction) * n_samples)
n_outliers = int(outliers_fraction * n_samples)
ground_truth = np.ones(n_samples, dtype=int)
ground_truth[-n_outliers:] = -1

# Fit the problem with varying cluster separation
for i, offset in enumerate(clusters_separation):
    np.random.seed(42)
    # Data generation
    X1 = 0.3 * np.random.randn(n_inliers // 2, 2) - offset
    X2 = 0.3 * np.random.randn(n_inliers // 2, 2) + offset
    X = np.r_[X1, X2]
    # Add outliers
    X = np.r_[X, np.random.uniform(low=-6, high=6, size=(n_outliers, 2))]

    # Fit the model
    plt.figure(figsize=(10.8, 3.6))
    for i, (clf_name, clf) in enumerate(classifiers.items()):
        # fit the data and tag outliers
        clf.fit(X)
        scores_pred = clf.decision_function(X)
        threshold = stats.scoreatpercentile(scores_pred,
                                            100 * outliers_fraction)
        y_pred = clf.predict(X)
        n_errors = (y_pred != ground_truth).sum()
        # plot the levels lines and the points
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        subplot = plt.subplot(1, 3, i + 1)
        subplot.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),
                         cmap=plt.cm.Blues_r)
        a = subplot.contour(xx, yy, Z, levels=[threshold],
                            linewidths=2, colors='red')
        subplot.contourf(xx, yy, Z, levels=[threshold, Z.max()],
                         colors='orange')
        b = subplot.scatter(X[:-n_outliers, 0], X[:-n_outliers, 1], c='white')
        c = subplot.scatter(X[-n_outliers:, 0], X[-n_outliers:, 1], c='black')
        subplot.axis('tight')
        subplot.legend(
            [a.collections[0], b, c],
            ['learned decision function', 'true inliers', 'true outliers'],
            prop=matplotlib.font_manager.FontProperties(size=11),
            loc='lower right')
        subplot.set_title("%d. %s (errors: %d)" % (i + 1, clf_name, n_errors))
        subplot.set_xlim((-7, 7))
        subplot.set_ylim((-7, 7))
    plt.subplots_adjust(0.04, 0.1, 0.96, 0.92, 0.1, 0.26)

plt.show()


    only with Java?? oneClassClassifier1.0.4. http://sourceforge.net/projects/weka/files/weka-packages/




*color code resources*
    http://www.computerhope.com/htmcolor.htm
    http://www.rapidtables.com/web/color/RGB_Color.htm
    http://www.two4u.com/color/big-table.html
    http://www.colorsdb.com/
    http://chir.ag/projects/name-that-color/#6195ED HAS NAMES FOR ALL COLORS

    *python program/code!*
    http://stackoverflow.com/questions/138250/how-can-i-read-the-rgb-value-of-a-given-pixel-in-python

    *get all pixel values, output a numpy array*
    def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    pixel_values = numpy.array(pixel_values).reshape((width, height, channels))
    return pixel_values

    *install PIL using the command "sudo apt-get install python-imaging" and run the following program. It will print RGB values of the image. If the image is large redirect the output to a file using '>' later open the file to see RGB values*
    import PIL
    import Image
    FILENAME='fn.gif' #image can be in gif jpeg or png format
    im=Image.open(FILENAME).convert('RGB')
    pix=im.load()
    w=im.size[0]
    h=im.size[1]
    for i in range(w):
      for j in range(h):
        print pix[i,j]

    *use PIL to load the image:*
    from PIL import Image
    img = Image.open('yourimage.png')
    *I'm going to suggest a method that messes directly with the image data, without accessing individual pixels by coordinates.
    You can get the image data in one big byte string:*
    data = str(img.tobytes) #data = img.tostring() is deprecated
    *You should check img.mode for the pixel format. Assuming it's 'RGBA', the following code will give you separate channels:*
    R = data[::4]
    G = data[1::4]
    B = data[2::4]
    A = data[3::4]
    *If you want to access pixels by coordinate you could do something like:*
    width = img.size[0]
    pixel = (R[x+y*width],G[x+y*width],B[x+y*width],A[x+y*width])
    *Now to put it back together, there's probably a better way, but you can use zip:*
    new_data = zip(R,G,B,A)
    *And reduce:*
    new_data = ''.join(reduce(lambda x,y: x+y, zip(R,G,B,A)))
    *Then to save the picture:*
    new_img = Image.fromstring('RGBA', img.size, new_data)
    new_img.save('output.png')

    *PyPNG - lightweight PNG decoder/encoder
    Although the question hints at JPG, I hope my answer will be useful to some people.
    PyPNG is a single pure Python module less than 4000 lines long, including tests and comments.
    PIL is a more comprehensive imaging library, but it's also significantly heavier.
    Here's how to read and write PNG pixels using PyPNG module:*
    import png, array
    point = (2, 10) # coordinates of pixel to be painted red
    reader = png.Reader(filename='image.png')
    w, h, pixels, metadata = reader.read_flat()
    pixel_byte_width = 4 if metadata['alpha'] else 3
    pixel_position = point[0] + point[1] * w
    new_pixel_value = (255, 0, 0, 0) if metadata['alpha'] else (255, 0, 0)
    pixels[
      pixel_position * pixel_byte_width :
      (pixel_position + 1) * pixel_byte_width] = array.array('B', new_pixel_value)
    output = open('image-with-red-dot.png', 'wb')
    writer = png.Writer(w, h, **metadata)
    writer.write_array(output, pixels)
    output.close()
