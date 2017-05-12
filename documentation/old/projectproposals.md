#NOTE: these project proposals are not in any particular order of preference.


**\ WORKING NAME: COOKING INSPIRATION /**

    *HIGH-LEVEL DESCRIPTION* Mood-based recipe recommender for competent home cooks stuck in a rut.

    *WHY?* Most recipe apps currently available are either geared towards hand-holding beginners or only offer basic search queries from a single website (see: http://www.tomsguide.com/us/pictures-story/634-best-recipe-apps.html#s1). I believe there's a significant customer base being overlooked -- people like my friends and I who enjoy cooking, don't trust most online recipe reviews but do trust a few sources, and most importantly, can't get it together to actually go through our bookmarked recipes when menu planning. Basically, I want to build a recipe recommender that my friends and I will actually use long after this project is over.

    *PRESENTATION* probably a web app

    *NEXT STEPS*
      - scrape one food blog site, check feasibility (not terrible so far but not done yet)
      - figure out sequencing steps for model (current thoughts below):
          - make corpus => each document in corpus is an individual recipe (lemmatized, drop stop words, unigram, bigram, maybe trigram).
              - the 'individual recipe' will include the recipe instructions and blogger description.
              - benefit of recipes on blogs is that bloggers provides descriptive text along with the recipe itself. my working thesis is that this descriptive text will be helpful in categorizing recipes...
                  see link for an example: https://smittenkitchen.com/2006/10/when-the-funk-hits-the-fan/
          - create additional engineered features (3 right now want to test out)
          - get latent features from corpus excluding engineered features (allow negative matrix factorization here okay?)
              - check latent features to make sure it generally makes sense
          - how best to boost latent features with engineered features?
              - other ways to use combination of latent features + engineered features?
      - need to figure out how compare user's parameter inputs (the engineered features)
      - need to figure out how I can do testing on this?

    *DATA SOURCES* scrape favorite food blogs/sites to create recipe database
      - scrape at minimum: http://www.smittenkitchen.com/ MY FAVORITE EVER
      - figure out which other ones to add, and prioritize
      - http://www.thewednesdaychef.com/
      - https://cooking.nytimes.com/
      - http://fiveandspice.com/recipes/
      - http://orangette.net/recipes/

    *HOW IT WOULD WORK*
      1. User selects recipe parameters (engineered features):
            - level of effort to make:
            - primary ingredient type(s): chicken, beef, pork, other meat, fish, other seafood, veggies, eggs, noodles, potato, rice, legumes, tofu
            - what you're in the mood for: A Feast, Just Need Semi-Nutritious Calories, Comfort Food, Too Hot to Eat, Too Cold to Move, Food in Face NOW, Fresh Off the Farm, etc.
      2. Model would then find recipes with similar features, output top 3-5 recipes with recipe urls.
    *ADDITIONAL BELLS & WHISTLES*
      3. User can set X# of sites, and add to list of curated sites, used to make recipe recommendations.
          -can show a list of the most frequently added sites by other users.
      4. User can also give feedback ('this was a good recommendation, or this was a bad recommendation'), so the model learns.



**\ WORKING NAME: DO THESE COLORS GO TOGETHER? /**

    *HIGH-LEVEL DESCRIPTION* Taking the guesswork out of evaluating colors in online product images.

    *WHY?* Hard to gauge the true color of something you see online, and hard to tell whether it will match something you have in mind. This has stopped me on numerous occasions from buying things online, even if i can return it because returning is still a hassle. So, want to build something that could ID the color composition in a photo (or in a part of a photo).

    *PRESENTATION* probably web app

    *NEXT STEPS*
      - figure out way to grab color code/value from online pictures http://imagecolorpicker.com/
      - try pulling in data from at least the two websites below to build my own database of colors.
      - try to create own database of color matches
          - how determine what constitutes a match (can manually collect/select pictures with colors that go well together?)
          - start with matching two colors? work up from there?

    *DATA SOURCES*
      - I think I can gather info from different databases available online like the two below:
      http://www.two4u.com/color/big-table.html, http://www.colorsdb.com/

    *HOW IT WOULD WORK*
      1. extract color code/value from an online photo (e.g., curtains or clothing)
          - first limit to singular color
          - move onto patterns later (e.g., store patterned color as dict of the unique color code/values & percentage of picture occupied by that color code/value)
      2. similarly extract color code/value from a camera photo of thing you want to match (e.g., wall color or skintone).
      3. figure out some way to normalize the color code/value from online photo to the camera photo
      4. compare the normalized color combination to a database of color combinations & predict if good match or not.
          - will need to make own database of color combinations. take from styled pics online?
      5. Also output visual representation of the two colors so user can visually make the final determination on whether it 'matches' or not, depending on user taste.
      6. Send feedback immediately to model either affirming model prediction or not. That way, testing data becomes training data.



**\ WORKING NAME: HOW CREDIBLE IS THIS CLAIM? /**

    *HIGH-LEVEL DESCRIPTION* Faster way to fact-check a claim in an article.

    *WHY?* Currently, it takes a lot of effort to figure out whether a claim in an article is credible or not. You can do your own research/digging, manually cross reference the article claims with individual factcheck sites, or rely on one of the few new fake news tools, which aren't particularly suited for this type of fast checking. As context: I've been thinking about this issue for a while and wrote up some thoughts/questions I had re: development of future fake news apps at the end of this markdown text. Interesting (disheartening) study that came out recently: https://sheg.stanford.edu/upload/V3LessonPlans/Executive%20Summary%2011.21.16.pdf

    *PRESENTATION* For project purposes, probably a web site where you can paste the snippet of article text you want verified. This doesn't really lower the usage barrier much, although it would at least consolidate the fact-checking sites a user would need to visit. Ideally, this could be offered as an extension to existing apps as an additional option alongside the typical copy/paste/select options that pop up when you highlight text on your phone.

    *NEXT STEPS*
      - take a look at the data from the API pull from Hoaxy (https://market.mashape.com/truthy/hoaxy)
      - figure out scraping for snopes.com & factcheck.org
      - create corpus => each document is a claim (lemmatized/stemmatized/without stop words?, uni/bi/tri/etc grams, need to figure out what combo of these makes sense) & true/false (develop more nuanced categorization as future step?)
      - would i just compare whatever claim user inputs/highlights to database??
          - too many features for KNN? not sure...
          - https://en.wikipedia.org/wiki/K-d_tree
      - think about how to limit KNN results & how results should be presented to user:
          - if there is a 'close match': user sees: true/false, fact-checked by X out of X sites, and link to explanation from one site.
          - if there's no 'close match': user sees: 'this claim hasn't been reported by fact-checking sites, click here to send claim to each fact-checking site for follow-up'
      - but what if want to evaluate potentially new claims? does it even make sense to try and predict based on just the influential words in a claim?
          - i don't think so, prob would need more info about the claim, like what site it originated from, etc?

    *DATA SOURCES* start out with two at minimum, then do others, depending on ease of scraping:
      - https://market.mashape.com/truthy/hoaxy
      - http://www.snopes.com/feed/
      - factcheck.org
      - politifact.org
      - washingtonpost.com/news/fact-checker

    *SOME ADDITIONAL THOUGHTS*
      I don't think the actual data science work would be particularly inventive (although I'm still not sure what method should be applied exactly). However, i think the idea is worth looking into, definitely something I'd want to discuss further with others. some other food for thought: http://pressthink.org/2015/04/its-not-that-we-control-newsfeed-you-control-newsfeed-facebook-please-stop-with-this/



***OTHER IDEAS***

**How else can we measure unemployment (different segments, in real-time or at least more frequently) that could help inform private businesses decision-making?**

**Optimize what to plant on fallow fields that will be most cost effective/beneficial for rejuvenating field for future crop yields**



***DRAFT: SOME THOUGHTS RE DEVELOPING FAKE NEWS APPS***

Recently, I’ve noticed a lot of fanfare surrounding the roll-out of new fake news apps, most notably, Indiana University’s Hoaxy, Google’s fake news detector, and Facebook’s warning labels.

Intrigued, I tested these three out. In the process, I did some additional research and realized that most of the analysis focuses on difficulties with the content. Yes, the content is incredibly hard to define and identify. But just as importantly, it’s also incredibly difficult to define what you, as the creator, want the user to take away from seeing a fake news alert, how to deliver the alert in a user-friendly and effective way, and measure impact from your app. Ultimately, I came away with even more questions than I started with!

  1.	What is the end goal of these apps?

      The stated goal of the three above were to educate.  I wonder if education is an interim goal and the logical (unstated) end goal is to decrease user propensity towards consuming/circulating fake news in the future?

  2.	Who are these apps targeting?

      People on the fence? Do those still exist? No, seriously, I’m asking if anyone has a good definition, a decent way to measure this, and what percentage of the U.S. population are still on the fence.

  3.	How effective are these current apps?

      Counterintuitively, ‘educate’ seems like the easier target to hit but it’s also more nebulous. There could, or could not, be a concrete change in behavior tied to education. Regardless, it’s difficult to quantify effectiveness towards either ‘educate’ and ‘stop consuming/circulating’ goals.

  4.	How can we measure effectiveness? A few ideas came to mind (comments/suggestions welcome!):

      ♣	More targeted but also more invasive?
        →	Browsing history/social media activity/purchasing history over time for users that have downloaded, or been exposed to, fact-checking apps

      ♣	Noisier but less invasive?
        →	Changes in voting history for users that have downloaded, or been exposed to, fact-checking apps (also very infrequent although there have been a couple special elections recently to tide us over until 2018).
        →	Site traffic over time for websites with most egregious history of circulating fake news- as a more general measure of increasing education elevates all browsing activity?

      ♣	More precise but extremely labor intensive and expensive?
        →	Survey a very robust sample of users! With just the right number of unbiased questions! Over time!
        →	As a former field organizer, I think you get higher quality data from a door-to-door canvassing program, when structured appropriately, rather than from call centers. Even if it means occasionally getting bitten by a dog.

  5.	Are users receptive to the way information is being delivered in these apps? Are there other delivery methods that are more effective or effective in different ways?

      As someone who is contrarian by nature, I can easily understand the reflexive, and sometimes irrational, defiant response a user might have if they start seeing fake news tags all over their favorite news feeds. It just might have the exact opposite effect.

      It seems to me that current users of fake news apps are likely already biased- they made the conscious decision to download Google’s add-on or visit the hoaxy site. Facebook is the outlier here, but they are, understandably, cautious about what gets tagged. For companies like Facebook and Google, I also wonder how much they stand to lose in terms of business if they get more aggressive in their fake news detection, and whether we, as users, should be relying so heavily on them to deal with this issue.

      One example comes to mind: there’s an article circulating recently titled: “Chicago Tribune Says Facebook's 'Fake News' Filter Is Killing Its Traffic“. It looks suspicious, is only getting circulated by zerohedge/briebart types, but it’s not registering on any of the fake news apps. The article also includes a lot of charts that should be impressive but only increases the number of questions I have!
