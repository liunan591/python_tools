# -*- coding: utf-8 -*-

import pandas as pd

def merage_table(fa,fb,ka,kb,patten):
    fa_df = pd.read_excel(fa)
    fb_df = pd.read_excel(fb)
    out_complete = pd.merge(fa_df,fb_df,how=patten,left_on=ka,right_on=kb)
    return out_complete

def merage_table_column(fa,fb,ka,kb,ob,patten):
    fa_df = pd.read_excel(fa)
    fb_df = pd.read_excel(fb)
    fb_df = fb_df[[kb,ob]]
    out_complete = pd.merge(fa_df,fb_df,how=patten,left_on=ka,right_on=kb)
    return out_complete





if __name__ == "__main__":
    fa = "遗漏的备件.xlsx"
    fb = "2018年10月份备件库盘点表 - .xls1111.xls"
    fa_df = pd.read_excel(fa)
    fb_df = pd.read_excel(fb)
    fb_df = fb_df[["封装规格","物料名称"]]
    out_complete = pd.merge(fa_df,fb_df,how="left",left_on="品号",right_on="封装规格")
    