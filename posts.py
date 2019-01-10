import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def merge_csvs():
    # Aug 18 - Jan 19
    df1 = pd.read_csv('Post_1.csv')
    df1 = df1.drop(df1.index[0])
    #Dec 17 - Mar 18
    df2 = pd.read_csv('Post_2.csv')
    df2 = df2.drop(df2.index[0])
    #Mar-Aug 2018
    df3 = pd.read_csv('Post_3.csv')
    df3 = df3.drop(df3.index[0])

    dfs = [df1, df2, df3]

    merged = pd.concat(dfs, sort=False, ignore_index=True)

    merged.to_csv('posts_merged.csv')
    pd.options.display.max_rows = 999
    pd.options.display.max_columns = 999

def cleaning(df):
    df = df.rename(index=str, columns={'Post ID':'id',
    'Permalink':'url',
    'Post Message':'text',
    'Type':'type',
    'Posted':'timestamp',
    'Lifetime Post Total Reach':'total_reach',
    'Lifetime Post organic reach':'org_reach',
    'Lifetime Post Paid Reach':'paid_reach',
    'Lifetime Post Total Impressions':'total_imp',
    'Lifetime Post Organic Impressions':'org_imp',
    'Lifetime Post Paid Impressions':'paid_imp',
    'Lifetime Engaged Users':'engaged',
    'Lifetime Matched Audience Targeting Consumers on Post':'clickers',
    'Lifetime Matched Audience Targeting Consumptions on Post':'clicks',
    'Lifetime Negative Feedback from Users':'neg_users',
    'Lifetime Negative Feedback':'neg',
    'Lifetime Negative Feedback from Users by Type - hide_all_clicks':'neg_users_hide',
    'Lifetime Negative Feedback by Type - hide_all_clicks':'neg_hide',
    'Lifetime Post Impressions by people who have liked your Page':'like_interest',
    'Lifetime Post reach by people who like your Page':'like',
    'Lifetime Post Paid Impressions by people who have liked your Page':'like_interact_paid',
    'Lifetime Paid reach of a post by people who like your Page':'like_paid',
    'Lifetime People who have liked your Page and engaged with your post':'like_engage',
    'Lifetime Organic views to 95%':'vid_95',
    'Lifetime Paid views to 95%':'vid_95_paid',
    'Lifetime Organic Video Views':'vid',
    'Lifetime Paid Video Views':'vid_paid',
    'Lifetime Average time video viewed':'vid_avg',
    'Lifetime Video length':'vid_length',
    'Lifetime Talking About This (Post) by action type - share':'story_share',
    'Lifetime Talking About This (Post) by action type - like':'story_like',
    'Lifetime Talking About This (Post) by action type - comment':'story_comment',
    'Lifetime Post Stories by action type - share':'post_share',
    'Lifetime Post Stories by action type - like':'post_like',
    'Lifetime Post Stories by action type - comment':'post_comment',
    'Lifetime Post Audience Targeting Unique Consumptions by Type - other clicks':'audience_clicks_other',
    'Lifetime Post Audience Targeting Unique Consumptions by Type - link clicks':'audience_clicks_link',
    'Lifetime Post Audience Targeting Unique Consumptions by Type - photo view':'audience_photo',
    'Lifetime Post Audience Targeting Unique Consumptions by Type - video play':'audience_video',
    'Lifetime Matched Audience Targeting Consumptions by Type - other clicks':'email_clicks_other',
    'Lifetime Matched Audience Targeting Consumptions by Type - link clicks':'email_clicks_link',
    'Lifetime Matched Audience Targeting Consumptions by Type - photo view':'email_clicks_photo',
    'Lifetime Matched Audience Targeting Consumptions by Type - video play':'email_clicks_video'})

    df.drop(['Countries', 'Audience Targeting','Languages','Lifetime Organic views to 95%.1', 'Lifetime Paid views to 95%.1', 'Lifetime Organic Video Views.1', 'Lifetime Paid Video Views.1'], axis=1, inplace=True)

    df[['total_reach', 'org_reach', 'paid_reach', 'total_imp', 'org_imp', 'paid_imp', 'engaged', 'clickers', 'clicks', 'neg_users', 'neg', 'neg_users_hide', 'neg_hide', 'like_interest', 'like', 'like_interact_paid', 'like_paid', 'like_engage', 'vid_95', 'vid_95_paid', 'vid', 'vid_paid',  'vid_avg', 'vid_length', 'story_share', 'story_like', 'story_comment', 'post_share', 'post_like', 'post_comment', 'audience_clicks_other', 'audience_clicks_link', 'audience_photo', 'audience_video', 'email_clicks_other', 'email_clicks_link', 'email_clicks_photo', 'email_clicks_video']] = df[['total_reach', 'org_reach', 'paid_reach', 'total_imp', 'org_imp', 'paid_imp', 'engaged', 'clickers', 'clicks', 'neg_users', 'neg', 'neg_users_hide', 'neg_hide', 'like_interest', 'like', 'like_interact_paid', 'like_paid', 'like_engage', 'vid_95', 'vid_95_paid', 'vid', 'vid_paid', 'vid_avg', 'vid_length', 'story_share', 'story_like', 'story_comment', 'post_share', 'post_like', 'post_comment', 'audience_clicks_other', 'audience_clicks_link', 'audience_photo', 'audience_video', 'email_clicks_other', 'email_clicks_link', 'email_clicks_photo', 'email_clicks_video']].apply(pd.to_numeric)

    col_list = ['engaged', 'clickers', 'clicks', 'neg_users', 'neg_users_hide', 'neg_hide', 'like_interest', 'like', 'like_interact_paid', 'like_paid', 'like_engage','story_share', 'story_like', 'story_comment', 'post_share', 'post_like', 'post_comment', 'audience_clicks_other', 'audience_clicks_link', 'audience_photo', 'audience_video', 'email_clicks_other', 'email_clicks_link', 'email_clicks_photo', 'email_clicks_video']

    #data are wonky for this post: there are 0 'total reach', but there are values for 'engaged' etc...??? DROP
    df = df.drop(df.index[205])

    #set timestampe as index
    timestamp = df['timestamp']
    df['timestamp'] = pd.to_datetime(timestamp,infer_datetime_format=True)
    df = df.set_index(['timestamp'])

    return make_prop(df, col_list)

