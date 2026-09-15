clear all
set more off
set rmsg on

cap mkdir "Data/Interim"
cap mkdir "Data/Final"
cap mkdir "Results/Figures"
cap mkdir "Results/Tables"


*****************************************************************
*** Step 1: Creat the Panel with geographic and rebel Information
*****************************************************************
shp2dta using "Data/Raw/V4wgs84/samplemap", database("Data/Interim/samplemap_d") coordinates("Data/Interim/samplemap_c") replace 

import excel using "Data/Raw/Geo_raw.xlsx", firstrow clear // Created in ArcGIS
keep OBJECTID NAME_PY LEV1_PY LEV2_PY X_COORD Y_COORD NEAR_FID NEAR_DIST NEAR_ANGLE
gen location=1 if NEAR_ANGLE>-90 & NEAR_ANGLE<90
replace location=-1 if NEAR_ANGLE<-90 | (NEAR_ANGLE>90 & NEAR_ANGLE<180)
drop if NEAR_FID==-1
gen T1=1 if NEAR_DIST==0
replace T1=0 if T1==.
expand 262
bysort OBJECTID: gen year=_n+1649
save "Data/Interim/geo_panel.dta", replace

merge 1:1 OBJECTID year using "Data/Raw/rawrebellion.dta"
drop _merge 

save "Data/Interim/temppanel1.dta", replace 


*****************************************************************
*** Step 2: Add the first set of geographic variables
*****************************************************************
*** Coast
import excel using "Data/Raw/coast.xlsx", firstrow clear
keep OBJECTID NEAR_DIST
rename NEAR_DIST distance_coast
replace distance_coast=distance_coast/1000
save "Data/Interim/coast.dta", replace
*** Huang He
import excel using "Data/Raw/ToHuang.xlsx", firstrow clear
keep OBJECTID NEAR_DIST NEAR_ANGLE
rename NEAR_DIST distance_huang
rename NEAR_ANGLE angle_huang
replace distance_huang=distance_huang/1000
gen alonghuang=1 if distance_huang==0
replace alonghuang=0 if distance_huang>0
save "Data/Interim/huang.dta", replace
*** Yangtze River
import excel using "Data/Raw/ToYangtze.xlsx", firstrow clear
keep OBJECTID NEAR_DIST
rename NEAR_DIST distance_yangtze
replace distance_yangtze=distance_yangtze/1000
gen alongyangtze=1 if distance_yangtze==0
replace alongyangtze=0 if distance_yangtze>0
save "Data/Interim/yangtze.dta", replace

*** Put together everything
use "Data/Interim/temppanel1.dta", clear
//(2) Coast
merge m:1 OBJECTID using "Data/Interim/coast.dta"
drop if _merge<3
drop _merge
//(3) Huanghe
merge m:1 OBJECTID using "Data/Interim/huang.dta"
drop if _merge<3
drop _merge
//(4) Yangtze River
merge m:1 OBJECTID using "Data/Interim/yangtze.dta"
drop if _merge<3
drop _merge
//(5) Save
save "Data/Interim/temppanel2.dta", replace 


*****************************************************************
*** Step 3: Define basic variables
*****************************************************************
use "Data/Interim/temppanel2.dta", clear

***Dependent variables
rename upspring onset_all
gen onset_any=onset_all
replace onset_any=1 if onset_all>0
*** Treatment Variables
gen alongcanal=1 if NEAR_DIST==0
replace alongcanal=0 if NEAR_DIST>0
gen distance_canal=NEAR_DIST/1000
drop NEAR_DIST
gen alongcoast=(distance_coast==0)

