*High-Level Description* Taking the guesswork out of evaluating colors from online products.

*Motivation* It's hard to gauge the true color of something you see online and figure out whether it will match something you have in mind. This has stopped me on numerous occasions from buying things online, even if I can return it because returning is still a hassle. So, I want to build something that could ID the color composition in a photo (or in a part of a photo) & predict whether it will match what user had in mind.

*Data* How will I determine what is a good color combination? I'll use the color composition found in top-rated National Geographic nature/landscape photos as my reference point.

*Presentation* Via web app, user uploads two photos ("home" and "prospective"). Model will then predict whether the combined colors from user photos are 'good' color combinations by comparing to dataset of 'good' color combinations pulled from top National Geographic nature/landscape photos.

*Visualizations* Depending on the EDA phase, there could be an interesting viz of the clustering of color values or something. TBD.

*Next Steps* At the bottom, I've fleshed out two workflows: overall high-level project & more detailed predictive model. In terms of next steps, I'm currently at #3b of the predictive model workflow. I need to work through clustering with a smaller subset of color values so I can get a better feel for the data and also figure out if my conceptualization of the data is correct. Once that happens, then I will probably need to start setting up/utilizing AWS for the rest of my project (I already ran out of memory once trying to cluster one unpacked picture).

*Overall Project High-level Workflow*
#1	user inputs
	basic option:    upload home & prospective photos into web app
                     don't allow photos with whitespace/background

    advanced option: upload home & prospective photos into web app
	                 allow photos with whitespace/background

#2	user input transformation
	basic option:    makes R, G, B values for each input
                     outputs combined RGB values	 
    advanced option: makes R, G, B values for each input
	                 outputs combined RGB values & RGB values for home photo only

#3	model(s)- more details in bottom section
    basic option:    predictive model
                     takes combined RGB values
                     predicts: inlier/outlier

    advanced option: predictive model
	                 takes combined RGB values
                     predicts: inlier/outlier
                     recommender_model
                     takes RGB values for home photo
                     outputs: most frequent colors found with home photo color(s)

#4	output for user consumption
    basic option:    returns whether color combination of two photos are good
                     (inlier=good, outlier=not good)
	advanced option: returns whether color combination of two photos are good
	                 (inlier=good, outlier=not good)
		             also returns additional color combinations suggestions
		             (in picture form)

*More Detailed Predictive Model Workflow*
#3a	Compile raw photos
	basic option:    from NatGeo Photo of the Day Archives (Nature, Landscapes)
                     (currently pulled in about 1900 pictures)
    additional:      NatGeo Nature Photo Contest Finalists
                     Flickr/Instagram API

#3b	Translate pictures into pixel values
	per picture:     PIL/Image+Numpy
                     each pixel has 3 separate R, G, and B features
                     cluster pixels using DBSCAN (set params, min_samples, distance_metric)
                     get centroid/mode of DBSCAN clusters
                     get count of how many in each cluster
                     collapse dataset down to centroid/mode & weight
	basic option:    final features per picture: centroid/mode value(s), weight(s)
    additional:      assess if benefit from another DBSCAN across all pictures

#3c	Make train/test/split on data set

#3d	Fit train set with unary classifier
	if dataset small:  bootstrap
	                   try smote?
    if dataset large:  crossvalidate

    basic classifiers: OneClassSVM (sklearn)
                       ensemble.IsolationForest (sklearn)
                       covariance.MinCovDet (sklearn)
    additional:        Unary classifier with TensorFlow
                       (https://github.com/zblasingame/unary-classifier)

#3e	Evaluate train prediction
	basic option:      compare # predicted outliers vs inliers
                       with unary classifer, all should be inliers
                       create my own confusion matrix to calc model scores
    additional:        Other anomaly detector models evaluation methods

#3f	Tune parameters (GridSearchCV) & re-evaluate model

#3g	Predict with test set & get out-of-sample model evaluation score