def make_prop(df, col_list):
    var_name = ''
    # if df.loc[:, (df['total_reach'])] != 0:
    for i in col_list:
        var_name = i+'_prop'
        df[var_name] = df[i]/df['total_reach']
    return df

def boxplots(df, vars, ylab, save_as):
    box = pd.DataFrame(data=df, columns=vars)
    print(box.describe())
    ax = sns.boxplot(x='variable', y='value', data=pd.melt(box))
    ax.set_xticklabels(ax.get_xticklabels(),rotation=60)
    plt.xlabel('Variable', weight='bold')
    plt.ylabel(ylab, weight='bold')
    plt.tight_layout()
    # plt.show()
    plt.savefig(save_as)

def top_ten(df, describe_upper,  prop_var):
    '''GET INDEX OF COLUMN'''
    idx = df.columns.get_loc(prop_var)
    type_idx = df.columns.get_loc('type')
    URL_idx = df.columns.get_loc('url')
    text_idx = df.columns.get_loc('text')
    print('\n******TOP TEN {}******'.format(describe_upper))
    print('\nProportion: \n\n{}'.format(df.iloc[:10, idx]))
    print('\nPost Type: \n\n{}'.format(df.iloc[:10, type_idx]))
    # print('\nDates and Times: \n\n{}'.format(df.iloc[:10, 4]))
    print('\nURLS: \n\n{}'.format(df.iloc[:10, URL_idx]))
    print('\nText: \n\n{}'.format(df.iloc[:10, text_idx]))