*** Time Treatment
gen reform = (year>1825)
gen interaction1=alongcanal*reform
gen interaction2=distance_canal*reform
*** Time Period
gen period=ceil((year-1825)/20)*20
replace period=1000 if period<-100
tab period, gen(period)
drop period12
*** Other Variables
egen distance_toriver=rowmin(distance_huang distance_yangtze)
egen alongriver=rowmax(alonghuang alongyangtze)
*** Prefectual id and Province id
encode LEV1_PY, gen(provid)
encode LEV2_PY, gen(prefid)
bysort prefid: egen prefalong=max(alongcanal)
*** Order and Label
label variable year  "Year"
label variable reform "After Year 1825"
label variable alongcanal "Being Along the Grand Canal"
label variable alongcoast "Being Along the Coast"
label variable prefalong "Prefectures along the Grand Canal"
label variable distance_coast "Distance from the Coast (km)"
label variable distance_huang "Distance from Huang River (km)"
label variable distance_yangtze "Distance from Yangtze River (km)"
label variable distance_canal "Distance from the Grand Canal (km)"
label variable distance_toriver "The Minimum Distance from Huang/Yangtze River (km)"
label variable onset_all "Number of Onset"
label variable onset_any "Onset Dummy"
label variable attack "Number of Military Attack"
label variable defend "Number of Military Suppress"
label variable stay "Number of Rebellions Already Exist"
label variable runinto "Number of Rebels Running into"
label variable interaction1 "Along Canal $\times$ After Abolishment"
label variable interaction2 "Distance to Canal $\times$ After Abolishment"
label variable NAME_PY "Name of Counties"
label variable LEV1_PY "Name of Provinces"
label variable LEV2_PY "Name of Profectures"
label variable alonghuang "Along Huang River"
label variable alongyangtze "Along Yangtze River"
label variable alongriver "Along Huang/Yangtze River"
label variable prefid "ID of Prefectures"
label variable provid "ID of Provinces"
label variable OBJECTID "ID of Counties"
order OBJECTID year onset* interaction* reform along* distance* attack defend stay runinto 
save "Data/Interim/rebellion_temp1.dta", replace


*****************************************************************
*** Step 4: Prepare the additional variables to add
*****************************************************************
*** Ruggedness
run "Program/Clean/clean_ruggedness.do"  // Output saved as "Data/Interim/ruggedness.dta"

*** Courier Route
clear
import delimited using "Data/Raw/nearcourier.txt", clear
keep in_fid near_dist
rename in_fid OBJECTID
rename near_dist distance_courier
gen alongcourier=(distance_courier==0)
label variable alongcourier "Along the Qing Courier Routes"
label variable distance_courier "Distance to the Qing Courier Routes"
save "Data/Interim/distcourier.dta", replace

*** Taiping
import excel using "Data/Raw/taipingregion.xlsx", firstrow clear
rename OBJECTID Shpid
keep Shpid Taiping
label variable Taiping "Taiping Heavenly Kingdom Severity"
save "Data/Interim/taiping.dta", replace

*** Military
import excel using "Data/Raw/Soldier_all.xlsx", firstrow clear
drop if OBJECTID==.
collapse (sum) soldier, by(OBJECTID)
save "Data/Interim/soldier.dta", replace

*** Crop and Suitability
shp2dta using "Data/Raw/suitability/joinwheat", database("Data/Interim/wheat_d") coordinates("Data/Interim/wheat_c") replace 
use "Data/Interim/wheat_d.dta", clear
keep OBJECTID Avg_grid_c _ID
rename Avg_grid_c si_wheat
gen suitable_wheat_good=(si_wheat>=5500)
label variable OBJECTID "Countycode"
label variable si_wheat "Suitability Index for Wheat (Irrigation, M Input)"
label variable suitable_wheat_good "Good or Better (SI>=5500) for Wheat (Irrigation, M Input)"
save "Data/Interim/wheat_suitability.dta", replace

import delimited using "Data/Raw/suitability/wlrice.txt", clear
keep objectid avg_grid_code objectid_12
rename objectid OBJECTID
rename avg_grid_code si_rice
rename objectid_12 _ID
gen suitable_rice_good=(si_rice>=5500)
label variable OBJECTID "Countycode"
label variable si_rice "Suitability Index for Wetland Rice (Irrigation, M Input)"
label variable suitable_rice_good "Good or Better (SI>=5500) for Wetland Rice (Irrigation, M Input)"
save "Data/Interim/rice_suitability.dta", replace

*** Climate
run "Program/Clean/clean_mann.do"  // Output saved as "Data/Interim/mann_recon.dta"
use "Data/Raw/climate500.dta", clear
rename id Maizeid
label variable year "Year"
label variable climate "1-Drought to 5-Flood"
save "Data/Interim/climate500.dta", replace

