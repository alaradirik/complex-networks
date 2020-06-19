import os
import pandas as pd


relations = pd.read_csv("data/RelationshipsFromSurveys.csv")


def update_relationships(df):
    for index, row in df.iterrows():
        mask = (df['id.A']==row['id.A']) & (df['id.B']==row['id.B'])
        methods = df.loc[mask, 'relationship'].tolist()

        if 'CloseFriend' in methods:
            df.loc[mask, 'social_status'] = 'CloseFriend'
        elif ('SocializeTwicePerWeek' or 'FacebookAllTaggedPhotos') in methods and 'CloseFriend' not in methods:
            df.loc[mask, 'social_status'] = 'Friend'
        else:
            df.loc[mask, 'social_status'] = 'Acquaintance'

    df.drop(columns=['relationship'], inplace=True)
    df.drop_duplicates(inplace=True) 

    return df

if __name__ == '__main__':
    frames = []
    for date in relations['survey.date'].unique():
        df = relations[relations['survey.date']==date]
        frames.append(update_relationships(df))

    result = pd.concat(frames)
    result.to_csv('output/relationships.csv')
