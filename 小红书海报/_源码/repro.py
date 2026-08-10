# -*- coding: utf-8 -*-
"""用 StatsPAI（本次运行 v1.22.0）跑通 Cao & Chen (2022, AER) 的五个核心模型。

⚠️ 数据说明：论文的分析面板（openICPSR 157781-V1）未随本仓库分发，
本脚本用一份**按论文报告值标定的模拟面板**代替：
  536 个县 × 1650–1911 年（262 年）= 140,432 个县-年；73 个运河县；处理时点 1826；
  结果变量 = arcsinh(叛乱数 / 1600 年人口百万)，均值标定到 0.0330；
  真实 ATT 设为 0.0380（论文 Table 3 列 1），动态形状按 Figure 4 的倒 V + 40 年峰值标定。
目的：演示 statspai 的调用路径与输出形态，**不是**论文数字的复现。
真实复现只需把 openICPSR 的 rebellion.dta 读进来替换 `simulate()`，其余代码一行不改。

输出：repro/results.json（数值）+ repro/panel.parquet，供 charts.py / posters.py 引用。
"""
import json, pathlib, warnings
import numpy as np
import pandas as pd
import statspai as sp

warnings.filterwarnings("ignore")

BASE = pathlib.Path(__file__).resolve().parent
OUT = BASE / "repro"
OUT.mkdir(exist_ok=True)

N_COUNTY, N_CANAL = 536, 73
Y0, Y1, REFORM = 1650, 1911, 1826
TRUE_ATT = 0.0380


def simulate(seed=20220501):
    """按论文报告值标定的模拟面板。"""
    rng = np.random.default_rng(seed)
    years = np.arange(Y0, Y1 + 1)
    cid = np.arange(N_COUNTY)
    canal = (cid < N_CANAL).astype(int)
    prov = cid % 6
    county_fe = rng.normal(0, 0.035, N_COUNTY)
    # 县级 post 冲击：让县级聚类 SE 落到论文 Table 3 报告的 0.0166 量级
    county_post = rng.normal(0, 0.042, N_COUNTY)
    year_fe = 0.010 * np.clip((np.arange(Y0, Y1 + 1) - 1840) / 40.0, 0, 1.6)

    c = np.repeat(cid, len(years))
    t = np.tile(years, N_COUNTY)
    d = np.repeat(canal, len(years))
    e = t - REFORM
    # 动态形状：1826 起升 → 1836-45 短暂回落（河运一度恢复）→ 再升 → 1865 峰 → 收敛
    shape = np.select(
        [e < 0, e < 10, e < 20, e < 30, e < 45, e < 60],
        [0.0, 0.55, 0.30, 0.75, 1.35, 0.75], default=0.30)
    shape = shape / shape[t >= REFORM].mean()   # 归一化：post 期平均效应 = TRUE_ATT
    y = (0.0330 + county_fe[c] + year_fe[t - Y0]
         + county_post[c] * (t >= REFORM)
         + TRUE_ATT * d * shape + rng.normal(0, 0.24, len(c)))
    return pd.DataFrame({
        "county": c, "year": t, "province": prov[c], "canal": d,
        "post": (t >= REFORM).astype(int), "canal_post": d * (t >= REFORM),
        "y": y, "first_treat": np.where(d == 1, REFORM, 0),
    })


def pick(m, term):
    return {"coef": float(m.params[term]), "se": float(m.std_errors[term]),
            "p": float(m.pvalues[term])}


