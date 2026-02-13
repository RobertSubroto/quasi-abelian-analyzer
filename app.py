# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 2026
@author: Bobby Subroto
"""

import streamlit as st
from engine import GroupAlg  # Imports the logic from your engine.py

# --- STREAMLIT UI CONFIG ---
st.set_page_config(page_title="QA Code Analyzer", page_icon="🔬")

st.title("🧬 Quasi-Abelian Group Code Analyzer")
st.markdown("""
This tool computes the **Wedderburn decomposition** of group algebras $\mathbf{F}[G]$ for finite abelian groups $G$ and finite field $\mathbf{F}$. 
It determines the irreducible components and checks for semisimplicity, essential for analyzing **Quasi-Abelian (QA) codes**.
""")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Input Parameters")
p = st.sidebar.number_input("Characteristic (p)", min_value=2, value=2, step=1)
t = st.sidebar.number_input("Field Power (t)", min_value=1, value=1, step=1)
param_input = st.sidebar.text_input("Group Parameters (comma separated)", value="5, 5, 32")

try:
    # Convert input string to list of integers
    param_list = [int(x.strip()) for x in param_input.split(",")]
    
    # Run the engine
    algebra = GroupAlg(p, t, param_list)

    # --- METRICS OVERVIEW ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Dimension", algebra.dim)
    col2.metric("Complexity (η)", algebra.complexity)
    col3.metric("Semisimple", "Yes" if algebra.is_semisimple else "No")

    # Warnings for Non-Semisimple cases
    if not algebra.is_semisimple:
        st.warning("⚠️ **Non-Semisimple Algebra:** The Jacobson Radical is non-trivial.")
    else:
        st.success("✅ **Semisimple Algebra:** Maschke's condition is satisfied.")

    # --- TABLE OF DECOMPOSITION ---
    st.subheader("Wedderburn Decomposition")
    if algebra.components is not None:
        display_df = algebra.components.copy()
        
        # Clean representation: remove [1] if the algebra is semisimple
        def clean_repr(comp):
            repr_str = str(comp)
            if algebra.is_semisimple and repr_str.endswith("[1]"):
                return repr_str.replace("[1]", "")
            return repr_str

        display_df['Isomorphism Type'] = display_df['Component'].apply(clean_repr)
        
        # Display the table with selected columns
        st.table(display_df[['Isomorphism Type', 'Count']])
        
        # Dimension Check (Verification)
        check_sum = sum(row['Component'].dim * row['Count'] for _, row in algebra.components.iterrows())
        if check_sum == algebra.dim:
            st.info(f"Verification: Dimension sum matches original algebra ($D = {check_sum}$)")
    else:
        st.info("This algebra is local and cannot be decomposed further.")

except Exception as e:
    st.error(f"Input Error: Please ensure parameters are integers separated by commas. (Details: {e})")

# --- FOOTER ---
# --- FOOTER ---
st.markdown("---")
st.markdown(f"[🔗 Visit my Personal Website](https://robertsubroto.github.io/)")
st.caption("Developed by Robert Christian Subroto")