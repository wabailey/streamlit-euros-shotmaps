import streamlit as st
import pandas as pd
import json
from mplsoccer import VerticalPitch

st.set_page_config(
   page_title="UEFA Euro 2024 Shot Maps",
   page_icon="⚽",
)

st.title("UEFA Euro 2024 Player Shot Maps")
st.subheader('Filter by teams and players to view shots taken and goals scored.')
st.text('The larger the circle the higher the xG of the shot.')

df = pd.read_csv('euros_2024_shot_map.csv') # load the csv into a pandas dataframe

df = df[df['type'] == 'Shot'].reset_index(drop=True)
df['location'] = df['location'].apply(json.loads)

team = st.selectbox('Select a team', df['team'].sort_values(ascending=True).unique(), index=None)
player = st.selectbox('Select a player', df[df['team'] == team]['player'].sort_values().unique(), index=None)

def filter_data(df, team, player):
  if team:
    df = df[df['team'] == team]
  if player:
    df = df[df['player'] == player]

  return df

filtered_df = filter_data(df, team, player)

pitch = VerticalPitch(pitch_type='statsbomb', half=True)
fig, ax = pitch.draw(figsize=(10, 10))

def plot_shots(df, ax, pitch):
  for x in df.to_dict(orient='records'):
    pitch.scatter(
      x = float(x['location'][0]),
      y = float(x['location'][1]),
      ax = ax,
      s = 1000 * x['shot_statsbomb_xg'],
      color = 'red' if x['shot_outcome'] == 'Goal' else 'black',
      edgecolors = 'black',
      alpha = .8 if x['shot_outcome'] == 'Goal' else .4,
      zorder = 2 if x['shot_outcome'] == 'Goal' else 1
    )

plot_shots(filtered_df, ax, pitch)

st.pyplot(fig)