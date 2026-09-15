//下载命令
ssc install panelview,replace
ssc install xtdidregress,replace
ssc install bacondecomp,replace
//查看plus文件夹路径
sysdir
//改名（个人习惯）
rename DT DID

//查看数据
panelview Patent DID Size Age Lev Capex Agdp Pop, i(stkcd) t(year) type(treat) xtitle("年份") ytitle("个体") title("处理状况") leavegap theme(bw)

panelview Patent DID Size Age Lev Capex Agdp Pop if stkcd>=1 & stkcd<=10, i(stkcd) t(year) type(treat) xtitle("年份") ytitle("个体") title("处理状况") leavegap theme(bw)


//基准估计
reghdfe Patent DID Size Age Lev Capex Agdp Pop,a(year stkcd) cluster(stkcd)
//出现问题（不平衡）
bacondecomp Patent DID,ddetail
//平衡
xtbalance,range(2003 2018)

***第一种(加不加vce(cluster stkcd) 结果不变)
//基准估计
reghdfe Patent DID Size Age Lev Capex Agdp Pop,a(year stkcd) vce(cluster stkcd)

//bacon分解
ddtiming Patent DT,i(stkcd) t(year)

***第二种
xtdidregress (Patent) (DID), group(stkcd) time(year) vce(cluster stkcd)
estat bdecomp

***第三种
bacondecomp Patent DID,ddetail


***加入控制变量
//1
xtdidregress (Patent Size Age Lev Capex Agdp Pop) (DID), group(stkcd) time(year) vce(cluster stkcd)
estat bdecomp

//2
bacondecomp Patent DID Size Age Lev Capex Agdp Pop