*** Towns, location of Chongs and county admins
shp2dta using "Data/Raw/towns/town1820", database("Data/Interim/town1820_d") coordinates("Data/Interim/town1820_c") replace
shp2dta using "Data/Raw/towns/town1911", database("Data/Interim/town1911_d") coordinates("Data/Interim/town1911_c") replace
shp2dta using "Data/Raw/Chong/chong", database("Data/Interim/chong_d") coordinates("Data/Interim/chong_c") replace
shp2dta using "Data/Raw/countyadmin/countyadmin", database("Data/Interim/ctadmin_d") coordinates("Data/Interim/ctadmin_c") replace

**** First import the distance data
foreach pts in admin chong town1820 town1911 {
	foreach nr in tocanal tocourier {
		import delimited using "Data/Raw/Canal/`pts'`nr'.txt", clear
		rename objectid `pts'
		rename near_dist pts_`nr'
		keep `pts' pts_`nr'
		save "Data/Interim/`pts'`nr'.dta", replace
	}
}
**** Chong
use "Data/Interim/chong_d.dta", clear
rename _ID chong
merge 1:1 chong using "Data/Interim/chongtocanal.dta"
drop _merge
merge 1:1 chong using "Data/Interim/chongtocourier.dta"
drop _merge
duplicates drop W72_LAT W71_LONG, force
geoinpoly W72_LAT W71_LONG using "Data/Interim/samplemap_c.dta"
drop if _ID==.
merge m:1 _ID using "Data/Interim/samplemap_d.dta"
collapse (count) chong (min) pts_tocanal pts_tocourier, by(OBJECTID)
rename pts_tocanal chong_canal
rename pts_tocourier chong_courier
replace chong_canal=chong_canal/1000
replace chong_courier=chong_courier/1000
label variable chong "1820 Busy Xian (Chong)"
label variable chong_canal "Distance from Chong to Canal"
label variable chong_courier "Distance from Chong to Courier"
save "Data/Interim/chong.dta", replace
**** County Administration Area
use "Data/Interim/ctadmin_d.dta", clear
rename _ID admin
merge 1:1 admin using "Data/Interim/admintocanal.dta"
drop _merge
merge 1:1 admin using "Data/Interim/admintocourier.dta"
drop _merge
duplicates drop X_COORD Y_COORD, force
geoinpoly Y_COORD X_COORD using "Data/Interim/samplemap_c.dta"
drop if _ID==.
drop OBJECTID
merge m:1 _ID using "Data/Interim/samplemap_d.dta"
collapse (count) admin (min) pts_tocanal pts_tocourier, by(OBJECTID)
rename pts_tocanal ctadmin_canal
rename pts_tocourier ctadmin_courier
replace ctadmin_canal=ctadmin_canal/1000
replace ctadmin_courier=ctadmin_courier/1000
label variable admin "County Administration Area Recorded"
label variable ctadmin_canal "Distance from County Administration Area to Canal (km)"
label variable ctadmin_courier "Distance from County Administration Area to Courier (km)"
save "Data/Interim/ctadmin.dta", replace
**** Town1820
use "Data/Interim/town1820_d.dta", clear
rename _ID town1820
merge 1:1 town1820 using "Data/Interim/town1820tocanal.dta"
drop _merge
merge 1:1 town1820 using "Data/Interim/town1820tocourier.dta"
drop _merge
duplicates drop Y_COORD X_COORD, force
geoinpoly Y_COORD X_COORD using "Data/Interim/samplemap_c.dta"
drop if _ID==.
drop SYS_ID
merge m:1 _ID using "Data/Interim/samplemap_d.dta"
foreach i in canal courier{
	gen r10`i'=(pts_to`i'/1000<=10)
	local radius `radius' r10`i'
}
gen r10both=(pts_tocanal/1000<=10) & (pts_tocourier/1000<=10)
local radius `radius' r10both
disp "`radius'"
collapse (count) town1820 (mean) AREA pts_tocanal pts_tocourier (sum) `radius', by(OBJECTID)
rename pts_tocanal town1820_canal_avg
rename pts_tocourier town1820_courier_avg
gen town1820density=town1820/AREA
replace town1820_canal_avg=town1820_canal_avg/1000
replace town1820_courier_avg=town1820_courier_avg/1000 
foreach i in canal courier both {
   rename r10`i' town1820_r10`i'
   label variable town1820_r10`i' "# of 1820 Towns within 10 km to `i'"
}
label variable town1820 "Number of Towns in 1820"
label variable town1820density "Number of Towns per $ km^2 $ in 1820"
label variable town1820_canal_avg "Avg distance from 1820 town to canal"
label variable town1820_courier_avg "Avg distance from 1820 town to courier"
drop AREA
save "Data/Interim/town1820.dta", replace
**** Town1911
use "Data/Interim/town1911_d.dta", clear
rename _ID town1911
merge 1:1 town1911 using "Data/Interim/town1911tocanal.dta"
drop _merge
merge 1:1 town1911 using "Data/Interim/town1911tocourier.dta"
drop _merge
duplicates drop Y_COORD X_COORD, force
geoinpoly Y_COORD X_COORD using "Data/Interim/samplemap_c.dta"
drop if _ID==.
drop SYS_ID NOTE_ID
merge m:1 _ID using "Data/Interim/samplemap_d.dta"
foreach i in canal courier{
	gen r10`i'=(pts_to`i'/1000<=10)
	local radius1 `radius1' r10`i'
}
gen r10both=(pts_tocanal/1000<=10) & (pts_tocourier/1000<=10)
local radius1 `radius1' r10both
disp "`radius'"
collapse (count) town1911 (mean) AREA pts_tocanal pts_tocourier (sum) `radius1', by(OBJECTID)
rename pts_tocanal town1911_canal_avg
rename pts_tocourier town1911_courier_avg
gen town1911density=town1911/AREA
replace town1911_canal_avg=town1911_canal_avg/1000
replace town1911_courier_avg=town1911_courier_avg/1000 
foreach i in canal courier both {
   rename r10`i' town1911_r10`i'
   label variable town1911_r10`i' "# of 1911 Towns within 10 km to `i'"
}
label variable town1911 "Number of Towns in 1911"
label variable town1911density "Number of Towns per $ km^2 $ in 1911"
label variable town1911_canal_avg "Avg distance from 1911 town to canal"
label variable town1911_courier_avg "Avg distance from 1911 town to courier"
drop AREA
save "Data/Interim/town1911.dta", replace

