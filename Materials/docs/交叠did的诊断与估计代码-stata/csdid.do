//下载
ssc install csdid,replace
ssc install drdid,replace
ssc install event_plot,replace
//生成冲击年份
bys stkcd:gen aaa=sum(DID)
gen actionyear = year if aaa==1
bys stkcd:egen Action=min(actionyear)
replace Action=0 if Action==.
//生成冲击年份(快速版）
egen Action=csgvar(DT),tvar( year) ivar( stkcd)
//跑数据
csdid Patent Size Age Lev Capex Agdp, time(year) gvar( Action) ivar( stkcd) notyet

estat simple
estat calendar
estat group
estat event
csdid_plot,style(rcap) scale(1.0) xtitle("时期") ytitle("平均处理效应") title("CS估计量")

//拓展
estat event, window(-4,4)
estat all
