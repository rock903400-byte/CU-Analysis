import pandas as pd
import streamlit as st

from data.utils import format_large_number
from services.finance_service import calc_yoy_pct


def render_kpi_cards(annual_agg: pd.DataFrame, prev_agg: pd.DataFrame | None):
    """頂部 KPI 卡片：總收入 / 總支出 / 本期損益（含 YoY delta）"""
    income  = annual_agg[annual_agg["會計科目"].str.match(r"^4")]["當月金額"].sum()
    expense = annual_agg[annual_agg["會計科目"].str.match(r"^5")]["當月金額"].sum()
    profit  = income - expense

    def yoy_delta(curr, prev_df, pattern):
        if prev_df is None or prev_df.empty:
            return None
        prev = prev_df[prev_df["會計科目"].str.match(pattern)]["當月金額"].sum()
        pct = calc_yoy_pct(curr, prev)
        return f"{pct:.1%}" if pct is not None else None

    c1, c2, c3 = st.columns(3)
    c1.metric("💵 年度總收入（新台幣）", format_large_number(income),  yoy_delta(income,  prev_agg, r"^4"))
    c2.metric("💸 年度總支出（新台幣）", format_large_number(expense), yoy_delta(expense, prev_agg, r"^5"))
    c3.metric("📊 本期損益（新台幣）",   format_large_number(profit),  yoy_delta(profit,  prev_agg, r"^4"))