*** Intensity of treatment
shp2dta using "Data/Raw/Canal/canal", database("Data/Interim/canal_d") coordinates("Data/Interim/canal_c") replace
use "Data/Interim/canal_c.dta", clear
rename _ID rvid
geoinpoly _Y _X using "Data/Interim/samplemap_c.dta"
duplicates drop _ID, force
drop if _ID==.
gen cross=1
keep _ID cross
save "Data/Interim/crosscounty.dta", replace
 
import delimited using "Data/Raw/CanalProj/intertab.txt", clear
rename objectid_1 OBJECTID
keep OBJECTID length
collapse (sum) length, by(OBJECTID)
merge 1:1 OBJECTID using "Data/Interim/samplemap_d.dta"
drop _merge
merge 1:1 _ID using "Data/Interim/crosscounty.dta"
drop _merge
replace length=length*cross
sum length
disp r(sum)
keep OBJECTID _ID length AREA
gen canal_den=length/AREA*100
rename length canal_length
replace canal_length=0 if canal_length==.
replace canal_den=0 if canal_den==.
label variable canal_length "Length of Canal"
label variable canal_den "Length of Canal per 100 $ km^2 $"
save "Data/Interim/canalden.dta", replace

*** Obtain additional data from Chen and Kung (2016)
use "Data/Raw/maize_raw_data.dta", clear 
bysort id: egen sd=mean(shuidao)
bysort id: egen ar=mean(area)
replace shuidao=sd
replace area=ar
drop sd ar
gen popden=exp(popden_ln)
drop popden_ln
rename area area_pref
reshape wide popden wage urbanshare, i(id) j(year)
rename id Maizeid
rename adopyear maizeyear
rename shuidao riceregion
rename sweetpotato swtpotatoyear
label variable maizeyear "Year of Maize Adoption"
label variable riceregion "Region of Rice Plantation"
label variable swtpotatoyear "Year of Sweet Potato Adoption"
expand 262
bysort Maizeid: gen year=_n+1649
gen maize=(year>=maizeyear)
gen sweetpotato=(year>=swtpotatoyear)
label variable maize "Maize Adopted"
label variable sweetpotato "Sweet Potato Adopted"
save "Data/Interim/maize.dta", replace


