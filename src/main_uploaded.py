import cluster
import get_colorvalues
import make_app_ready_results
import numpy as np
import pandas as pd
import pdb
import save_scraped
import silhouette
import transform_final

'''
********
MAKE #3 - #8 INTO A SEPARATE FUNCTION WHEN DONE!

OH SHIT...this only compares one photo right now....shit.

def webapp_results(num_jpgs_user_uploaded):
    ...
    return x,y,z,etc
******
'''


def analyzer(path):
    # 1: convert uploaded picture from web app
    # 1a: get list of jpegs in upload folder
    # path = "/Users/colinbottles/Desktop/Cat/school/color-match/uploads/"
    jpg_uploaded = save_scraped.get_files_in_folder(path)
    try:
        jpg_uploaded.remove(path+'.DS_Store')
    except ValueError:
        pass
    else:
        pass

    # 2: create empty list to hold final data.
    U_clustered = []
    U_baseline = []
    U_jpgs_covered = []
    # 1b: loop over all functions for each jpg to get final data for each jpg
    for item in jpg_uploaded:
        # 3a: converts jpg to np array
        pixel_values, rgb_or_not = get_colorvalues.convert_jpg_array(item,
                                                                     downsize_factor=0.25)
        # make sure the jpg is RGB, not b&w:
        if rgb_or_not == 'RGB':
            # save down simple averaged pixel_values for baseline model
            U_baseline.append(get_colorvalues.get_baseline_arr(pixel_values))
            # clusters raw pixel values & keeps just the ones need
            csind, labels, raw_df = cluster.dbscan_indiv_pic(pixel_values,
                                                             epsilon=3,
                                                             min_clust_size=10,
                                                             algo='ball_tree',
                                                             dist_metric='euclidean',
                                                             num_jobs=2,
                                                             jpg_num=item)
            # transforms clustered pixel values into final format
            arr_one_color_combo = transform_final.create_final_X_dataset(csind,
                                                                         labels,
                                                                         raw_df)
            # appends arr_one_color_combo to final format
            U_clustered.append(arr_one_color_combo)
            # keeps tally of which jpgs were scrubbed in, in same oder as 3 f&g
            U_jpgs_covered.append(item)

    # 2: unpickle clustered/baseline arrays & order for calculations
    filepath = '/Users/colinbottles/Desktop/Cat/school/color-match/data/processed/'
    filename = 'pickled_list_arr'
    basename = 'pickled_list_arr_baseline'
    order = 'pickled_jpg_order'
    list_clusters = transform_final.unpick(filepath+filename)
    list_baseline = transform_final.unpick(filepath+basename)
    list_order = transform_final.unpick(filepath+order)

    # 3: set which photo in uploaded want to score for (order)
    uploaded = 0

    # 4: calculate silhouette score in RGB space & convert all RGB to HEX for web
    # uploaded = num_jpgs_user_uploaded - 1
    list_scores_cl = []
    list_hex_arr = []
    uploaded_arr = U_clustered[uploaded]
    list_hex_uploaded_arr = get_colorvalues.convert_to_hex(uploaded_arr)

    for arr in list_clusters:
        score = silhouette.calc_silhouette_score(arr, uploaded_arr)
        list_scores_cl.append(score)
        hex_arr = get_colorvalues.convert_to_hex(arr)
        list_hex_arr.append(hex_arr)

    # 5: calculate baseline score in RGB space & convert all RGB to HEX for web
    list_scores_base = []
    list_hex_barr = []

    uploaded_barr = U_baseline[uploaded]
    list_hex_uploaded_barr = get_colorvalues.convert_to_hex(uploaded_barr)

    for barr in list_baseline:
        if len(uploaded_barr) == 1 & len(barr) == 1:
            '''workaround for when both clusters are just points,
               then silhouette doesnt work obvs'''
            baseline_score = silhouette.calc_distance(barr, uploaded_barr)
            list_scores_base.append(baseline_score)
        else:
            baseline_score = silhouette.calc_silhouette_score(barr,
                                                              uploaded_barr)
            list_scores_base.append(baseline_score)
        hex_barr = get_colorvalues.convert_to_hex(barr)
        list_hex_barr.append(hex_barr)

    # 6: make df of silhouette & baseline scores & order
    score_comparison = pd.DataFrame(np.column_stack([list_order,
                                                    list_scores_base,
                                                    list_scores_cl,
                                                    list_hex_arr,
                                                    list_hex_barr]),
                                    columns=['jpg_path', 'baseline',
                                             'clustered', 'hex_clustered',
                                             'hex_baseline'])

    # 7: clean df: convert column format, round if numeric, parse if string
    score_comparison = score_comparison.astype(dtype={"jpg_path": "str",
                                                      "baseline": "float64",
                                                      "clustered": "float64",
                                                      "hex_clustered": "str",
                                                      "hex_baseline": "str"})

    score_comparison[['baseline', 'clustered']] = score_comparison[['baseline', 'clustered']].apply(lambda x: pd.Series.round(x, 2))
    score_comparison['jpg'] = score_comparison['jpg_path'].apply(lambda x: x.split('/')[-1])
    score_comparison = score_comparison.drop('jpg_path', axis=1)

    # 8A: predict if color combination is appealing (e.g., the lowest score)
    # STILL HAVE TO SET THRESHOLD FOR WHAT IS GOOD VS NOT!
    # REQUIRES TWO PHOTOS TO BE UPLOADED BY USER VIA WEBAPP
    lowest_score_cl = score_comparison['clustered'].min()
    if lowest_score_cl > 1.09:
        clustered_prediction = 'Clustered Prediction: Palette is not appealing'
    else:
        clustered_prediction = 'Clustered Prediction: Palette is appealing'
    # FOR PRESENTATION - DEFEND WHY NOT GO WITH SIMPLE BASELINE:
    lowest_score_base = score_comparison['baseline'].min()
    if lowest_score_base > 1.09:
        baseline_prediction = 'Baseline prediction: Palette is not appealing'
    else:
        baseline_prediction = 'Baseline prediction: Palette is appealing'

    # 8B: suggested appealing palette(s) (using the lowest score(s))
        # REQUIRES ONLY ONE PHOTO TO BE UPLOADED BY USER VIA WEBAPP
    # de-duplicate hex_codes already in user uploaded clustered palette
    msug = score_comparison.sort_values(['clustered']).head(1).hex_clustered.values.tolist()
    list_msug = []
    for num in range(len(msug)):
        entire = msug[num].split("['")[-1].split("']")[0].split("', '")
        deduped = [x for x in entire if x not in list_hex_uploaded_arr]
        list_msug.append(deduped)
    # FOR PRESENTATION ONLY: WHY NOT GO WITH SIMPLE BASELINE?
    bentire = score_comparison.sort_values(['hex_baseline']).head(1).hex_baseline.values.tolist()
    # de-duplicate hex_codes already in user uploaded baseline palette
    list_bsug = [x for x in bentire if x not in list_hex_uploaded_barr]
    ''' because this is pure euclidean distance from one ave RGB to another,
        will only tell you how similar one RGB is to another
    '''

    # 8C: suggested appealing palette(s) (using score(s) around 1)
    # REQUIRES ONLY ONE PHOTO TO BE UPLOADED BY USER VIA WEBAPP
    # de-duplicate hex_codes already in user uploaded clustered palette
    m2sug = score_comparison.query('0.95 <= clustered <= 1.09').sort_values(['clustered']).head(1).hex_clustered.values.tolist()
    list_m2sug = []
    for num in range(len(m2sug)):
        entire = m2sug[num].split("['")[-1].split("']")[0].split("', '")
        deduped = [x for x in entire if x not in list_hex_uploaded_arr]
        list_m2sug.append(deduped)
    # FOR PRESENTATION ONLY: WHY NOT GO WITH SIMPLE BASELINE?
        ''' there is no similar comparison for baseline score, right???
            because this is pure euclidean distance from one ave RGB to another
        '''

    # 9A: create dynamic html ready tables for suggested palettes
    # using lowest score(s)
    colors1 = make_app_ready_results.table_ready_2loops(list_msug)
    sugg1 = make_app_ready_results.html_ready(list_col1=colors1,
                                              name_col1='colors',
                                              dtype_col1='str',
                                              list_col2=list_msug[0],
                                              name_col2='codes',
                                              dtype_col2='str')
    # using score(s) around 1
    colors2 = make_app_ready_results.table_ready_2loops(list_m2sug)
    sugg2 = make_app_ready_results.html_ready(list_col1=colors2,
                                              name_col1='colors',
                                              dtype_col1='str',
                                              list_col2=list_m2sug[0],
                                              name_col2='codes',
                                              dtype_col2='str')

    # 9B: create dynamic html ready table for user uploaded base palette
    colorsb = make_app_ready_results.table_ready_1loop(list_hex_uploaded_arr)
    suggb = make_app_ready_results.html_ready(list_col1=colorsb,
                                              name_col1='colors',
                                              dtype_col1='str',
                                              list_col2=list_hex_uploaded_arr,
                                              name_col2='codes',
                                              dtype_col2='str')

    # 10: RETURN!!
    return clustered_prediction, baseline_prediction, sugg1, sugg2, suggb

    '''WHAT I WANT TO SHOW ON WEBAPP

    base clustered palette: colored_cell1 colored_cell2 colored_cell3 ... etc
                                hex1          hex2            hex3    ... etc

    Suggested clust palette: colored_cell1 colored_cell2 colored_cell3 ... etc
                                hex1          hex2            hex3     ... etc
    '''

    '''NEED TO RETURN FROM MAIN_UPLOADED.PY TO MAKE THIS HAPPEN

    Your base palette: uploaded_arr -> HEX CODE
    '''

    '''HOW TO RETURN THIS IN THE RIGHT FORMAT
    structure data so the template doesn't depend on the order of the cells:

    from itertools import izip
    x = [dict(user=u, sug=s) for u, s in izip(score_comparison['user'],
                                              score_comparison['sug'])]
    Then you can access your data like this:

    {% for row in x %}
        <tr>
          <td>{{ row['user']|tojson|safe }}</td>
          <td>{{ row['sug'] }}</td>
        </tr>
    {% endfor %}

    '''
