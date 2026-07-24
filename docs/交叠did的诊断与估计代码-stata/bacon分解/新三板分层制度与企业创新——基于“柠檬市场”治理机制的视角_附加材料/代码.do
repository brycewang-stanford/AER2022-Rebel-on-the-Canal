***************************************************************************
*** 新三板分层制度与企业创新——基于"柠檬市场"治理机制的视角
***************************************************************************
clear
cd 

**************************************
** 描述性统计 **
**************************************
use "neeq.dta",clear
logout, save("tabel1_sum") word replace: ///
tabstat neeq sumpat1 lnsumpat1  sumpatsale1 ln研发支出 研发支出总额占营业收入比例 ln营业收入 asset ln股东权益2015 资产负债率2015 净资产收益率ROE2015  ln董事会人数2015, s(n  mean  sd min p50  max) c(s) f(%9.3f)



**************************************
** 基准回归 **
**************************************

//创新产出
reghdfe lnsumpat1 neeq ln营业收入 asset, absorb(year code) vce(cluster code)
est store x1

reghdfe lnsumpat1 neeq ln营业收入  asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code) vce(cluster code) 
est store x2

reghdfe lnsumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code) 
est store x3


//创新投入
reghdfe ln研发支出 neeq ln营业收入 asset , absorb(year code  ) vce(cluster code) 
est store x4

reghdfe ln研发支出 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code  ) vce(cluster code) 
est store x5

reghdfe ln研发支出 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code) 
est store x6

esttab x1 x2 x3 x4 x5 x6 using "基准回归结果.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order(neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015)  se b(%7.3f) t(%7.3f)title("基准回归结果")



**************************************
** 平行趋势 **
**************************************

** 企业创新产出

use "图1左.dta",clear

