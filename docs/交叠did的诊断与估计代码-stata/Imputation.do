
//下载命令
ssc install did_imputation,replace
ssc install event_plot,replace
//生成冲击日期变量(同sadid:对照组为空)
gen aaa=year if DT==1
bys stkcd:egen action=min(aaa)
//核心命令
did_imputation Patent stkcd year action,allhorizons pretrends(14) autosample controls(Size Age Lev Capex Agdp Pop) fe(stkcd year) cluster(stkcd) tol(1) maxit(100)
//画图
event_plot, default_look graph_opt(xtitle("时期") ytitle("平均处理效应") title("Borusyak(2021)&Imputation&插补  估计量") xlabel(-14(1)5)) ciplottype(rcap) together

//总估计量
did_imputation Patent stkcd year action,autosample controls(Size Age Lev Capex Agdp Pop) fe(stkcd year) cluster(stkcd) tol(1) maxit(100)

//画图不想连线
event_plot, default_look graph_opt(xtitle("时期") ytitle("平均处理效应") title("Borusyak(2021)&Imputation&插补  估计量") xlabel(-5(1)5)) ciplottype(rcap) 

//估计前后3期
did_imputation Patent stkcd year action,horizons(0/5) pretrends(5) autosample controls(Size Age Lev Capex Agdp Pop) fe(stkcd year) cluster(stkcd) tol() maxit(100)


**如果出现下列报错，经过试验，把tol(  )括号里的数字调大
**Convergence of standard errors is not achieved for coefs: __w_tau0 __w_tau1 __w_tau2 __w_tau3 __w_tau4 __w_tau5.
**Try increasing the tolerance, the number of iterations, or use the nose option for the point estimates without SE.
**convergence not achieved
**r(430);