*****************************************************************
*** Step 5: Merge the Additional Variables created in previous step
*****************************************************************
***First, merge data at the prefecture level
import excel using "Data/Raw/PrefwID.xlsx", firstrow clear // crosswalk between datasets, manually created by authors
keep lev2id Shpid Maizeid
gen oid=_n
expand 262
bysort oid: gen year=_n+1649
*** Taiping
merge m:1 Shpid using "Data/Interim/taiping.dta"
replace Taiping=0 if Taiping==.
drop _merge
*** Climate500
merge m:1 Maizeid year using "Data/Interim/climate500.dta"
drop if _merge==2
drop _merge
*** Grain Price
rename Maizeid id
merge m:1 id year using "Data/Raw/grainprice.dta"
drop if _merge==2
rename id Maizeid
drop _merge
label variable mp "Average Grain Price (Tael/KCal)"
*** Other variables from Chen and Kung (2016)
merge m:1 Maizeid year using "Data/Interim/maize.dta"
drop if _merge==2
drop _merge
drop if lev2id==.
save "Data/Interim/addvar_pref.dta", replace

***Next, merge data at the county level
use "Data/Interim/samplemap_d.dta", clear
keep OBJECTID LEV2_PY AREA
encode LEV2_PY, gen(lev2id)
expand 262
bysort OBJECTID: gen year=_n+1649
sort year OBJECTID
*** Ruggedness
merge m:1 OBJECTID using "Data/Interim/ruggedness.dta"
drop _merge
*** Courier routes
merge m:1 OBJECTID using "Data/Interim/distcourier.dta"
drop _merge
*** Soldier
merge m:1 OBJECTID using "Data/Interim/soldier.dta"
replace soldier=0 if soldier==.
drop _merge
*** Crop suitability
merge m:1 OBJECTID using "Data/Interim/rice_suitability.dta"
drop _merge
merge m:1 OBJECTID using "Data/Interim/wheat_suitability.dta"
drop _merge
*** Climate
merge 1:1 OBJECTID year using "Data/Interim/mann_recon.dta"
drop _merge
*** Towns and Chong
merge m:1 OBJECTID using "Data/Interim/chong.dta"
drop _merge
merge m:1 OBJECTID using "Data/Interim/ctadmin.dta"
drop _merge
merge m:1 OBJECTID using "Data/Interim/town1820.dta"
drop _merge
merge m:1 OBJECTID using "Data/Interim/town1911.dta"
drop _merge
*** Intensity of Treatment
merge m:1 OBJECTID using "Data/Interim/canalden.dta"
drop _merge
*** Shipping Amount
merge m:1 year using "Data/Raw/amount.dta"
drop _merge
egen amount=rowtotal(shipping_main shipping_cost1 shipping_cost2 shipping_extra shipping_cost3 shipping_cost4) 
replace amount=. if amount==0
replace amount=amount/1000000
replace shipping_zj=shipping_zj/1000000
gen mtpl=amount/shipping_zj
su mtpl
local mtpl=r(mean)
replace amount=`mtpl'*shipping_zj if amount==.
replace shipping_zj=amount/`mtpl' if shipping_zj==.
gen lamount=ln(amount)
*** Fu level Variables
merge m:1 lev2id year using "Data/Interim/addvar_pref.dta"
drop _merge
save "Data/Interim/addvar.dta", replace


*****************************************************************
*** Step 6: Merge the Additional variables to the Main dataset
*****************************************************************
use "Data/Interim/rebellion_temp1.dta", clear 
merge 1:1 OBJECTID year using "Data/Interim/addvar.dta"
drop _merge
*** Define Treatment Measure
recode year (1650/1660=1) (1661/1722=2) (1723/1735=3) (1736/1795=4) (1796/1820=5) ///
			(1821/1849=6) (1850/1861=7) (1862/1874=8) (1875/1908=9) (1909/1911=10) ///
			,gen(emperor)
