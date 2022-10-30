import streamlit as st
import pandas as pd
import numpy as np
import pickle

from bs4 import BeautifulSoup

with open("dedup-test.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

if 'count' not in st.session_state:
	st.session_state.count = 1

def increment_counter():
	st.session_state.count += 1


all_imgs = [i['src'] for i in soup.find_all('img')]


img_num = st.sidebar.text_input('Sample Nr', f'{st.session_state.count}')
img_num = int(img_num) - 1


st.image(all_imgs[img_num * 13], width=150, caption=f"Sample Nr: {img_num + 1}")

checkboxes = [st.sidebar.checkbox(label=f'{i}') for i in range(12)]

st.text("Similar images")
st.image(all_imgs[img_num * 13 + 1: img_num * 13 + 13], width=150, caption=[str(i) for i in range(12)])

save = st.sidebar.button('Save')
if save:
    with open(f"label_res_dict.pkl", "rb") as f:
        label_res_dict = pickle.load(f)
    f.close()

    label_res_dict[img_num + 1] = [int(i) for i in checkboxes]

    print(label_res_dict)
with open(f"label_res_dict.pkl", "wb") as f:
    pickle.dump(label_res_dict, f, pickle.HIGHEST_PROTOCOL)
    f.close()

st.sidebar.button('Next', on_click=increment_counter)