twoway (connected b event, sort lcolor(black) mcolor(black) ///
msymbol(circle_hollow) cmissing(n))(rcap LB UB event, lcolor(black)lpattern(dash) ///
msize(medium)),ytitle(Percentage change) ///
ytitle(, size(small))  yline(0, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(, labsize(small) angle(horizontal) nogrid) ///
xtitle(Years relative to branch deregulation) ///
xtitle(, size(small)) xline(-1, lwidth(vthin) lpattern(dash) lcolor(teal))  ///
xlabel(-3(1)5, labsize(small))  xmtick(-2(1)2, nolabels ticks) ///
legend(off)graphregion(fcolor(white) lcolor(white) ifcolor(white) ilcolor(white))


** 企业创新投入
use "图1右.dta",clear

twoway (connected b event, sort lcolor(black) mcolor(black) ///
msymbol(circle_hollow) cmissing(n))(rcap LB UB event, lcolor(black)lpattern(dash) ///
msize(medium)),ytitle(Percentage change) ///
ytitle(, size(small))  yline(0, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(, labsize(small) angle(horizontal) nogrid) ///
xtitle(Years relative to branch deregulation) ///
xtitle(, size(small)) xline(-1, lwidth(vthin) lpattern(dash) lcolor(teal))  ///
xlabel(-3(1)5, labsize(small))  xmtick(-2(1)2, nolabels ticks) ///
legend(off)graphregion(fcolor(white) lcolor(white) ifcolor(white) ilcolor(white))




**************************************
** 排除政策制定标准带来的选择效应 **
**************************************

** A股主板为对照组 **

use "附表4.dta",clear

//回归结果——创新产出
reghdfe lnsumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if _weight!=., absorb(year code year code i.incode#c.year i.xcode#c.year) vce(cluster code) 
 est store x1

reghdfe sumpatsale1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if _weight!=., absorb(year code i.incode#c.year i.xcode#c.year) vce(cluster code) 
est store x2

//回归结果——创新投入
reghdfe ln研发支出 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if _weight!=., absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code) 
est store x3

reghdfe 研发支出总额占营业收入比例 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if _weight!=., absorb(year code  i.incode#c.year i.xcode#c.year ) vce(cluster code) 
est store x4


esttab x1 x2 x3 x4 using "A股主板为对照组的PSM-DID结果.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order(neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 ) se b(%7.3f) t(%7.3f) title("A股主板为对照组的PSM-DID结果")


//平行趋势检验
use "附图1左.dta",clear

twoway (connected b event, sort lcolor(black) mcolor(black) ///
msymbol(circle_hollow) cmissing(n))(rcap LB UB event, lcolor(black)lpattern(dash) ///
msize(medium)),ytitle(Percentage change) ///
ytitle(, size(small))  yline(0, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(, labsize(small) angle(horizontal) nogrid) ///
xtitle(Years relative to branch deregulation) ///
xtitle(, size(small)) xline(-1, lwidth(vthin) lpattern(dash) lcolor(teal))  ///
xlabel(-3(1)5, labsize(small))  xmtick(-2(1)2, nolabels ticks) ///
legend(off)graphregion(fcolor(white) lcolor(white) ifcolor(white) ilcolor(white))



//平行趋势_创新投入
use "附图1右.dta",clear
twoway (connected b event, sort lcolor(black) mcolor(black) ///
msymbol(circle_hollow) cmissing(n))(rcap LB UB event, lcolor(black)lpattern(dash) ///
msize(medium)),ytitle(Percentage change) ///
ytitle(, size(small))  yline(0, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(, labsize(small) angle(horizontal) nogrid) ///
xtitle(Years relative to branch deregulation) ///
xtitle(, size(small)) xline(-1, lwidth(vthin) lpattern(dash) lcolor(teal))  ///
xlabel(-3(1)5, labsize(small))  xmtick(-2(1)2, nolabels ticks) ///
legend(off)graphregion(fcolor(white) lcolor(white) ifcolor(white) ilcolor(white))

**************************************
** 稳健性检验 **
**************************************

** 预期效应检验 

use "neeq.dta",clear

gen policy=year-创新层挂牌日year
replace policy=. if 创新层挂牌日year==2022

tab policy
forvalues i = 8(-1)1{
  gen pre_`i' = (policy == -`i') 
}

g prene=pre_1*ne

reghdfe lnsumpat1 prene neeq  ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 , absorb(year code i.incode#c.year i.xcode#i.year) vce(cluster code)
est store x1

reghdfe ln研发支出 prene neeq  ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 , absorb(year code i.incode#i.year i.xcode#i.year ) vce(cluster code)
est store x2

esttab x1 x2 using "排除预期效应的干扰.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order( prene neeq  ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 ) se b(%7.3f) t(%7.3f) title("排除预期效应的干扰")


** 安慰剂检验 Monte Carlo 

use  "monte.dta" , clear
#delimit ;
dpplot beta, xline(0.11, lc(black*0.5) lp(dash))
             xline(0, lc(black*0.5) lp(solid))
             xtitle("虚假系数估计值", size(*0.8)) 
             xlabel(-0.08(0.02)0.15, format(%7.2f) labsize(small))
             ytitle("密度分布", size(*0.8)) 
             ylabel(, nogrid format(%4.1f) labsize(small)) 
             note("") caption("") 
             graphregion(fcolor(white)) ;
#delimit cr
graph save "Graph" "mento.gph",replace


** 贝肯分析

use "neeq.dta",clear

//bacondecomp 分解结果
ddtiming lnsumpat1 neeq,i(code) t(year)


** possion回归负二项回归结果

use "neeq.dta",clear

ppmlhdfe sumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 , absorb(year code i.incode#i.year i.xcode#i.year ) vce(cluster code) 

nbreg  sumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 i.year i.code, vce(cluster code)



**更换被解释变量

use "neeq.dta",clear

reghdfe sumpatsale1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year) vce(cluster code) 
est store x1

reghdfe 研发支出总额占营业收入比例 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year) vce(cluster code) 
est store x2

esttab x1 x2 using "更换被解释变量.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order(neeq  ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 ) se b(%7.3f) t(%7.3f) title("更换被解释变量")


**************************************
** 机制分析 **
**************************************

**创新层流动性 **

use "表2_1.dta",clear


reghdfe 交易天数1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x1

reghdfe ln成交量 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x2

reghdfe ln成交金额 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x3

esttab x1 x2 x3  using "创新层流动性检验1.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order( neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015) se b(%7.3f) t(%7.3f) title("创新层流动性检验1'")

use "表2_2.dta",clear

reghdfe lnamihud1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x1

esttab x1  using "创新层流动性检验2股票流动性.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order( neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015) se b(%7.3f) t(%7.3f) title("创新层流动性检验2股票流动性'")



//平行趋势图机制检验

use "附图4左.dta",clear
twoway (connected b event, sort lcolor(black) mcolor(black) ///
msymbol(circle_hollow) cmissing(n))(rcap LB UB event, lcolor(black)lpattern(dash) ///
msize(medium)),ytitle(Percentage change) ///
ytitle(, size(small))  yline(0, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(, labsize(small) angle(horizontal) nogrid) ///
xtitle(Years relative to branch deregulation) ///
xtitle(, size(small)) xline(-1, lwidth(vthin) lpattern(dash) lcolor(teal))  ///
xlabel(-3(1)5, labsize(small))  xmtick(-2(1)2, nolabels ticks) ///
legend(off)graphregion(fcolor(white) lcolor(white) ifcolor(white) ilcolor(white))


use "附图4右.dta",clear
twoway (connected b event, sort lcolor(black) mcolor(black) ///
msymbol(circle_hollow) cmissing(n))(rcap LB UB event, lcolor(black)lpattern(dash) ///
msize(medium)),ytitle(Percentage change) ///
ytitle(, size(small))  yline(0, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(, labsize(small) angle(horizontal) nogrid) ///
xtitle(Years relative to branch deregulation) ///
xtitle(, size(small)) xline(-1, lwidth(vthin) lpattern(dash) lcolor(teal))  ///
xlabel(-3(1)5, labsize(small))  xmtick(-2(1)2, nolabels ticks) ///
legend(off)graphregion(fcolor(white) lcolor(white) ifcolor(white) ilcolor(white))

**融资约束检验 **
use "表3.dta" ,clear


reghdfe fc neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x1

reghdfe lnsumpat1 fc ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code) 
est store x2

reghdfe lnsumpat1 fc neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x3


esttab  x1 x2 x3  using "机制检验融资约束.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order(neeq fc ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 ) se b(%7.3f) t(%7.3f) title("机制检验融资约束")


**************************************
** 异质性检验 **
**************************************

//机构持股比例
use "表4.dta",clear
reghdfe lnsumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if x1==1, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x1

reghdfe sumpatsale1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if x1==1, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x2

reghdfe lnsumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if x1==0, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x3

reghdfe sumpatsale1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if x1==0, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x4

esttab x1 x2 x3  x4  using "异质性_机构持股比例回归结果.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order(neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015) se b(%7.3f) t(%7.3f) title("异质性_机构持股比例回归结果")


//定向增发
use "neeq.dta",clear

reghdfe lnsumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if 增发==1, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x1

reghdfe sumpatsale1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if 增发==1, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x2

reghdfe lnsumpat1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if 增发==0, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x3


reghdfe sumpatsale1 neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015 if 增发==0, absorb(year code i.incode#c.year i.xcode#c.year ) vce(cluster code)
est store x4


esttab x1 x2 x3  x4 using "异质性_定向增发.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order( neeq ln营业收入 asset ln股东权益2015_post2015 资产负债率2015_post2015 净资产收益率ROE2015_post2015 ln董事会人数2015_post2015) se b(%7.3f) t(%7.3f) title("异质性_定向增发")

**************************************
** 进一步分析 **
**************************************

use "表6.dta",clear

reghdfe lnsumpat1 did ln营业收入  净资产收益率ROE ln股东权益 资产负债率 asset ,absorb(year code ) vce(cluster code) 
est store x1
reghdfe sumpatsale1 did ln营业收入  净资产收益率ROE ln股东权益 资产负债率 asset  ,absorb(year code ) vce(cluster code) 
est store x2
reghdfe ln研发支出 did ln营业收入  净资产收益率ROE ln股东权益  资产负债率 asset  ,absorb(year code ) vce(cluster code) 
est store x3
reghdfe 研发支出总额占营业收入比例 did ln营业收入  净资产收益率ROE ln股东权益 资产负债率  asset  ,absorb(year code ) vce(cluster code) 
est store x4
esttab x1 x2 x3  x4  using "北交所企业创新水平.rtf", replace star( * 0.10 ** 0.05 *** 0.01 ) ///
staraux r2 nogaps order(did ln营业收入  asset  净资产收益率ROE ln股东权益 资产负债率   ) se b(%7.3f) t(%7.3f)  title("北交所企业创新水平")