def make_2d_bar(df, save_as):
    type = pd.DataFrame(data=df, columns=['type','engaged_prop', 'clickers_prop', 'clicks_prop'])
    grouped=type.groupby(['type']).mean()
    sorted = grouped.sort_values(by=['engaged_prop'], ascending=False)
    #source: https://python-graph-gallery.com/8-add-confidence-interval-on-barplot/
    #width of the bars
    barWidth = .3
    # Choose the height of the blue bars
    bars1=sorted.iloc[:, 0]
    # Choose the height of the red bars
    bars2=sorted.iloc[:, 1]
    # Choose the height of the yellow bars
    bars3=sorted.iloc[:, 2]
    # The x position of bars
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    # Create blue bars
    plt.bar(r1, bars1, width = barWidth, color = '#4C72B0', edgecolor = 'black', label='Engaged')
    # Create red bars
    plt.bar(r2, bars2, width = barWidth, color = '#DD8452', edgecolor = 'black', label='Clickers')
    # Create yellow bars
    plt.bar(r3, bars3, width = barWidth, color = '#55A868', edgecolor = 'black', label='Clicks')
    # general layout
    plt.xticks([r + barWidth for r in range(len(bars1))], ['Shared Video', 'Video', 'Photo', 'Link', 'Status'])
    plt.ylabel('Mean Proportion', weight='bold')
    plt.legend()
    plt.xlabel('Post Type', weight='bold')
    plt.xticks(rotation=60, horizontalalignment='right')
    # plt.title('Average Proportion Engagement Activity by Post Type', weight='bold', fontsize=13)
    plt.tight_layout()
    # plt.show()
    plt.savefig(save_as)

if __name__=='__main__':
    '''Can only export 180 days of data at a time. Need to merge dfs.'''
    merge_csvs()
    merged = pd.read_csv('posts_merged.csv')
    '''Then clean up the dfs so they are easier to work with'''
    df = cleaning(merged)

    '''Creating a subset of data for this time last year (winter)'''
    df_winter = df.loc['2017-12':'2018-04']

    '''EDA'''
    #lists of variables to display in boxplots
    reach_impressions=['total_reach', 'total_imp', 'org_reach', 'org_imp', 'paid_reach', 'paid_imp']
    engage_click=['engaged', 'clicks', 'clickers']
    likes=['like_interest', 'like', 'like_interact_paid', 'like_paid', 'like_engage']
    vids=['vid_95', 'vid_95_paid', 'vid', 'vid_paid', 'vid_avg']
    post_story=['story_share', 'post_share', 'story_like', 'post_like', 'story_comment', 'post_comment']
    audience=['audience_clicks_other', 'audience_clicks_link', 'audience_photo', 'audience_video', 'email_clicks_other', 'email_clicks_link', 'email_clicks_photo', 'email_clicks_video']
    neg=['neg', 'neg_users', 'neg_users', 'neg_hide']
    prop_engage_click=['engaged_prop', 'clickers_prop', 'clicks_prop']

    '''Figure 1'''
    # boxplots(df_winter, reach_impressions, 'Count', 'FB_analytics/images/reach_imp_box.png')

    '''There is variability in engagement. Which posts receive most engagement?'''
    '''Figures 2a and 2b'''
    # boxplots(df_winter, engage_click, 'Count', 'FB_analytics/images/engage_click_box.png')
    # boxplots(df_winter, prop_engage_click, 'Proportion: Activity/Total Reach', 'FB_analytics/images/engage_click_prop_box.png')

    '''What type of post is most effective (Type variable)?'''
    '''Figure 3'''
    make_2d_bar(df_winter, 'FB_analytics/images/prop_bar.png')

    '''What are the top 10 posts in terms of engagement, clickers, and clicks?'''
    top_engaged = df_winter.sort_values(by=['engaged_prop'], ascending=False)
    top_clickers = df_winter.sort_values(by=['clickers_prop'], ascending=False)
    top_clicks = df_winter.sort_values(by=['clicks_prop'], ascending=False)

    # print(top_ten(top_engaged, 'ENGAGED', 'engaged_prop'))
    # print(top_ten(top_clickers, 'CLICKERS', 'clickers_prop'))
    # print(top_ten(top_clicks, 'CLICKS', 'clicks_prop'))

    '''What do we need to filter out in order to only be looking at actual advertisement posts'''