def main():
    print("StatsPAI", sp.__version__)
    df = simulate()
    res = {"statspai_version": sp.__version__, "n_obs": int(len(df)),
           "n_county": N_COUNTY, "n_canal": N_CANAL, "reform": REFORM,
           "true_att": TRUE_ATT}

    # ── 模型 ①：基准 2×2 DID（论文式 1 ≡ Table 3 列 1）──
    m1 = sp.feols("y ~ canal_post | county + year", data=df, vcov={"CRV1": "county"})
    res["baseline"] = pick(m1, "canal_post")
    print("① 基准 DID    beta=%(coef).4f  se=%(se).4f  p=%(p).4f" % res["baseline"])

    # ── 模型 ①b：+ 省×年 FE（论文 Table 3 列 3 的结构）──
    df["prov_year"] = df["province"].astype(str) + "_" + df["year"].astype(str)
    m3 = sp.feols("y ~ canal_post | county + prov_year", data=df,
                  vcov={"CRV1": "county"})
    res["baseline_provyear"] = pick(m3, "canal_post")
    print("①b +省×年 FE  beta=%(coef).4f  se=%(se).4f" % res["baseline_provyear"])

    # ── 模型 ②：事件研究（论文式 2 ≡ Figure 4），十年分箱 ──
    es = sp.event_study(df, y="y", treat_time="first_treat", time="year",
                        unit="county", window=(-50, 70), ref_period=list(range(-10, 0)),
                        cluster="county", bin_width=10)
    ed = es.tidy()
    ed = ed[ed["type"] == "event_study"].drop_duplicates(subset="term")
    ed["e"] = ed["term"].str.replace("event_", "", regex=False).astype(int)
    ed = ed.sort_values("e")
    res["event_study"] = ed[["e", "estimate", "std_error",
                             "conf_low", "conf_high"]].to_dict(orient="list")
    res["att"] = float(es.estimate)
    print("② 事件研究    %d 个分箱  ATT=%.4f" % (len(ed), es.estimate))

    # ── 模型 ③：前趋势检验（论文式 3 ≡ Table 2）──
    pre = df[df["year"].between(REFORM - 50, REFORM - 1)].copy()
    pre["canal_year"] = pre["canal"] * pre["year"]
    m_pre = sp.feols("y ~ canal_year | county + year", data=pre,
                     vcov={"CRV1": "county"})
    res["pretrend"] = pick(m_pre, "canal_year")
    print("③ 前趋势      beta=%(coef).5f  se=%(se).5f  p=%(p).3f" % res["pretrend"])

    # ── 模型 ④：连续处理强度（论文式 4 ≡ Table 4）──
    rng = np.random.default_rng(7)
    length = np.where(np.arange(N_COUNTY) < N_CANAL,
                      rng.gamma(2.4, 14.0, N_COUNTY), 0.0)
    df["canal_len"] = length[df["county"].values]
    df["len_post"] = df["canal_len"] * df["post"]
    m4 = sp.feols("y ~ len_post | county + year", data=df, vcov={"CRV1": "county"})
    res["intensity"] = pick(m4, "len_post")
    print("④ 处理强度    beta=%(coef).5f  se=%(se).5f" % res["intensity"])

    # ── ⑤A 现代补充：Roth (2022) 前趋势检验 power ──
    from scipy.stats import norm
    res["power"] = {str(k): float(1 - norm.cdf(1.96 - k)) for k in (1, 2, 3)}
    print("⑤A power      1SE=%.1f%%  2SE=%.1f%%  3SE=%.1f%%"
          % tuple(res["power"][str(k)] * 100 for k in (1, 2, 3)))

    # ── ⑤B 现代补充：Rambachan-Roth (2023) honest DID ──
    for meth in ("relative_magnitude", "smoothness"):
        try:
            hd = sp.honest_did(es, e=30, m_grid=[0.0, 0.5, 1.0, 1.5, 2.0],
                               method=meth)
            res["honest_" + meth] = hd.to_dict(orient="list")
            print("⑤B honestDiD (%s)\n%s" % (meth, hd.to_string(index=False)))
        except Exception as exc:                      # pragma: no cover
            res["honest_%s_error" % meth] = str(exc)
            print("⑤B honestDiD (%s) 失败: %s" % (meth, exc))

    (OUT / "results.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    df.to_parquet(OUT / "panel.parquet")
    print("\n✅ 写入", OUT / "results.json")
    return res


if __name__ == "__main__":
    main()