label variable emperor "Emperor on the Throne"
*** Define interactions with density
replace interaction2=canal_length*reform
label variable interaction2 "Canal Length $\times$ After Abandonment"
*** Label
label variable onset_any "Presence"
label variable onset_all "Number"
*** Set Panel
sort OBJECTID year
xtset OBJECTID year
save "Data/Interim/rebellion_temp2.dta", replace


*****************************************************************
*** Step 7: Another set of variables to add
*****************************************************************
*** The old yellow river
import excel using "Data/Raw/oldyellowriver.xls", firstrow clear
keep OBJECTID NEAR_DIST NEAR_ANGLE
rename NEAR_DIST distance_oldhuang
rename NEAR_ANGLE angle_oldhuang 
label variable distance_oldhuang "Distance to Old Yellow River (unknown units)"
gen along_oldhuang=(distance_oldhuang==0)
drop distance_oldhuang
save "Data/Interim/oldyellow.dta", replace

*** Green Gang
import excel using "Data/Raw/Addvar2.xlsx", firstrow clear
keep OBJECTID LEV1_CH LEV2_CH associations_pref boats_prov green_senior Pref_capital
replace green_senior=0 if green_senior==.
replace Pref_capital=0 if Pref_capital==.
rename Pref_capital pref_capital
recode boats_prov (1638=21) (1538=21) (1258=16) (688=9) (709=9) (187=1) (800.8=10.5) (310=4), gen(n_gangs)
gen boats_gang=boats_prov/n_gangs
sort LEV2_CH associations_pref boats_prov
by LEV2_CH associations_pref boats_prov: egen n_associations=count(OBJECTID)
gen associations_exp=associations_pref/n_associations
replace associations_exp=associations_exp/4 if inlist(OBJECTID,902,878,835,815)
replace associations_exp=1 if inlist(OBJECTID,1103,1115,1065,1062)
replace associations_exp=0 if associations_exp==.
replace boats_gang=310/4 if inlist(OBJECTID,1103,1115,1065,1062)
replace boats_gang=0 if boats_gang==.
gen boats_exp=associations_exp*boats_gang
drop n_gangs boats_gang n_associations associations_pref boats_prov
label variable green_senior "Senior Green Gang Members"
label variable pref_capital "Prefecture Capital"
label variable associations_exp "Expected Number of Boatmen's Associations"
label variable boats_exp "Expected Number of Registered Grain Transportation Boats"
save "Data/Interim/addvar2.dta", replace

*** Merge these variables to the main dataset
use "Data/Interim/rebellion_temp2.dta", clear 

**** The old yellow river
merge m:1 OBJECTID using "Data/Interim/oldyellow.dta"
drop _merge
**** Green Gang
merge m:1 OBJECTID using "Data/Interim/addvar2.dta"
drop _merge

*** Organize and Save data
save "Data/Interim/rebellion_temp3.dta", replace


*****************************************************************
*** Step 8: Final set of variables
*****************************************************************
use "Data/Interim/rebellion_temp3.dta", clear

*** First Opium War battle fields
gen opiumbattle=inlist(OBJECTID,522,716,478,548,704,505)
*** Ming population
tempfile countypop_ming
preserve
    import excel using "Data/Raw/countypop_ming.xls", firstrow clear
    rename OBJECTID OBJECTID1
    rename SPLITID OBJECTID2
    reshape long OBJECTID, i(ID_MING) j(cw)
    sort OBJECTID cw ID_MING household
    save "`countypop_ming'.dta", replace
