//下载命令eventstudyinteract
ssc install eventstudyinteract,replace

//生成队列变量（重点：对照组为空）
gen aaa=year if DT==1
bys stkcd:egen action=min(aaa)
//生成控制队列变量
gen never=(action==.)
//生成平行趋势的时期虚拟变量
gen pd=year-action
forvalues i = 14(-1)1{
	gen pre_`i'=(pd==-`i')
}
gen current =(pd==0)
forvalues j = 1(1)5{
	gen las_`j'=(pd==`j')
}
//sadid
eventstudyinteract Patent pre_14 pre_13 pre_12 pre_11 pre_10 pre_9 pre_8 pre_7 pre_6 pre_5 pre_4 pre_3 pre_2 current las_1 las_2 las_3 las_4 las_5 pre_1,cohort(action) control_cohort(never) covariates(Size Age Lev Capex Agdp Pop) absorb(i.stkcd i.year) vce(cluster stkcd)
matrix b = e(b_iw)
matrix V = e(V_iw)
ereturn post b V
coefplot,baselevels omitted keep(pre* current las*) vertical recast(connect) color(black) order(pre_14 pre_13 pre_12 pre_11 pre_10 pre_9 pre_8 pre_7 pre_6 pre_5 pre_4 pre_3 pre_2 pre_1 current las_1 las_2 las_3 las_4 las_5) yline(0,lp(solid) lc(black)) xline(15,lp(dash) lc(black)) xtitle("时期") ytitle("平均处理效应") title("SA估计量")  ciopts(recast(rcap) lc(black) lp(dash) lw(thin)) scale(1.0)


//算ATT（系数+显著性）
lincom(current +las_1+ las_2 +las_3+ las_4+ las_5)/6


//特殊情况
drop if action==.
gen lastnever=(action==2018)
eventstudyinteract Patent pre_14 pre_13 pre_12 pre_11 pre_10 pre_9 pre_8 pre_7 pre_6 pre_5 pre_4 pre_3 pre_2 current las_1 las_2 las_3 las_4 las_5 pre_1 if action<2018,cohort(action) control_cohort(lastnever) covariates(Size Age Lev Capex Agdp Pop) absorb(i.stkcd i.year) vce(cluster stkcd)








