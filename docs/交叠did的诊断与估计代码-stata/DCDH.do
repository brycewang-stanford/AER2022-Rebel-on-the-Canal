clear
use "G:\双重差分\多期did\交叠DID\技术转移与企业高质量创新数据\非平衡面板数据.dta" 

bys stkcd:gen aaa=sum(DT)
gen actionyear = year if aaa==1
bys stkcd:egen Action=min(actionyear)
replace Action=0 if Action==.
gen pd=year-Action
replace pd=. if pd>2000
tab pd
//命令安装
ssc install twowayfeweights,replace
ssc install did_multiplegt,replace
//算权重
twowayfeweights Patent stkcd year DT,type(feTR) controls(Size Age Lev Capex Agdp Pop)
//算估计量(缺点：横坐标标错)
did_multiplegt_dyn Patent stkcd year DT,effects(6) placebo(6) controls(Size Age Lev Capex Agdp Pop) cluster(stkcd)


//大小关系：假设当期+事后一共p期，n<=m<=p
did_multiplegt_dyn Patent stkcd year DT,effects(m) placebo(n)  controls(Size Age Lev Capex Agdp Pop) cluster( stkcd)

event_plot e(estimates)#e(variances), default_look graph_opt(xtitle("时期") ytitle("平均处理效应") title("De Chaisemartin and d'Haultfoeuille(2020)估计量") xlabel(-6(1)6))  stub_lag(Effect_#) stub_lead(Placebo_#)  ciplottype(rcap)  together

//算估计量(缺点：计算时间长)
did_multiplegt Patent stkcd year DT,robust_dynamic dynamic(5) placebo(5) controls(Size Age Lev Capex Agdp Pop) cluster(stkcd)