restore
tempfile cntypop
preserve
    duplicates drop OBJECTID, force
    keep OBJECTID prefid area_pref AREA popden*
    merge 1:m OBJECTID using "`countypop_ming'.dta", nogen keep(1 3)
    collapse (sum) household (first) ID_MING prefid area_pref AREA popden*, by(OBJECTID)
    bysort ID_MING: egen area_beforesplit=total(AREA)
    replace household=(household*AREA/area_beforesplit)
    bysort prefid: egen totalarea=total(AREA)
    bysort prefid: egen totalhh=total(household)
    gen popden1368=totalhh*4/totalarea
    replace popden1368=. if popden1368==0
    foreach y of numlist 1600 1776 1820 1851 1880 1910 {
        gen cntypop`y'=household*4*popden`y'/popden1368
        replace cntypop`y'=popden`y'*AREA if cntypop`y'==.
    }
    rename household household1368
    keep OBJECTID popden1368 household cntypop*
    save "`cntypop'.dta", replace
restore
merge m:1 OBJECTID using "`cntypop'.dta", assert(3)

*** Additional geographic measures
preserve
tempfile temp_1
import excel using "Data/Raw/lengths/Ming_Routes_2016_Identity_St1_TableToExcel.xls", firstrow clear
drop FREQUENCY-SUM_length OBJECTID
save "`temp_1'.dta", replace

tempfile temp_2
import excel using "Data/Raw/lengths/chgis_1820_county_seat_TableToExcel.xls", firstrow clear
keep NAME_PY NAME_CH LEV2_CH NEAR_DIST
egen merge_id=concat(NAME_CH LEV2_CH)
duplicates drop merge_id, force
save "`temp_2'.dta", replace

tempfile temp_3
import excel using "Data/Raw/lengths/Changjiang_Output_Identity_S_TableToExcel.xls", firstrow clear
drop FREQUENCY-SUM_length OBJECTID
drop in 1
save "`temp_3'.dta", replace

tempfile distanceto_changjiang
import excel using "Data/Raw/lengths/v4_1911_cnty_pgn_gbk_TableToExcel.xls", firstrow clear
keep OBJECTID NAME_PY NAME_CH LEV2_CH
egen merge_id=concat(NAME_CH LEV2_CH)
duplicates drop merge_id, force
rename NAME_CH NAME_CH_yizhan
rename NAME_PY NAME_PY_yizhan
rename LEV2_CH LEV2_CH_yizhan
merge 1:1 merge_id using "`temp_2'.dta", keep(3)
keep OBJECTID NEAR_DIST
rename NEAR_DIST distanceto_changjiang
replace distanceto_changjiang=distanceto_changjiang/1000
save "`distanceto_changjiang'.dta", replace

tempfile courier_length
import excel using "Data/Raw/lengths/v4_1911_cnty_pgn_gbk_TableToExcel.xls", firstrow clear
keep OBJECTID NAME_PY NAME_CH LEV2_PY
duplicates drop NAME_CH, force
merge 1:1 NAME_CH using "`temp_1'.dta", keep(3)
drop _merge
sort OBJECTID

rename NAME_CH NAME_CH_yizhan
rename NAME_PY NAME_PY_yizhan
rename LEV2_PY LEV2_PY_yizhan
save "`courier_length'.dta", replace

tempfile jingneichangjiang_length
import excel using "Data/Raw/lengths/v4_1911_cnty_pgn_gbk_TableToExcel.xls", firstrow clear
keep OBJECTID NAME_PY NAME_CH LEV2_PY
duplicates drop NAME_CH, force
merge 1:1 NAME_CH using "`temp_3'.dta", keep(3)
drop _merge
sort OBJECTID

rename NAME_CH NAME_CH_yizhan
rename NAME_PY NAME_PY_yizhan
rename LEV2_PY LEV2_PY_yizhan
save "`jingneichangjiang_length'.dta", replace
restore

drop _merge
merge m:1 OBJECTID using "`courier_length'.dta"
drop if _merge==2
drop _merge NAME_CH_yizhan NAME_PY_yizhan LEV2_PY_yizhan
replace courier_length=0 if courier_length==.
merge m:1 OBJECTID using "`distanceto_changjiang'.dta"
drop if _merge==2 
drop _merge
merge m:1 OBJECTID using "`jingneichangjiang_length'.dta"
drop if _merge==2
drop _merge NAME_CH_yizhan NAME_PY_yizhan LEV2_PY_yizhan
replace changjiang_jingnei=0 if changjiang_jingnei==.
save "Data/Final/rebellion.dta", replace